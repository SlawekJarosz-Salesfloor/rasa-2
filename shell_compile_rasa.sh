~/miniconda3/envs/rasa/bin/python -m rasa train --data ./data/nlu_1st_level.yml --domain ./prep/domain_2_levels.yml --out ./models/nlu_1st_level --force

max=10
for i in `seq 1 $max`
do
    echo "Creating 2nd level NLU buffer: $i"
    ~/miniconda3/envs/rasa/bin/python -m rasa train --data ./data/nlu_2nd_level_$i.yml --domain ./prep/domain_2_levels.yml --out ./models/nlu_2nd_level_$i --force
done