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

def is_band_open_time(direction,lastprice,middle_val,bigger_edge1,bigger_edge2):
	# this is used to judge is time to band open
	if direction ==LONG:
		upval = middle_val + bigger_edge2
		downval = middle_val + bigger_edge1
		if lastprice > downval  and lastprice < upval:
			return True
	elif direction ==SHORT:
		downval = middle_val - bigger_edge2
		upval = middle_val - bigger_edge1
		if lastprice < upval  and lastprice > downval:
			return True
	return False

def is_band_close_time(direction,lastprice,middle_val,close_edge):
	# this is used to judge is time to band is close time
	if direction ==LONG:
		lossval = middle_val - close_edge
		# 尽量避免损失，如果达到止损条件，即使止损
		if lastprice < lossval:
			return True
	elif direction ==SHORT:
		lossval = middle_val + close_edge
		if lastprice > lossval:
			return True
	return False

def is_trigger_up_time(now_md_price,pre_md_price,spread_edge,multiple):
	# judge the tirgger size price is up
	diff_volume = now_md_price[VOLUME] - pre_md_price[VOLUME]
	diff_turnover = now_md_price[TURNONER] -pre_md_price[TURNONER]
	if diff_volume ==0 or diff_turnover ==0 or multiple ==0:
		return False

	avg_price = float(diff_turnover)/diff_volume/multiple
	if pre_md_price[ASKPRICE1] == pre_md_price[BIDPRICE1]:
		return False
	tmp = 100*(avg_price - pre_md_price[BIDPRICE1])/(pre_md_price[ASKPRICE1] - pre_md_price[BIDPRICE1])
	# print str(diff_volume) + " , " + str(diff_turnover) + " , " +str(multiple) + " , " + str(avg_price) 
	if tmp >= spread_edge:
		# print "the tmp is " + str(tmp) + "the spread is "+ str(spread_edge)
		# print "the diff turn over : " + str(diff_turnover) + ", the diff volume :" + str(diff_volume)
		# print str(tmp)+" , "+str(spread_edge)+" , "+str(avg_price)+","+str(pre_md_price[ASKPRICE1])+","+str(pre_md_price[BIDPRICE1])
		return True
	return False

def is_trigger_down_time(now_md_price,pre_md_price,spread_edge,multiple):
	# judge the tirgger size price is down
	diff_volume = now_md_price[VOLUME] - pre_md_price[VOLUME]
	diff_turnover = now_md_price[TURNONER] - pre_md_price[TURNONER]
	if diff_volume ==0 or diff_turnover ==0 or multiple ==0:
		return False
	avg_price = float(diff_turnover)/diff_volume/multiple
	tmp = 100*(pre_md_price[ASKPRICE1] - avg_price)/(pre_md_price[ASKPRICE1] - pre_md_price[BIDPRICE1])
	if tmp >= spread_edge:
		# print "the tmp is " + str(tmp) + "the spread is "+ str(spread_edge)
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


def is_trigger_size_open_time(direction,diff_volume,limit_diff_volume,spread,limit_spread):
	# this is used to judge the time of trigger size to open
	if diff_volume < limit_diff_volume:
		return False
	if direction ==LONG:
		if spread >= limit_spread:
			return True
	elif direction ==SHORT:
		spread = 100 - spread
		if spread >= limit_spread:
			return True
	return False

def is_trigger_size_close_time(direction,now_md_price,pre_md_price,volume_open_edge,
							openinterest_edge,spread_edge,multiple):
	# this is used to judge the time of trigger size to close
	if now_md_price[VOLUME] - pre_md_price[VOLUME] < volume_open_edge:
		return False
	if now_md_price[OPENINTEREST] - pre_md_price[OPENINTEREST] <= openinterest_edge:
		return False
	if direction ==LONG:
		return is_trigger_down_time(now_md_price,pre_md_price,spread_edge,multiple)
	elif direction ==SHORT:
		return is_trigger_up_time(now_md_price,pre_md_price,spread_edge,multiple)
	return False

def get_ema_data(lastprice,pre_ema_val,period):
	# this is used to get the ema get ema data
	if period ==1:
		return lastprice
	tmp = float(((period -1)*pre_ema_val + 2*lastprice))/(period + 1)
	return tmp

def get_ema_data_2(data_array,period):
	l = len(data_array)
	begin = max(0,l - period)
	tmp = 1
	sum_tmp =0
	for i in xrange(begin,l):
		sum_tmp += data_array[i]*tmp
		tmp +=1
	return float(2*sum_tmp)/(tmp *(tmp-1))

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
	print time + "," + str(ret)
	return ret

def get_sd_data(time,price_array,period):
	# this is used to get the sd data
	if len(price_array) ==0 or period ==0:
		return 0
	tmpsum = 0
	l = len(price_array)
	for i in xrange(l-1,-1,-1):
		if i>=(l - period):
			tmpsum +=price_array[i]
	avg = float(tmpsum)/period
	tmpsum = 0
	for i in xrange(l-1,-1,-1):
		if i>= (l - period):
			tmpsum += (price_array[i]-avg)**2
	tmpsum = float(tmpsum)/period
	return math.sqrt(tmpsum)

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

def get_sum(num_array,period):
	ret = 0
	l = len(num_array)
	for i in xrange(l-1,-1,-1):
		if i >= (l - period):
			ret +=num_array[i]
	return ret

def get_weighted_mean(target_array,weight_array,period):
	if len(target_array) != len(weight_array):
		print "basic_fun.py: the target array is not == weight array"
		return 0
	l = len(target_array)
	total_sum = 0
	weight_sum = 0
	for i in xrange(l-1,-1,-1):
		if i >= (l - period):
			total_sum += (target_array[i]*weight_array[i])
			weight_sum += weight_array[i]
	if total_sum ==0 or weight_sum ==0:
		return 0
	return float(total_sum)/weight_sum

def write_config_info(pre_ema_val,lastprice_array,config_path):
	config_file = open(config_path,"w")
	line1 = "pre_ema_val:,"+str(pre_ema_val)
	line2 = "lastpricearray:"
	for i in lastprice_array:
		line2 = line2 + ","+str(i)
	write_lines = [line1+'\n',line2+'\n']
	config_file.writelines(write_lines)
	config_file.close()

def get_config_info(pre_ema_val_array,lastprice_array,config_path):
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
				lastprice_array.append(tmp)
		else:
			print "this is not the config line"
	config_file.close()

def is_wvad_open_time(direction,wvad,limit_wvad):
	if direction ==LONG:
		if wvad > limit_wvad:
			return True
	elif direction ==SHORT:
		wvad = 0 - wvad
		if wvad > limit_wvad:
			return True
	return False

def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	# only get the day data
	return ret

if __name__=='__main__': 
	print "this is basic fun like c++ so"
	# tmp = is_band_open_time(1,10,10.2,2,0.5)
	# print tmp
	data_array = [1,2,3,4,5]
	tmp = get_ema_data_2(data_array,1)
	print tmp