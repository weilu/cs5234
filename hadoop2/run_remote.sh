#!/usr/bin/env bash
set -xe

EMR_CLUSTER_ID=j-1RXFH6ZCHBH5L
aws s3 rm --recursive s3://cs5234/temp_out

check_status () {
  STATE=`aws emr list-steps --cluster-id $EMR_CLUSTER_ID | jq .Steps[0].Status.State`
  STATE=`echo $STATE | tr -d \"` # remove ""
  while [[ "$STATE" = "RUNNING" || "$STATE" = "PENDING" ]]
  do
    sleep 20
    STATE=`aws emr list-steps --cluster-id $EMR_CLUSTER_ID | jq .Steps[0].Status.State`
    STATE=`echo $STATE | tr -d \"`
  done

  if [ "$STATE" = "FAILED" ]
  then
    LOGFILES=$(aws emr list-steps --cluster-id $EMR_CLUSTER_ID | jq .Steps[0].Status.FailureDetails.LogFile | tr -d \")
    aws s3 sync $LOGFILES log/
    exit 1
  fi
}

run_step () {
  aws emr add-steps --cluster-id $EMR_CLUSTER_ID --steps file://./emr/$1.json
  check_status
}

run_step degree
run_step threshold

aws s3 cp s3://cs5234/temp_out/threshold/part-00000 /tmp/
read M N THRESHOLD DENSITY <<< $(cat /tmp/part-00000)
echo "edges: $M, nodes: $N, threshold: $THRESHOLD, density: $DENSITY"
MAX_DENSITY=$DENSITY
rm /tmp/part-00000

while [[ ! -z "$N" && $N -gt 0 ]]
do
  sed "s/THRESHOLD/$THRESHOLD/g" <emr/vertex_removal.json.template >emr/vertex_removal.json
  run_step vertex_removal

  aws s3 rm --recursive s3://cs5234/out
  run_step edge_removal

  aws s3 rm --recursive s3://cs5234/temp_out
  run_step degree_no_reverse
  run_step threshold

  aws s3 cp s3://cs5234/temp_out/threshold/part-00000 /tmp/
  read M N THRESHOLD DENSITY <<< $(cat /tmp/part-00000)
  echo "edges: $M, nodes: $N, threshold: $THRESHOLD, density: $DENSITY"

  if [[ ! -z "$DENSITY" && $(echo "$DENSITY>$MAX_DENSITY" | bc ) -eq 1 ]]
  then
    MAX_DENSITY=$DENSITY
    echo "updating MAX_DENSITY = $MAX_DENSITY"
  fi
done

echo "densest subgraph density: $MAX_DENSITY"
