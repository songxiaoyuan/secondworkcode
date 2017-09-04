# -*- coding:utf8 -*-
import cx_Oracle  
import csv
import band_and_trigger
import basic_fun as bf
import shutil

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20
LONG =1
SHORT =0


# "info!!!! this must be run only once!!!!!!!!"
# 这个是铅的
param_dict_pb = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":50
			,"limit_rsi_data":75,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":310}

param_dict_pb_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":50
			,"limit_rsi_data":75,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":312}
# 这个是螺纹钢的
param_dict_rb = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":320}

param_dict_rb_3600 = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":322}

# 这个是橡胶的
param_dic_ru = {"limit_max_profit":250,"limit_max_loss":100,"rsi_bar_period":100
			,"limit_rsi_data":70,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":330}

param_dic_ru_3600 = {"limit_max_profit":250,"limit_max_loss":100,"rsi_bar_period":100
			,"limit_rsi_data":70,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":332}
			
# 这个是锌的
param_dic_zn = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":340}

param_dic_zn_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":342}

# 这个是锌的
param_dic_i = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":100,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":350}

param_dic_i_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":100,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":352}

# 这个是锌的
param_dic_ni = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":360}

param_dic_ni_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":362}

param_dic_al = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":370}

param_dic_al_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":372}

# 这个是锌的
param_dic_hc = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":380}

param_dic_hc_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":382}

# 这个是锌的
param_dic_cu = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":70,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":390}

param_dic_cu_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":392}


param_dic_au = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":400}

param_dic_au_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":402}

param_dic_ag = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":410}

param_dic_ag_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":412}

param_dic_bu = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":420}

param_dic_bu_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":422}

param_dic_sn = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":430}

param_dic_sn_3600 = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":432}

nameDict = {
	"rb1801":{"param":[param_dict_rb,param_dict_rb_3600]},
	"ru1801":{"param":[param_dic_ru,param_dic_ru_3600]},
	"zn1710":{"param":[param_dic_zn,param_dic_zn_3600]},
	"cu1710":{"param":[param_dic_cu,param_dic_cu_3600]},
	"hc1801":{"param":[param_dic_hc,param_dic_hc_3600]},
	"i1801":{"param":[param_dic_i,param_dic_i_3600]},
	"ni1801":{"param":[param_dic_ni,param_dic_ni_3600]},
	"al1710":{"param":[param_dic_al,param_dic_al_3600]},
	"au1712":{"param":[param_dic_au,param_dic_au_3600]},
	"ag1712":{"param":[param_dic_ag,param_dic_ag_3600]},
	"bu1712":{"param":[param_dic_bu,param_dic_bu_3600]},
	"sn1709":{"param":[param_dic_sn,param_dic_sn_3600]},
	"pb1710":{"param":[param_dict_pb,param_dict_pb_3600]}
}

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()

		self._write_to_csv_data = []

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

		self._multiple = param_dic["multiple"]

		self._rsi_array = []
		self._pre_rsi_lastprice =0 
		self._now_bar_rsi_tick = 0
		self._ris_data = 0
		self._rsi_period = param_dic["rsi_period"]
		self._rsi_bar_period = param_dic["rsi_bar_period"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]

		# self._limit_twice_sd = 2

		self._moving_theo = "EMA"
		# band param
		self._param_period = param_dic["band_period"]


		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		if len(self._lastprice_array) ==0:
			print "this is init function"
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
		print self._pre_ema_val
		print len(self._lastprice_array)
		print self._rsi_array
		print self._pre_rsi_lastprice
		# print "the length of lastprice is: " +str(len(self._lastprice_array))


	def __del__(self):
		print "this is the over function"
		config_file = "../config_server/"+str(self._config_file)
		bf.write_config_info(self._pre_ema_val,self._lastprice_array
			,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],config_file)

		config_file = "../config_server/"+str(self._config_file+1)
		bf.write_config_info(self._pre_ema_val,self._lastprice_array
			,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],config_file)

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		# md_array[LASTPRICE] = float(md_array[LASTPRICE])
		# md_array[VOLUME] = float(md_array[VOLUME])
		# md_array[OPENINTEREST] = float(md_array[OPENINTEREST])
		# md_array[TURNONER] = float(md_array[TURNONER])
		# md_array[BIDPRICE1] = float(md_array[BIDPRICE1])
		# md_array[ASKPRICE1] = float(md_array[ASKPRICE1])


		self._pre_md_price = self._now_md_price
		self._now_md_price = md_array

		lastprice = self._now_md_price[LASTPRICE]
		if len(self._pre_md_price) ==0:
			return
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

		# if len(self._lastprice_array) > self._param_period:
		# 	self._lastprice_array.pop(0)

		self._lastprice_array.append(lastprice)

		if len(self._lastprice_array) <= self._param_period:
			# this is we dont start the period.
			# print  "the lastprice length is small: " +str(len(self._lastprice_array))
			ema_period = len(self._lastprice_array)
			pre_ema_val = bf.get_ema_data(lastprice,self._pre_ema_val,ema_period)
			self._pre_ema_val = pre_ema_val
			# save the pre_ema_val and return
			if lastprice not in self._lastprice_map:
				self._lastprice_map[lastprice] =1
			else:
				self._lastprice_map[lastprice] +=1
			return True

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
		
		self._now_sd_val =bf.get_sd_data_by_map(self._lastprice_map,self._param_period)	
	
		return True


