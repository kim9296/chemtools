
import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser(description='Preprocess Raw Inhibition Data')
parser.add_argument('--csv', help='csv file', required=True, type=str)
parser.add_argument('--ref', help='smiles csv file', required=True, type=str)


def fill_smiles(csv_name, ref_name):
    
    df = pd.read_csv(csv_name)
    df = df.fillna(method='pad')
    df_ref = pd.read_csv(ref_name)
    
    out_name = csv_name.replace('raw', 'result')

    temp = {name:value for name, value in zip(df_ref['Molecule Name'].tolist(), df_ref['SMILES'].tolist())}
    
    idxs = list()

    for i, row in df.iterrows():
        if row['Compound ID'] in temp.keys():
            idxs.append(i)
    
    df = df.loc[idxs].reset_index(drop=True)
    df['SMILES'] = df['Compound ID'].map(lambda x : temp[x])
    df[['Plate ID', 'Compound ID', 'SMILES', 'Min (%)', 'IC50', 'IC90']].rename(columns={'Plate ID' : 'batch', 'Compound ID' : 'cpd_id', 'Min (%)' : 'inh'}).to_csv(out_name, index = False)

if __name__  == '__main__':
    args = parser.parse_args()
    csv_name = args.csv
    ref_name = args.ref

    fill_smiles(csv_name, ref_name)

    print ('finish')