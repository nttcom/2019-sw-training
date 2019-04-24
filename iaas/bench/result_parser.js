'use strict';

// Check the result file is specified or not.
let resultfile;
if (!process.argv[2]) {
    console.error('第1引数に解析対象のファイルを指定してください');
    process.exit(1);
} else {
    resultfile = process.argv[2];
}

// Check the target URL is specified or not. This value is used for notification.
let targetUrl;
if (!process.argv[3]) {
    console.error('第2引数にテスト対象URLを指定してください');
    process.exit(1);
} else {
    targetUrl = process.argv[3];
}

let testLevel;
if (!process.argv[4]) {
    console.error('第3引数にテストレベル(lv1 or lv2)を指定してください');
    process.exit(1);
} else {
    testLevel = process.argv[4];
}

// This array is used for to read RAW result from k6 output.
const rawResults = [];

// Main process triggered after finished parsing RAW result.
const parseResults = () => {
    const httpReqDurationResults = rawResults.filter(result => {
        return result.metric === 'checks' && result.type === 'Point'
    });

    const listResults = {};
    const getResults = {};
    const postResults = {};
    const putResults = {};
    const deleteResults = {};

    createResultAggregator('list')(httpReqDurationResults, listResults);
    createResultAggregator('get')(httpReqDurationResults, getResults);
    createResultAggregator('post')(httpReqDurationResults, postResults);
    createResultAggregator('put')(httpReqDurationResults, putResults);
    createResultAggregator('delete')(httpReqDurationResults, deleteResults);

    preProcessBeforeCalcScore([listResults, getResults, postResults, putResults, deleteResults]);
    const score = calcResults([listResults, getResults], [postResults, putResults, deleteResults]);

    const slackBody = constructBodyForSlack(getResults, listResults, postResults, putResults, deleteResults, score);
    notifySlack(slackBody);

    const firebaseBody = constructBodyForFirebase(getResults, listResults, postResults, putResults, deleteResults, score);
    postDataForDashboard(firebaseBody);
};

const constructBodyForFirebase = (getResults, listResults, postResults, putResults, deleteResults, score) => {
    const intLevel = parseInt(testLevel.slice(-1), 10);
    const unixTimestampMsec = new Date() / 1000;
    const body = {
        score: score,
        level: intLevel,
        results: {
            get: [getResults['1'], getResults['0']],
            list: [listResults['1'], listResults['0']],
            post: [postResults['1'], postResults['0']],
            put: [putResults['1'], putResults['0']],
            delete: [deleteResults['1'], deleteResults['0']],
        },
        timestamp: unixTimestampMsec
    };
    if (score > THRESHOLD) {
        body.pass = true;
    } else {
        body.pass = false;
    }
    return body;
};

// Build body for Slack message with benchmark results.
const constructBodyForSlack = (getResults, listResults, postResults, putResults, deleteResults, score) => {
    const body = {
        text: `${targetUrl} へのベンチマーク結果です:\n\
GET_OK: ${getResults['1']}, GET_NG: ${getResults['0']},\n\
LIST_OK: ${listResults['1']}, LIST_NG: ${listResults['0']}\n\
POST_OK: ${postResults['1']}, POST_NG: ${postResults['0']}\n\
PUT_OK: ${putResults['1']}, PUT_NG: ${putResults['0']}\n\
DELTE_OK: ${deleteResults['1']}, DELETE_NG: ${deleteResults['0']}\n\
score: ${score} `
    };

    // 1 means just "Practice", so we don't judge the result; just return the score and stats.
    if (testLevel === 'lv1') {
        return body;
    }

    if (score > THRESHOLD) {
        body.pass = true
        body.text += '\n:tada::tada::tada:おめでとうございます！合格です！:tada::tada::tada:'
    } else {
        body.pass = false
    }
    return body;
}

// Post Slack channel
const notifySlack = body => {
    const commonBody = { username: "INPUT_SLACK_USER_NAME", icon_emoji: ':INPUT_ICON_EMOJI_HERE:' };
    const mergedBody = JSON.stringify(Object.assign(body, commonBody));
    const options = {
        hostname: 'hooks.slack.com',
        port: 443,
        path: 'INPUT_SLACK_WEBHOOK_URL_HERE',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(mergedBody)
        }
    };
    const req = require('https').request(options, res => {
        if (res.statusCode === 200) {
            console.log('Succeeded in posting data to Slack.');
        } else {
            console.error('Failed to post data to Slack. Status code is', res.statusCode);
        }
    });
    req.on('error', e => {
        console.error('Failed to post data to Slack.')
        console.error(e);
    });
    req.write(mergedBody);
    req.end();
};

// todo: store data for dashboard
const postDataForDashboard = (body) => {
    const teamName = require('url').parse(targetUrl).host.split('.')[0];
    const strBody = JSON.stringify(body);
    const options = {
        hostname: 'INPUT_FIREBASE_HOST_NAME_HERE',
        port: 443,
        path: `/iaas/teams/${teamName}.json`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(strBody)
        }
    };
    const req = require('https').request(options, res => {
        if (res.statusCode === 200) {
            console.log('Succeeded in posting data to Firebase.');
        } else {
            console.error('Failed to post data to Firebase. Status code is', res.statusCode);
        }
    });
    req.on('error', e => {
        console.error('Failed to post data to Firebase.')
        console.error(e);
    });
    req.write(strBody);
    req.end();

};

// Utility function to create function to aggregate raw result easily
const createResultAggregator = httpMethod => {
    return (array, typeResults) => {
        array.filter(result => {
            return result.data.tags.group === `::${httpMethod}`;
        }).forEach(result => {
            typeResults[result.data.value] = (typeResults[result.data.value] || 0) + 1;
        });
    };
};

// This value is used for calculate score, when the HTTP triggers READ query such as SELECT.
const READ_WEIGHT = 0.2;
// This value is used for calculate score, when the HTTP request fails
const FAIL_WEIGHT = 20;
// Judge the test is passed or failed.
const THRESHOLD = 5000;

const calcResults = (readResults, writeResults) => {
    let score = 0;
    readResults.forEach(result => {
        score += (result['1'] - result['0'] * FAIL_WEIGHT) * READ_WEIGHT
    });
    writeResults.forEach(result => {
        score += (result['1'] - result['0'] * FAIL_WEIGHT)
    });
    return score;
}

const preProcessBeforeCalcScore = resultsList => {
    resultsList.forEach(results => {
        initwithZero(results);
    });
}

const initwithZero = (results) => {
    if (!results['0']) {
        results['0'] = 0;
    }
    if (!results['1']) {
        results['1'] = 0;
    }
}

// Read results from files
const lineReader = require('readline').createInterface({
    input: require('fs').createReadStream(resultfile)
})

lineReader.on('line', line => {
    const result = JSON.parse(line);
    rawResults.push(result);
});

lineReader.on('close', () => {
    parseResults();
});