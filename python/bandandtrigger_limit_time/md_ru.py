# -*- coding:utf8 -*-
import csv
import band_and_trigger
import band_and_wvad
import basic_fun

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20



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
	ret = getSortedData(ret)
	return ret

def start_to_run_md(band_obj,data):
	for row in data:
		band_obj.get_md_data(row)

def create_band_obj(data,param_dict):
	file = param_dict["file"]
	for i in xrange(0,2):
		param_dict["direction"] = i
		band_and_trigger_obj = band_and_trigger.BandAndTrigger(param_dict)
		# band_and_wvad_obj = band_and_wvad.BandAndWvad(param_dict)
		if i==0:
			# continue
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
			# print "start to write the file"
			# csv_data = band_and_trigger_obj.get_to_csv_data()
			# path_new = "../data/"+filename+ "_band_data" +".csv"
			# basic_fun.write_data_to_csv(path_new,csv_data)
		else:
			print "方向是long的交易情况："
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../data/"+filename+".csv"
	csv_data = read_data_from_csv(path)
	path = filename+"_trade.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_max_profit":2500,"limit_max_loss":600,"multiple":10
				,"rsi_bar_period":120,"limit_rsi_data":80,"rsi_period":14
				,"diff_period":1
				,"band_open_edge1":0,"band_open_edge2":0.5,"band_loss_edge":0.5,"band_profit_edge":30,"band_period":7200
				,"limit_max_draw_down":0,"file":file
				,"open_interest_edge":0,"spread":85,"volume_open_edge":500
				,"limit_sd":4,"limit_sd_open_edge":2,"limit_sd_close_edge":1,"config_file":399}

	for band_type in xrange(0,7):
		if band_type ==0:
			# continue
			mesg = "完全按照1退出，3退出。900进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =150
			param_dict["sd_lastprice"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==1:
			continue
			param_dict["wvad_period"] =120
			param_dict["limit_wvad"] =2000
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
	data = [20170911]
	for item in data:
		path = "ru1801_"+ str(item)
		print path
		main(path)	
	# print WRITETOFILE