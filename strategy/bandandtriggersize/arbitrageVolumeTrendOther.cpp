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
	new_Price=getNewPrice(g_arrChannel,less_md_index);

	last_Price=getLastPrice(g_arrChannel,less_md_index);


	if (new_Price.Volume	==0	||	new_Price.OpenInterest	==	0	||	new_Price.Turnover	==0||	new_Price.LastPrice	==	0
	  ||last_Price.Volume	==0	||	last_Price.OpenInterest	==	0	||	last_Price.Turnover	==0||	last_Price.LastPrice	==	0)
	{
		return false;
	}

	//通过 positionAdj来设置band的开仓边界，一般都是0.5,这边除以了10，所以设置的时候，应该在10倍。
	bandOpenEdge = (param->less.PositionAdj)/10;
	// 通过设置shortcompxvae来设置band的平仓边界，一般都是2
	bandCloseEdge = (param->less.ShortCompXave)/10;

	// 此部分代码主要是用来保存计算middledata和sd的price。
	double price = new_Price.LastPrice;
	if (prices.size() < param->less.CompXave)
	{
		prices.push_back(price);
		double tmp = getEMAData(price);
		return false;
	}
	else{
		prices.push_back(price);
		vector<double>::iterator it = prices.begin();
		it = prices.erase(it);
	}
	//已经达到了周期，开始计算middle data和sd的data
	if (param->less.CompTheo == "EMA"){
		middleData = getEMAData(price);
	}
	else
	{
		middleData = getMAData(prices);
	}
	sdData = getSDData(prices);

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

	// 表示现在交易量之间的差值必须达到一定的数值。
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;
	if (diffVolume	<	param->less.openEdge)
	{
		return false;
	}

	// 表示现在持仓量之间的差值需要达到一定的数值。
	int diffOpenInterest	=	new_Price.OpenInterest	-	last_Price.OpenInterest;

	if (diffOpenInterest	<=	param->less.index)
	{
		return false;
	}

	// 获取band的信号，判断根据布林带是不是已经达到开仓条件。
	// 如果没有达到的话，直接返回false, 达到的话判断trigger size是不是达到.
	bool bandSignal = isBandOpenTime();
	if (bandSignal ==false)
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

	//现在根据袁总的要求，在判断平仓的时候，只是根据band的平仓条件。
	// 所以trigger size 的平仓条件先忽略。
	return isBandCloseTime();

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
	int multiple=getVolumeMultiple(g_arrChannel,less_md_index);   //返回合约乘数
	int diffVolume	=	new_Price.Volume	-	last_Price.Volume;  //返回持仓量的变化
	double diffTurnover	=	new_Price.Turnover	-	last_Price.Turnover;  //返回成交金额的变化

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

		if (ordermsg->status	==	1) //挂单状态，考虑是否撤单
		{
			lessAction_action_Lock(ordermsg);

		}
	}
	pthread_mutex_unlock(&pTraderInfo->cs_trader_order);
}

double CHyArbitrageVolumeTrendOther::getMAData(vector<double> prices){
	double sum =0;
	if (prices.size()==0)
	{
		return 0;
	}
	for (int i = 0; i < prices.size(); i++)
	{
		sum +=prices[i];
	}
	return sum/prices.size();
}

double CHyArbitrageVolumeTrendOther::getSDData(vector<double> prices){
	int size = prices.size();
	if (size ==0)
	{
		return 0;
	}
	double sum = 0;
	for (int i = 0; i < prices.size(); i++)
	{
		sum +=prices[i];
	}
	double avg = sum/size;
	sum = 0;
	for (int i = 0; i < size; i++)
	{
		sum += (prices[i]-avg)*(prices[i]-avg);
	}
	return sqrt(sum);
}

double CHyArbitrageVolumeTrendOther::getEMAData(double price){
	if (prices.size()==1)
	{
		emaTickNum =1;
		lastPrice = price;
		return lastPrice;
	}
	if (emaTickNum < param->less.CompXave)
	{
		emaTickNum +=1;
	}
	double ret = ((emaTickNum-1)*lastPrice + 2*price)/(emaTickNum+1);
	lastPrice = ret;
	return ret;
}


bool CHyArbitrageVolumeTrendOther::isLongOpenTime(double price,double middleval,double upval){
	if (price < upval && price > middleval)
	{
		return true;
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther::isLongCloseTime(double price,double profitval,double lossval){
	if (price < lossval || price > profitval)
	{
		return true;
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther::isShortOpenTime(double price,double middleval,double downval){
	if (price>downval && price < middleval)
	{
		return true;
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther::isShortCloseTime(double price,double profitval,double lossval){
	if (price > lossval || price < profitval )
	{
		return true;
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther::isBandOpenTime(){
	if (arbitrageDirection	==	Direction_long)
	{
		bool isLoneOpen = isLongOpenTime(price,middleData,middleData + sdData*bandOpenEdge);
		if (isLoneOpen)
		{
			return true;
		}
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		bool isShortOpen =isShortOpenTime(price,middleData,middleData-sdData*bandOpenEdge);
		if (isShortOpen)
		{
			return true;
		}
	}
	return false;
}

bool CHyArbitrageVolumeTrendOther::isBandCloseTime(){

	if (arbitrageDirection	==	Direction_long)
	{
		bool isLongClose = isLongCloseTime(price,middleData+sdData*bandCloseEdge,middleData - sdData*bandOpenEdge);
		if(isLongClose){
			return true;
		}
	}
	else if (arbitrageDirection	==	Direction_short)
	{
		bool isShortClose = isShortCloseTime(price,middleData-sdData*bandCloseEdge,middleData + sdData*bandOpenEdge);
		if (isShortClose){
			return true;
		}
	}
	return false;
}

void CHyArbitrageVolumeTrendOther::closeTraded(char direction,double price)
{


}

void CHyArbitrageVolumeTrendOther::openTraded(char direction,double price)
{

}