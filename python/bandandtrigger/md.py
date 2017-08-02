# -*- coding:utf8 -*-
import csv
import basic_fun

TIME = 0
LASTPRICE = 1
MIDDLE = 2
SD = 3
RSI = 4
DIFF_VOLUME = 5
DIFF_OPENINTEREST = 6
SPREAD = 7
EMA_DIFF_VOLUME = 8
EMA_DIFF_OPENINTEREST = 9
EMA_SPREAD = 10
LONG =1
SHORT =0

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._now_middle_value =0
		self._now_sd_val = 0
		self._lastprice = 0
		self._direction = param_dic["direction"]


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


		# self._limit_twice_sd = 2

		self._direction = param_dic["direction"]
		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		# band param
		self._param_open_edge = param_dic["band_open_edge"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_close_edge =param_dic["band_profit_edge"]
		self._param_period = param_dic["band_period"]
		

		# trigger param
		self._param_volume_open_edge = param_dic["volume_open_edge"]
		self._param_open_interest_edge = param_dic["open_interest_edge"]
		self._param_spread = param_dic["spread"]

		self._ris_data = 0

		self._limit_sd = param_dic["limit_sd"]
		self._limit_sd_open_edge = param_dic["limit_sd_open_edge"]
		self._limit_sd_close_edge = param_dic["limit_sd_close_edge"]

		self._now_interest = 0
		self._limit_interest = 1


	def __del__(self):
		print "this is the over function"
		# bf.write_config_info(self._pre_ema_val,self._lastprice_array
		# 	,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],self._config_file)

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		# md_array[TIME] = float(md_array[TIME])
		md_array[LASTPRICE] = float(md_array[LASTPRICE])
		md_array[MIDDLE] = float(md_array[MIDDLE])
		md_array[SD] = float(md_array[SD])
		md_array[RSI] = float(md_array[RSI])
		md_array[DIFF_VOLUME] = float(md_array[DIFF_VOLUME])
		md_array[DIFF_OPENINTEREST] = float(md_array[DIFF_OPENINTEREST])
		md_array[SPREAD] = float(md_array[SPREAD])
		md_array[EMA_DIFF_VOLUME] = float(md_array[EMA_DIFF_VOLUME])
		md_array[EMA_DIFF_OPENINTEREST] = float(md_array[EMA_DIFF_OPENINTEREST])
		md_array[EMA_SPREAD] = float(md_array[EMA_SPREAD])


		self._lastprice = md_array[LASTPRICE]
		# print lastprice
		self._ris_data = md_array[RSI]
		self._now_middle_value = md_array[MIDDLE]
		self._now_sd_val = md_array[SD]



		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._now_interest +=1
			# print "we start to open"
			self._open_lastprice = lastprice
			self._max_profit = 0
			mesg= "the time of open: "+md_array[TIME] + ",the price: " + str(lastprice)
			mesg1 = "the diff volume: "+str(md_array[EMA_DIFF_VOLUME])+", the interest: " + str(md_array[EMA_DIFF_OPENINTEREST]) + ", the spread: "+ str(md_array[EMA_SPREAD])
			self._file.write(mesg+"\n")
			self._file.write(mesg1+"\n")
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			self._now_interest -=1
			# print "we need to close"
			if self._direction ==LONG:
				self._profit +=(self._now_md_price[LASTPRICE] - self._open_lastprice)
			elif self._direction ==SHORT:
				self._profit +=(self._open_lastprice - self._now_md_price[LASTPRICE])
			self._open_lastprice = 0
			self._max_profit = 0
			mesg= "the time of close:"+md_array[TIME]+ ",the price: " + str(lastprice)
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):

		open_val = self._param_open_edge
		is_band_open = bf.is_band_open_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,open_val,
											self._limit_sd,self._limit_sd_open_edge)
		# return is_band_open
		if is_band_open ==False:
			return False
		is_trigger_open = bf.is_trigger_size_open_time(self._direction,self._now_md_price,self._pre_md_price,
													self._param_volume_open_edge,self._param_open_interest_edge,
													self._param_spread,self._multiple,self._diff_volume_array,
													self._diff_open_interest_array,
													self._diff_spread_array,self._diff_period)
		return is_trigger_open

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
		
		# if tmp_profit >= self._max_profit:
		# 	self._max_profit = tmp_profit
		# # 如果达到最大回撤之后，也开始平仓，这个可以自己添加
		# tmp_draw_down = self._max_profit - tmp_profit
		# # print tmp_draw_down
		# if tmp_draw_down > self._draw_down:
		# 	print "the max draw down!!"
		# 	return True


		# if self._now_sd_val < self._param_limit_sd_value and self._now_sd_val > self._limit_twice_sd:
		# 	# open_val = self._param_limit_bigger*self._param_open_edge
		# 	open_val = self._param_loss_edge
		# 	# close_val = self._param_limit_bigger*self._param_close_edge
		# 	close_val = self._param_close_edge + self._param_limit_bigger
		# elif self._now_sd_val <= self._limit_twice_sd:
		# 	open_val = self._param_loss_edge
		# 	close_val = self._param_close_edge + self._param_limit_bigger
		# else:
		loss_val = self._param_loss_edge
		close_val = self._param_close_edge
		is_band_close = bf.is_band_close_time(self._direction,self._now_md_price[LASTPRICE],
											self._now_middle_value,self._now_sd_val,loss_val,close_val
											,self._ris_data,self._limit_rsi_data,self._limit_sd,self._limit_sd_close_edge)
		return is_band_close
		


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
	# for line in night:
	# 	ret.append(line)
	# for line in zero:
	# 	ret.append(line)
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
	data = getSortedData(ret)
	return data

