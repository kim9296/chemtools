from argparse import ArgumentParser
from csv2sdf import csv2sdf
from preprocessing_inhibition import fill_smiles
import os

parser = ArgumentParser(description='ligand docking')
parser.add_argument('--csv', metavar='CSV', help='input csv', dest='csv', required=True)
parser.add_argument('--ref', help='smiles csv file', default=None, type=str)
parser.add_argument('--grid', metavar='grid', help='docking grid', dest='grid', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    
    csv_name = os.path.abspath(args.csv)
    if args.ref is not None:
    	ref_name = os.path.abspath(args.ref)
    out_name = csv_name.replace('raw', 'result')
    grid_name = os.path.abspath(args.grid)
    dir_name = os.path.dirname(out_name)
    sdf_name = out_name.replace('.csv', '.sdf')
    grid_base = os.path.basename(grid_name)
    ligand_name = sdf_name.replace('.sdf', '.maegz')
    docking_in = sdf_name.replace('.sdf', '_{}.in'.format(grid_base.split('.zip')[0]))
    docking_out = sdf_name.replace('.sdf', '_pv.maegz')    
    
    if not os.path.exists(ligand_name):
        #if args.ref is not None:
        #    print ('preprocess csv')
        #    fill_smiles(csv_name, ref_name)
        #else:
        #os.system('cp {} {}'.format(csv_name, out_name))
        
        #print ('convert sdf')
        #csv2sdf(out_name, sdf_name)
    
        os.chdir(dir_name)   
    
        print ('ligprep')
        os.system('$SCHRODINGER/ligprep -u s_sd_cpd\_id -isd {} -omae {} -epik -HOST node4:10 -TMPLAUNCHDIR -WAIT'.format(sdf_name, ligand_name))
    
    else:
        os.chdir(dir_name)

    with open(docking_in, 'w') as f:
        f.write('FORCEFIELD   OPLS_2005\n')
        f.write('GRIDFILE   {}\n'.format(grid_name))
        f.write('LIGANDFILE   {}\n'.format(ligand_name))
        f.write('PRECISION   SP\n')
        f.write('WRITE_RES_INTERACTION   True\n')
    f.close()

    os.makedirs('glide', exist_ok=True)
    os.chdir('glide')

    print ('ligand docking')
    os.system('$SCHRODINGER/glide {} -adjust -HOST node4:10 -NOJOBID -TMPLAUNCHDIR -WAIT'.format(docking_in))
    os.system('mv {} ../'.format(docking_out))

    print ('finish')
