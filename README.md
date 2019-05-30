# 2019_Summer_PMT_Waveforms
## p1
### Preliminary Steps
* Set up directories (This ensures programs work properly when saving files)
    * Base directory: G:/data/watchman/YYYYMMDD_watchman_spe/ in which "YYYYMMDD" is the date of data collection in that format
        * d1/
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
* Collect data from pulse generator/oscilloscope/PMT setup, save to base directory
* Create d0_info.txt file including information from physical setup, save to base directory (format below)
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
* p1/p1_sort (sort is called by p1, applies lowpass filter, determines which waveforms are SPEs or not)
* d1rename (renames SPE files to have sequential numbers while keeping order, removing gaps)
* baselineshift (calculates and removes remaining baseline from SPE files)
* d1shift50 (calculates average index location of 50% rising point, shifts all 50% rising points to that location, makes time = 0 at that location, and chops off any indices that rolled over)
* d1normalization (normalizes 50% rising centered waveforms for later use)
* Histograms/Average Waveform
    * These can be done in any order, but must be done before final p1b step as p1b uses products of this step
* p1b (processes waveforms to remove lingering doubles by comparing peak and charge to means of the histogram, creates d1_info.txt and adds to final dataset)

## p2/3