def start_to_run_md(band_obj,data):
	for row in data:
		band_obj.get_md_data(row)

def create_band_obj(data,param_dict):
	file = param_dict["file"]
	for i in xrange(0,2):
		param_dict["direction"] = i
		band_and_trigger_obj = band_and_trigger.BandAndTrigger(param_dict)
		if i==0:
			# continue
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
			# if write_to_file ==True:
			# 	print "start to write the file"
			# 	csv_data = band_and_trigger_obj.get_to_csv_data()
			# 	path_new = "../data/"+filename+ "_band_data" +".csv"
			# 	basic_fun.write_data_to_csv(path_new,csv_data)
		else:
			print "方向是long的交易情况："
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../data/"+filename+"_band_data.csv"
	csv_data = read_data_from_csv(path)
	path = filename+"_trade.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_max_profit":250,"limit_max_loss":30,"multiple":5
				,"rsi_bar_period":100,"limit_rsi_data":80,"rsi_period":10
				,"diff_period":1
				,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
				,"limit_max_draw_down":0,"file":file
				,"open_interest_edge":0,"spread":100,"volume_open_edge":900
				,"limit_sd":20,"limit_sd_open_edge":1,"limit_sd_close_edge":3,"config_file":310}

	for band_type in xrange(0,7):
		if band_type ==0:
			continue
			mesg = "完全按照1退出，3退出。900进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =900
			param_dict["sd_lastprice"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==1:
			# continue
			mesg = "1，3退出，diff_period =1 900进入,limit sd = 4"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =20
			create_band_obj(csv_data,param_dict)
		elif band_type ==2:
			continue
			mesg = "1，3退出，sd／last price <9 不平，diff_period =6 300进入 spread =90 volume_open_edge=300"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =300
			param_dict["sd_lastprice"] =9
			param_dict["diff_period"] =6
			param_dict["spread"] =95
			param_dict["open_interest_edge"] = 800
			create_band_obj(csv_data,param_dict)
		elif band_type ==3:
			continue
			mesg = "1，3退出，sd／last price <9 不平，1000进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =1000
			param_dict["sd_lastprice"] =9
			create_band_obj(csv_data,param_dict)
		elif band_type ==4:
			continue
			mesg = "完全按照1退出，3退出。1200进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =1200
			param_dict["sd_lastprice"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==5:
			continue
			mesg = "1，3退出，sd／last price <9 不平，1200进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =1200
			param_dict["sd_lastprice"] =9
			create_band_obj(csv_data,param_dict)
		elif band_type ==6:
			continue
			mesg = "根据1退出 3退出,添加Max draw down"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =1000
			param_dict["limit_max_draw_down"] =10
			create_band_obj(csv_data,param_dict)
		else:
			pass
	file.close()



if __name__=='__main__': 
	# main("ru1709_20170622")
	# data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data2 =[20170703,20170704,20170705,20170706,20170707,20170711,20170712,20170713,20170714,20170717]
	# data = data1+data2
	data = [20170801]
	for item in data:
		path = "pb1709_"+ str(item)
		print path
		main(path)	
	# print WRITETOFILE