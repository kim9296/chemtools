#!/bin/bash 

#SBATCH --job-name=hj_lrrk2_dock
#SBATCH --partition=normal
#SBATCH --nodelist=node2
#SBATCH --ntasks=30
#SBATCH --cpus-per-task=4 
#SBATCH --output=/home/novorex/hj/Novorex/LRRK2/slurm/slurm-%A.out

#/home/novorex/anaconda3/envs/ENL/bin/python dock_multigrid.py --csv /home/novorex/hj/Novorex/LRRK2/wild/raw/CDD_LRRK2.csv --dir /home/novorex/hj/Novorex/LRRK2/wild/raw
/home/novorex/anaconda3/envs/ENL/bin/python ligand_docking.py --csv /home/novorex/hj/Novorex/LRRK2/wild/raw/ChEMBL_LRRK2.csv --grid /home/novorex/hj/Novorex/LRRK2/wild/raw/glide-grid_5OPU.zip
