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

def is_band_open_time(direction,lastprice,middle_val,sd_val,open_edge):
	# this is used to judge is time to band open
	if direction ==LONG:
		upval = middle_val + open_edge*sd_val
		if lastprice > middle_val and lastprice < upval:
			return True
	elif direction ==SHORT:
		downval = middle_val - open_edge*sd_val
		if lastprice < middle_val and lastprice > downval:
			return True
	return False

def is_band_close_time(direction,lastprice,middle_val,sd_val,open_edge,close_edge,cur_rsi_data,limit_rsi_data,sd_lastprice):
	# this is used to judge is time to band is close time
	if 10000*(sd_val/lastprice) <=sd_lastprice:
		return False
	if direction ==LONG:
		profitval = middle_val + close_edge*sd_val
		lossvla = middle_val - open_edge*sd_val
		# 尽量避免损失，如果达到止损条件，即使止损
		if lastprice < lossvla:
			return True
		# 判断止盈条件，大于几倍的band，并且同时rsi大于80，然后可能在加上最大回撤的值。
		# 因为ris是按照这个bar来计算的，所以应该一段时间判断一次，如果没有达到这个段的时间，应该就直接不平仓
		if lastprice > profitval and cur_rsi_data >= limit_rsi_data and cur_rsi_data >=0:
			return True
	elif direction ==SHORT:
		profitval = middle_val - close_edge*sd_val
		lossval = middle_val + open_edge*sd_val
		if lastprice > lossval:
			return True
		ris = 100 - cur_rsi_data
		if lastprice < profitval and ris >= limit_rsi_data and cur_rsi_data >=0 :
			return True
	return False

def is_trigger_up_time(now_md_price,pre_md_price,spread_edge,multiple):
	# judge the tirgger size price is up
	diff_volume = now_md_price[VOLUME] - pre_md_price[VOLUME]
	diff_turnover = now_md_price[TURNONER] -pre_md_price[TURNONER]
	if diff_volume ==0 or diff_turnover ==0 or multiple ==0:
		return False

	avg_price = float(diff_turnover)/diff_volume/multiple
	tmp = 100*(avg_price - pre_md_price[BIDPRICE1])/(pre_md_price[ASKPRICE1] - pre_md_price[BIDPRICE1])
	# print str(diff_volume) + " , " + str(diff_turnover) + " , " +str(multiple) + " , " + str(avg_price) 
	if tmp >= spread_edge:
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
		return True
	return False

def is_trigger_size_open_time(direction,now_md_price,pre_md_price,volume_open_edge,
							openinterest_edge,spread_edge,multiple):
	# this is used to judge the time of trigger size to open
	# print now_md_price[VOLUME] - pre_md_price[VOLUME]
	if now_md_price[VOLUME] - pre_md_price[VOLUME] < volume_open_edge:
		return False
	if now_md_price[OPENINTEREST] - pre_md_price[OPENINTEREST] <= openinterest_edge:
		return False
	if direction ==LONG:
		return is_trigger_up_time(now_md_price,pre_md_price,spread_edge,multiple)
	elif direction ==SHORT:
		return is_trigger_down_time(now_md_price,pre_md_price,spread_edge,multiple)
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

def get_rsi_data(rsi_array,period):
	# get the current rsi ,the array is the increase and low val
	if len(rsi_array) ==0:
		return 0
	rise =0
	total =0
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

def get_rsi_data2(tmpdiff,rsi_array,period):
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



if __name__=='__main__': 
	print "this is basic fun like c++ so"
	tmp = is_band_open_time(1,10,10.2,2,0.5)
	print tmp