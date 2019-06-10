#plots negatives and positives clustered to visualize

#import necessary
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

#plotting data
datadate = '20190516'
subfolder = 'raw'
savedir = 'G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/images/'
if not os.path.exists(savedir):
    os.makedirs(savedir)
savename = savedir + 'bars_' + str(subfolder) + '.png'

true_positives_third = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/true_positives'))
true_negatives_third = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/true_negatives'))
false_positives_third = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/false_positives'))
false_negatives_third = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/false_negatives'))

true_positives_fourth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/third/'+subfolder+'/true_positives'))
true_negatives_fourth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/true_negatives'))
false_positives_fourth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/false_positives'))
false_negatives_fourth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/fourth/'+subfolder+'/false_negatives'))

true_positives_sixth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/true_positives'))
true_negatives_sixth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/true_negatives'))
false_positives_sixth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/false_positives'))
false_negatives_sixth = len(os.listdir('G:/data/watchman/'+datadate+'_watchman_spe/studies/trigger/sixth/'+subfolder+'/false_negatives'))

bar_width = 0.15
bars_true_pos = [true_positives_third,true_positives_fourth,true_positives_sixth]
bars_false_neg = [false_negatives_third,false_negatives_fourth,false_negatives_sixth]
bars_true_neg = [true_negatives_third,true_negatives_fourth,true_negatives_sixth]
bars_false_pos = [false_positives_third,false_positives_fourth,false_positives_sixth]

ind = np.arange(len(bars_true_pos))

fig, ax = plt.subplots()
rects1 = ax.bar(ind, bars_true_pos, bar_width, color = 'blue')
rects2 = ax.bar(ind + bar_width, bars_false_neg, bar_width, color = 'red')
rects3 = ax.bar(ind + 2*bar_width, bars_true_neg, bar_width, color = 'green')
rects4 = ax.bar(ind + 3*bar_width, bars_false_pos, bar_width, color = 'purple')

ax.set_title('Risetime Type: ' + subfolder)
ax.set_ylabel('Number of Files')
ax.set_xlabel('Threshold',fontweight='bold')
ax.set_xticks(ind + 1.5*bar_width)
ax.set_xticklabels(('One Third Mean Peak','One Fourth Mean Peak','One Sixth Mean Peak'))

ax.legend((rects1[0],rects2[0],rects3[0],rects4[0]),('\nTrue\nPositives\n','\nFalse\nNegatives\n','\nTrue\nNegatives\n','\nFalse\nPositives\n'),loc='center left',bbox_to_anchor=(1,0.5))

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, 1.005*height,'%d' % int(height),ha='center',va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)

plt.get_current_fig_manager().window.showMaximized()
plt.show()
fig.savefig(savename,dpi=500)