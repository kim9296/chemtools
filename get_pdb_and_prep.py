from argparse import ArgumentParser
import os

parser = ArgumentParser(description='Get PDB and run prepwizard')
parser.add_argument('--inp', help='PDB code', dest='inp', nargs='+', required=True)

def GetPDBandPrep(pdb_code):
    if os.path.exists('proteinprep_{}'.format(pdb_code)):
        return
    os.system('$SCHRODINGER/utilities/getpdb {}'.format(pdb_code))
    os.makedirs('proteinprep_{}'.format(pdb_code))
    os.system('mv {}.pdb proteinprep_{}'.format(pdb_code, pdb_code))
    os.chdir('proteinprep_{}'.format(pdb_code))
    os.system('$SCHRODINGER/utilities/prepwizard {}.pdb proteinprep_{}.maegz'.format(pdb_code, pdb_code))
    os.chdir('..')

if __name__ == '__main__':
    args = parser.parse_args()
    for pdb in args.inp:
        GetPDBandPrep(pdb)
    print ('finish')