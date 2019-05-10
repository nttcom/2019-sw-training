
### create temporary stats file
log_dir=`\ls -1t ./results/ | head -1`
log_file="results/${log_dir}/simulation.log"
stat_file='stat_tmp.txt'

### calc score
egrep '(OK|KO)' ${log_file} | awk '{print $2, $7}' | sort | uniq -c > ${stat_file}
result_list_ok=`grep 'request-LIST OK' ${stat_file} | awk 'BEGIN{A=0} {A+=$1} END{print A}'`
result_list_ng=`grep 'request-LIST KO' ${stat_file} | awk 'BEGIN{A=0} {A+=$1} END{print A}'`
result_post_ok=`grep 'request-POST OK' ${stat_file} | awk 'BEGIN{A=0} {A+=$1} END{print A}'`
result_post_ng=`grep 'request-POST KO' ${stat_file} | awk 'BEGIN{A=0} {A+=$1} END{print A}'`

score=$(( 10 * (${result_list_ok} - ${result_list_ng} + ${result_post_ok} - ${result_post_ng}) ))
### offset to 0 if required
# if [ ${score} -lt 0 ]; then
#     score=0
# fi

### judgement
threshold=24000
pass=false
message="./bin/.msg_failure.txt"
if [ ${score} -ge ${threshold} ]; then
    pass=true
    message="./bin/.msg_success.txt"
fi

cat ${message}
echo "-------------------------------------------"
echo "  Score / Threshold : ${score} / ${threshold}"
echo "-------------------------------------------"


### submit
team=`hostname -s`
time=$((`date +%s` * 1000 * 1000))

body="{
    \"pass\": ${pass},
    \"score\": ${score},
    \"results\": {
        \"list\": [${result_list_ok}, ${result_list_ng}],
        \"post\": [${result_post_ok}, ${result_post_ng}]
    },
    \"timestamp\": ${time}
}"

# curl -sX POST https://<dummydashboard>.firebaseio.com/faas/teams/${team}.json -d "$body" > /dev/null && echo "... Score submitted to the dashboard."
