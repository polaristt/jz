

import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from datetime import datetime
import datetime as dt
import os
import re
import numpy as np
os.chdir('D:/君正/008.人行报告/019.规则调整')
engine = create_engine('postgresql://usr01:User1024@dataware-public.cdybc2uwbiyi.cn-north-1.redshift.amazonaws.com.cn:5439/dataware')

sql_1='select * from datamart.dm_pboc_loan_info'
sql_2='select * from datamart.dm_pboc_summary'
sql_3='select report_number,name,query_time,report_time from datamart.dm_pboc_personal'
sql_4='select * from report.personal_image'
sql_5='select * from report.rj_deltails'


#载入数据
loan=pd.read_sql(sql_1,engine)
personal=pd.read_sql(sql_3,engine)
image=pd.read_sql(sql_4,engine)
rj=pd.read_sql(sql_5,engine)
summary=pd.read_sql(sql_2,engine)


#=======================================================================
#1、月供计算
l1=['个人住房贷款','个人商用房（包括商住两用）贷款','个人商用房','个人房贷款','个人住房公积金贷款']
l2=['个人住房贷款','个人商用房（包括商住两用）贷款','个人商用房','个人房贷款']
loan2=loan[(loan['loan_type'].isin(l1))&(loan['acct_stat']!='结清')]      
#商业贷款最大值
loan3=loan2[['report_number','deserved_pmt']][loan2['loan_type'].isin(l2)].groupby('report_number').max().add_prefix('sh_').reset_index()

#公积金贷款最大值
loan4=loan2[['report_number','deserved_pmt']][loan2['loan_type'].isin(['个人住房公积金贷款'])].groupby('report_number').max().add_prefix('gj_').reset_index()

loan5=pd.merge(loan3,loan4,on='report_number',how='outer').fillna(0)

loan5['yg']=np.where(loan5.sh_deserved_pmt>0,loan5.sh_deserved_pmt,loan5.gj_deserved_pmt)


#=======================================================================
#2、支出计算
loan6=loan[['report_number','assu_method','deserved_pmt']][loan.deserved_pmt>0]
loan6['zc1']=np.where(loan6['assu_method'].isin(['抵押担保','质押（含保证金）担保']),loan6['deserved_pmt']*0.5,loan6['deserved_pmt'])
loan7=loan6[['report_number','zc1']].groupby('report_number').sum().reset_index()

summ=summary[['report_number','cr_avg_6mth_bal','qr_avg_6mth_bal']]
summ['zc2']=summ['cr_avg_6mth_bal']*0.1

f1=pd.merge(loan7,summ,on='report_number',how='outer').fillna(0)
f1['zc']=f1['zc1']+f1['zc2']

#=======================================================================
#合并
f2=pd.merge(loan5[['report_number','yg']],f1[['report_number','zc']],on='report_number',how='outer').fillna(0)
f2['rule1']=np.where((f2.yg<20000)&(f2.zc>=70000),1,0)
f2['rule2']=np.where((f2.yg>=20000)&(f2.zc>=150000),1,0)
f2['rule']=f2['rule1']+f2['rule2']
f2.to_excel('f2.xlsx')



