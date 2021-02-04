#!/usr/bin/env python
#
# Read CSV from eprime_to_csv.py and perform study-specific analysis
# for GF WM task

import argparse
import pandas
import os

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Parse CSV for GF WM task')
    parser.add_argument('-o', '--outdir', help='Path to store the output summary CSV')
    parser.add_argument('eprime_csv', help='CSV file from eprime_to_csv.py', metavar='EPRIME_CSV')
    args = parser.parse_args()

    # Generate output CSV path+filename
    out_csv = os.path.basename(args.eprime_csv).replace('.csv','_summary.csv')    
    if args.outdir is None:
        out_csv = os.path.join(os.path.dirname(args.eprime_csv),out_csv)
    else:
        out_csv = os.path.join(args.outdir,out_csv)
    
    # Read in CSV
    edat = pandas.read_csv(args.eprime_csv)

    # Use the offset time of trigger item as start time
    start_trigger_idx = edat.loc[:,'GetReady.OffsetTime'].idxmin()
    start_time = edat.loc[start_trigger_idx,'GetReady.OffsetTime']

    # Times for each stimulus, removing rows with empty StimType
    info = edat.loc[edat.StimType.notna(),
        ('BlockType','StimType','Stim.OnsetTime','Stim.RT','Stim.ACC')]

    # Unique stimulus types, sorted
    stims = info.loc[:,('BlockType','StimType')].drop_duplicates()
    stims = stims.sort_values(by=['BlockType','StimType'],ignore_index=True)

    # Initialize various things
    stims['Condition'] = [() for x in range(stims.index.size)]
    stims['OnsetsSec'] = [() for x in range(stims.index.size)]
    stims['DurationsSec'] = [() for x in range(stims.index.size)]
    stims['Accuracy'] = [() for x in range(stims.index.size)]
    stims['PctAccuracy'] = [() for x in range(stims.index.size)]
    stims['RTms'] = [() for x in range(stims.index.size)]
    stims['MeanCorrectRTms'] = [() for x in range(stims.index.size)]
    stims['MedianCorrectRTms'] = [() for x in range(stims.index.size)]

    # For each stimulus, a list of onset times. We subtract the start time and convert to sec.
    # Also compute accuracy and RT.
    for s in range(stims.index.size):

        stim = stims.iloc[s,:]
        inds = (info.BlockType==stim.BlockType) & (info.StimType==stim.StimType)
        inds_correct = (info.BlockType==stim.BlockType) & (info.StimType==stim.StimType) \
            & (info.loc[:,'Stim.ACC']==1)

        stims.Condition[s] = (stim.BlockType + '_' + stim.StimType)

        stim_times = info.loc[inds,'Stim.OnsetTime']
        stim_times = round( (stim_times - start_time) / 1000, 1)
        stims.OnsetsSec[s] = list(stim_times)
    
        # Assume event durations are constant - hard coded rather than from eprime.txt
        stims.DurationsSec[s] = [2.5 for x in range(len(stims.OnsetsSec[s]))]
    
        stims.RTms[s] = list(round(info.loc[inds,'Stim.RT']))
        stims.MeanCorrectRTms[s] = round(info.loc[inds_correct,'Stim.RT'].mean())
        stims.MedianCorrectRTms[s] = round(info.loc[inds_correct,'Stim.RT'].median())

        stims.Accuracy[s] = list(info.loc[inds,'Stim.ACC'].astype(int))
        stims.PctAccuracy[s] = 100 * info.loc[inds,'Stim.ACC'].mean()


    # Display and write to file
    pandas.set_option('display.max_colwidth',100)
    print(stims)
    stims.to_csv(out_csv,index=False)



if __name__ == "__main__":
    main()
    
