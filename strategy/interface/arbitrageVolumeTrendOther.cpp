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
	new_Price=getNewPrice(g_arrChannel,less_md_index);

	last_Price=getLastPrice(g_arrChannel,less_md_index);

	if (new_Price.Volume	==0	||	new_Price.OpenInterest	==	0	||	new_Price.Turnover	==0||	new_Price.LastPrice	==	0
	  ||last_Price.Volume	==0	||	last_Price.OpenInterest	==	0	||	last_Price.Turnover	==0||	last_Price.LastPrice	==	0)
	{
		return false;
	}

	STraderChannel *pTraderInfo_open=&g_arrTraderChannel[less_open_order_index];
	cancelNotMatchOrder(pTraderInfo_open);

	STraderChannel *pTraderInfo_close=&g_arrTraderChannel[less_close_order_index];
	cancelNotMatchOrder(pTraderInfo_close);

	isTrendOpenTime		=	isOpenTrendTime();
	isTrendCloseTime	=	isCloseTrendTime();

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
	double price=0;
	if (Direction	==	THOST_FTDC_D_Buy)				//Âò
	{
		price	=	0;
	}
	else if(Direction	==	THOST_FTDC_D_Sell)			//Âô
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
	int multiple=getVolumeMultiple(g_arrChannel,less_md_index);
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;
	double diffTurnover	=	new_Price.Turnover	-	last_Price.Turnover;

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

		if (ordermsg->status	==	1) //¹Òµ¥×´Ì¬£¬¿¼ÂÇÊÇ·ñ³·µ¥
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