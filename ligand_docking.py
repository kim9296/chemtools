from argparse import ArgumentParser
from csv2sdf import csv2sdf
from preprocessing_inhibition import fill_smiles
import os

parser = ArgumentParser(description='ligand docking')
parser.add_argument('--inp', help='input files (csv, sdf)', dest='inp', required=True)
parser.add_argument('--ref', help='smiles csv file', default=None, type=str)
parser.add_argument('--grid', metavar='grid', help='docking grid', dest='grid', required=True)
parser.add_argument('--node', help='clac_node', dest='node', default='node4')
parser.add_argument('--num',  help='num of node', dest='num', default=10)

def ligand_docking(input_file, ref, grid, node, num):
    curdir = os.path.abspath('.')
    csv_name = os.path.abspath(input_file)
    if ref is not None:
    	ref_name = os.path.abspath(ref)
    out_name = csv_name.replace('raw', 'result')
    grid_name = os.path.abspath(grid)
    dir_name = os.path.dirname(out_name)
    if 'sdf' in csv_name:
	    sdf_name = out_name
    else:
        sdf_name = out_name.replace('.csv', '.sdf')
    grid_base = os.path.basename(grid_name)
    ligand_name = sdf_name.replace('.sdf', '.maegz')
    docking_in = sdf_name.replace('.sdf', '_{}.in'.format(grid_base.split('.zip')[0]))
    docking_out = os.path.basename(docking_in.replace('.in', '_pv.maegz'))    

    if not os.path.exists(ligand_name):
        if ref is not None:
            print ('preprocess csv')
            fill_smiles(csv_name, ref_name)
        else:
            os.system('cp {} {}'.format(csv_name, out_name))
        
        if 'sdf' not in csv_name:
            print ('convert sdf')
            csv2sdf(out_name, sdf_name)
    
        os.chdir(dir_name)   
    
        print ('ligprep')
        os.system('$SCHRODINGER/ligprep -u s_sd_cpd\_id -isd {} -omae {} -epik -HOST {}:{} -TMPLAUNCHDIR -WAIT'.format(sdf_name, ligand_name, node, num))
    
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
    os.system('$SCHRODINGER/glide {} -adjust -HOST {}:{} -NOJOBID -TMPLAUNCHDIR -WAIT'.format(docking_in, node, num))
    os.system('mv {}/glide/{} ../'.format(dir_name, docking_out))

    os.chdir('../')

    mae = os.path.join(dir_name, docking_out)
    csv = os.path.abspath(mae.replace('_pv.maegz', '_IFP.csv'))
    sdf = csv.replace('.csv', '.sdf')
    os.system('$SCHRODINGER/run interaction_fingerprints.py -i {} -ocsv {}'.format(mae, csv))
    os.system('$SCHRODINGER/utilities/sdconvert -n 2: -imae {} -osd {}'.format(mae, sdf))

    os.chdir(curdir)
    
if __name__ == '__main__':
    args = parser.parse_args()
    ligand_docking(args.inp, args.ref, args.grid, args.node, args.num)
    print ('finish')
