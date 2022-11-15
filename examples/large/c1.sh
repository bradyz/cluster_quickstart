#!/bin/zsh
ls /opt
ls /scratch/cluster/yzhao
export CUDA_PATH=/scratch/cluster/yzhao/cuda-9.2
export CUDA_HOME=/scratch/cluster/yzhao/cuda-9.2
export PATH=/scratch/cluster/yzhao/cuda-9.2:$PATH
export LD_LIBRARY_PATH=/scratch/cluster/yzhao/cuda-9.2/lib64:$LD_LIBRARY_PATH
nvidia-smi
source activate dgx
cd ~/code/Mask2Former
# train UVO sparse
python -c "import torch;print('cuda',torch.version.cuda,torch.cuda.is_available())"
python train_net.py --num-gpus 8 --resume \
    --config-file configs/coco/instance-segmentation/maskformer2_R50_bs16_24ep_896.yaml \
    OUTPUT_DIR ./logs/mf/uvo_sparse/samp_randn_query_anything_m2f_cls0_lr-5_v2    \
    DATASETS.TRAIN "('uvo_train_sparse',)" \
    DATASETS.TEST  "('uvo_val_sparse',)"   \
    MODEL.WEIGHTS ./models/mask2former_r50_coco.pkl \
    MODEL.SEM_SEG_HEAD.NUM_CLASSES 1 MODEL.ROI_HEADS.NUM_CLASSES 1 MODEL.RETINANET.NUM_CLASSES 1 \
    SOLVER.BASE_LR 0.00001  SOLVER.MAX_ITER 30000 \
    MODEL.MASK_FORMER.CLASS_WEIGHT 1. \
    SOLVER.CHECKPOINT_PERIOD 10000 TEST.EVAL_PERIOD 10000 \
    INPUT.MASK_FORMAT bitmask \
    WANDB.GROUP uvo_img_pe \
    SEED 42 \
    NO_JIT True

