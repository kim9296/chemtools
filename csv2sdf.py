import pandas as pd
from argparse import ArgumentParser
from rdkit import Chem


################################ parameter ##############################################

# csv_name = 'result.csv'

# columns = [ 'cpd_name',  
#             'smiles',        
#             'AS_ENL',
#             'AS_AF9', 
#             'FS_50_ENL', 
#             'FS_90_ENL', 
#             'FS_50_AF9', 
#             'FS_90_AF9'
#             ]

##########################################################################################

parser = ArgumentParser(description='csv2sdf')
parser.add_argument('--csv', metavar='CSV', help='input csv', dest='csv', required=True)
parser.add_argument('--sdf', metavar='SDF', help='output sdf', dest='sdf', required=True)

def csv2sdf(csv_name, sdf_name):
    
    df = pd.read_csv(csv_name)

    for col in df.columns:
        if 'smiles' == col.lower():
            smiles_col = col
    
    writer = Chem.SDWriter(sdf_name)

    for i, row in df.iterrows():
        mol = Chem.MolFromSmiles(row[smiles_col])
        for col in df.columns:
            mol.SetProp(col, str(row[col]).strip())
        writer.write(mol)

if __name__ == '__main__':
    args = parser.parse_args()
    csv2sdf(args.csv, args.sdf)
    print ('finish')
