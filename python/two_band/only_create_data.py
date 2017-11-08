# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os
import cx_Oracle  

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
BIDPRICE1VOLUME = 23
ASKPRICE1 =24
ASKPRICE1VOLUME =25
TIME = 20
LONG =1
SHORT =0

# 这个是铅的
param_dict_pb = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":310}
# 这个是螺纹钢的
param_dict_rb = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":320}

# 这个是橡胶的
param_dic_ru = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":330}

# 这个是锌的
param_dic_zn = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":340}

param_dict_i = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":350}

param_dic_ni = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":1,"file":file,"config_file":360}

param_dic_al = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":370}

param_dict_hc = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":380}

param_dict_cu = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":390}


param_dic_au = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":1000,"file":file,"config_file":400}

param_dic_ag = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":15,"file":file,"config_file":410}

param_dic_j = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":420}

param_dic_jm = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":60,"file":file,"config_file":430}

param_dic_pp = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":440}

param_dic_v = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":5,"file":file,"config_file":450}

param_dic_y = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":460}

param_dic_p = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":470}

param_dic_c = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":480}

param_dic_a = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":490}

param_dic_m = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":500}

param_dic_jd = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":510}

nameDict = {
	"rb1801":{"param":param_dict_rb},
	"ru1801":{"param":param_dic_ru},
	"zn1712":{"param":param_dic_zn},
	"cu1712":{"param":param_dict_cu},
	"i1801":{"param":param_dict_i},
	"hc1801":{"param":param_dict_hc},
	"ni1801":{"param":param_dic_ni},
	"al1710":{"param":param_dic_al},
	"au1712":{"param":param_dic_au},
	"ag1712":{"param":param_dic_ag},
	"j1801":{"param":param_dic_j},
	"jm1801":{"param":param_dic_jm},
	"pp1801":{"param":param_dic_pp},
	"v1801":{"param":param_dic_v},
	"y1801":{"param":param_dic_y},
	"p1801":{"param":param_dic_p},
	"c1801":{"param":param_dic_c},
	"a1801":{"param":param_dic_a},
	"m1801":{"param":param_dic_m},
	"jd1801":{"param":param_dic_jd},
	"pb1710":{"param":param_dict_pb}
}

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()

		self._write_to_csv_data = []

		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []


		self._pre_ema_val_60 = 0
		self._now_middle_60 =0

		self._pre_ema_val_5 = 0
		self._now_middle_5 = 0
		self._now_ema_tick_5 = 0
		self._limit_ema_tick_5 = param_dic["limit_ema_tick_5"]

		self._pre_ema_val_1 = 0
		self._now_middle_1 = 0
		self._now_ema_tick_1 = 0
		self._limit_ema_tick_1 = param_dic["limit_ema_tick_1"]

		self._ema_period = 20
		self._current_hour = 9

		self._multiple = param_dic["multiple"]

		self._rsi_period = param_dic["rsi_period"]
		self._rsi_val = 0

		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		if len(self._lastprice_array) ==0:
			print "this is init function " + str(self._config_file)
			tmp_pre_ema_array_60 = []
			tmp_pre_ema_array_5 = []
			tmp_pre_ema_array_1 = []
			config_file = "../config_two/"+str(self._config_file)
			bf.get_config_info(tmp_pre_ema_array_60,tmp_pre_ema_array_5,tmp_pre_ema_array_1,self._lastprice_array,config_file)
			if len(tmp_pre_ema_array_60)==0:
				self._pre_ema_val_60 = 0
				self._pre_ema_val_5 = 0
				self._pre_ema_val_1 = 0
			else:
				self._pre_ema_val_60 = tmp_pre_ema_array_60[0]
				self._pre_ema_val_5 = tmp_pre_ema_array_5[0]
				self._pre_ema_val_1 = tmp_pre_ema_array_1[0]
		# print self._pre_ema_val_60
		print len(self._lastprice_array)
		# print "the length of lastprice is: " +str(len(self._lastprice_array))


	def __del__(self):
		print "this is the over function " + str(self._config_file)

		config_file = "../config_two/"+str(self._config_file)
		bf.write_config_info(self._pre_ema_val_60,self._pre_ema_val_5,self._pre_ema_val_1,
			self._lastprice_array,self._ema_period,config_file)
		print "has write the config file"


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
		# self._lastprice_array.append(lastprice)
		# print lastprice
		if len(self._pre_md_price) ==0:
			# "the is the first line data"
			return

		if self._pre_ema_val_60 ==0:
			self._pre_ema_val_60 = lastprice
			self._pre_ema_val_5 = lastprice
			self._pre_ema_val_1 = lastprice
		self._now_middle_60 = bf.get_ema_data(lastprice,self._pre_ema_val_60,self._ema_period)
		self._now_middle_5 = bf.get_ema_data(lastprice,self._pre_ema_val_5,self._ema_period)
		self._now_middle_1 = bf.get_ema_data(lastprice,self._pre_ema_val_1,self._ema_period)
		
		self._sd_val = bf.get_sd_data(lastprice,self._lastprice_array,self._ema_period)
		self._rsi_val = bf.get_rsi_data(lastprice,self._lastprice_array,self._rsi_period)

		# print len(self._lastprice_array)
		hour = int(self._now_md_price[TIME].split(':')[0])
		if hour != self._current_hour and hour !=13 and hour != 21:
			# print "the hour is not  equal "
			self._current_hour = hour
			self._pre_ema_val_60 = self._now_middle_60
			self._lastprice_array.append(lastprice)
		if self._now_ema_tick_1 >= self._limit_ema_tick_1:
			self._now_ema_tick_1 = 0
			self._pre_ema_val_1 = self._now_middle_1
		else:
			self._now_ema_tick_1 +=1
		if self._now_ema_tick_5 >= self._limit_ema_tick_5:
			self._now_ema_tick_5 = 0
			self._pre_ema_val_5 = self._now_middle_5
		else:
			self._now_ema_tick_5 +=1

		diff_volume = self._now_md_price[VOLUME] - self._pre_md_price[VOLUME]
		diff_interest = self._now_md_price[OPENINTEREST] - self._pre_md_price[OPENINTEREST]
		diff_turnover = self._now_md_price[TURNONER] - self._pre_md_price[TURNONER]

		if diff_volume != 0 and (self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1]) !=0:
			avg_price = float(diff_turnover)/diff_volume/self._multiple
			spread = 100*(avg_price - self._pre_md_price[BIDPRICE1])/(self._pre_md_price[ASKPRICE1] - self._pre_md_price[BIDPRICE1])
		else:
			spread = 50


		tmp_to_csv = [self._now_md_price[TIME],self._now_md_price[LASTPRICE],
					round(self._now_middle_60,2),round(self._now_middle_5,2),round(self._now_middle_1,2),round(self._sd_val,2),
					round(self._rsi_val,2),round(diff_volume,2),round(spread,2)]
		# print tmp_to_csv
		self._write_to_csv_data.append(tmp_to_csv)

		return True

	def get_to_csv_data(self):
		return self._write_to_csv_data

