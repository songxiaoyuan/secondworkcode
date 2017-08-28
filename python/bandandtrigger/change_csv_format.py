# -*- coding:utf8 -*-

import os
import csv

def get_ema_data(data_array,period):
	l = len(data_array)
	begin = max(0,l - period)
	tmp = 1
	sum_tmp =0
	for i in xrange(begin,l):
		sum_tmp += data_array[i]*tmp
		tmp +=1
	return float(2*sum_tmp)/(tmp *(tmp-1))

def get_sum(num_array,period):
	ret = 0
	l = len(num_array)
	for i in xrange(l-1,-1,-1):
		if i >= (l - period):
			ret +=num_array[i]
	return ret

def get_weighted_mean(spread_array,volume_array,period):
	if len(spread_array) != len(volume_array):
		print "basic_fun.py: the target array is not == weight array"
		return 0
	l = len(spread_array)
	total_sum = 0
	weight_sum = 0
	for i in xrange(l-1,-1,-1):
		if i >= (l - period):
			total_sum += (spread_array[i]*volume_array[i])
			weight_sum += volume_array[i]
	if total_sum ==0 or weight_sum ==0:
		return 0
	return float(total_sum)/weight_sum

def change_last_three_format(data):
	volume_array = []
	openinterest_array = []
	spread_array = []
	# avg_array = []
	period = 10
	for line in data:
		volume_array.append(line[5])
		openinterest_array.append(line[6])
		spread_array.append(line[7])
		# avg_array.append(line[11])
		line[8] = get_sum(volume_array,period)
		line[9] = get_sum(openinterest_array,period)
		line[10] = round(get_weighted_mean(spread_array,volume_array,period),2)
		# line[12] = get_sum(avg_array,period)
	


def change_format(path):
	f = open(path,'rb')
	data = []
	reader = csv.reader(f)
	for row in reader:
		for x in xrange(2,11):
			row[x] = round(float(row[x]),2)
		data.append(row)
		# if row[5] !=0:
		# 	data.append(row)
	f.close()

	print "start to format the data"
	change_last_three_format(data)
	print "has finish the format data"
	
	csvfile = file(path, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(data)
	csvfile.close()

def get_files(file_dir): 
    for root, dirs, files in os.walk(file_dir):
        for file in files:
        	if "band_data" in file:
        		tmp_path = os.path.join(root,file)
        		print tmp_path
        		change_format(tmp_path)

def main():
	# path = "../data/cu1710_20170815_band_data.csv"
	# path = "../data/hc1710_20170815_band_data.csv"
	# path = "../zn"
	# get_files(path)
	data = [20170817]
	# instrumentid_array = ["ru1801","rb1710","zn1709","pb1709"]
	instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801"]
	for item in data:
		for instrumentid in instrumentid_array:
			path = "../data/"+instrumentid+ "_"+str(item)+"_band_data.csv"
			print path
			change_format(path)


if __name__ == '__main__':
	main()