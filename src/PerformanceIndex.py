# -*- coding: utf-8 -*-

import math
import sys 
import scipy.stats

# import matplotlib
import matplotlib.font_manager as managerfront
import curvefit
INFINITE = 1000000


reload(sys) 
sys.setdefaultencoding('utf-8')
myfont = managerfront.FontProperties(fname=r'C:/Windows/Fonts/msyh.ttf')


def GetMaxReverse(result):
    peak = 0.0
    max_reverse = 0.0
    for money in result:
        if money > peak:
            peak = money
        else:
            reverse = (peak - money)/peak
            if reverse > max_reverse:
                max_reverse = reverse
    return max_reverse
    
def GetProfitPerYear(result):
#     print result[0],result[-1]
    profit_per_year = (result[-1]/result[0] - 1)*100/len(result)*250
 
    return profit_per_year

def TransPriceList2ProfitList(pricelist):
    lastprice = 0.0
    profit = 0.0
    profit_list = []
    for price in pricelist:
        if price > 0 and lastprice > 0:
            profit = (price/lastprice - 1) * 100
            if profit > 20:
                print "error"
                return None
        else:
            profit = 0.0
            
        if price > 0:
            lastprice = price
        profit_list.append(profit)
    return profit_list
               
    
def GetCov(portfolio,standard):
    len1 = len(portfolio)
    len2 = len(standard)
    if len1 != len2:
        return None;
    portfolio_mean = sum(portfolio)/len1
    standard_mean = sum(standard)/len1
    print portfolio_mean,standard_mean
    cov_sum = 0.0
    for x,y in zip(portfolio,standard):
#         print x,y
        cov_sum += (x - portfolio_mean)*(y - standard_mean)
    cov = cov_sum/len1
    return cov
                
def GetVar(profit_list):
    length1 = len(profit_list)
    profit_mean = sum(profit_list)/length1
    square_sum = 0.0
    for profit in profit_list:
        square_sum += pow(profit - profit_mean, 2)
    var =  square_sum/length1
    """����"""
    var = math.sqrt(var)
    return var

def GetGunDongNianHua(valuelist):
    GunDongNianHua = []
    for i in range(len(valuelist)):
        if i < 250:
            GunDongNianHua.append(0)
        else:
            profit_year = valuelist[i]/valuelist[i - 250] - 1
            GunDongNianHua.append(profit_year)
    
    return GunDongNianHua
        
def GetProfitPerMonth(alltradingdate,valuelist):
    ProfitPerMonth = []
    current_month = 0
    endvalue = 0.0
    if len(alltradingdate) != len(valuelist):
        return None
    startvalue = valuelist[0]
    listlength = len(valuelist)
    for i in range(listlength):
        tradingdate = alltradingdate[i]
        month = tradingdate[5:7]
        month = int(month)
        if month != current_month and current_month != 0:
            """new month"""
            current_month = month
            endvalue = valuelist[i - 1]
            profit_month = endvalue/startvalue - 1
            ProfitPerMonth.append(profit_month)
            startvalue = valuelist[i]
            
    return ProfitPerMonth
            
def GetRegressionProfitPerYear(valuelist):
    listlength = len(valuelist)
    x = [i for i in range(listlength)]
    y = valuelist
    paras = curvefit.polyfit(x,y,"linear")
    print paras["para"]
    fgradient = paras["para"][0]
    intercept = paras["para"][1]
    fitting_result = x[-1] * fgradient + intercept
    print fitting_result    
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    R_sqr = pow(r_value,2)
    print r_value,R_sqr
    return fitting_result,R_sqr
        
def GetWinningPercent(valuelist):
    winningtimes = 0
    profit_list = TransPriceList2ProfitList(valuelist)
    for i in range(len(profit_list)):
        if profit_list[i] > 0:
            winningtimes += 1
    return winningtimes/len(valuelist)

def GetProfitLastDay(valuelist):
    winlastdays = 0
    max_winlastdays = 0
    lostlastdays = 0
    max_lostlastdays = 0
    preprofit = 0
    profit_list = TransPriceList2ProfitList(valuelist)
    for i in range(profit_list):
        currentprofit = profit_list[i]
        if currentprofit > 0:
            if preprofit < 0:
                """ recount """
                winlastdays = 0
            winlastdays += 1
        elif currentprofit < 0:
            if preprofit > 0:
                lostlastdays = 0
            lostlastdays = 0
               
        if winlastdays > max_winlastdays:
            max_winlastdays = winlastdays
        
        if lostlastdays > max_lostlastdays:
            max_lostlastdays = lostlastdays
        
        """end this loop"""
        if currentprofit != 0:
            preprofit = currentprofit
    
    return max_winlastdays,max_lostlastdays
                
