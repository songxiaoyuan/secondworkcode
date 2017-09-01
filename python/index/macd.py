# coding: utf-8
import sys, csv , operator  
#!/usr/bin/python
# -*- coding:utf8 -*-
import xml.etree.ElementTree as ET
import os
quicktime=120
slowtime=360
quick=12
slow=26
emadea=9


quicktimequickema=100000
quicktimeslowema=100000
quicktimedeaema=100000
quicktimeupda=100000

slowtimequickema=100000
slowtimeslowema=100000
slowtimedea=100000

updatenowquicktimequickema=100000
updatenowslowtimequickema=100000
updatenowquicktimeslowema=100000
updatenowslowtimeslowema=100000


quickmincloseprice=100000
slowmincloseprice=100000

quicktimeyellowline=100000
slowtimeyellowline=100000
updatequickyellowline=100000
updateslowyellowline=100000

quicktimediff=100000
slowtimediff=100000

updatequickdiff=100000
updateslowdiff=100000


quicktimemacdbar=100000
slowtimemacdbar=100000

index=0
i=0
def readxml(path):
	tree = ET.parse(path)
	root = tree.getroot()

	quickmincloseprice=float(root.find('lastprice').text)
	slowmincloseprice=float(root.find('lastprice').text)


	quicktimequickema=float(root.find('quicktimequickema').text)
	quicktimeslowema=float(root.find('quicktimeslowema').text)
	quicktimediff=float(root.find('quicktimediff').text)
	quicktimeyellowline=float(root.find('quicktimeyellowline').text)


	slowtimequickema=float(root.find('slowtimequickema').text)
	slowtimeslowema=float(root.find('slowtimeslowema').text)
	slowtimediff=float(root.find('slowtimediff').text)
	slowtimeyellowline=float(root.find('slowtimeyellowline').text)


	updatequickdiff=float(root.find('updatequickdiff').text)
	updateslowdiff=float(root.find('updateslowdiff').text)


def writexml(path):
	tree = ET.parse(path)
	root = tree.getroot()

	root.find('lastprice').text=str(quickmincloseprice)
	root.find('quicktimequickema').text=str(quicktimequickema)
	root.find('quicktimeslowema').text=str(quicktimeslowema)
	root.find('quicktimediff').text=str(quicktimediff)
	root.find('quicktimeyellowline').text=str(quicktimeyellowline)


	root.find('slowtimequickema').text=str(slowtimequickema)
	root.find('slowtimeslowema').text=str(slowtimeslowema)
	root.find('slowtimediff').text=str(slowtimediff)
	root.find('slowtimeyellowline').text=str(slowtimeyellowline)


	root.find('updatequickdiff').text=str(updatequickdiff)
	root.find('updateslowdiff').text=str(updateslowdiff)

	tree.write(path, encoding="utf-8",xml_declaration=True)
def calema(quicktimea,quickmincloseprice,lastema):
	if(lastema==100000):
		return quickmincloseprice
	else:
		returnema=float(lastema)*float(quicktimea-1)/float(quicktimea+1)+float((quickmincloseprice)*2)/float(quicktimea+1)
		return returnema

def printPath(level, path):
	global allFileNum
	dirList = []
	fileList = []
	files = os.listdir(path)
	dirList.append(str(level))
	for f in files:
		if(os.path.isdir(path + '\\' + f)):
			if(f[0] == '.'):
				pass
			else:
 				dirList.append(f)
		if(os.path.isfile(path + '\\' + f)):
			fileList.append(f)
	i_dl = 0
	for dl in dirList:
		if(i_dl == 0):
			i_dl = i_dl + 1
		else:
			print '-' * (int(dirList[0])), dl
			printPath((int(dirList[0]) + 1), path + '\\' + dl)
	return fileList



