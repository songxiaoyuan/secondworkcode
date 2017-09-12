# -*- coding:utf8 -*-
import csv
import band_and_trigger
import basic_fun as bf

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20
LONG =1
SHORT =0


class BandAndTriggerFade(object):
	"""docstring for BandAndTriggerFade"""
	def __init__(self,param_dic):
		super(BandAndTriggerFade, self).__init__()
		# self.arg = arg
		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._lastprice_map = dict()
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		self._csv_data = []

		self._max_profit = 0
		self._limit_max_draw_down = param_dic["limit_max_draw_down"]
		self._limit_max_profit = param_dic["limit_max_profit"]
		self._limit_max_loss = param_dic["limit_max_loss"]

		self._multiple = param_dic["multiple"]

		self._rsi_array = []
		self._pre_rsi_lastprice =0 
		self._now_bar_rsi_tick = 0
		self._rsi_period = param_dic["rsi_period"]
		self._rsi_bar_period = param_dic["rsi_bar_period"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]

		self._param_period = param_dic["param_period"]


		# self._limit_twice_sd = 2
		self._band_status = 0
		self._direction = param_dic["direction"]
		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1
		# self._band_add_edge = 1
		# self._close_band_num =2

		# band param
		self._param_open_edge = param_dic["band_open_edge"]
		self._param_close_edge = param_dic["band_close_edge"]

		self._open_lastprice = 0
		self._profit = 0

		self._bigger_band = 3
		# self._ris_data = 0

		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		if len(self._lastprice_array) ==0:
			print "this is init function " + str(self._config_file)
			tmp_pre_ema_array = []
			tmp_rsi_lastprice = []
			config_file = "../config_pic/"+str(self._config_file)
			bf.get_config_info(tmp_pre_ema_array,self._lastprice_array,self._lastprice_map
				,self._rsi_array,tmp_rsi_lastprice,config_file)
			if len(tmp_pre_ema_array)==0:
				self._pre_ema_val = 0
				self._pre_rsi_lastprice = 0 
			else:
				self._pre_ema_val = tmp_pre_ema_array[0]
				self._pre_rsi_lastprice = tmp_rsi_lastprice[0]


	def __del__(self):
		print "this is the over function"
		# bf.write_config_info(self._pre_ema_val,self._lastprice_array
		# 	,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],self._config_file)
		path_new = "../tmp/test_fade_band_data"+".csv"
		bf.write_data_to_csv(path_new,self._csv_data)

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		md_array[LASTPRICE] = float(md_array[LASTPRICE])
		md_array[VOLUME] = float(md_array[VOLUME])
		md_array[OPENINTEREST] = float(md_array[OPENINTEREST])
		md_array[TURNONER] = float(md_array[TURNONER])
		md_array[BIDPRICE1] = float(md_array[BIDPRICE1])
		md_array[ASKPRICE1] = float(md_array[ASKPRICE1])


		self._pre_md_price = self._now_md_price
		self._now_md_price = md_array

		lastprice = self._now_md_price[LASTPRICE]
		# print lastprice
		if self._direction ==LONG:
			openval = self._now_middle_value - self._param_open_edge*self._now_sd_val
			if openval - lastprice > self._bigger_band:
				self._band_status = -1
		elif self._direction ==SHORT:
			openval = self._now_middle_value + self._param_open_edge*self._now_sd_val
			if lastprice - openval > self._bigger_band:
				self._band_status = 1
		if len(self._pre_md_price) ==0:
			return
			# self._rsi_array.append(0)
		else:
			# self._rsi_array.append(lastprice - self._pre_md_price[LASTPRICE])
			if self._now_bar_rsi_tick >= self._rsi_bar_period:
				# 表示已经到了一个bar的周期。
				tmpdiff = lastprice - self._pre_rsi_lastprice		
				self._pre_rsi_lastprice = lastprice
				self._now_bar_rsi_tick = 1
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				self._rsi_array.append(tmpdiff)
			else:
				self._now_bar_rsi_tick +=1
				tmpdiff = lastprice - self._pre_rsi_lastprice
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				# self._ris_data = 0

		
		if len(self._lastprice_array) < self._param_period:
			self._lastprice_array.append(lastprice)
			# this is we dont start the period.
			ema_period = len(self._lastprice_array)
			pre_ema_val = bf.get_ema_data(lastprice,self._pre_ema_val,ema_period)
			self._pre_ema_val = pre_ema_val
			# save the pre_ema_val and return
			if lastprice not in self._lastprice_map:
				self._lastprice_map[lastprice] =1
			else:
				self._lastprice_map[lastprice] +=1
			return True
		else:
			self._lastprice_array.append(lastprice)
			front_lastprice = self._lastprice_array[0]
			self._lastprice_array.pop(0)
			if front_lastprice != lastprice:
				if lastprice not in self._lastprice_map :
					self._lastprice_map[lastprice] = 1
				else:
					self._lastprice_map[lastprice] +=1

				self._lastprice_map[front_lastprice] -=1

		# start the judge
		if self._moving_theo =="EMA":
			self._now_middle_value = bf.get_ema_data(lastprice,self._pre_ema_val,self._param_period)
			self._pre_ema_val = self._now_middle_value
		else:
			self._now_middle_value = bf.get_ma_data(self._lastprice_array,self._param_period)
		
		# self._now_sd_val =bf.get_sd_data(self._now_md_price[TIME], self._lastprice_array,self._param_period)			
		self._now_sd_val =bf.get_sd_data_by_map(self._lastprice_map,self._param_period)	
		# self.f.write(str(self._now_md_price[TIME])+","+str(lastprice)+","+str(self._now_middle_value)+","+str(self._now_sd_val)+","+str(self._ris_data)+"\n")

		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],round(self._now_middle_value,2),
							round(self._now_sd_val,2),round(self._ris_data,2),0,0,0,0,0,0]
		self._csv_data.append(tmp_to_csv)

		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			# self._now_interest +=1
			# print "we start to open"
			self._open_lastprice = self._now_md_price[LASTPRICE]
			self._now_interest +=1
			self._max_profit = 0
			mesg= "the time of open: "+self._now_md_price[TIME] + ",the price: " + str(self._now_md_price[LASTPRICE])
			self._file.write(mesg+"\n")
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			# self._now_interest -=1
			# print "we need to close"
			if self._direction ==LONG:
				self._profit +=(self._now_md_price[LASTPRICE] - self._open_lastprice)
			elif self._direction ==SHORT:
				self._profit +=(self._open_lastprice - self._now_md_price[LASTPRICE])
			self._open_lastprice = 0
			self._max_profit = 0
			self._now_interest = 0
			mesg= "the time of close:"+self._now_md_price[TIME] + ",the price: " + str(self._now_md_price[LASTPRICE])
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):

		is_band_open = self.is_band_open_time(self._direction,self._now_md_price[LASTPRICE],
											self._now_middle_value,self._now_sd_val,self._param_open_edge,
											self._bigger_band)
		return is_band_open

	def is_band_open_time(self,direction,lastprice,middle_val,open_edge,sd_val,bigger_edge):
		# this is used to judge is time to band open
		if direction ==LONG:
			openval = middle_val - open_edge*sd_val
			if self._band_status == -1 and (self._lastprice - openval) > bigger_edge:
				self._band_status = 1
				return True
		elif direction ==SHORT:
			openval = middle_val + open_edge*sd_val
			if self._band_status == 1 and (openval - self._lastprice) > bigger_edge:
				self._band_status = -1
				return True
		return False

	def is_band_close_time(self,direction,lastprice,middle_val,sd_val,loss_edge,profit_edge,bigger_edge):
		# this is used to judge is time to band open
		if direction ==LONG:
			profitval = middle_val + profit_edge*sd_val
			lossval = middle_val - loss_edge*sd_val - bigger_edge 
			if lastprice > profitval or lastprice < lossval:
				return True
		elif direction ==SHORT:
			profitval = middle_val - profit_edge*sd_val
			lossval = middle_val + loss_edge*sd_val +bigger_edge
			if lastprice > lossval or lastprice < profitval:
				return True
		return False

	def is_trend_close_time(self):
		# this is used to jude the time to close return bool
		# first base band, if the sd is too small ,wo need to bigger
		# current the close signal is only band
		if self._now_interest <=0:
			return False

		# base the max draw down
		# 达到最大盈利之后，或者最大亏损之后，就开始平仓。这个是系统自带的。
		# 现在根据李总的说法，添加了maxdrawdown的功能。！！！！！
		if self._direction ==LONG:
			tmp_profit = self._now_md_price[LASTPRICE] - self._open_lastprice
		elif self._direction ==SHORT:
			tmp_profit = self._open_lastprice - self._now_md_price[LASTPRICE]
		else:
			return False
		if tmp_profit < (0 - self._limit_max_loss) or tmp_profit > self._limit_max_profit:
			# print "the profit is bigger or loss"
			return True

		is_drawdown = bf.is_max_draw_down(self._direction,self._now_md_price[LASTPRICE],self._open_lastprice
			,self._multiple,self._max_profit,self._limit_max_draw_down)
		self._max_profit = is_drawdown[1]
		if is_drawdown[0]:
			mesg= 'this is the max draw down ' + str(self._max_profit)
			self._file.write(mesg +"\n")
			return True

		close_band = self._param_open_edge + self._now_interest - self._close_band_num -1
		# print "the interest is "+ str(self._now_interest) + " the colse band is "  +str(close_band)

		is_band_close = self.is_band_close_time(self._direction,self._lastprice,
													self._now_middle_value,self._now_sd_val,
													self._param_open_edge,self._param_close_edge,self._bigger_band)
		
		return is_band_close
		

	def get_total_profit(self):
		return self._profit

