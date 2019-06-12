#plots negatives and positives clustered to visualize

#import necessary
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

#plotting data
def bar_chart(datadate,subfolder,dark_rate):
    savedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/images/'
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    savename = savedir + 'bars_' + str(subfolder) + '.png'

    true_positives_third = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/true_positives'))
    false_negatives_third = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/false_negatives'))

    true_positives_fourth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/true_positives'))
    false_negatives_fourth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/false_negatives'))

    true_positives_sixth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/true_positives'))
    false_negatives_sixth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/false_negatives'))

    bar_width = 0.4
    bars_true_pos = [true_positives_third,true_positives_fourth,true_positives_sixth]
    bars_false_neg = [false_negatives_third,false_negatives_fourth,false_negatives_sixth]

    ind = np.arange(len(bars_true_pos))

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, bars_true_pos, bar_width, color = 'blue')
    rects2 = ax.bar(ind + bar_width, bars_false_neg, bar_width, color = 'red')

    dark_rate_third = dark_rate[0]
    dark_rate_fourth = dark_rate[1]
    dark_rate_sixth = dark_rate[2]

    ax.set_title('Risetime Type: ' + subfolder + '\nNoise Detection Rate, One Third Mean Peak: ' + dark_rate_third + '\nNoise Detection Rate, One Fourth Mean Peak: ' + dark_rate_fourth + '\nNoise Detection Rate, One Sixth Mean Peak: ' + dark_rate_sixth)
    ax.set_ylabel('Number of Files')
    ax.set_xlabel('Threshold',fontweight='bold')
    ax.set_xticks(ind + 0.5*bar_width)
    ax.set_xticklabels(('One Third Mean Peak','One Fourth Mean Peak','One Sixth Mean Peak'))

    ax.legend((rects1[0],rects2[0]),('\nDetected\nSPEs\n','\nMissed\nSPEs\n'),loc='center left',bbox_to_anchor=(1,0.5))

    #labelling bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, 1.005*height,'%d' % int(height + 0.5),ha='center',va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
    fig.savefig(savename,dpi=500)

#main function
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="bar chart",description="Generates bar chart comparing detection vs miss.")
    parser.add_argument('--datadate',type = str,help = 'date when data was gathered, YYYYMMDD', default = '20190516')
    parser.add_argument('--subfolder',type = str,help = 'how much the rise time was altered', default = 'raw')
    parser.add_argument('--dark_rate',type = list,help = 'occurence rate of noise being detected as spe, format = [1/3, 1/4, 1/6]', default = ['5 Hertz','10 Hertz','20 Hertz'])
    args = parser.parse_args()

    bar_chart(args.datadate,args.subfolder,args.dark_rate)