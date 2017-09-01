# -*- coding:utf8 -*-
import basic_fun as bf
import adv

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20
LONG =1
SHORT =0

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._lastprice_map = dict()
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		self._diff_volume_array = []
		self._diff_open_interest_array = []
		self._diff_spread_array = []
		self._diff_period =param_dic["diff_period"]

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
		self._param_open_edge1 = param_dic["band_open_edge1"]
		self._param_open_edge2 = param_dic["band_open_edge2"]
		self._param_loss_edge = param_dic["band_loss_edge"]
		self._param_close_edge =param_dic["band_profit_edge"]
		self._param_period = param_dic["band_period"]
		

		# trigger param
		self._param_volume_open_edge = param_dic["volume_open_edge"]
		self._param_open_interest_edge = param_dic["open_interest_edge"]
		self._param_spread = param_dic["spread"]

		self._open_lastprice = 0
		self._profit = 0
		self._ris_data = 0

		self._limit_sd = param_dic["limit_sd"]
		self._limit_sd_open_edge = param_dic["limit_sd_open_edge"]
		self._limit_sd_close_edge = param_dic["limit_sd_close_edge"]

		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		adv_param_dict = {}
		adv_param_dict["period"] = 120
		adv_param_dict["pre_adv"] = 0
		self._adv_obj = adv.ADV(adv_param_dict)

		if len(self._lastprice_array) ==0:
			print "this is init function " + str(self._config_file)
			tmp_pre_ema_array = []
			tmp_rsi_lastprice = []
			config_file = "../config_server/"+str(self._config_file)
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
		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]
		diff_interest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]
		diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]

		self._diff_volume_array.append(diff_volume)
		self._diff_open_interest_array.append(diff_interest)

		# data_mesg = self._now_md_price[TIME]+","+str(lastprice)+","+str(self._now_middle_value)+","+str(self._now_sd_val)+","+str(diff_volume)+","+str(diff_interest)+","+str(self._ris_data)
		# self._file.write(data_mesg+"\n")

		if diff_volume ==0:
			self._diff_spread_array.append(0)
			return True
		avg_price = float(diff_turnover)/diff_volume/self._multiple
		if self._direction ==SHORT:
			spread = 100*(self._pre_md_price[ASKPRICE1] - avg_price)/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])
		else:
			spread = 100*(avg_price - self._pre_md_price[BIDPRICE1])/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])
		self._diff_spread_array.append(spread)


		ema_diff_volume = bf.get_sum(self._diff_volume_array,self._diff_period)
		ema_diff_openinerest = bf.get_sum(self._diff_open_interest_array,self._diff_period)
		ema_spread = bf.get_weighted_mean(self._diff_spread_array,self._diff_volume_array,self._diff_period)

		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._now_interest +=1
			# print "we start to open"
			self._open_lastprice = self._now_md_price[LASTPRICE]
			self._max_profit = 0
			mesg= "the time of open: "+self._now_md_price[TIME] + ",the price: " + str(self._now_md_price[LASTPRICE])
			mesg1 = "the diff volume: "+str(ema_diff_volume)+", the interest: " + str(ema_diff_openinerest) + ", the spread: "+ str(ema_spread)
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
			mesg= "the time of close:"+self._now_md_price[TIME] + ",the price: " + str(self._now_md_price[LASTPRICE])
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):
		# "'this is used to jude the time used to open return bool'"
		# first base the sd,find is time to open band 
		# if self._now_sd_val < self._param_limit_sd_value:
		# 	# open_val = self._param_limit_bigger*self._param_open_edge
		# 	open_val = self._param_open_edge
		# else:
		open_val = self._param_open_edge1
		is_band_open = bf.is_band_open_time(self._direction,self._now_md_price[LASTPRICE],
											self._now_middle_value,self._now_sd_val,open_val,self._param_open_edge2,
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
		

	def get_total_profit(self):
		return self._profit

if __name__=='__main__': 
	print "this is the band and trigger size"