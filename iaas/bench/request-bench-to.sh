#!/bin/bash
# 受講生側のVMからベンチマークを要求するためのスクリプト

SLACK_URL='INPUT_SLACK_WEBHOOK_URL_HERE'

function report_usage() {
    echo "Usage: "
    echo "  Level1 ベンチ実行の場合:"
    echo "    ./request-bench-to.sh https://example.com lv1"
    echo "  Level2 ベンチ実行の場合:"
    echo "    ./request-bench-to.sh https://example.com lv2"
}

# Some validation for commands

if [ $# -lt 2 ]; then
    echo -e "引数にURLと、実行レベルを指定してください\n"
    report_usage
    exit 1
fi

if ! [[ $1 =~ https://[a-zA-Z0-9]+.example.com$ ]]; then
    echo -e "第1引数のURLが指定されたフォーマットに一致していません\n"
    report_usage
    exit 2
fi

if ! [[ $2 =~ lv[12] ]] ; then
    echo -e "第2引数の指定されたレベルではありません\n"
    report_usage
    exit 3
fi

# Main Process

redis_host=`gcloud redis instances describe iaas-queue --region asia-northeast1 | grep host | cut -c 7-`

if [ -n "$redis_host" ]; then
    echo "${1} に対して、${2} ベンチマークリクエストを発行します。"
    redis-cli -h ${redis_host} lpush benchqueue "${1}@${2}" > /dev/null

    curl -s -X POST --data-urlencode \
        "payload={\"username\": \"INPUT_SLACK_USER_NAME_HERE\", \"text\": \"${1} に対する ${2} ベンチマークリクエストを受領しました。\", \"icon_emoji\": \":INPUT_ICON_EMOJI_HERE:\"}" \
        ${SLACK_URL} > /dev/null
else
    echo "ベンチマークリクエスト先のRedisホストが見つかりません。"
fi