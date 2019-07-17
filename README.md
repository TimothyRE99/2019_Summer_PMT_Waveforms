# 2019_Summer_PMT_Waveforms

## p1
### Preliminary Steps
1. Collect data from pulse generator/oscilloscope/PMT setup, save to base directory
1. Create d0_info.txt file including information from physical setup, save to base directory (format below)
    * Data acquisition,<VALUE>
    * PMT HV (V),<VALUE>
    * Nominal gain,<VALUE>
    * DG 535 offset,<VALUE>
    * DG 535 trigger delay (ns),<VALUE>
    * DG 535 amplitude (V),<VALUE>
    * Oscilloscope sample rate (Hz),<VALUE>
    * Oscilloscope bandwidth (Hz),<VALUE>
    * Oscilloscope noise filter (bits),<VALUE>
    * Oscilloscope resistance (ohms),<VALUE>

### Processing Steps
1. p1/p1_sort (sort is called by p1, applies lowpass filter, determines which waveforms are SPEs or not)
1. d1rename (renames SPE files to have sequential numbers while keeping order, removing gaps)
1. baselineshift (calculates and removes remaining baseline from SPE files)
1. d1shift50 (calculates average index location of 50% rising point, shifts all 50% rising points to that location, makes time = 0 at that location, and chops off any indices that rolled over)
1. d1normalization (normalizes 50% rising centered waveforms for later use)
1. Histograms/Average Waveform
    * These can be done in any order, but must be done before final p1b step as p1b uses products of this step
1. p1b (processes waveforms to remove lingering doubles by comparing peak and charge to means of the histogram, creates d1_info.txt and adds to final dataset)

### Additional Programs
* 50risingcheck: Checks location of 50% rising point for files with such place located before index 370 
* deletedfilerename: Deletes a file and then renames every file after it in a directory to be 1 less in the number
* gausshistogram: Determines the guess mean and standard deviation from central data for use in readhistogram
* info_file: Takes information from program and d0_info.txt to create d1_info.txt
* readhistogram: Takes a histogram txt file and gauss histogram guesses to make a plot of the histogram and fit a gaussian to the central data
* readwaveform: Takes a waveform txt file and turns it into several arrays, one for each header, time, and volts
* waveform_viewer: Cycles through waveforms in a directory and displays them as a plot
* writehistogram: Takes in values that need to go into histograms and the labels based on those values and writes a histogram txt file
* writewaveform: Takes in arrays for time, volts, and headers and writes them to a waveform txt file

## p2
### Preliminary Steps
* No preliminary steps for P2. All functions create their own directories as needed

### Processing Steps
1. p2_prelim (moves files from d1_final_spes to d2_raw, including info file, and renames appropriately)
1. p2_risetime_check/p2_lowpass(manually) (Used to establish comparison graphs of tau vs. rise time and determine proper taus to use in p2 for doubling each step of the rise time, will need to run each of these three times, once for each double, quadruple, and octuple, changing which files you're using each time)
1. p2 (doubles waveform risetime, then doubles again, then doubles final time in three steps, uses values from average WF, adds noise each time to mimic analogue LPF circuit)

### Additional Programs
* p2_lowpass: Lowpass filter formula/function to be called from p2 processing stages
* p2_lpf_plotting: Plots the four versions of d2 data for each file, cycling through to compare, set title to include rise times
* readwaveform: same as p1, ported over to allow use by p2 files
* waveform_viewer: same as p1, ported over to allow use by p2 files
* writewaveform: same as p1, ported over to allow use by p2 files
* readhistogram: same as p1, ported over to allow use by p2 files
* writehistogram: same as p1, ported over to allow use by p2 files
* gausshistogram: same as p1, ported over to allow use by p2 files
* determine10_90risetime: same as p1, ported over to allow use by p2 files

## p3
### Preliminary Steps
* No preliminary steps for P3. All functions create their own directories as needed

### Processing Steps
1. p3_prelim (Moves files from d2 to d3, including info file, and renames appropriately)
1. p3 (Downsamples and digitizes waveforms)

### Additional Programs
* p3_downdigit_plotting.py: plots the four versions of d3 for each file, cycling through to compare, option to include scatter points
* writewaveform: same as p1, ported over to allow use by p3 files
* readhistogram: same as p1, ported over to allow use by p3 files
* three_stage_compare: plots 3 versions of same waveform, one from after each processing step

## Trigger Studies
### Preliminary Steps
* No preliminary steps for trigger. All functions create their own directories as needed

### Processing Steps
1. determinepeakamplitude.py: calculates histogram of peak amplitudes of waveforms to be studied
1. trigger_study.py: determines if a waveform would be a hit or miss from 1/3, 1/4, and 1/6 average peak height and then runs bar_chart.py to plot this as well as dark rate

### Additional Programs
* bar_chart.py: program to plot barchart of hits vs. misses for triggering as well as dark rate in title
* readwaveform: same as p1, ported over to allow use by trigger files
* writewaveform: same as p1, ported over to allow use by trigger files
* readhistogram: same as p1, ported over to allow use by trigger files
* writehistogram: same as p1, ported over to allow use by trigger files
* gausshistogram: same as p1, ported over to allow use by trigger files

## Timing Studies
### Preliminary Steps
* No preliminary steps for timing. All functions create their own directories as needed

### Processing Steps
1. timing_CFD.py: Applies CFD function to waveforms to prepare for calculating zero crossing location
1. zcf_determine.py: Calculates proper zero crossing location and interpolates time, generates histogram of zero crossing times

### Additional Programs
* readwaveform: same as p1, ported over to allow use by timing files
* writewaveform: same as p1, ported over to allow use by timing files
* readhistogram: same as p1, ported over to allow use by timing files
* readhistogram_log: same as readhistogram but with log scale for y-axis
* writehistogram: same as p1, ported over to allow use by timing files
* gausshistogram: same as p1, ported over to allow use by timing files
* plot_waveform: opens waveforms and shows plot of them and CFD process

## Charge Studies
### Preliminary Steps
* No preliminary steps for charge. All functions create their own directories as needed

### Processing Steps
1. charge_calc.py: Calculates charges through various summing methods of normal and downsampled waveforms and creates histograms
1. charge_compare.py: Calculates percent error (without absolute value) between normal and downsample waveform charges and creates histogram

### Additional Programs
* readwaveform: same as p1, ported over to allow use by charge files
* readhistogram: same as p1, ported over to allow use by charge files
* writehistogram: same as p1, ported over to allow use by charge files
* gausshistogram: same as p1, ported over to allow use by charge files

## Extraneous
### Additional Programs
* datamanipulatetest: Original method of sorting out SPEs, ineffective
* datareadtest: Original way of reading data into array, ineffective
* enumerate_test: Tests functionality of [k for k, x in enumerate(check) if x]
* namecheck: Checks original name of file based on number after renaming
* npwheretest: Tests functionality of numpy.where