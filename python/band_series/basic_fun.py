# -*- coding:utf8 -*-
import math
import csv

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20
LONG =1
SHORT =0

def is_band_open_time(direction,lastprice,middle_val,sd_val,open_edge1,open_edge2):
	# this is used to judge is time to band open
	if direction ==LONG:
		upval = middle_val + open_edge2*sd_val
		if lastprice > middle_val + open_edge1*sd_val and lastprice < upval:
			return True
	elif direction ==SHORT:
		downval = middle_val - open_edge2*sd_val
		if lastprice < middle_val - open_edge1*sd_val and lastprice > downval:
			return True
	return False

def is_band_close_time(direction,lastprice,middle_val,sd_val,close_edge,cur_rsi_data,limit_rsi_data):
	# this is used to judge is time to band is close time
	if direction ==LONG:
		profitval = middle_val + close_edge*sd_val
		# 判断止盈条件，大于几倍的band，并且同时rsi大于80，然后可能在加上最大回撤的值。
		# 因为ris是按照这个bar来计算的，所以应该一段时间判断一次，如果没有达到这个段的时间，应该就直接不平仓
		if lastprice > profitval and cur_rsi_data >= limit_rsi_data and cur_rsi_data >=0:
			return True
	elif direction ==SHORT:
		profitval = middle_val - close_edge*sd_val
		ris = 100 - cur_rsi_data
		if lastprice < profitval and ris >= limit_rsi_data and cur_rsi_data >=0 :
			return True
	return False

def is_diff_volume_open_time(tmp_sum_diff_volume,diff_volume_array,limit_multiple,limit_large_period):
	left_index = len(diff_volume_array) - limit_large_period
	if len(diff_volume_array) ==0:
		return False
	if left_index <0:
		left_index = 0
	for x in xrange(left_index+1,len(diff_volume_array)):
		if (diff_volume_array[left_index] * limit_multiple) > diff_volume_array[x]:
			return False
	if (diff_volume_array[left_index] * limit_multiple) > tmp_sum_diff_volume :
		return False
	return True

def is_lastprice_series_open_time(direction,series_lastprice,limit_series_lastprice):

	if direction ==LONG:
		if series_lastprice >=  limit_series_lastprice:
			return True
	elif direction ==SHORT:
		series_lastprice = 0 - series_lastprice
		if series_lastprice >=  limit_series_lastprice:
			return True
	return False

def is_lastprice_open_time(direction,lastprice,lastprice_array,limit_large_period):
	left_index = len(lastprice_array) - limit_large_period
	if len(lastprice_array) ==0 or left_index < 0:
		return False
	series = 0
	if direction == LONG:
		for x in xrange(left_index+1,len(lastprice_array)):
			if lastprice_array[x] >= lastprice_array[left_index]:
				series +=1
			else:
				return False
		if lastprice >= lastprice_array[left_index]:
			series +=1
	elif direction ==SHORT:
		for x in xrange(left_index+1,len(lastprice_array)):
			if lastprice_array[x] <= lastprice_array[left_index]:
				series +=1
			else:
				return False
		if lastprice <= lastprice_array[left_index]:
			series +=1
	else:
		return False
	if series == limit_large_period:
		return True
	else:
		return False
			


def get_ema_data(lastprice,pre_ema_val,period):
	# this is used to get the ema get ema data
	if period ==1:
		return lastprice
	tmp = float(((period -1)*pre_ema_val + 2*lastprice))/(period + 1)
	return tmp


def get_ma_data(price_array,period):
	# this is used to get the ma data
	if len(price_array) ==0 or period ==0:
		return 0
	tmpsum =0
	l = len(price_array)
	for i in xrange(l-1,-1,-1):
		if i >= (l - period):
			tmpsum +=price_array[i]
	ret=float(tmpsum)/period
	return ret


def get_sd_data_by_map(price_map,period):
	tmpsum =0
	for item in price_map:
		tmpsum = tmpsum + (item*price_map[item])
	avg = float(tmpsum)/period
	tmpsum = 0
	for item in price_map:
		tmpsum += ((item - avg)* (item - avg)*price_map[item])
	tmpsum = float(tmpsum)/period
	return math.sqrt(tmpsum) 


