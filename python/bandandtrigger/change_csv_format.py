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
	tmp = period
	for i in xrange(l-1,-1,-1):
		if i >= (l - period):
			total_sum += (spread_array[i]*volume_array[i]*tmp)
			weight_sum += (volume_array[i]*tmp)
			tmp -=1
	if total_sum ==0 or weight_sum ==0:
		return 0
	return float(total_sum)/weight_sum

def get_continue_price(lastprice,lastprice_array):
	if len(lastprice_array) ==0:
		return 0
	ret = 0
	if lastprice > lastprice_array[-1]:
		ret = 1
	elif lastprice < lastprice_array[-1]:
		ret = -1
	l = len(lastprice_array)-2
	lastprice = lastprice_array[-1]
	for i in xrange(l,-1,-1):
		if ret ==0:
			return ret
		if ret >0 and lastprice > lastprice_array[i]:
			ret +=1
		elif ret <0 and lastprice < lastprice_array[i]:
			ret -=1
		else:
			return ret
		lastprice = lastprice_array[i]
	return ret

def get_continue_wvad(lastprice,lastprice_array,volume_array):
	if len(lastprice_array) != len(volume_array):
		print "the lastprice array is not len the volume array"
		return 0
	if len(lastprice_array) ==0:
		return 0

	period = 120
	begin_index = max(0,len(lastprice_array) - period)
	min_price = 0
	max_price = 0
	volume_sum = 0
	for x in xrange(begin_index,len(lastprice_array)):
		if min_price ==0 or min_price > lastprice_array[x]:
			min_price = lastprice_array[x]
		if max_price ==0 or max_price < lastprice_array[x]:
			max_price = lastprice_array[x]
		volume_sum += volume_array[x]

	if max_price == min_price:
		return 0

	ret = (float(lastprice) - float(lastprice_array[begin_index]))/(float(max_price) - float(min_price))
	ret = ret * float(volume_sum)
	return round(ret,2)





def change_last_three_format(data):
	volume_array = []
	openinterest_array = []
	spread_array = []
	avg_array = []
	lastprice_array = []
	period = 60
	for line in data:
		# volume_array.append(line[5])
		# openinterest_array.append(line[6])
		# spread_array.append(line[7])
		lastprice = line[1]
		volume = line[5]
		continue_price = get_continue_price(lastprice,lastprice_array)
		# continut_wvad = get_continue_wvad(lastprice,lastprice_array,volume_array)
		line.append(continue_price)
		# line.append(continut_wvad)
		lastprice_array.append(lastprice)
		# volume_array.append(volume)
		# avg_array.append(line[11])
		# line[8] = round(get_sum(volume_array,period),2)
		# line[9] = round(get_sum(openinterest_array,period),2)
		# line[10] = round(get_weighted_mean(spread_array,volume_array,period),2)
		# line[11] = continue_price
		# line[12] = continut_wvad
	


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

	change_last_three_format(data)
	
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
	data = [20170821,20170822,20170823,20170824,20170825,20170828,20170829,20170830]
	# data = [20170822]
	# instrumentid_array = ["ru1801","ru1801","zn1710","ni1801","cu1710","pb1710","hc1801","i1801"]
	instrumentid_array = ["rb1801"]
	for item in data:
		for instrumentid in instrumentid_array:
			path = "../data/"+instrumentid+ "_"+str(item)+"_band_data.csv"
			print path
			change_format(path)


if __name__ == '__main__':
	main()
	# data = [0,1,2,3,4,5]
	# l = len(data)-1
	# for x in xrange(l,-1,-1):
	# 	print data[x]