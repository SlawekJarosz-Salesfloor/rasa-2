To start server
    ~/miniconda3/envs/rasa/bin/python -m rasa run --enable-api

To train NLU
    ~/miniconda3/envs/rasa/bin/python -m rasa train
    ~/miniconda3/envs/rasa/bin/python -m rasa train --data ./data/nlu_Coats_Dresses_Jeans_Sweatshirts_T04.yml --out ./models/nlu_Coats_Dresses_Jeans_Sweatshirts_T04

To enter shell
    ~/miniconda3/envs/rasa/bin/python -m rasa shell


    usage: rasa train [-h] [-v] [-vv] [--quiet] [--logging-config-file LOGGING_CONFIG_FILE] [--data DATA [DATA ...]] [-c CONFIG] [-d DOMAIN] [--out OUT] [--dry-run] [--augmentation AUGMENTATION] [--debug-plots]
                  [--num-threads NUM_THREADS] [--fixed-model-name FIXED_MODEL_NAME] [--persist-nlu-data] [--force] [--finetune [FINETUNE]] [--epoch-fraction EPOCH_FRACTION] [--endpoints ENDPOINTS]
                  {core,nlu} ...