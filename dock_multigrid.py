import os
from argparse import ArgumentParser
from ligand_docking import ligand_docking

parser = ArgumentParser(description='multi grid docking')
parser.add_argument('--csv', metavar='CSV', help='input file(csv, sdf)', dest='csv', required=True)
parser.add_argument('--ref', help='smiles csv file', default=None, dest='ref')
parser.add_argument('--dir', help='raw data directory', dest='dir', required = True)
parser.add_argument('--node', help='clac_node', dest='node', default='node4')
parser.add_argument('--num',  help='num of node', dest='num', default=10)

if __name__=='__main__':
    args = parser.parse_args()
    for x in [x for x in os.listdir(args.dir) if 'glide-grid' in x]:
        grid_zip = '{}/{}/{}.zip'.format(args.dir, x, x)
        ligand_docking(args.csv, args.ref, grid_zip, args.node, args.num)
        # os.system('/home/novorex/anaconda3/envs/ENL/bin/python ligand_docking.py --csv {} --ref {} --grid {}/{}/{}.zip --node {} --num {}'.format(args.csv, args.ref, args.dir, x, x, args.node, args.num))
    
