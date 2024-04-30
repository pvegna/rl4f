#!/bin/bash -l

# Base path to store the outputs.
BASE_PATH="/scratch/network/pvegna/rl4f/outputs/alphabetize_output"

# Name of the project and experiment for wandb.
PROJECT_NAME="rl4f_alphabetize_sup"
EXPERIMENT_NAME="t5large_bs32_wd0.01_lr1e-5_beam5_min5_max_20_seed0"

# Wandb API key.
WANDB_KEY=

# Wandb entity name.
WANDB_ENTITY=pvegna

# Create the directory to store the results.
mkdir -p $BASE_PATH/$PROJECT_NAME/$EXPERIMENT_NAME

WANDB_API_KEY=$WANDB_KEY python /scratch/network/pvegna/rl4f/scripts/training/train_text_generation.py \
--base_path_to_store_results $BASE_PATH \
--config_path /scratch/network/pvegna/rl4f/scripts/training/task_configs/alphabetize/t5_supervised_large.yaml \
--project_name $PROJECT_NAME \
--experiment_name $EXPERIMENT_NAME \
--entity_name $WANDB_ENTITY \
--log_to_wandb
