import datetime
import numpy as np

#open and read d0_info.txt
def read_info_file(datadate):
    file_name = 'd0_info.txt'
    fin = 'G:/data/watchman/'+datadate+'_watchman_spe/'+file_name
    myfile = open(fin,'r')      #opening d0_info.txt file
    y = np.array([])            #initializing array
    #appendin values for each line in the d0_info.txt files to array
    for line in myfile:
        y = np.append(y,str(line.split(',')[1]))
    myfile.close
    #setting values in array to appropriate variable name
    acq_date_time = y[0]
    pmt_hv = y[1]
    gain =y[2]
    offset = y[3]
    trig_delay = y[4]
    amp = y[5]
    fsps = y[6]
    band = y[7]
    nfilter = y[8]
    r = y[9]
    return(acq_date_time,pmt_hv,gain,offset,trig_delay,amp,fsps,band,nfilter,r)

# Creates info file
def info_file(datadate):
    acq_date_time, pmt_hv, gain, offset, trig_delay, amp, fsps, band, nfilter, r = read_info_file(datadate)
    now = datetime.datetime.now()
    file_name = 'd1_info.txt'
    fin = 'G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/'+file_name
    myfile = open(fin, 'w')
    myfile.write('Data acquisition,' + acq_date_time)                   # date and time of raw data acquisition from previous info file
    myfile.write('Data processing,' + str(now))                         # current date & time
    myfile.write('\nSource data,G:/data/watchman/'+datadate+'_watchman_spe/')   # path to source data
    myfile.write('\nDestination data,G:/data/watchman/'+datadate+'_watchman_spe/d1/d1_final_spes/') # path to folder of current data
    myfile.write('\nPMT HV (V),' + str(pmt_hv))                         # voltage of PMT from previous info file
    myfile.write('Nominal gain,' + str(gain))                           # gain of PMT from previous info file
    myfile.write('DG 535 offset,' + str(offset))                        # offset of pulse generator from previous info file
    myfile.write('DG 535 trigger delay (ns),' + str(trig_delay))        # trigger delay of pulse generator from previous info file
    myfile.write('DG 535 amplitude (V),' + str(amp))                    # amplitude of pulse generator from previous info file
    myfile.write('Oscilloscope sample rate (Hz),' + str(fsps))          # sample rate of oscilloscope from previous info file
    myfile.write('Oscilloscope bandwidth (Hz),' + str(band))            # bandwidth of oscilloscope from previous info file
    myfile.write('Oscilloscope noise filter (bits),' + str(nfilter))    # oscilloscope noise filter from previous info file
    myfile.write('Oscilloscope resistance (ohms),' + str(r))            # resistance of oscilloscope from previous info file
    myfile.close()
    return

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="info file",description="write d1_info.txt.")
    parser.add_argument("--datadate",type=str,help='date of collection, yyyymmdd',default='20190516')
    args = parser.parse_args()

    info_file(args.datadate)