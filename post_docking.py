from argparse import ArgumentParser
import pandas as pd
import numpy as np
from rdkit import Chem

parser = ArgumentParser(description='post docking process')
parser.add_argument('--csv', help='input IFP csv file', dest='csv', required=True)
parser.add_argument('--xcol', help='ligand column name', dest='xcol', required=True)
parser.add_argument('--ycol', help='y coloumn name', dest='ycol', default=None)
parser.add_argument('--res',
                    metavar='<residue>',
                    help='key residue which has hbond with ligand (ex: 117,119)',
                    dest='res',
                    default = None)

def str2range(inp, maxlen):
    result = list()
    temp = inp.split(',')
    for x in temp:
        if ':' in x:
            tmp = x.split(':')
            if tmp[0] == '':
                tmp[0] = 1
            elif tmp[1] == '':
                tmp[1] = maxlen
            result += range(int(tmp[0]) - 1, int(tmp[1]))
        else:
            result.append(int(x))
    return result

def make_dataset(csv, xcol, res, ycol=None):
    sdf = csv.replace('.csv', '.sdf')
    df = pd.read_csv(csv)
    df['index'] = df.index.map(lambda x: x)
    
    ycols = [x for x in df.columns if ycol in x]
    if len(ycols) == 2:
        df[ycol] = np.where(pd.notnull(df[ycols[0]]) == True, df[ycols[0]], df[ycols[1]])
    elif len(ycols) > 2:
        raise ('too many ycols, check IFP.csv')
    else:
        df[ycol] = df[ycols[0]]

    df = df.sort_values(by='r_i_glide_gscore', ascending=True).reset_index(drop=True)
    raw = Chem.SDMolSupplier(sdf)
    raw_mols = list()
    for mol in raw:
        raw_mols.append(mol)    

    result = dict()
    indexs = list()
    for i, row in df.iterrows():
        if row[xcol] not in result.keys():
            result[row[xcol]] = row['index']
            indexs.append(i)

    # indexs = list(result.values())
    df.loc[indexs].to_csv(csv.replace('.csv', '_full_dataset.csv'), index = False)
    
    out_mol = Chem.SDWriter(sdf.replace('.sdf', '_full_dataset.sdf'))
    for i in list(result.values()):
        out_mol.write(raw_mols[i])
    out_mol.close()

    if res is not None:
        
        res_columns = ['r_glide_res:A{}_hbond'.format(x.strip()) for x in res.split(',')]

        result = dict()
        indexs = list()
        for i, row in df.iterrows():
            if row[xcol] not in result.keys() and sum(row[res_columns]) != 0:
                result[row[xcol]] = row['index']
                indexs.append(i)

        # indexs = list(result.values())
        df.loc[indexs].to_csv(csv.replace('.csv', '_pose_dataset.csv'), index = False)
        
        out_mol = Chem.SDWriter(sdf.replace('.sdf', '_pose_dataset.sdf'))
        for i in list(result.values()):
            out_mol.write(raw_mols[i])
        out_mol.close()

if __name__ == '__main__':
    args = parser.parse_args()
    
    # Make Dataset
    print ('make Dataset from IFP')
    make_dataset(args.csv, args.xcol, args.res, args.ycol)

    print ('finish')
