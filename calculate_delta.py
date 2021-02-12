#!/usr/bin/env python3

import datetime
from datetime import date
#from datetime import datetime, timedelta
import io
import csv
from csv import writer
from csv import reader
import time
import pandas as pd
#import matplotlib.pyplot as plt



def IG_epoch(milsec,ts):
	#unix_epoch = 
	time_s = milsec/1000 #TIme from shortcode in seconds wrt to IG_epoch
	time_p = ts #Time from HTML in seconds wrt to unix_epoch
	#IG_epoch = unix_epoch + time_p - time_s
	x = time_p - time_s #IG_epoch wrt to unix_epoch
	#print(x)
	IG_epoch = datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')
	return IG_epoch


if __name__ == "__main__":
	#my_filtered_csv = pd.read_csv(filename, usecols=['col1', 'col3', 'col7']) if it's necessary to filter out the columns and read
	#my_csv = pd.read_csv("dateVSvid_duration.csv")
	my_csv = pd.read_csv("Shortcode_epoch_estimate.csv")
	column = my_csv['epoch_estimate'].tolist()
	#duration =  my_csv['duration'].tolist()
	#shortcode = my_csv['shortcode'].tolist()
	# for item1 in duration:
	# 	item1 = int(item1)
	#print(column)
	off_values = []
	for item2 in column:
		date = datetime.datetime.strptime(item2, '%Y-%m-%d %H:%M:%S')
		IG_epoch = datetime.datetime.strptime("2011-08-24 21:07:00",'%Y-%m-%d %H:%M:%S')
		off_by = date - IG_epoch
		off_by = int(off_by.seconds)
		off_values.append(off_by)
	my_csv['off_by'] = off_values
	my_csv.to_csv('Shortcode_epoch_estimate.csv')
	# off_values, duration, shortcode = zip(*sorted(zip(off_values, duration, shortcode)))
	# with open("plot.csv", "w") as g:
	# 	writer = csv.writer(g)
	# 	writer.writerows(zip(shortcode, off_values, duration))
	# plt.plot(off_values, duration)
	# plt.show()


