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
def write_fun1(f):
	f.write("this is fun1 !!\n")

def write_fun2(f):
	f.write("this is fun2 !!\n")

def fun_dict(dic):
	print dic["a"]
	print dic["c"]
	f = dic["f"]
	f.write("this is fun dic")

def adddic(dic):
	dic[2] = 1
def fixarray(array):
	array.pop(0)
	array = [1]
	print "the fun of is :"
	print array

def main():
	# f = open("test.txt","w")
	# for x in xrange(1,10):
	# 	if x%2 ==0:
	# 		write_fun1(f)
	# 	else:
	# 		write_fun2(f)
	# f.close()
	# dic ={"a":"bb","c":"dd","f":f}
	# fun_dict(dic)
	# f.close()
	# dic = dict()
	# dic[3] = 45
	# print dic[3]
	# adddic(dic)
	# print dic[2]
	array = [1,2,3,4,5]
	print array
	array.pop(0)
	print array
	fixarray(array)
	print array

if __name__=='__main__': 
	main()