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
			file.write(profit+"\n")
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
			file.write(profit+"\n")



def main(filename):
	path = "../data/"+filename+".csv"
	csv_data = read_data_from_csv(path)
	path = filename+"_trade.txt"
	file = open(path,"w")
	param_dict = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":120
				,"limit_rsi_data":80,"rsi_period":14
				,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":3600
				,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file}
	for band_type in xrange(0,2):
		if band_type ==0:
			# continue
			mesg = "但是只是根据止盈止损来退出"
			print mesg
			file.write(mesg)
			param_dict["band_loss_edge"] =100
			param_dict["band_profit_edge"] =100
			create_band_obj(csv_data,param_dict)
		elif band_type ==1:
			mesg = "1退出，盈利通过止盈数来做"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =100
			create_band_obj(csv_data,param_dict)
		elif band_type ==2:
			mesg = "根据止盈止损的值，然后加上Max draw dowm“"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =100
			param_dict["band_profit_edge"] =100
			param_dict["limit_max_draw_down"] =100
			create_band_obj(csv_data,param_dict)
		elif band_type ==3:
			mesg = "根据1退出 根据止盈数值来止盈，然后加上Max draw dowm“"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =100
			param_dict["limit_max_draw_down"] =100
			create_band_obj(csv_data,param_dict)
		elif band_type ==4:
			mesg = "根据1退出 3退出，然后加rsi，周期是120，14"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =1
			param_dict["band_profit_edge"] =3
			param_dict["limit_max_draw_down"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==5:
			mesg = "根据1退出 3退出，然后加rsi，周期是300，14"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =100
			param_dict["band_profit_edge"] =100
			param_dict["rsi_bar_period"] =300
			param_dict["limit_max_draw_down"] =0
			create_band_obj(csv_data,param_dict)
		elif band_type ==6:
			mesg = "根据1退出 3退出，然后加rsi，周期是120，14,添加Max draw down"
			print mesg
			file.write(mesg+"\n")
			param_dict["band_loss_edge"] =100
			param_dict["band_profit_edge"] =100
			param_dict["rsi_bar_period"] =120
			param_dict["limit_max_draw_down"] =100
			create_band_obj(csv_data,param_dict)
		else:
			pass
	file.close()



if __name__=='__main__': 
	# main("ru1709_20170622")
	data = [20170628,20170627,20170623,20170622,20170621,20170620,20170619,20170616]
	# data = [20170628]
	for item in data:
		path = "rb1710_"+ str(item)
		# print path
		main(path)	
	# print WRITETOFILE