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

    # Use the onset of trigger item as start time
    start_trigger_idx = edat.loc[:,'scanstart2.OnsetTime'].idxmin()
    start_time = edat.loc[start_trigger_idx,'scanstart2.OnsetTime']

    # Times for each stimulus, keeping only rows marked MainStimuli
    info = edat.loc[edat.Running=='MainStimuli',
        ('Running','duration','tone','MainScreen.OnsetTime','MainScreen.RT','MainScreen.ACC')]

    # Unique stimulus types
    info['Condition'] = ['' for x in range(info.index.size)]
    info.loc[info.tone=='stimuli\\silence.wav','Condition'] = 'Silence'
    info.loc[info.tone=='stimuli\\1000.wav','Condition'] = 'Tone'
    info.loc[info.tone=='stimuli\\1200.wav','Condition'] = 'Oddball'

    stims = info.loc[:,('Running','Condition')].drop_duplicates().reset_index(drop=True)

    # Initialize various things
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
        inds = (info.Condition==stim.Condition)
        inds_correct = (info.Condition==stim.Condition) & (info.loc[:,'MainScreen.ACC']==1)

        stim_times = info.loc[inds,'MainScreen.OnsetTime']
        stim_times = round( (stim_times - start_time) / 1000, 1)
        stims.OnsetsSec[s] = list(stim_times)

        stim_durs = info.loc[inds,'duration']
        stim_durs = round( stim_durs / 1000, 1)
        stims.DurationsSec[s]  = list(stim_durs)
        
        # Only the oddball trials have responses recorded
        if stim.Condition=='Oddball':
            
            stims.RTms[s] = list(round(info.loc[inds,'MainScreen.RT']))
            stims.MeanCorrectRTms[s] = round(info.loc[inds_correct,'MainScreen.RT'].mean())
            stims.MedianCorrectRTms[s] = round(info.loc[inds_correct,'MainScreen.RT'].median())

            stims.Accuracy[s] = list(info.loc[inds,'MainScreen.ACC'].astype(int))
            stims.PctAccuracy[s] = round( 100 * info.loc[inds,'MainScreen.ACC'].mean(), 1)


    # Display and write to file
    pandas.set_option('display.max_colwidth',100)
    print(stims)
    stims.to_csv(out_csv,index=False)



if __name__ == "__main__":
    main()
    