def readcsv(path):
	csvFile = file(path,'rb')
	reader = csv.reader(csvFile)
	quicktimeindex=0
	slowtimeindex=0

	global quicktimequickema
	global quicktimeslowema
	global quicktimedeaema
	global quicktimeupda

	global slowtimequickema
	global slowtimeslowema
	global slowtimedea

	global updatenowquicktimequickema
	global updatenowslowtimequickema
	global updatenowquicktimeslowema
	global updatenowslowtimeslowema


	global quickmincloseprice
	global slowmincloseprice

	global quicktimeyellowline
	global slowtimeyellowline
	global updatequickyellowline
	global updateslowyellowline
	global index
	global quicktimediff
	global slowtimediff

	global updatequickdiff
	global updateslowdiff

	global quicktimemacdbar
	global slowtimemacdbar
	global i
	writelist=[]
	slowmin=False
	quickmin=False
	writlist=[]
	
	for line in reader:
		i=i+1
		if i<2:
			continue
			pass
		nowlist=[]
		lastprice=float(line[4])
		if (lastprice-0)<0.00001:
			continue
			pass
		#ema 计算
		#快线ema计算
		#
		index=index+1
		quickmin=False
		slowmin=False
		quicktimeindex=quicktimeindex+1
		slowtimeindex=slowtimeindex+1
		if quicktimeindex>quicktime:#1分钟
			quicktimeindex=0
			quickmincloseprice=lastprice
			quickmin=True
		if slowtimeindex>slowtime:#5分钟
			slowtimeindex=0
			slowmincloseprice=lastprice
			slowmin=True


		if quickmin==True:
			quicktimequickema=calema(quick,quickmincloseprice,quicktimequickema)#quick bar
			quicktimeslowema=calema(slow,quickmincloseprice,quicktimeslowema)#quick bar
			quicktimediff=quicktimequickema-quicktimeslowema# quick bar diff
			quicktimeyellowline=calema(emadea,quicktimediff,quicktimeyellowline)
		if slowmin==True:
			slowtimequickema=calema(quick,slowmincloseprice,slowtimequickema)#slow bar
			slowtimeslowema=calema(slow,slowmincloseprice,slowtimeslowema)#slow bar
			slowtimediff=slowtimequickema-slowtimeslowema# slow bar diff
			slowtimeyellowline=calema(emadea, slowtimediff,slowtimeyellowline)


		updatenowquicktimequickema=calema(quick,lastprice,quicktimequickema)#实时价格quicktime ema计算
		updatenowslowtimequickema=calema(quick,lastprice,slowtimequickema)#实时价格slowtime ema计算
	#慢线ema计算
		
		updatenowquicktimeslowema=calema(slow,lastprice,quicktimeslowema)#实时价格quicktime ema计算
		updatenowslowtimeslowema=calema(slow,lastprice,slowtimeslowema)#实时价格slowtime ema计算
	#diff 计算 whiteline	
		
		updatequickdiff=float(updatenowquicktimequickema)-float(updatenowquicktimeslowema)  #quick bar diff 
		updateslowdiff=float(updatenowslowtimequickema)-float(updatenowslowtimeslowema)  # slow bar diff
	#dea计算 yellow line		
		
		updatequickyellowline=calema(emadea,updatequickdiff,quicktimeyellowline)
		updateslowyellowline=calema(emadea,updateslowdiff,slowtimeyellowline)




	#macd bar计算
		quicktimemacdbar=2*(quicktimediff-quicktimeyellowline)#短周期 macd bar计算
		slowtimemacdbar=2*(slowtimediff-slowtimeyellowline)#长周期 macd bar 计算
		
		if quicktimequickema!=100000 and slowtimequickema!=100000:

			timeLine = line[20].split(":")
			# tick = line[21]
			nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])
			nowTime=nowTime+int(line[21])/500
			nowlist=[index,quicktimediff, slowtimediff, updatequickdiff, updateslowdiff, quicktimeyellowline,slowtimeyellowline,updatequickyellowline,updateslowyellowline,lastprice,quicktimemacdbar,slowtimemacdbar]
			writelist.append(nowlist)
			# with open('everydayfiveminandonemin_from0711.csv', 'ab') as csvfile:
			# 	spamwriter = csv.writer(csvfile,dialect='excel')
			# 	spamwriter.writerow([index,quicktimediff, slowtimediff, updatequickdiff, updateslowdiff, quicktimeyellowline,slowtimeyellowline,updatequickyellowline,updateslowyellowline,lastprice])

 	with open('everydayfiveminandonemin_from0711lessoone.csv', 'ab') as csvfile:
		spamwriter = csv.writer(csvfile,dialect='excel')
		for line in writelist:
			pass
			spamwriter.writerow(line)





if __name__=='__main__': 
	#listtime=[20170608,20170607,20170606,20170605]
	# listtime=[20170727]
	# #listinstrument=['m1709-P-2750','m1709-C-2750','m1709']
	# listinstrument=['rb1710']
	# #listinstrument=['rb1710']
	# #
	# #for myday in xrange(20170417,20170630):
	# for myday in listtime:

	# 	evemonth(myday,listinstrument)
	fileList=[]
	fileList=printPath(1, 'D:\\data\\rb\\clean')
	for x in fileList:
		readxml('D:\py\py\py\macdxml.xml')
		filepath='D:\\data\\rb\\clean\\'+x
		readcsv(filepath)
		writexml('D:\\py\\py\\py\\macdxml.xml')