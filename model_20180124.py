# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:24:09 2018

@author: 15840
"""

import os
import pandas as pd
import numpy as np
import math
os.chdir('D:/model/其他')
#ddq= pd.read_sas('doudou_v11.sas7bdat')

ddq= pd.read_excel('data.xlsx')
#a2=pd.pivot_table(a1,index=["LND_DAY"],values=["TARGET"],aggfunc=[np.sum,len],margins=True)

##step1.分为开发、验证样本
#=============================================================================
##step2.计算IV值 
#1、lnd_day:0.40361
#2、当前正常的信用卡账户当前负债额:0.47868
#3、贷款合同金额合计:0.32907
#tt=ddq[['TARGET','LND_DAY',''NORM_CDT_BAL_RCNT','LNSI_CDT_LMT']]
#tt=ddq[['TARGET','LND_DAY','当前正常的信用卡账户当前负债额','贷款合同金额合计']]
#=============================================================================
sample=ddq.drop(['业务号','授信月','auth_id','STATS_MONTH','EOC_DLQ_STATUS','EOM_DLQ_STATUS','MOB','CREATED_DATE','IDENTITYNO','产品类型','互联网征信报告主表ID','_TYPE_','_FREQ_'],1)

##输入样本，输出iv_list
def iv(tt):
    var=list(tt.columns)#筛选所有变量的列表
    var.remove('TARGET')
    try:
        
        for i in range(len(var)): 
            a1=tt[['TARGET',var[i]]]
            l1=list(a1.columns)
            a2=pd.crosstab(a1[l1[1]],a1[l1[0]],margins=True).reset_index() ##交叉表
            a2['p_0']=a2[0]/12839
            a2['p_1']=a2[1]/1747    
            
            for n in range(len(a2.index)):
                if a2['p_0'][n]>0 and a2['p_1'][n]>0:
                    a2.loc[n,'woe']=math.log(a2['p_0'][n]/a2['p_1'][n])
                    a2.loc[n,'iv']=(a2['p_0'][n]-a2['p_1'][n])*a2['woe'][n]
                else:
                    a2.loc[n,'woe']=-9999
                    a2.loc[n,'iv']=-9999
            
            c=a2[a2.iv>0].reset_index(drop=True)
            iv=c['iv'].sum()  ##计算合计
            #print (i)
            iv_list.append(iv)
            #iv_dict= dict(zip(var,iv_list))    
    except:
        pass
    l1=pd.DataFrame(var,columns=['name'])
    l2=pd.DataFrame(iv_list,columns=['iv'])
    l3=l1.join(l2)

    return (l3)

#所有变量iv列表
iv_list=[]
iv=iv(sample)

#iv值按大小排序，删除较小值
iv_sort=iv.sort_index(by=['iv'],ascending=False)#419条
iv_final=iv_sort[(iv_sort.iv>=0.01)&(iv_sort.iv<1)]#323条

#=============================================================================
##step3.finebin
1、分组：取值大于50,分50组，
        取值小于20组，取相应组数
        否则取20组

#1、lnd_day:
#2、当前正常的信用卡账户当前负债额:0.47868
#3、贷款合同金额合计:0.32907
#tt=ddq[['TARGET','LND_DAY',''NORM_CDT_BAL_RCNT','LNSI_CDT_LMT']]
#tt=ddq[['TARGET','LND_DAY','当前正常的信用卡账户当前负债额','贷款合同金额合计']]
#=============================================================================

tt=ddq[['TARGET','LND_DAY','当前正常的信用卡账户当前负债额','贷款合同金额合计']]
#分组，50组
len(tt['LND_DAY'].unique()) #1503
tt['R_LND_DAY']=pd.qcut(tt['LND_DAY'],50,labels=False)
tt['R_var2']=pd.qcut(tt['当前正常的信用卡账户当前负债额'],50,labels=False)
###=============================================================================


def group(tt):
    var=list(tt.columns)#筛选所有变量的列表
    var.remove('TARGET')
    try:
        for i in range(len(var)): 
            n=len(tt[var[i]].unique())
            if n>50:
                tt['r_'+var[i]]=pd.qcut(tt[var[i]],50,labels=False)
            elif n<20:
                tt['r_'+var[i]]=pd.qcut(tt[var[i]],n,labels=False)
            else:
                tt['r_'+var[i]]=pd.qcut(tt[var[i]],20,labels=False)
            print (tt.head())
    except:
        pass
###=============================================================================

def pct_rank_qcut(series, n):
    edges = pd.Series([float(i) / n for i in range(n + 1)])
    f = lambda x: (edges >= x).argmax()
    return series.rank(pct=1).apply(f)

def group1(tt):
    var=list(tt.columns)#筛选所有变量的列表
    var.remove('TARGET')
    try:
        for i in range(len(var)): 
            n=len(tt[var[i]].unique())
            if n>50:
                tt['r_'+var[i]]=pct_rank_qcut(tt[var[i]],50)
            elif n<20:
                tt['r_'+var[i]]=pct_rank_qcut(tt[var[i]],n)
            else:
                tt['r_'+var[i]]=pct_rank_qcut(tt[var[i]],20)
            #print (tt.head())
    except:
        pass
          
#sample1['r_'+'USED_CREDIT_LIMIT_AMOUNT']=pct_rank_qcut(sample1.USED_CREDIT_LIMIT_AMOUNT, 50)
#sample1['r_'+'ds2']=pct_rank_qcut(sample1.DS, 50)

##筛选求秩后的变量 
var1=list(iv_final.name)
var1.append('TARGET')
sample1=pd.DataFrame(sample,columns=var1)##筛选iv值大于0.01之后的样本
group1(sample1)##等距分段   

var2=list(sample1.columns) 
#筛选r_ 开头的字段
var3=[]
for i in range(len(var2)):
    if var2[i].find('r_')>=0:
        var3.append(var2[i])
var3.append('TARGET')    
sample2=pd.DataFrame(sample1,columns=var3)          
iv_list=[]
aft_iv=iv(sample2)

#iv值按大小排序，删除较小值
aft_iv_sort=aft_iv.sort_index(by=['iv'],ascending=False)#323条
aft_iv_final=aft_iv_sort[(aft_iv_sort.iv>=0.01)&(aft_iv_sort.iv<1)]#303条


def findbin(tt,sample):
    l0=pd.DataFrame(columns=['rank','woe','fmtname','max'])
    var=list(tt.columns)#筛选所有变量的列表
    var.remove('TARGET')
    try:
        for i in range(len(var)): 
            a1=tt[['TARGET',var[i]]]
            l1=list(a1.columns)
            a2=pd.crosstab(a1[l1[1]],a1[l1[0]],margins=True).reset_index() ##交叉表
            a2['p_0']=a2[0]/12839
            a2['p_1']=a2[1]/1747   
            a2['fmtname']=var[i]
            
            for n in range(len(a2.index)):
                if a2['p_0'][n]>0 and a2['p_1'][n]>0:
                    a2.loc[n,var[i]+'_woe']=math.log(a2['p_0'][n]/a2['p_1'][n])
                else:
                    a2.loc[n,var[i]+'_woe']=-9999
            finebin=a2[[var[i],var[i]+'_woe','fmtname']]
            finebin2=finebin.rename(columns={var[i]:'rank',var[i]+'_woe':'woe'})
            
            sample3=pd.merge(sample2,finebin2,on='',how='left')
            #print (finebin2.head())
            l0=pd.concat([l0,finebin2])  
    except:
        pass
    return (l0)
   
finebin=findbin(sample2)
finebin2=finebin[finebin['rank']!='All'].reset_index(drop=True)


def findbin(tt,sample):
    l0=pd.DataFrame(columns=['rank','woe','fmtname','max'])
    var=list(tt.columns)#筛选所有变量的列表
    var.remove('TARGET')
    try:
        for i in range(len(var)): 
            a1=tt[['TARGET',var[i]]]
            l1=list(a1.columns)
            a2=pd.crosstab(a1[l1[1]],a1[l1[0]],margins=True).reset_index() ##交叉表
            a2['p_0']=a2[0]/12839
            a2['p_1']=a2[1]/1747   
            a2['fmtname']=var[i]
            
            for n in range(len(a2.index)):
                if a2['p_0'][n]>0 and a2['p_1'][n]>0:
                    a2.loc[n,var[i]+'_woe']=math.log(a2['p_0'][n]/a2['p_1'][n])
                else:
                    a2.loc[n,var[i]+'_woe']=-9999
            finebin=a2[[var[i],var[i]+'_woe','fmtname']]
            finebin2=finebin.rename(columns={var[i]:'rank',var[i]+'_woe':'woe'})
            
            sample3=pd.merge(sample2,finebin2,on='',how='left')
            #print (finebin2.head())
            l0=pd.concat([l0,finebin2])  
    except:
        pass
    return (l0)



#计算每组最大值
a1=sample1[['LND_DAY','r_LND_DAY']]
a2=tt[[var[i],]].groupby('r_LND_DAY').max().add_prefix('max_').reset_index()

#=============================================================================
##step4.bootstrap
1、随机抽样80%
2、跑100次逻辑回归，计数
3、筛选变量，频数>80

#=============================================================================


def bootstrap():
    for i in range(len(tt.index)):
        dev=tt.sample(frac=0.8)##随机抽样80%
        
        

















