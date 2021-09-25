#!/usr/bin/env sh

FILES="co-est2020.csv co-est2020-alldata.csv"

mkdir -p ../data

for FILE in $FILES
do
  curl https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/counties/totals/$FILE --output ../data/$FILE
done

