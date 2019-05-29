#renames all files after a certain number to one less than their current number if a file needs to be deleted

#import necessary
import os

#main body
def delete_rename(directory,data_date,deleted_number):
    os.remove('G:/data/watchman/'+data_date+'_watchman_spe/d1/'+directory+'/D1--waveforms--%0.05d.txt' % deleted_number)
    Nloops = len(os.listdir('G:/data/watchman/'+data_date+'_watchman_spe/d1/'+directory))
    for i in range(deleted_number+1,Nloops+1):
        print(i)
        os.rename('G:/data/watchman/'+data_date+'_watchman_spe/d1/'+directory+'/D1--waveforms--%.05d.txt' % i, 'G:/data/watchman/'+data_date+'_watchman_spe/d1/'+directory+'/D1--waveforms--%.05d.txt' % (i-1))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='deletedfilerename', description='deleting file and renaming all files after it')
    parser.add_argument('--directory',type = str,help = 'directory to work in', default = 'AVOID DELETION')
    parser.add_argument('--data_date',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--deleted_number',type=int,help='file number to delete',default = 6147)
    args = parser.parse_args()

    delete_rename(args.directory,args.data_date,args.deleted_number)