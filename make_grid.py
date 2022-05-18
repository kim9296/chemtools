import os

cur_dir = os.path.abspath('/home/novorex/hj/Novorex/LRRK2/raw')
print (cur_dir)
os.chdir(cur_dir)

with open('glide-grid_MSD_homology/glide-grid_MSD_homology.in', 'r') as f:
    temp = f.readlines()
f.close()

for x in [x for x in os.listdir('.') if 'proteinprep_7' in x]:
    grid_dir = x.replace('proteinprep', 'glide-grid')
    if not os.path.exists(grid_dir):
   	print (grid_dir)
    	os.makedirs(grid_dir)
    	os.system('cp {}/{}-out.maegz {}/{}.maegz'.format(x, x, grid_dir, grid_dir))
    	os.chdir(grid_dir)
    	with open('{}.in'.format(grid_dir), 'w') as f:
	    f.write(temp[0])
	    f.write(temp[1])
	    f.write('GRIDFILE    {}.zip\n'.format(grid_dir))
	    f.write(temp[3])
	    f.write(temp[4])
	    f.write('RECEP_FILE    {}.maegz'.format(grid_dir))
    	f.close()
    	os.system('$SCHRODINGER/glide {}.in -OVERWRITE -HOST node4:10 -TMPLAUNCHDIR'.format(grid_dir))
    	os.chdir(cur_dir)  