def clean_night_data(data):
	ret = []
	amBegin = 9*3600
	pmEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[0].split(":")
		# print timeLine
		# tick = line[21]
		nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])

		if nowTime>=amBegin and nowTime <=pmEnd:
			ret.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	return ret



def main():
	# data1 =[20170801,20170802,20170803,20170804]
	# data2 =[20170807,20170808,20170809,20170810,20170811]
	# data3 =[20170814,20170815,20170816,20170817,20170818]
	# data4 =[20170821,20170822,20170823,20170824,20170825]	
	# data5 =[20170828,20170829,20170830,20170831,20170901]
	# data6 =[20170904,20170905,20170906,20170907,20170908]
	# data7 =[20170911,20170912,20170913,20170914,20170915]	
	# data8 =[20170918,20170919,20170920,20170921,20170922]
	# data9 =[20170925,20170926,20170927,20170928,20170929]
	# data10 =[20171009,20171010,20171011,20171012,20171013]
	# data11 =[20171016,20171017,20171018,20171019,20171020]	
	# data12 =[20171023,20171024,20171025,20171026,20171027]
	# data13 =[20171030,20171031]
	# data = data1+data2+data3+data4+data5+data6+data7+data8+data9+data10+data11+data12+ data13
	# # data = data8+data9+data10+data11+data12
	data =[20171024]
	# instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid_array = ["rb1801"]
	
	for item in data:
		for instrumentid in instrumentid_array:
			# first get the sql data
			# getSqlData(item,instrumentid)
			bt = BandAndTrigger(nameDict[instrumentid]["param"])
			filename = instrumentid+ "_"+str(item)
			path = "../data/"+filename+".csv"
			# path = "../data/"+filename
			# read_data_from_csv(path)
			f = open(path,'rb')
			print "the instrument id is: "+filename
			reader = csv.reader(f)
			for row in reader:
				bt.get_md_data(row)
				# tranfer the string to float
			f.close()
	
			data = bt.get_to_csv_data()

			data = clean_night_data(data)
			path_new = "../tmp/"+filename+ "_band_data"+".csv"
			bf.write_data_to_csv(path_new,data)



if __name__=='__main__':
	main()