#!/bin/bash

TOPIC_NAME='iaas'
SLEEP_TIME=30
BENCH_TIME_FOR_TEST=15
BENCH_TIME_FOR_PROD=120
NUM_VIRTUAL_USERS_FOR_TEST=5
NUM_VIRTUAL_USERS_FOR_PROD=30
ZONE='asia-northeast1-b'
SLACK_URL='INPUT_SLACK_WEBHOOK_URL_HERE'

while true
do
    redis_host=`gcloud redis instances describe iaas-queue --region asia-northeast1 | grep host | cut -c 7-`
    # 受講生からのベンチマークリクエストを取得、キューからリクエストはすぐ消す
    message=`redis-cli -h ${redis_host} rpop benchqueue`

    if [ -n "$message" ]; then
        # 必要なホスト名とレベルだけを抜く
        target_host=`echo $message | awk '{split($1, a, "@"); print a[1]}'`
        level=`echo $message | awk '{split($1, a, "@"); print a[2]}'`
        second_host="iaas-compute-${target_host:12:2}-2"

        echo "Going to start ${level} benchmark to ${target_host} ..."
        curl -s -X POST --data-urlencode \
            "payload={\"username\": \"INPUT_SLACK_USERNAME_HERE\", \"text\": \"${target_host} に対する ${level} ベンチマークを開始します。\", \"icon_emoji\": \":INPUT_ICON_EMOJI_HERE:\"}" \
            ${SLACK_URL} > /dev/null

        # DBのTable初期化する、仮に失敗した場合はベンチを実行しない
        curl -f -s ${target_host}/initialize
        if [ $? -ne 0 ]; then
            echo "Debug ${target_host}/initialize"
            curl -s -X POST --data-urlencode \
                "payload={\"username\": \"INPUT_SLACK_USERNAME_HERE\", \"text\": \"${target_host}/initialize のテーブル初期化に失敗したため、ベンチマークを実行しません。\", \"icon_emoji\": \":INPUT_ICON_EMOJI_HERE:\"}" ${SLACK_URL} > /dev/null
                continue
        fi

        filename=`date "+%Y%m%d_%H%M%S"`
        # レベルに応じて、ベンチマークを実行
        if [ "${level}" = "lv1" ]; then
            # 練習のケース、VMを落とさない
            k6 run -e TARGET_URL=${target_host} --out json=/var/tmp/${filename}.json --vus ${NUM_VIRTUAL_USERS_FOR_TEST} --duration ${BENCH_TIME_FOR_TEST}s test_scenario.js
        else
            # 2台目が存在するか確認し、そもそも存在しない場合はベンチマークを実行しない。
            gcloud compute instances describe ${second_host} --zone ${ZONE} > /dev/null 2>&1
            if [ $? -ne 0 ]; then
                curl -s -X POST --data-urlencode \
                    "payload={\"username\": \"iaas-bot\", \"text\": \"${second_host}が存在しないため、ベンチマークを実行しません。\", \"icon_emoji\": \":INPUT_ICON_EMOJI_HERE:\"}" ${SLACK_URL} > /dev/null
                continue
            fi

            # 本番のケース、VMを落として対象のURLが生き延びれられるか確認する
            # 削除対象のホストを抽出
            reset_target_host="iaas-compute-${target_host:12:2}-$(($RANDOM%2 + 1))"
            curl -s -X POST --data-urlencode \
                "payload={\"username\": \"INPUT_SLACK_USER_NAME\", \"text\": \"約1分後に${reset_target_host}を落とします\", \"icon_emoji\": \":INPUT_ICON_EMOJI_HERE:\"}" ${SLACK_URL} > /dev/null

        # 1分後にマシンの電源リセット(https://cloud.google.com/sdk/gcloud/reference/compute/instances/reset)
        echo "gcloud compute instances reset ${reset_target_host} --zone ${ZONE}" | at now + 1 minute

            k6 run -e TARGET_URL=${target_host} --out json=/var/tmp/${filename}.json --vus ${NUM_VIRTUAL_USERS_FOR_PROD} --duration ${BENCH_TIME_FOR_PROD}s test_scenario.js
        fi

        # 試験実行結果をParse、またSlack通知はNode内部から実行した。（bashだとメッセージ組み立てがめんどくさいので）
        node result_parser.js /var/tmp/${filename}.json ${target_host} ${level}
    else
        echo "Seems there's no benchmark request in the queue. Let's just wait for ${SLEEP_TIME} secs..."
    fi
    sleep ${SLEEP_TIME}
done