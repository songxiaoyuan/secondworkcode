#ifndef ARBITRAGEXXXX_H
#define ARBITRAGEXXXX_H
#include "hyArbitrage_Interface.h"
using namespace std;

class CHyArbitrageXXXX:public CHyArbitrageBase
{
public:
/*********************************************************************************************************
构造函数与析构函数，在基类中处理，派生类中不用处理。
**********************************************************************************************************/
	CHyArbitrageXXXX(Parameter* Param):CHyArbitrageBase(Param){}
	~CHyArbitrageXXXX(){};
public:
/*********************************************************************************************************
派生类中需要实现的函数。
**********************************************************************************************************/

//策略启动与停止都会调用此函数，公有数据在基类中会初始化处理，此处不用处理。私有变量在此处进行初始化处理
	virtual void clearVector();
	
	
//计算failValuve,行情更新（tick数据或者bar数据），会调用此函数，可计算或处理相应的数据，公有数据直接使用，特有数据可在私有变量处定义后使用，fv为计算出的failValue，如果策略不需要fv,返回0即可。
	virtual bool get_fv_less(double &fv); 
	
//计算挂单价，行情更新之后，调用get_fv_less之后，会继续调用此函数。
//OffsetFlag表示开平仓标志。
//Direction表示买卖方向。
//fv为get_fv_less函数中计算出来的fv。
//perside表示挂单的档位，目前策略基本为1档，可以无视这个参数。
	virtual double calculateLessPrice(char OffsetFlag,char Direction,double fv,int perside);
	
//收到平仓成交后的处理函数
	virtual void   closeTraded();
	
	
//收到开仓成交后的处理函数
	virtual void   openTraded();
	
	
//若上述函数无法满足策略的要求，需要额外的函数，可真行定义虚函数。
	
private:

/*********************************************************************************************************
派生类中需要定义的私有变量。下面仅仅是一个例子，具体需要定义的私有变量根据策略的实际情况而定。
**********************************************************************************************************/

	//vector <double> m_less_theo;
	//vector <double> m_main_theo;
	//vector <double> m_less_emaTheo;
	//vector <double> m_main_emaTheo;
	//vector <double> m_fv;
	//vector <double> m_fv_ema_fast;
	//vector <double> m_fv_ema_slow;
	//vector <double> m_atr_diff;
	//double atrValue;
	
private:
/*********************************************************************************************************
派生类中需要定义的私有函数。下面仅仅是一个例子，具体需要定义的私有函数根据策略的实际情况而定。
**********************************************************************************************************/
	//double calAtrValue();
	//double ChangePrice(char Direction,char offsetFlag,double price);
	//double getMaxValue(vector <double> &m_src,int nStartIndex,int nStopIndex);
	//double getMinValue(vector <double> &m_src,int nStartIndex,int nStopIndex);
	
	
};

#endif