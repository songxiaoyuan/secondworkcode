#include "arbitrageVolumeTrendOther.h"


void CHyArbitrageVolumeTrendOther::clearVector()
{
	memset(&new_Price,0,sizeof(mdPrice));
	memset(&last_Price,0,sizeof(mdPrice));
	isTrendOpenTime=false;
	isTrendCloseTime=false;
}

bool CHyArbitrageVolumeTrendOther::get_fv_less(double &fv)
{
	// 获取最新的价格。问题：这个mdprice对象每一个参数的作用？
	// trigger size 需要输入一个参数，100，这个参数是什么，在哪里起作用。
	new_Price=getNewPrice(g_arrChannel,less_md_index);

	last_Price=getLastPrice(g_arrChannel,less_md_index);

	if (new_Price.Volume	==0	||	new_Price.OpenInterest	==	0	||	new_Price.Turnover	==0||	new_Price.LastPrice	==	0
	  ||last_Price.Volume	==0	||	last_Price.OpenInterest	==	0	||	last_Price.Turnover	==0||	last_Price.LastPrice	==	0)
	{
		return false;
	}

	// 根据最新的价格判断已经下的单子是不是需要撤单
	// 问题：我需要一个参数，现在来决定到了这个边界就开始撤单，那么我怎么调用。达到布林带的某一个标准的时候。
	STraderChannel *pTraderInfo_open=&g_arrTraderChannel[less_open_order_index];
	cancelNotMatchOrder(pTraderInfo_open);

	STraderChannel *pTraderInfo_close=&g_arrTraderChannel[less_close_order_index];
	cancelNotMatchOrder(pTraderInfo_close);

	
	// 计算开仓和平仓的时机，通过这个tick的数据，来判断是不是需要进行开仓或者平仓。
	isTrendOpenTime		=	isOpenTrendTime();
	isTrendCloseTime	=	isCloseTrendTime();

	// 如果达到开仓的时机，那么就进行开仓的操作，如果达到平仓的时机，那么就进行平仓的操作？
	//如果到了开仓的时机，但是已经进行开仓了，还会继续开仓吗，还是这个函数会自己判断。
	// 如果已经平仓了也是同样的道理，判断是不是已经平仓了吗。
	if (isTrendOpenTime)
	{
		STraderChannel *pTraderInfo=&g_arrTraderChannel[less_open_order_index];
		less_process_Lock(pTraderInfo);
	}
	else if (isTrendCloseTime)
	{
		STraderChannel *pTraderInfo=&g_arrTraderChannel[less_close_order_index];
		less_process_Lock(pTraderInfo);

	}
	return true;
}
double CHyArbitrageVolumeTrendOther::calculateEmaFvAdj()
{
	return 0;
}

double CHyArbitrageVolumeTrendOther::calculateLessPrice(char OffsetFlag,char Direction,double fv,int perside)
{
	
	// 这个最后的挂单价根本就没有计算啊，还是这个maxprice已经改变了。
	// tirgger 感觉根本就不需要计算挂单价，直接达到下单条件之后，根据选择的下单方式直接下单就好了
	double price=0;
	if (Direction	==	THOST_FTDC_D_Buy)				//买
	{
		price	=	0;
	}
	else if(Direction	==	THOST_FTDC_D_Sell)			//卖
	{
		price	=	MaxPrice;
	}
	return price;


}

bool CHyArbitrageVolumeTrendOther::isOpenTrendTime()
{
	if (status	==	STATUS_Exit	||	status	==	STATUS_Pause)
	{
		return false;
	}

	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;
	if (diffVolume	<	param->less.openEdge)
	{
		return false;
	}

	int diffOpenInterest	=	new_Price.OpenInterest	-	last_Price.OpenInterest;

	if (diffOpenInterest	<=	param->less.index)
	{
		return false;
	}

	double edge =param->less.spread;

	if (arbitrageDirection	==	Direction_long)
	{
		return isUpTime(edge);
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		return isDownTime(edge);
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther::isCloseTrendTime()
{
	if (status	==	STATUS_Pause)
	{
		return false;
	}

	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;
	if (diffVolume	<	param->less.closeEdge)
	{
		return false;
	}

	int diffOpenInterest	=	new_Price.OpenInterest	-	last_Price.OpenInterest;

	if (diffOpenInterest	>=	-	param->less.index)
	{
		return false;
	}


	double edge =param->less.spread;


	if (arbitrageDirection	==	Direction_long)
	{
		return isDownTime(edge);
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		return isUpTime(edge);
	}
	return false;
}



bool CHyArbitrageVolumeTrendOther::isUpTime(double edge)
{
	int multiple=getVolumeMultiple(g_arrChannel,less_md_index);
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;
	double diffTurnover	=	new_Price.Turnover	-	last_Price.Turnover;

	if (diffVolume	==	0	||	diffTurnover	==	0	||	multiple	==	0)
	{
		return false;
	}
	double avePrice	=	diffTurnover/diffVolume/multiple;

	double temp	=	100*(avePrice	-	last_Price.BidPrice1)/(last_Price.AskPrice1-last_Price.BidPrice1);

	if (temp >=	edge)
	{
		return true;

	}
	return false;

}

bool CHyArbitrageVolumeTrendOther::isDownTime(double edge)
{
	int multiple=getVolumeMultiple(g_arrChannel,less_md_index);    //这个参数是什么意思，我怎么计算。
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;    //数量差？
	double diffTurnover	=	new_Price.Turnover	-	last_Price.Turnover;  //成交金额差

	if (diffVolume	==	0	||	diffTurnover	==	0	||	multiple	==	0)
	{
		return false;
	}

	double avePrice	=	diffTurnover/diffVolume/multiple;

	double temp	=	100*(last_Price.AskPrice1	-	avePrice)/(last_Price.AskPrice1-last_Price.BidPrice1);
	if (temp >=	edge)
	{
		return true;

	}
	return false;

}
void CHyArbitrageVolumeTrendOther::cancelNotMatchOrder(STraderChannel* pTraderInfo)
{
	pthread_mutex_lock(&pTraderInfo->cs_trader_order);
	for (unsigned int i=0;i<pTraderInfo->trader_order.size();i++)
	{
		orderMsg *ordermsg=&pTraderInfo->trader_order[i];
		if (ordermsg->remainVolume	==	0)
		{
			continue;
		}

		if (ordermsg->status	==	1) //挂单状态，考虑是否撤单
		{
			lessAction_action_Lock(ordermsg);

		}
	}
	pthread_mutex_unlock(&pTraderInfo->cs_trader_order);
}

void CHyArbitrageVolumeTrendOther::closeTraded(char direction,double price)
{


}

void CHyArbitrageVolumeTrendOther::openTraded(char direction,double price)
{

}