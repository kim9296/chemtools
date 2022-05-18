#!/bin/bash 

#SBATCH --job-name=hj_lrrk2_dock
#SBATCH --partition=normal
#SBATCH --nodelist=node4
#SBATCH --ntasks=30
#SBATCH --cpus-per-task=4 
#SBATCH --output=/home/novorex/hj/Novorex/LRRK2/slurm/slurm-%A.out

PATH_NAME='/home/novorex/hj/Novorex/LRRK2/wild/result'

cd ${PATH_NAME}
folder_list="$(ls ChEMBL*5OPU_pv.maegz)"

for folder in $folder_list

do
    
    /home/novorex/anaconda3/envs/ENL/bin/python /home/novorex/hj/Novorex/chemtools/post_docking.py --mae ${folder} --col s_sd_chembl\\_id

done 
