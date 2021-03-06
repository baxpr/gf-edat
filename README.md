# E-Prime processing for specific fMRI tasks Oddball, SPT, WM

## Example command line
```
singularity run --contain --cleanenv \
  --bind INPUTS:/INPUTS \
  --bind OUTPUTS:/OUTPUTS \
  container-gf-edat.simg \
  --project PROJECT \
  --subject SUBJECT \
  --session SESSION \
  --scan SCAN \
  --task WM \
  --eprime_txt /INPUTS/eprime.txt
```

## Inputs
```
project, subject, session, scan   XNAT-specific info for report if desired
task                              Oddball, OddballOld, SPT, or WM
eprime_txt                        Path to E-Prime's .txt log file
```

## Outputs
```
eprime_summary.pdf    Text report for viewing
EPRIME_CSV            E-Prime log converted to csv/spreadsheet format
SUMMARY_CSV           List of task/stimulus conditions with RT, accuracy,
                         onsets, durations
```
