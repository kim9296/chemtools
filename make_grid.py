import os
from argparse import ArgumentParser

parser = ArgumentParser(description='make grid from ref grid')
parser.add_argument('--ref', help='ref grid', dest='ref', required = True)
parser.add_argument('--prt', help='protein for make grid', dest='prt', required =True)

args = parser.parse_args()

with open(args.ref, 'r') as f:
    temp = f.readlines()
f.close()

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
