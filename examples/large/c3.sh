#!/bin/zsh

nvidia-smi
cd ~/code/Deformable-DETR
source activate deformable_detr
GPUS_PER_NODE=8 ./tools/run_dist_launch.sh 8 \
    ./configs/1010/detr.sh

