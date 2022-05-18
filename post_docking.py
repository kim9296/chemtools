from argparse import ArgumentParser
import pandas as pd
import os
import json
from rdkit import Chem

parser = ArgumentParser(description='post docking process')
parser.add_argument('--mae', metavar='MAE', help='input pose viewer file', dest='mae', required=True)
parser.add_argument('--col', help='input col name of compound', dest='col', default='s_sd_cpd\_id')

def make_ifp(mae, csv):
    os.system('$SCHRODINGER/run interaction_fingerprints.py -i {} -ocsv {}'.format(mae, csv))

def make_result_json(dir_name, df, outmae, col):
    result = dict()
    for i, row in df.sort_values(by = ['r_i_glide_gscore']).iterrows():
        if row[col] not in result:
            result[row[col]] = [i]
        else:
            result[row[col]].append(i)

    with open(os.path.join(dir_name, outmae.replace('_pv.maegz','_cpd_indexs.json')), 'w') as f:
        json.dump(result, f, indent=4)
    f.close()
    
    return result

def split_ligand(mae, split_dir):

    outmae = os.path.basename(mae)
    os.system('$SCHRODINGER/utilities/structconvert -n 2: -split-nstructures 1 {} {}'.format(mae, os.path.join(split_dir, outmae.replace('_pv.maegz', '.mae'))))

    for mae_file in os.listdir(split_dir):
        os.system('$SCHRODINGER/utilities/mol2convert -imae {} -omol2 {}'.format(os.path.join(split_dir, mae_file), os.path.join(split_dir, mae_file.replace('.mae', '.txt'))))

def collect_result(result_dir, split_dir, cpd_indexs, df, outmae):
    result = dict()
    indexs = list()
    fname = outmae.split('.mae')[0]
    for cpd, values in cpd_indexs.items():
        for i in values:
            mol = Chem.MolFromMol2File('{}/{}-{}.txt'.format(split_dir, fname, str(i + 2).zfill(4)))
            if mol is not None:
                result[cpd] = i
                indexs.append(i)
                os.system('cp {}/{}-{}.txt {}/{}-{}.txt'.format(split_dir, fname, str(i + 2).zfill(4), result_dir, fname, str(i + 2).zfill(4)))
                break
    
    dir_name = os.path.dirname(split_dir) 
    
    with open(os.path.join(dir_name, outmae.replace('.mae', 'result_index.json')),'w') as f:
        json.dump(result, f, indent=4)
    f.close()
    
    df['mol2'] = df.index.map(lambda x : '{}-{}.txt'.format(fname, , str(x + 2).zfill(4)))
    df.loc[indexs].to_csv(os.path.join(dir_name, 'ML_result.csv'), index = False)

if __name__ == '__main__':
    args = parser.parse_args()
    dir_name = os.path.dirname(args.mae)
    outmae = os.path.basename(args.mae)
    csv_name = os.path.abspath(os.path.join(dir_name, outmae.replace('_pv.maegz', '_IFP.csv')))
    
    # Make IFP csv files
    print ('make IFP')
    make_ifp(args.mae, csv_name)

    # Get Result Json
    print ('get result json')
    df = pd.read_csv(csv_name)
    cpd_indexs = make_result_json(dir_name, df, outmae, args.col)

    # split ligand from pv and change to mol2
    print ('split ligand')

    split_dir = os.path.join(dir_name, 'split_ligand')
    os.makedirs(split_dir, exist_ok=True)

    split_ligand(args.mae, split_dir)

    # collect result
    print ('collect result')
    result_dir = os.path.join(dir_name, 'final')
    os.makedirs(result_dir, exist_ok=True)
    
    collect_result(result_dir, split_dir, cpd_indexs, df, outmae)

    print ('finish')