def start_create_config(instrumentid,data):
	print "start create the config file of " + instrumentid
	if instrumentid not in nameDict:
		print "the instrument id " + instrumentid + " is not in the dict"
	for param in nameDict[instrumentid]["param"]:
		bt = BandAndTrigger(param)
		for row in data:
			bt.get_md_data(row)
			# tranfer the string to float


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
	night = sorted(night, key = lambda x: (x[20], int(x[21])))
	zero = sorted(zero, key = lambda x: (x[20], int(x[21])))
	day = sorted(day, key = lambda x: (x[20], int(x[21])))
	# for line in night:
	# 	ret.append(line)
	# for line in zero:
	# 	ret.append(line)
	for line in day:
		ret.append(line)

	return ret

def copy_file():
	print "start create the real server data"
	shutil.copy('../config_server/340', '../real_server/520')
	shutil.copy('../config_server/340', '../real_server/521')
	shutil.copy('../config_server/320', '../real_server/522')
	shutil.copy('../config_server/320', '../real_server/523')
	shutil.copy('../config_server/330', '../real_server/524')
	shutil.copy('../config_server/330', '../real_server/525')
	shutil.copy('../config_server/310', '../real_server/526')
	shutil.copy('../config_server/310', '../real_server/527')

	shutil.copy('../config_server/310', '../config_server/314')
	shutil.copy('../config_server/310', '../config_server/315')
	shutil.copy('../config_server/320', '../config_server/324')
	shutil.copy('../config_server/320', '../config_server/325')
	shutil.copy('../config_server/330', '../config_server/334')
	shutil.copy('../config_server/330', '../config_server/335')
	shutil.copy('../config_server/340', '../config_server/344')
	shutil.copy('../config_server/340', '../config_server/345')
	shutil.copy('../config_server/350', '../config_server/354')
	shutil.copy('../config_server/350', '../config_server/355')
	shutil.copy('../config_server/360', '../config_server/364')
	shutil.copy('../config_server/360', '../config_server/365')
	shutil.copy('../config_server/370', '../config_server/374')
	shutil.copy('../config_server/370', '../config_server/375')
	shutil.copy('../config_server/380', '../config_server/384')
	shutil.copy('../config_server/380', '../config_server/385')
	shutil.copy('../config_server/390', '../config_server/394')
	shutil.copy('../config_server/390', '../config_server/395')
	shutil.copy('../config_server/400', '../config_server/404')
	shutil.copy('../config_server/400', '../config_server/405')
	shutil.copy('../config_server/410', '../config_server/414')
	shutil.copy('../config_server/410', '../config_server/415')
	shutil.copy('../config_server/420', '../config_server/424')
	shutil.copy('../config_server/420', '../config_server/425')

def getSqlData(myday,instrumentid): 

	conn = cx_Oracle.connect('hq','hq','114.251.16.210:9921/quota')    
	cursor = conn.cursor () 

	mysql="select *from hyqh.quotatick where TRADINGDAY = '%s' AND INSTRUMENTID = '%s'" % (str(myday),instrumentid)

	print mysql
	cursor.execute (mysql)  

	icresult = cursor.fetchall()
	# get the data and sort it.
	# sortedlist = sorted(icresult, key = lambda x: (x[20], int(x[21])))
	cleandata = getSortedData(icresult)
	# instrumentid = str(myday)+instrumentid
	start_create_config(instrumentid,cleandata)

	# copy_file()



if __name__=='__main__':
	# data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data2 =[20170703,20170704,20170705,20170706,20170707,20170711,20170712,20170713,20170714,20170717]
	# data = data1+ data2
	data = [20170831]
	instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	# instrumentid_array = ["al1710","au1712","ag1712","bu1712"]
	# instrumentid_array = ["ni1801"]
	for item in data:
		for instrumentid in instrumentid_array:
			getSqlData(item,instrumentid)	

	copy_file()