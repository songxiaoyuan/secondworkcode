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


# 这个是铅的
# param_dict = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
# 			,"limit_rsi_data":80,"rsi_period":14
# 			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
# 			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
# 			,"sd_lastprice":100,"open_interest_edge":0,"spread":100}
# 这个是螺纹钢的
# param_dict = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":120
# 			,"limit_rsi_data":80,"rsi_period":14
# 			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
# 			,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
# 			,"sd_lastprice":100,"open_interest_edge":0,"spread":100}

# 这个是锌的
# param_dic = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
# 			,"limit_rsi_data":80,"rsi_period":14
# 			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
# 			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
# 			,"sd_lastprice":0,"open_interest_edge":0,"spread":100}
# 这个是橡胶的
param_dic = {"limit_max_profit":250,"limit_max_loss":100,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100}
class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self):
		super(BandAndTrigger, self).__init__()

		self._write_to_csv_data = []

		self._diff_volume_array = []
		self._diff_period =30
		self._diff_open_interest_array = []

		self._diff_spread_array = []

		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		self._max_profit = 0
		self._limit_max_draw_down = param_dic["limit_max_draw_down"]
		self._limit_max_profit = param_dic["limit_max_profit"]
		self._limit_max_loss = param_dic["limit_max_loss"]

		self._multiple = param_dic["multiple"]

		self._rsi_array = []
		self._rsi_period = param_dic["rsi_period"]
		self._pre_rsi_lastprice =0 
		self._now_bar_rsi_tick = 0
		self._rsi_bar_period = param_dic["rsi_bar_period"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]

		self._rsi_array_3 = []
		self._pre_rsi_lastprice_3 =0
		self._now_bar_rsi_tick_3 = 0
		self._rsi_period_3 = 20
		self._ris_data_3 = 0


		# self._limit_twice_sd = 2

		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		# band param
		self._param_open_edge = param_dic["band_open_edge"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_close_edge =param_dic["band_profit_edge"]
		self._param_period = param_dic["band_period"]
		
		# if the sd is too small like is smaller than _param_limit_sd_value,
		# the open edge and close edge will bigger 
		# self._param_limit_sd_value = limit_sd_val
		# self._param_limit_bigger = 0

		# trigger param
		self._param_volume_open_edge = param_dic["volume_open_edge"]
		self._param_open_interest_edge = param_dic["open_interest_edge"]
		self._param_spread = param_dic["spread"]

		self._open_lastprice = 0
		self._profit = 0
		self._ris_data = 0

		self._sd_lastprice = param_dic["sd_lastprice"]



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
		self._lastprice_array.append(lastprice)
		# print lastprice

		if len(self._pre_md_price) ==0:
			self._rsi_array.append(0)
			self._pre_rsi_lastprice = lastprice
			self._ris_data = -1
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
				# self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				self._ris_data = 0

			if self._now_bar_rsi_tick_3 >= self._rsi_bar_period:
				# 表示已经到了一个bar的周期。
				tmpdiff1 = lastprice - self._pre_rsi_lastprice_3		
				self._pre_rsi_lastprice_3 = lastprice
				self._now_bar_rsi_tick_3 = 1
				self._ris_data_3 =bf.get_rsi_data2(tmpdiff1,self._rsi_array_3,self._rsi_period_3)
				self._rsi_array_3.append(tmpdiff1)
			else:
				self._now_bar_rsi_tick_3 +=1
				tmpdiff1 = lastprice - self._pre_rsi_lastprice_3
				# self._ris_data_3 =bf.get_rsi_data2(tmpdiff1,self._rsi_array_3,self._rsi_period_3)
				self._ris_data_3 = 0
				# self._ris_data = -1
		# self._now_bar_rsi_tick +=1
		# if self._now_bar_rsi_tick >= self._rsi_period:
		# 	self._ris_data =bf.get_rsi_data(self._rsi_array,self._rsi_period)
		# 	self._now_bar_rsi_tick =0
		# else:
		# 	self._ris_data =0
		# print self._ris_data	

		if len(self._lastprice_array)-1 < self._param_period:
			# this is we dont start the period.
			ema_period = len(self._lastprice_array)
			pre_ema_val = bf.get_ema_data(lastprice,self._pre_ema_val,ema_period)
			self._pre_ema_val = pre_ema_val
			# save the pre_ema_val and return
			return True

		# start the judge
		if self._moving_theo =="EMA":
			self._now_middle_value = bf.get_ema_data(lastprice,self._pre_ema_val,self._param_period)
			self._pre_ema_val = self._now_middle_value
		else:
			self._now_middle_value = bf.get_ma_data(self._lastprice_array,self._param_period)
		

		
		# self._ris_data = bf.get_rsi_data(self._rsi_array,self._rsi_period)
		self._now_sd_val =bf.get_sd_data(self._now_md_price[TIME], self._lastprice_array,self._param_period)
		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]

		diff_interest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]

		diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]
		self._diff_volume_array.append(diff_volume)
		if diff_interest <0:
			self._diff_open_interest_array.append(0 - diff_interest)
		else:
			self._diff_open_interest_array.append(diff_interest)

		ema_diff_volume = bf.get_ema_data_2(self._diff_volume_array,self._diff_period)
		ema_diff_openinterest = bf.get_ema_data_2(self._diff_open_interest_array,self._diff_period)

		if diff_volume ==0:
			return True
		avg_price = float(diff_turnover)/diff_volume/self._multiple
		# if lastprice > self._now_middle_value:
		spread = 100*(avg_price - self._pre_md_price[BIDPRICE1])/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])
		# else:
			# spread = 100*(self._pre_md_price[ASKPRICE1] - avg_price)/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])

		self._diff_spread_array.append(spread)
		spread = bf.get_ema_data_2(self._diff_spread_array,self._diff_period)
		tmpsd_lastprice = 1000*self._now_sd_val/self._now_md_price[LASTPRICE]
		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],self._now_middle_value,
					self._now_sd_val,self._ris_data,diff_volume,self._ris_data_3,tmpsd_lastprice
					,diff_interest,spread,ema_diff_volume,ema_diff_openinterest]
		self._write_to_csv_data.append(tmp_to_csv)

		return True

	def get_to_csv_data(self):
		return self._write_to_csv_data


def main(filename):
	path = "../data/"+filename+".csv"
	# read_data_from_csv(pth)
	f = open(path,'rb')
	reader = csv.reader(f)
	bt = BandAndTrigger()
	for row in reader:
		bt.get_md_data(row)
		# tranfer the string to float
	f.close()
	
	data = bt.get_to_csv_data()
	path_new = "../data/"+filename+ "_band_data"+".csv"
	bf.write_data_to_csv(path_new,data)


if __name__=='__main__':
	# data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data2 =[20170703,20170704,20170705,20170706]
	# data = data1+ data2
	data = [20170707]
	instrumentid_array = ["ru1709","rb1710","zn1708","pb1708"]
	for item in data:
		for instrumentid in instrumentid_array:
			path = instrumentid+ "_"+str(item)
			print path
			main(path)	