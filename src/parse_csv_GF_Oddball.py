#!/usr/bin/env python3
#
# Read CSV from eprime_to_csv.py and perform study-specific analysis
# for GF Oddball task

import argparse
import pandas
import os

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Parse CSV for GF Oddball task')
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

    # Use the offset of trigger item as start time
    start_trigger_idx = edat.loc[:,'Start1.OffsetTime'].idxmin()
    start_time = edat.loc[start_trigger_idx,'Start1.OffsetTime']

    # Times for each stimulus, keeping only rows marked MainStimuli
    info = edat.loc[(edat.Procedure=='StandardProc') | (edat.Procedure=='DeviantProc'),
        ('Procedure','StandardTone.OnsetTime','StandardTone.RT','StandardTone.ACC',
        'DeviantTone.OnsetTime','DeviantTone.RT','DeviantTone.ACC')]

    # Unique stimulus types
    info['Condition'] = ['' for x in range(info.index.size)]
    info.loc[info.Procedure=='StandardProc','Condition'] = 'Standard'
    info.loc[info.Procedure=='DeviantProc','Condition'] = 'Deviant'

    stims = info.loc[:,('Procedure','Condition')].drop_duplicates().reset_index(drop=True)


    # Initialize various things
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
        inds = (info.Condition==stim.Condition)
        inds_correct = (info.Condition==stim.Condition) & (info.loc[:,stim.Condition+'Tone.ACC']==1)

        stim_times = info.loc[inds,stim.Condition+'Tone.OnsetTime']
        stim_times = round( (stim_times - start_time) / 1000, 1)
        stims.OnsetsSec[s] = list(stim_times)
        stims.DurationsSec[s]  = [0.5 for x in range(len(stims.OnsetsSec[s]))]
            
        stims.RTms[s] = list(round(info.loc[inds,stim.Condition+'Tone.RT']))
        stims.MeanCorrectRTms[s] = round(info.loc[inds_correct,stim.Condition+'Tone.RT'].mean(), 0)
        stims.MedianCorrectRTms[s] = round(info.loc[inds_correct,stim.Condition+'Tone.RT'].median(), 0)
        stims.MinCorrectRTms[s] = round(info.loc[inds_correct,stim.Condition+'Tone.RT'].min(), 0)
        stims.MaxCorrectRTms[s] = round(info.loc[inds_correct,stim.Condition+'Tone.RT'].max(), 0)
        
        stims.Accuracy[s] = list(info.loc[inds,stim.Condition+'Tone.ACC'].astype(int))
        stims.PctAccuracy[s] = round( 100 * info.loc[inds,stim.Condition+'Tone.ACC'].mean(), 1)


    # Write to file
    stims.to_csv(out_csv,index=False)



if __name__ == "__main__":
    main()
    
