#!/usr/bin/env python -W ignore::DeprecationWarning

~/miniconda3/envs/rasa/bin/python -m rasa run --enable-api -m ./models/salesfloor-rasa/models/nlu_1st_level/ -p 5006 &

max=10
for i in `seq 1 $max`
do
    echo "Running 2nd level Rasa server: $i"
    ~/miniconda3/envs/rasa/bin/python -m rasa run --enable-api -m ./models/salesfloor-rasa/models/nlu_2nd_level_$i/ -p "$((5006+i))" &
done

#kill $(lsof -t -i:5006)