import os
from argparse import ArgumentParser

parser = ArgumentParser(description='multi grid docking')
parser.add_argument('--csv', metavar='CSV', help='input file(csv, sdf)', dest='csv', required=True)
parser.add_argument('--ref', help='smiles csv file', default=None, dest='ref')
parser.add_argument('--dir', help='raw data directory', dest='dir', required = True)

if __name__=='__main__':
    args = parser.parse_args()
    for x in [x for x in os.listdir(args.dir) if 'glide-grid' in x]:
        os.system('/home/novorex/anaconda3/envs/ENL/bin/python ligand_docking.py --csv {} --ref {} --grid {}/{}/{}.zip'.format(args.csv, args.ref, args.dir, x, x))
    
