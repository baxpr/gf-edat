#!/usr/bin/env python3
#
# Read CSV from eprime_to_csv.py and perform study-specific analysis
# for ESOP SPT task

import argparse
import pandas
import os

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Parse CSV for SPT task, ESOP version')
    parser.add_argument('-o', '--outcsv', help='Path to store the output summary CSV')
    parser.add_argument('eprime_csv', help='CSV file from eprime_to_csv.py', metavar='EPRIME_CSV')
    args = parser.parse_args()

    # Generate output CSV path+filename
    if args.outcsv is None:
        out_csv = os.path.basename(args.eprime_csv).replace('.csv','_summary.csv')
    else:
        out_csv = args.outcsv
    
    # Read in CSV
    edat = pandas.read_csv(args.eprime_csv)

    # Use the offset time of trigger item as RTTime of the Instructions page
    start_trigger_idx = edat.loc[:,'Instructions.RTTime'].idxmin()
    start_time = edat.loc[start_trigger_idx,'Instructions.RTTime']

    # Times for each stimulus, removing rows with empty ImageType
    info = edat.loc[edat.ImageType.notna(),
        (
        'ImageType',
        'PresentPicture.OnsetTime',
        'PresentPicture.CRESP',
        'PresentPicture.RT',
        'PresentPicture.ACC',
        )]

    # Target vs foil
    info.loc[:,'Target'] = 'Foil'
    info.loc[info['PresentPicture.CRESP']==7,'Target'] = 'Target'
    
    # Unique stimulus types, sorted
    stims = info.loc[:,('ImageType','Target')].drop_duplicates()
    stims = stims.sort_values(by=['ImageType','Target'],ignore_index=True)

    # Initialize various things
    stims['Condition'] = [() for x in range(stims.index.size)]
    stims['OnsetsSec'] = [() for x in range(stims.index.size)]
    stims['DurationsSec'] = [() for x in range(stims.index.size)]
    stims['Accuracy'] = [() for x in range(stims.index.size)]
    stims['PctAccuracy'] = [() for x in range(stims.index.size)]
    stims['RTms'] = [() for x in range(stims.index.size)]
    stims['MeanCorrectRTms'] = [() for x in range(stims.index.size)]
    stims['MedianCorrectRTms'] = [() for x in range(stims.index.size)]
    stims['MinCorrectRTms'] = [() for x in range(stims.index.size)]
    stims['MaxCorrectRTms'] = [() for x in range(stims.index.size)]

    # For each stimulus, a list of onset times. We subtract the start time and convert to sec.
    # Also compute accuracy and RT.
    for s in range(stims.index.size):

        stim = stims.iloc[s,:]
        inds = (info.ImageType==stim.ImageType) & (info.Target==stim.Target)
        inds_correct = inds & (info.loc[:,'PresentPicture.ACC']==1)

        stims.Condition[s] = (stim.ImageType + '_' + stim.Target)

        stim_times = info.loc[inds,'PresentPicture.OnsetTime']
        stim_times = round( (stim_times - start_time) / 1000, 1)
        stims.OnsetsSec[s] = list(stim_times)
    
        # Assume event durations are constant - hard coded rather than from eprime.txt
        stims.DurationsSec[s] = [1.0 for x in range(len(stims.OnsetsSec[s]))]
    
        stims.Accuracy[s] = list(info.loc[inds,'PresentPicture.ACC'].astype(int))
        stims.PctAccuracy[s] = round( 100 * info.loc[inds,'PresentPicture.ACC'].mean(), 1 )

        # Only have RTs for target trials
        if stim.Target=='Target':
            stims.RTms[s] = list(round(info.loc[inds,'PresentPicture.RT'], 0))
            stims.MeanCorrectRTms[s] = round(info.loc[inds_correct,'PresentPicture.RT'].mean(), 0)
            stims.MedianCorrectRTms[s] = round(info.loc[inds_correct,'PresentPicture.RT'].median(), 0)
            stims.MinCorrectRTms[s] = round(info.loc[inds_correct,'PresentPicture.RT'].min(), 0)
            stims.MaxCorrectRTms[s] = round(info.loc[inds_correct,'PresentPicture.RT'].max(), 0)


    # Write to file
    stims.to_csv(out_csv,index=False)



if __name__ == "__main__":
    main()
    
