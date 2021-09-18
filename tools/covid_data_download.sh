#!/usr/bin/env sh

FILES="us-counties.csv us-states.csv us.csv"

mkdir -p ../data/archive

for FILE in $FILES
do
  curl https://raw.githubusercontent.com/nytimes/covid-19-data/master/$FILE --output ../data/$FILE

  #Save the todays version with a timestamp just in case
  BASENAME=`basename $FILE  .csv`
  cp ../data/$FILE ../data/archive/$BASENAME\_`date +"%Y%m%d"`.csv
done