def GetRectifyMaxReverse(valuelist):
    reverselist = []
    peak = 0.0
    max_reverse = 0.0
    for money in valuelist:
        if money > peak:
            peak = money
            if max_reverse != 0:
                reverselist.append(max_reverse)
                max_reverse = 0
        else:
            reverse = (peak - money)/peak
            if reverse > max_reverse:
                max_reverse = reverse
    if max_reverse != 0:
        reverselist.append(max_reverse)
      
    reverselist = sorted(reverselist,reverse=True)
    if len(reverselist) > 5:
        calcul_lenth = 5
    else:
        calcul_lenth = len(reverselist)
    
    reverse_sum = 0.0
    for i in range(calcul_lenth):
        reverse_sum += reverselist[i]
    
    reverse_ave = reverse_sum/calcul_lenth
    
    return reverselist,reverse_ave
    
       
def GetReverseDays(valuelist):
    peak = 0.0
    peakindex = 0
    max_reverse = 0.0
    reverse_days = 0
    max_reverse_days = 0
    reverse_days_sum = 0.0
    reverse_days_list = []
    period = len(valuelist)
    for i in range(period):
        money = valuelist[i]
        if money > peak:
            peak = money
            peakindex = i
            if reverse_days > 0:
                reverse_days_list.append(reverse_days)
                reverse_days = 0
                max_reverse = 0
        else:
            reverse = (peak - money)/peak
            if reverse > max_reverse:
                max_reverse = reverse
                reverse_days = i - peakindex
        if reverse_days > max_reverse_days:
            max_reverse_days = reverse_days
            
    if reverse_days > 0:
        reverse_days_list.append(reverse_days)
    reverse_days_list = sorted(reverse_days_list,reverse = True)  
    
    if len(reverse_days_list) > 5:
        calcul_num = 5
    else:
        calcul_num = len(reverse_days_list)
    
    for i in range(calcul_num):
        reverse_days_sum += reverse_days_list[i]
    reverse_days_ave = reverse_days_sum / calcul_num
    
    return reverse_days_list,max_reverse_days,reverse_days_ave
     
def Get1PercentVar(profitlist):
    """"""
    sortedlist = sorted(profitlist)
    span = int(len(sortedlist)/100)
    return sortedlist[0:span]
    
def GetStableSharp(valuelist):
    RegressionValue,R_squr = GetRegressionProfitPerYear(valuelist)
    g_var = GetVar(valuelist)
    RegressionProfit = (RegressionValue/valuelist[0] - 1)*250/len(valuelist)
    StableSharp = RegressionProfit/g_var
    return StableSharp
    
def GetIncomeRiskRadio(valuelist):
    """"""
    profit_per_year = GetProfitPerYear(valuelist)
    maxRevese = GetMaxReverse(valuelist)
    return profit_per_year/maxRevese
                                         
def GetRectifyIncomeRiskRadio(valuelist): 
    profit_per_year = GetProfitPerYear(valuelist)   
    rectify_max_reverse =   GetRectifyMaxReverse(valuelist)[1]   
    return profit_per_year/rectify_max_reverse     



def get_inde():
    readfile = r"D:\result2_2017.txt"
    rhandle = open(readfile,'r')
    lines = rhandle.readlines()
    val_list = []
    for line in lines:
        print line.split('\t\n')
        val_list.append(float(line.strip()))
    
    win_value = 0.0
    lose_value = 0.0
    win_times  = 0
    lost_times = 0
    stay_times = 0
    for i in range(len(val_list) - 1):
        if val_list[i + 1 ] > val_list[i]:
            win_value += val_list[i + 1 ] -  val_list[i]
            win_times += 1
        elif val_list[i + 1 ] < val_list[i]:
            print val_list[i ] , val_list[i + 1]
            lose_value += val_list[i ] -  val_list[i + 1]
            lost_times += 1
        else:
            stay_times += 1
    
    print win_value,lose_value, "%.4f"%(win_value/lose_value),"盈亏比:","%.4f"%((win_value/win_times)/(lose_value/lost_times))
    print win_times,lost_times, "%.4f"%(float(win_times)/(lost_times + win_times))
    print stay_times
        
        
        
# get_inde()

