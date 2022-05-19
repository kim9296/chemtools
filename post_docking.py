from argparse import ArgumentParser

parser = ArgumentParser(description='post docking process')
parser.add_argument('--mae', metavar='MAE', help='input pose viewer file', dest='mae', required=True)

def make_ifp(mae):
    csv = os.path.abspath(mae.replace('_pv.maegz', '_IFP.csv'))
    sdf = csv.replace('.csv', '.sdf')
    os.system('$SCHRODINGER/run interaction_fingerprints.py -i {} -ocsv {}'.format(mae, csv))
    os.system('$SCHRODINGER/utilities/sdconvert -n 2: -imae {} -osd {}'.format(mae, sdf))

if __name__ == '__main__':
    args = parser.parse_args()
    
    # Make IFP csv files
    print ('make IFP and convert sdf')
    make_ifp(args.mae)

    print ('finish')
