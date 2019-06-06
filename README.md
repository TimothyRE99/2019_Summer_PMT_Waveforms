# 2019_Summer_PMT_Waveforms

## p1
### Preliminary Steps
1. Set up directories (This ensures programs work properly when saving files)
    * Base directory: G:/data/watchman/YYYYMMDD_watchman_spe/ in which "YYYYMMDD" is the date of data collection in that format
        * d1
            * d1_50centered
            * d1_baseline_shifted
            * d1_final_doubles
            * d1_final_spes
            * d1_histograms
                * histogram_images
            * d1_normalized
            * d1_raw
            * d1_renamed
            * not_spe
            * unsure_if_spe
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
1. Set up directories (This ensures programs work properly when saving files)
    * Base directory: G:/data/watchman/YYYYMMDD_watchman_spe/ in which "YYYYMMDD" is the date of data collection in that format
        * d2
            * d2_histograms
                * histogram_images
            * d2_images
            * d2_raw

### Processing Steps
1. p2_prelim (moves files from d1_final_spes to d2_raw, including info file, and renames appropriately)
1. p2_risetime_check/p2_lowpass(manually) (Used to establish comparison graphs of tau vs. rise time and determine proper taus to use in p2 for doubling each step of the rise time, will need to run each of these three times, once for each double, quadruple, and octuple, changing which files you're using each time)
1. p2 (doubles waveform risetime, then doubles again, then doubles final time in three steps, uses values from average WF)

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

## Extraneous
### Additional Programs
* datamanipulatetest: Original method of sorting out SPEs, ineffective
* datareadtest: Original way of reading data into array, ineffective
* enumerate_test: Tests functionality of [k for k, x in enumerate(check) if x]
* namecheck: Checks original name of file based on number after renaming
* npwheretest: Tests functionality of numpy.where