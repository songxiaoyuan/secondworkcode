# -*- coding:utf8 -*-
import csv
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
param_dict_pb = {"tick":5,"config_file":"pb"}
# 这个是螺纹钢的
param_dict_rb = {"tick":1,"config_file":"rb"}

# 这个是橡胶的
param_dic_ru = {"tick":5,"config_file":"ru"}

# 这个是锌的
param_dic_zn = {"tick":5,"config_file":"zn"}

param_dict_i = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":350}

param_dic_ni = {"tick":10,"config_file":"ni"}

param_dic_al = {"tick":5,"config_file":"al"}

param_dict_hc = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":10,"file":file,"config_file":380}

param_dict_cu = {"tick":10,"config_file":"cu"}


param_dic_au = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":1000,"file":file,"config_file":400}

param_dic_ag = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":15,"file":file,"config_file":410}

param_dic_j = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":100,"file":file,"config_file":420}

param_dic_jm = {"rsi_period":14,"limit_ema_tick_5":600,"limit_ema_tick_1":120,
			"multiple":60,"file":file,"config_file":430}

param_dic_pp = {"tick":1,"config_file":"pp"}

param_dic_v = {"tick":5,"config_file":"v"}

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
	"cu1801":{"param":param_dict_cu},
	"i1801":{"param":param_dict_i},
	"hc1801":{"param":param_dict_hc},
	"ni1805":{"param":param_dic_ni},
	"al1801":{"param":param_dic_al},
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
	"pb1711":{"param":param_dict_pb}
}

class GetRange(object):
	"""docstring for GetRange"""
	def __init__(self,param_dic):
		super(GetRange, self).__init__()

		self._max_lastprice = 0
		self._min_lastprice = 0

		self._tick = param_dic["tick"]
		self._config_file = param_dic["config_file"]

		self._tick_num_dict = {}


	def __del__(self):
		print "this is the over function " + self._config_file

		config_file = "../range_config/"+self._config_file
		file = open(config_file,"w")
		write_lines = []
		for item in self._tick_num_dict:
			line = str(item) + " : "+ str(self._tick_num_dict[item]) + '\n'
			write_lines.append(line)
		file.writelines(write_lines)
		file.close()
		print "has write the config file"


	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		lastprice =  float(md_array[LASTPRICE])

		if self._max_lastprice == 0:
			self._max_lastprice = lastprice
		if self._min_lastprice ==0:
			self._min_lastprice = lastprice
		if lastprice > self._max_lastprice:
			self._max_lastprice = lastprice
		if lastprice < self._min_lastprice:
			self._min_lastprice = lastprice

	def get_tick_num(self):
		tick_num = (self._max_lastprice - self._min_lastprice)/self._tick
		tmp = int(tick_num/5)
		if tmp in self._tick_num_dict:
			self._tick_num_dict[tmp] +=1
		else:
			self._tick_num_dict[tmp] =1
		self._max_lastprice =0
		self._min_lastprice = 0

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
	data13 = [20171030,20171031,20171101,20171102,20171103]
	data14 = [20171106,20171107,20171108,20171109,20171110]
	data15 = [20171113,20171114]
	data = data13+data14+data15
	# instrumentid_array = ["ru1801","rb1801","zn1710","pb1710","cu1710","hc1801","i1801","ni1801","al1710","au1712","ag1712","bu1712"]
	instrumentid_array = ["pp1801","v1801"]
	for instrumentid in instrumentid_array:
		# instrumentid = "pb1711"
		bt = GetRange(nameDict[instrumentid]["param"])
		for item in data:
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
			bt.get_tick_num()
			f.close()


if __name__=='__main__':
	main()