def get_rsi_data(tmpdiff,rsi_array,period):
	# get the current rsi ,the array is the increase and low val
	period = period -1
	if len(rsi_array) ==0:
		return 0
	rise =0
	total =0
	if tmpdiff >0:
		rise += tmpdiff
		total +=tmpdiff
	else:
		total -=tmpdiff
	l = len(rsi_array)
	for i in xrange(l-1,-1,-1):
		if i >= (l - period):
			tmp = rsi_array[i]
			if tmp > 0:
				rise +=tmp
				total +=tmp
			else:
				total -=tmp
	if rise ==0 or total ==0:
		return 0
	return 100*float(rise)/total

def write_data_to_csv(path,data):
	csvfile = file(path, 'wb')
	writer = csv.writer(csvfile)
 	writer.writerows(data)
	csvfile.close()

def is_max_draw_down(direction,cur_price,open_price,multiple,max_profit,limit_max_draw_down):
	if open_price ==0 or limit_max_draw_down ==0:
		return (False,max_profit)
	if direction ==LONG:
		tmp_profit = cur_price - open_price;
	elif direction ==SHORT:
		tmp_profit = open_price - cur_price;
	else :
		return (False,0)
	tmp_profit = tmp_profit * multiple
	if max_profit < tmp_profit:
		max_profit = tmp_profit
	# f = open("rsidata.txt","a")
	# f.write(str(time)+","+str(cur_price)+","+str(open_price)+","+str(max_profit)+","+str(tmp_profit)+"\n")
	if (max_profit - tmp_profit) >= limit_max_draw_down :
		return (True,max_profit)
	else:
		return (False,max_profit)



def write_config_info(pre_ema_val,lastprice_array,rsi_array,rsi_array_period,pre_rsi_lastprice,config_path):
	config_file = open(config_path,"w")
	line1 = "pre_ema_val:,"+str(pre_ema_val)
	line2 = "lastpricearray:"
	for i in lastprice_array:
		line2 = line2 + ","+str(i)
	line3 = "rsiarray:"
	for i in xrange(len(rsi_array)-rsi_array_period,len(rsi_array)):
		line3 = line3 + "," + str(rsi_array[i])
	line4 = "pre_rsi_val:,"+str(pre_rsi_lastprice)
	write_lines = [line1+'\n',line2+'\n',line3+'\n',line4+'\n']
	config_file.writelines(write_lines)
	config_file.close()

def get_config_info(pre_ema_val_array,lastprice_array,lastprice_dic,rsi_array,rsi_pre_lastprice_array,config_path):
	try:
		config_file = open(config_path)
	except Exception as e:
		config_file = open(config_path,"w")
		return
	config_file = open(config_path)
	lines = config_file.readlines()
	for line in lines:
		if "pre_ema_val" in line:
			print "this is pre_ema_val"
			line = line.split(',')
			pre_ema_val_array.append(float(line[1].strip()))
		elif "lastpricearray" in line:
			print "this is lastprice array"
			line = line.split(',')[1:]
			for tmp in line:
				tmp = float(tmp.strip())
				if tmp not in lastprice_dic:
					lastprice_dic[tmp] =1
				else:
					lastprice_dic[tmp] +=1
				lastprice_array.append(tmp)
			# print "the length of lastprice is: " + str(len(lastprice_array))
		elif "rsiarray" in line:
			print "this is rsiarray"
			line = line.split(',')[1:]
			for tmp in line:
				rsi_array.append(float(tmp.strip()))
		elif "pre_rsi_val" in line:
			print "this is the pre rsi lastprice"
			rsi_pre_lastprice_array.append(float(line.split(',')[1].strip()))
		else:
			print "this is not the config line"
	config_file.close()


if __name__=='__main__': 
	print "this is basic fun like c++ so"
	# tmp = is_band_open_time(1,10,10.2,2,0.5)
	# print tmp
	data_array = [1,2,3,4,5]
	tmp = get_ema_data(data_array,1)
	print tmp