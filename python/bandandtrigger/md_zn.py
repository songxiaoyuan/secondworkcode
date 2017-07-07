# -*- coding:utf8 -*-
import csv
import band_and_trigger
import basic_fun

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20

# read the md data from csv, it uesd to like the csv
def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	return ret

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
	path = "../data/"+filename+".csv"
	csv_data = read_data_from_csv(path)
	path = filename+"_trade.txt"
	file = open(path,"w")
	# 这个是铅的 tick 5
	# param_dict = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
	# 			,"limit_rsi_data":80,"rsi_period":14
	# 			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
	# 			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
	# 			,"sd_lastprice":100,"open_interest_edge":0,"spread":100}
	# 这个是螺纹钢的 tick 1
	# param_dict = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":120
	# 			,"limit_rsi_data":80,"rsi_period":14
	# 			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
	# 			,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
	# 			,"sd_lastprice":100,"open_interest_edge":0,"spread":100}
	# 这个是锌的 tick 5
	param_dict = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
				,"limit_rsi_data":80,"rsi_period":14
				,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
				,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":5,"file":file
				,"sd_lastprice":0,"open_interest_edge":0,"spread":100}

	# 这个是橡胶的 tick 5
	# param_dict = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
	# 			,"limit_rsi_data":80,"rsi_period":14
	# 			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
	# 			,"volume_open_edge":180,"limit_max_draw_down":0,"multiple":10,"file":file
	# 			,"sd_lastprice":0,"open_interest_edge":0,"spread":100}

	for band_type in xrange(0,7):
		if band_type ==0:
			# continue
			mesg = "完全按照1退出，3退出。100进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =100
			param_dict["sd_lastprice"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==1:
			# continue
			mesg = "1，3退出，sd／last price <9 不平，100进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =100
			param_dict["sd_lastprice"] =9
			create_band_obj(csv_data,param_dict)
		elif band_type ==2:
			# continue
			mesg = "完全按照1退出，3退出。120进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =120
			param_dict["sd_lastprice"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==3:
			# continue
			mesg = "1，3退出，sd／last price <9 不平，120进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =120
			param_dict["sd_lastprice"] =9
			create_band_obj(csv_data,param_dict)
		elif band_type ==4:
			# continue
			mesg = "完全按照1退出，3退出。150进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =150
			param_dict["sd_lastprice"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==5:
			# continue
			mesg = "1，3退出，sd／last price <9 不平，150进入"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =150
			param_dict["sd_lastprice"] =9
			create_band_obj(csv_data,param_dict)
		elif band_type ==6:
			# continue
			mesg = "根据1退出 3退出,添加Max draw down"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["volume_open_edge"] =120
			param_dict["limit_max_draw_down"] =50
			create_band_obj(csv_data,param_dict)
		else:
			pass
	file.close()



if __name__=='__main__': 
	# main("ru1709_20170622")
	data1 = [20170630,20170629,20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	data2 =[20170703,20170704,20170705,20170706]
	data = data1+ data2
	# data = [20170703]
	for item in data:
		path = "zn1708_"+ str(item)
		print path
		main(path)	
	# print WRITETOFILE