def getSortedData(data):
	ret = []
	night = []
	zero = []
	day = []
	nightBegin = 21*3600
	nightEnd = 23*3600+59*60+60
	zeroBegin = 0
	zeroEnd = 9*3600 - 100
	dayBegin = 9*3600
	dayEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[20].split(":")
		# print timeLine
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])

		if nowTime >= zeroBegin and nowTime <zeroEnd:
			zero.append(line)
		elif nowTime >= dayBegin and nowTime <= dayEnd:
			day.append(line)
		elif nowTime >=nightBegin and nowTime <=nightEnd:
			night.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	for line in night:
		ret.append(line)
	for line in zero:
		ret.append(line)
	for line in day:
		ret.append(line)

	return ret
# read the md data from csv, it uesd to like the csv
def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	# only get the day data
	ret = getSortedData(ret)
	return ret

def start_to_run_md(band_obj,data):
	for row in data:
		band_obj.get_md_data(row)

def create_band_obj(data,param_dict):
	file = param_dict["file"]
	for i in xrange(0,2):
		param_dict["direction"] = i
		band_and_trigger_obj = BandAndTriggerFade(param_dict)
		if i==0:
			# continue
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../data/"+filename+".csv"
	csv_data = read_data_from_csv(path)
	path = "../outdata/"+filename+"_trade.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_max_profit":25000,"limit_max_loss":10000,"multiple":10
				,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
				,"band_open_edge":3,"config_file":399,"param_period":7200
				,"limit_max_draw_down":0,"file":file}

	for band_type in xrange(0,1):
		if band_type ==0:
			param_dict["band_open_edge"] =2
			param_dict["limit_max_draw_down"] =0
			param_dict["limit_max_loss"] =10
			param_dict["band_close_edge"] =2
			create_band_obj(csv_data,param_dict)
	file.close()



if __name__=='__main__': 
	# main("ru1709_20170622")
	# data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data2 =[20170703,20170704,20170705,20170706,20170707,20170711,20170712,20170713,20170714,20170717]
	# data = data1+data2
	data = [20170821]
	for item in data:
		path = "rb1801_"+ str(item)
		print path
		main(path)	
	# print WRITETOFILE