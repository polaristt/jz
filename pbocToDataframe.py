# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 09:23:22 2017

@author: 15840
"""

# -*- coding: utf-8 -*-

'''
人行解析至数据框函数名：
PersonalToDf  -- 个人基本信息
SummaryToDf   -- 汇总信息
CardinfoToDf  -- 卡明细信息
LoaninfoToDf  -- 贷款明细信息
DetailqryToDf -- 查询明细信息
AccfundToDf   -- 住房公积金信息
ForceinfoToDf -- 强制执行信息

'''
#==========================================================================

import pandas as pd
from locale import setlocale
from locale import LC_NUMERIC
from locale import atof
import numpy as np

#==========================================================================
#说明：将字典键值对中的值部分格式转化成字符串，输入内容必须为字典
def dict_str(dicts):
    if type(dicts)==dict:
        x=dicts.keys()
        for key in x:
            if type(dicts[key]) in [int,float]:
                dicts[key]=str(dicts[key])
            elif type(dicts[key])==dict:
                dict_str(dicts[key])
            elif type(dicts[key])==list:
                if dicts[key]:
                    for ii in dicts[key]:
                        dict_str(ii)
            else:
                pass
    else:
        pass
    
    return(dicts)

#==========================================================================
#说明：字典中的键值对提取至数据框中(用于处理信贷明细中的单条信息)，输入内容为字典，输出为数据框
def DictToDataframe(dicts):
    df=pd.DataFrame()
    if type(dicts)==dict:
        key_list_1=dicts.keys()
        for i in key_list_1:
            if type(dicts[i])==str:
                df=pd.concat([df,pd.DataFrame({i:[dicts[i]]})],axis=1)
            elif type(dicts[i])==dict:
                key_list_2=dicts[i].keys()
                for j in key_list_2:
                    df=pd.concat([df,pd.DataFrame({j:[dicts[i][j]]})],axis=1)
            else:
                pass
    else:
        pass
    
    return(df)

#==========================================================================
#说明：数值类型字段，string转float，含异常值处理
def StrToFloat(str_text):
    try:
        setlocale(LC_NUMERIC, 'English_US')
        if (str_text==None)|(str_text==''):
            output=np.nan
        elif type(str_text)==float:
            output=np.nan
        else:
            output=atof(str_text.replace('，',','))
    except:
        output=np.nan
    
    return(output)

#==========================================================================
#说明：数值类型字段，string转int，含异常值处理
def StrToInt(str_text):
    try:
        setlocale(LC_NUMERIC, 'English_US')
        if (str_text==None)|(str_text==''):
            output=np.nan
        elif type(str_text)==float:
            output=np.nan
        else:
            output=int(atof(str_text.replace('，',',')))
    except:
        output=np.nan
    
    return(output)

#==========================================================================
#说明：文本类型字段异常值处理
def StrOutlierModify(str_text):
    if (type(str_text)==float)|(str_text==''):
        output=None
    else:
        output=str_text
    
    return(output)

#==========================================================================
#说明：文本类型字段，转换日期格式(xxxx.xx.xx)
def StrToDate1(str_text):
    if (type(str_text)==float)|(str_text==''):
        output=None
    else:
        output=str_text.replace('.','-')
    
    return(output)

#==========================================================================
#说明：文本类型字段，转换日期格式(xxxx年xx月)
def StrToDate2(str_text):
    if (type(str_text)==float)|(str_text==''):
        output=None
    else:
        output=str_text[:4]+'-'+str_text[5:7]
    
    return(output)

#==========================================================================
#说明：文本类型字段，转换日期格式(xxxx年xx月xx日)
def StrToDate3(str_text):
    if (type(str_text)==float)|(str_text==''):
        output=None
    else:
        output=str_text[:4]+'-'+str_text[5:7]+'-'+str_text[8:10]
    
    return(output)

#==========================================================================
#说明：个人基本信息解析至数据框，输入内容为字典，输出为数据框
def PersonalToDf(PbocDict):    
    data=dict_str(PbocDict)
    personal=['REPORT_NUMBER', 'QUERY_TIME', 'REPORT_TIME', 'NAME', 'ID_TYPE',
           'ID_NO', 'RPT_QRY_RSN', 'RPT_QRY_FMT', 'RPT_QRY_ORG',
           'RPT_QRY_RST', 'SEX', 'BIRTH_DT', 'MARRIAGE_STATUS', 'MOBILE_NO',
           'UNIT_PHO', 'HOME_PHO', 'DEGREE', 'Q_DEGREE', 'COMM_ADDR',
           'RESADDR_INID', 'SPOUSE_NM', 'SPOUSE_ID_TYPE', 'SPOUSE_ID_NO',
           'SPOUSE_COMP', 'SPOUSE_PHO', 'RESID_ADDR_1', 'RESID_STATUS_1',
           'RES_UP_DT_1', 'RESID_ADDR_2', 'RESID_STATUS_2', 'RES_UP_DT_2',
           'RESID_ADDR_3', 'RESID_STATUS_3', 'RES_UP_DT_3', 'RESID_ADDR_4',
           'RESID_STATUS_4', 'RES_UP_DT_4', 'RESID_ADDR_5', 'RESID_STATUS_5',
           'RES_UP_DT_5', 'WORK_UNIT_1', 'UNIT_ADDR_1', 'VOCATION_1', 'INDUSTRY_1',
           'PROFES_TITLE_1', 'PROFES_POST_1', 'ENTER_OUR_UNIT_YEAR_1',
           'VOC_UP_DT_1', 'WORK_UNIT_2', 'UNIT_ADDR_2', 'VOCATION_2', 'INDUSTRY_2',
           'PROFES_TITLE_2', 'PROFES_POST_2', 'ENTER_OUR_UNIT_YEAR_2',
           'VOC_UP_DT_2', 'WORK_UNIT_3', 'UNIT_ADDR_3', 'VOCATION_3', 'INDUSTRY_3',
           'PROFES_TITLE_3', 'PROFES_POST_3', 'ENTER_OUR_UNIT_YEAR_3',
           'VOC_UP_DT_3', 'WORK_UNIT_4', 'UNIT_ADDR_4', 'VOCATION_4', 'INDUSTRY_4',
           'PROFES_TITLE_4', 'PROFES_POST_4', 'ENTER_OUR_UNIT_YEAR_4',
           'VOC_UP_DT_4', 'WORK_UNIT_5', 'UNIT_ADDR_5', 'VOCATION_5', 'INDUSTRY_5',
           'PROFES_TITLE_5', 'PROFES_POST_5', 'ENTER_OUR_UNIT_YEAR_5',
           'VOC_UP_DT_5']
    df=pd.DataFrame(columns=personal)
    
    #==============================================================================
    # 2.按照字段逐个更新
    #==============================================================================
    da={}
    #==============================================================================
    # (1)更新报告头数据
    #==============================================================================
    A=data.get('ReportMessage').get('Header').get('MessageHeader')
    da.update({'REPORT_NUMBER':A['ReportSN'],'QUERY_TIME':A['QueryTime'].replace('.','-'),'REPORT_TIME':A['ReportCreateTime'].replace('.','-')})
    #
    A=data.get('ReportMessage').get('Header').get('QueryReq')
    da.update({'NAME':A['Name'],'ID_TYPE':A['Certtype'],'ID_NO':A['Certno'],'RPT_QRY_RSN':A['QueryReason'],'RPT_QRY_FMT':A['Format'],'RPT_QRY_ORG':A['QueryOrg'],'RPT_QRY_RST':A['QueryResultCue']})
    ##==============================================================================
    ## (2)更新身份基本信息表
    ##==============================================================================
    A=data.get('ReportMessage').get('PersonalInfo').get('Identity')
    da.update({'SEX':A['Gender'],'BIRTH_DT':A['Birthday'].replace('.','-'),'MARRIAGE_STATUS':A['MaritalState'],'MOBILE_NO':A['Mobile'],'UNIT_PHO':A['OfficeTelephoneNo'],'HOME_PHO':A['HomeTelephoneNo'],'DEGREE':A['EduLevel'],'Q_DEGREE':A['EduDegree'],'COMM_ADDR':A['PostAddress'],'RESADDR_INID':A['RegisteredAddress']})
    
    A=data.get('ReportMessage').get('PersonalInfo').get('Spouse')
    da.update({'SPOUSE_NM':A['Name'],'SPOUSE_ID_TYPE':A['Certtype'],'SPOUSE_ID_NO':A['Certno'],'SPOUSE_COMP':A['Employer'],'SPOUSE_PHO':A['TelephoneNo']})
    #==============================================================================
    # (3)更新居住信息表
    #==============================================================================
    A=data.get('ReportMessage').get('PersonalInfo').get('Residence')
    if type(A) is list:
        if len(A)>0:        
            da.update({'RESID_ADDR_1':A[0].get('Address'),'RESID_STATUS_1':A[0].get('ResidenceType'),'RES_UP_DT_1':A[0].get('GetTime').replace('.','-') if A[0].get('GetTime') else None})
            if len(A)>1:
                da.update({'RESID_ADDR_2':A[1].get('Address'),'RESID_STATUS_2':A[1].get('ResidenceType'),'RES_UP_DT_2':A[1].get('GetTime').replace('.','-') if A[1].get('GetTime') else None})
                if len(A)>2:
                    da.update({'RESID_ADDR_3':A[2].get('Address'),'RESID_STATUS_3':A[2].get('ResidenceType'),'RES_UP_DT_3':A[2].get('GetTime').replace('.','-') if A[2].get('GetTime') else None})
                    if len(A)>3:
                        da.update({'RESID_ADDR_4':A[3].get('Address'),'RESID_STATUS_4':A[3].get('ResidenceType'),'RES_UP_DT_4':A[3].get('GetTime').replace('.','-') if A[3].get('GetTime') else None})
                        if len(A)>4:                      
                            da.update({'RESID_ADDR_5':A[4].get('Address'),'RESID_STATUS_5':A[4].get('ResidenceType'),'RES_UP_DT_5':A[4].get('GetTime').replace('.','-') if A[4].get('GetTime') else None})
    elif type(A) is dict:
        da.update({'RESID_ADDR_1':A['Address'],'RESID_STATUS_1':A['ResidenceType'],'RES_UP_DT_1':A['GetTime'].replace('.','-') if A.get('GetTime') else None})
    #==============================================================================
    # (4)更新职业信息表
    #==============================================================================
    A=data.get('ReportMessage').get('PersonalInfo').get('Professional')
    if type(A) is list:
        if len(A)>0:        
            da.update({'WORK_UNIT_1':A[0].get('Employer'),'UNIT_ADDR_1':A[0].get('EmployerAddress'),'VOCATION_1':A[0].get('Occupation'),'INDUSTRY_1':A[0].get('Industry'),'PROFES_TITLE_1':A[0].get('Title'),'PROFES_POST_1':A[0].get('Duty'),'ENTER_OUR_UNIT_YEAR_1':A[0].get('StartYear'),'VOC_UP_DT_1':A[0].get('GetTime').replace('.','-') if A[0].get('GetTime') else None})
            if len(A)>1:
                da.update({'WORK_UNIT_2':A[1].get('Employer'),'UNIT_ADDR_2':A[1].get('EmployerAddress'),'VOCATION_2':A[1].get('Occupation'),'INDUSTRY_2':A[1].get('Industry'),'PROFES_TITLE_2':A[1].get('Title'),'PROFES_POST_2':A[1].get('Duty'),'ENTER_OUR_UNIT_YEAR_2':A[1].get('StartYear'),'VOC_UP_DT_2':A[1].get('GetTime').replace('.','-') if A[1].get('GetTime') else None})
                if len(A)>2:
                    da.update({'WORK_UNIT_3':A[2].get('Employer'),'UNIT_ADDR_3':A[2].get('EmployerAddress'),'VOCATION_3':A[2].get('Occupation'),'INDUSTRY_3':A[2].get('Industry'),'PROFES_TITLE_3':A[2].get('Title'),'PROFES_POST_3':A[2].get('Duty'),'ENTER_OUR_UNIT_YEAR_3':A[2].get('StartYear'),'VOC_UP_DT_3':A[2].get('GetTime').replace('.','-') if A[2].get('GetTime') else None})
                    if len(A)>3:
                        da.update({'WORK_UNIT_4':A[3].get('Employer'),'UNIT_ADDR_4':A[3].get('EmployerAddress'),'VOCATION_4':A[3].get('Occupation'),'INDUSTRY_4':A[3].get('Industry'),'PROFES_TITLE_4':A[3].get('Title'),'PROFES_POST_4':A[3].get('Duty'),'ENTER_OUR_UNIT_YEAR_4':A[3].get('StartYear'),'VOC_UP_DT_4':A[3].get('GetTime').replace('.','-') if A[3].get('GetTime') else None})
                        if len(A)>4:                      
                            da.update({'WORK_UNIT_5':A[4].get('Employer'),'UNIT_ADDR_5':A[4].get('EmployerAddress'),'VOCATION_5':A[4].get('Occupation'),'INDUSTRY_5':A[4].get('Industry'),'PROFES_TITLE_5':A[4].get('Title'),'PROFES_POST_5':A[4].get('Duty'),'ENTER_OUR_UNIT_YEAR_5':A[4].get('StartYear'),'VOC_UP_DT_5':A[4].get('GetTime').replace('.','-') if A[4].get('GetTime') else None})
    elif type(A) is dict:
        da.update({'WORK_UNIT_1':A['Employer'],'UNIT_ADDR_1':A['EmployerAddress'],'VOCATION_1':A['Occupation'],'INDUSTRY_1':A['Industry'],'PROFES_TITLE_1':A['Title'],'PROFES_POST_1':A['Duty'],'ENTER_OUR_UNIT_YEAR_1':A['StartYear'],'VOC_UP_DT_1':A.get('GetTime').replace('.','-') if A.get('GetTime') else None})
    asstr=personal
    for a in asstr:
        if not da.get(a) or da.get(a)=='':
            da.update({a:None})
    df=df.append(da,ignore_index=True)    
    df=df.astype('str')
    
    return df

#==========================================================================
#说明：汇总信息解析至数据框，输入内容为字典，输出为数据框
def SummaryToDf(PbocDict):
    data=dict_str(PbocDict)
    summary=['REPORT_NUMBER', 'HOUSE_LOAN_CNT', 'OTHERLOAN_COUNT', 'FST_LOAN_MTH', 'CRD_CNT', 'FST_CRD_MTH', 'QCRD_CNT', 'FST_QCRD_MTH', 'ANNOUNCE_CNT', 'DISSENT_CNT', 'CHOUSE_LOAN_CNT', 'LN_DUE_CNT', 'LN_DUE_MTHS', 'LN_DUE_MAX_AMT', 'LN_DUE_MAX_MTHS', 'CR_DUE_CNT', 'CR_DUE_MTHS', 'CR_DUE_MAX_AMT', 'CR_DUE_MAX_MTHS', 'QR_DUE_CNT', 'QR_DUE_MTHS', 'QR_DUE_MAX_AMT', 'QR_DUE_MAX_MTHS', 'AS_DISPOSAL_AMT', 'AS_DISPOSAL_CNT', 'GU_DISPOSAL_AMT', 'GU_DISPOSAL_CNT', 'CH_DISPOSAL_AMT', 'CH_DISPOSAL_CNT', 'CR_LORG_CNT', 'CR_ORG_CNT', 'CR_CNT', 'CR_CONTRACT_AMT', 'CR_ORG_MAX_LMT', 'CR_ORG_MIN_LMT', 'CR_CRT_USE_LMT', 'CR_AVG_6MTH_BAL', 'QR_LORG_CNT', 'QR_ORG_CNT', 'QR_CNT', 'QR_CONTRACT_AMT', 'QR_ORG_MAX_LMT', 'QR_ORG_MIN_LMT', 'QR_CRT_USE_LMT', 'QR_AVG_6MTH_BAL', 'LN_LORG_CNT', 'LN_ORG_CNT', 'LN_CNT', 'LN_CONTRACT_AMT', 'LN_CRT_BAL', 'LN_AVG_6MTH_BAL', 'LN_AQRY_ORG_CNT1', 'CR_AQRY_ORG_CNT1', 'LN_AQRY_CNT1', 'CR_AQRY_CNT1', 'SELF_QRY_CNT1', 'POST_QRY_CNT24', 'GU_QRY_CNT24', 'SM_QRY_CNT24']
    df=pd.DataFrame(columns=summary)
    da={}
    #==============================================================================
    # 1.添加报告编号
    #==============================================================================
    A=data.get('ReportMessage').get('Header').get('MessageHeader')
    da.update({'REPORT_NUMBER':A['ReportSN']})
    #==============================================================================
    # 2. 添加信用提示
    #==============================================================================
    A=data.get('ReportMessage').get('InfoSummary').get('CreditCue').get('CreditSummaryCue')
    da.update({'HOUSE_LOAN_CNT':A['PerHouseLoanCount'],'OTHERLOAN_COUNT':A['OtherLoanCount'],'FST_LOAN_MTH':A['FirstLoanOpenMonth'].replace('.','-') if A['FirstLoanOpenMonth'] else None,'CRD_CNT':A['LoancardCount'],'FST_CRD_MTH':A['FirstLoancardOpenMonth'].replace('.','-') if A['FirstLoancardOpenMonth'] else None,'QCRD_CNT':A['StandardLoancardCount'],'FST_QCRD_MTH':A['FirstStandardLoancardOpenMonth'].replace('.','-') if A['FirstStandardLoancardOpenMonth'] else None,'ANNOUNCE_CNT':A['AnnounceCount'],'DISSENT_CNT':A['DissentCount'],'CHOUSE_LOAN_CNT':A['PerBusinessHouseLoanCount']})
    #==============================================================================
    # 3. 添加逾期信息汇总
    #==============================================================================
    A=data.get('ReportMessage').get('InfoSummary').get('OverdueAndFellback')
    if A:
        B=A.get('OverdueSummary')
        if B:
            C=B.get('LoanSum')
            if C:
                da.update({'LN_DUE_CNT':C['Count'],'LN_DUE_MTHS':C['Months'],'LN_DUE_MAX_AMT':C['HighestOverdueAmountPerMon'],'LN_DUE_MAX_MTHS':C['MaxDuration']})
            C=B.get('LoancardSum')
            if C:
                da.update({'CR_DUE_CNT':C['Count'],'CR_DUE_MTHS':C['Months'],'CR_DUE_MAX_AMT':C['HighestOverdueAmountPerMon'],'CR_DUE_MAX_MTHS':C['MaxDuration']})
            C=B.get('StandardLoancardSum')
            if C:
                da.update({'QR_DUE_CNT':C['Count'],'QR_DUE_MTHS':C['Months'],'QR_DUE_MAX_AMT':C['HighestOverdueAmountPerMon'],'QR_DUE_MAX_MTHS':C['MaxDuration']})
        B=A.get('FellbackSummary')
        if B:
            C=B.get('AssetDispositionSum')
            if C:
                da.update({'AS_DISPOSAL_AMT':C['Balance'],'AS_DISPOSAL_CNT':C['Count']})
            C=B.get('AssureerRepaySum')
            if C:
                da.update({'GU_DISPOSAL_AMT':C['Balance'],'GU_DISPOSAL_CNT':C['Count']})
            C=B.get('FellbackDebtSum')
            if C:
                da.update({'CH_DISPOSAL_AMT':C['Balance'],'CH_DISPOSAL_CNT':C['Count']})
    #==============================================================================
    # 4. 授信及负债信息概要
    #==============================================================================
    A=data.get('ReportMessage').get('InfoSummary').get('ShareAndDebt')
    if A:
        B=A.get('UndestoryLoancard')
        if B:
            da.update({'CR_LORG_CNT':B['FinanceCorpCount'],'CR_ORG_CNT':B['FinanceOrgCount'],'CR_CNT':B['AccountCount'],'CR_CONTRACT_AMT':B['CreditLimit'],'CR_ORG_MAX_LMT':B['MaxCreditLimitPerOrg'],'CR_ORG_MIN_LMT':B['MinCreditLimitPerOrg'],'CR_CRT_USE_LMT':B['UsedCreditLimit'],'CR_AVG_6MTH_BAL':B['Latest6MonthUsedAvgAmount']})
        B=A.get('UndestoryStandardLoancard')
        if B:
            da.update({'QR_LORG_CNT':B['FinanceCorpCount'],'QR_ORG_CNT':B['FinanceOrgCount'],'QR_CNT':B['AccountCount'],'QR_CONTRACT_AMT':B['CreditLimit'],'QR_ORG_MAX_LMT':B['MaxCreditLimitPerOrg'],'QR_ORG_MIN_LMT':B['MinCreditLimitPerOrg'],'QR_CRT_USE_LMT':B['UsedCreditLimit'],'QR_AVG_6MTH_BAL':B['Latest6MonthUsedAvgAmount']})
        B=A.get('UnpaidLoan')
        if B:
            da.update({'LN_LORG_CNT':B['FinanceCorpCount'],'LN_ORG_CNT':B['FinanceOrgCount'],'LN_CNT':B['AccountCount'],'LN_CONTRACT_AMT':B['CreditLimit'],'LN_CRT_BAL':B['Balance'],'LN_AVG_6MTH_BAL':B['Latest6MonthUsedAvgAmount']})
    
    #==============================================================================
    # 5. 查询记录汇总
    #==============================================================================
    A=data.get('ReportMessage').get('QueryRecord').get('RecordSummary')
    B=A.get('LatestMonthQueryorgSum')   
    if B:
        da.update({'LN_AQRY_ORG_CNT1':B[0]['Sum']})
        da.update({'CR_AQRY_ORG_CNT1':B[1]['Sum']})
    B=A.get('LatestMonthQueryrecordSum')   
    if B:
        da.update({'LN_AQRY_CNT1':B[0]['Sum']})
        da.update({'CR_AQRY_CNT1':B[1]['Sum']})
        da.update({'SELF_QRY_CNT1':B[2]['Sum']})
    B=A.get('TwoyearQueryrecordSum')   
    if B:
        da.update({'POST_QRY_CNT24':B[0]['Sum']})
        da.update({'GU_QRY_CNT24':B[1]['Sum']})
        da.update({'SM_QRY_CNT24':B[2]['Sum']})    
    #==============================================================================
    # 转换数据格式
    #==============================================================================
    asstr=['REPORT_NUMBER','FST_LOAN_MTH','FST_CRD_MTH','FST_QCRD_MTH']
    asflt=['HOUSE_LOAN_CNT','OTHERLOAN_COUNT','CRD_CNT','QCRD_CNT','ANNOUNCE_CNT','DISSENT_CNT','CHOUSE_LOAN_CNT',
           'LN_DUE_CNT','LN_DUE_MTHS', 'LN_DUE_MAX_MTHS','CR_DUE_CNT', 'CR_DUE_MTHS', 'CR_DUE_MAX_MTHS', 'QR_DUE_CNT',
           'QR_DUE_MTHS','QR_DUE_MAX_MTHS','AS_DISPOSAL_CNT','GU_DISPOSAL_CNT','CH_DISPOSAL_CNT','CR_LORG_CNT', 
           'CR_ORG_CNT', 'CR_CNT', 'QR_LORG_CNT', 'QR_ORG_CNT', 'QR_CNT', 'LN_LORG_CNT', 'LN_ORG_CNT', 'LN_CNT', 
           'LN_AQRY_ORG_CNT1', 'CR_AQRY_ORG_CNT1', 'LN_AQRY_CNT1', 'CR_AQRY_CNT1', 'SELF_QRY_CNT1', 'POST_QRY_CNT24', 'GU_QRY_CNT24', 'SM_QRY_CNT24',
           'AS_DISPOSAL_AMT','CH_DISPOSAL_AMT','CR_AVG_6MTH_BAL', 'CR_CONTRACT_AMT', 'CR_CRT_USE_LMT', 'CR_DUE_MAX_AMT', 
           'CR_ORG_MAX_LMT', 'CR_ORG_MIN_LMT', 'GU_DISPOSAL_AMT', 'LN_AVG_6MTH_BAL', 'LN_CONTRACT_AMT', 'LN_CRT_BAL',
           'LN_DUE_MAX_AMT', 'QR_AVG_6MTH_BAL', 'QR_CONTRACT_AMT', 'QR_CRT_USE_LMT', 'QR_DUE_MAX_AMT', 'QR_ORG_MAX_LMT', 'QR_ORG_MIN_LMT']
    for a in asflt:
        if not da.get(a) or da.get(a)=='':
            da.update({a:np.nan})
        else:
            da.update({a:str(da[a]).replace(',','').replace('，','')})
    for a in asstr:
        if not da.get(a) or da.get(a)=='':
            da.update({a:None})
    
    df=df.append(da,ignore_index=True)
    for s in asstr:
        df[s]=df[s].astype('str')
    for f in asflt:
        try:
            df[f]=df[f].astype('float')
        except:
            df[f]=np.nan
        
    return df

#==========================================================================
#说明：卡明细信息解析至数据框，输入内容为字典，输出为数据框
def CardinfoToDf(PbocDict):
    js=dict_str(PbocDict)
    #卡明细初始化(包括贷记卡和准贷记卡)
    card_info_names_t=['REPORT_NUMBER','ORG_NO','BIZ_NO','CURRENCY_TYPE','OPEN_DT','CREDIT_LMT','ASSU_METHOD','ACCT_STAT',
                       'ORG_TYPE','CREDIT_TYPE','STAT_EXPIRE_DT','SHARE_LMT','USED_LMT','AVG_6MTH_BAL','MAX_USE_LMT',
                       'BILL_DT','DESERVED_PMT','ACT_PMT','LST_PMT_DTE','CRT_DUE_MTHS','CRT_DUE_AMT','M6ABV_AMT','LST_MONTH','PMT_STATUS']
    card_info_t=pd.DataFrame([],columns=card_info_names_t)
    
    try:
        #1.贷记卡
        card_list=js.get('ReportMessage').get('CreditDetail').get('Loancard')
        card_info=pd.DataFrame()
        cnt=0
        for k in range(len(card_list) if type(card_list)==list else 1):
            cnt=cnt+1
            try:
                card_dict_temp=card_list[k]
            except:
                card_dict_temp=card_list
            card_df_temp=DictToDataframe(card_dict_temp)
            card_df_temp['Account']='X_LOANCARD_'+str(cnt)
            card_info=card_info.append(card_df_temp,ignore_index=True)
        
        card_info['ReportSN']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
        card_info=card_info.rename(columns={'ReportSN':'REPORT_NUMBER','FinanceOrg':'ORG_NO','Account':'BIZ_NO','Currency':'CURRENCY_TYPE',
                                            'OpenDate':'OPEN_DT','CreditLimitAmount':'CREDIT_LMT','GuaranteeType':'ASSU_METHOD',
                                            'State':'ACCT_STAT','FinanceType':'ORG_TYPE','StateEndDate':'STAT_EXPIRE_DT','ShareCreditLimitAmount':'SHARE_LMT',
                                            'UsedCreditLimitAmount':'USED_LMT','Latest6MonthUsedAvgAmount':'AVG_6MTH_BAL',
                                            'UsedHighestAmount':'MAX_USE_LMT','ScheduledPaymentDate':'BILL_DT','ScheduledPaymentAmount':'DESERVED_PMT',
                                            'ActualPaymentAmount':'ACT_PMT','RecentPayDate':'LST_PMT_DTE','CurrOverdueCyc':'CRT_DUE_MTHS',
                                            'CurrOverdueAmount':'CRT_DUE_AMT','EndMonth':'LST_MONTH','Latest24State':'PMT_STATUS'})    
        card_info['CREDIT_TYPE']='贷记卡'
        card_info_names_obj=list(set(card_info_names_t).intersection(set(card_info.columns)))
        card_info=card_info[card_info_names_obj]
        
        #2.准贷记卡
        qcard_list=js.get('ReportMessage').get('CreditDetail').get('StandardLoancard')
        qcard_info=pd.DataFrame()
        cnt=0
        for k in range(len(qcard_list) if type(qcard_list)==list else 1):
            cnt=cnt+1
            try:
                qcard_dict_temp=qcard_list[k]
            except:
                qcard_dict_temp=qcard_list
            qcard_df_temp=DictToDataframe(qcard_dict_temp)
            qcard_df_temp['Account']='X_ST_LOANCARD_'+str(cnt)
            qcard_info=qcard_info.append(qcard_df_temp,ignore_index=True)
        
        qcard_info['ReportSN']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
        qcard_info=qcard_info.rename(columns={'ReportSN':'REPORT_NUMBER','FinanceOrg':'ORG_NO','Account':'BIZ_NO','Currency':'CURRENCY_TYPE',
                                            'OpenDate':'OPEN_DT','CreditLimitAmount':'CREDIT_LMT','GuaranteeType':'ASSU_METHOD',
                                            'State':'ACCT_STAT','FinanceType':'ORG_TYPE','StateEndDate':'STAT_EXPIRE_DT','ShareCreditLimitAmount':'SHARE_LMT',
                                            'UsedCreditLimitAmount':'USED_LMT','Latest6MonthUsedAvgAmount':'AVG_6MTH_BAL',
                                            'UsedHighestAmount':'MAX_USE_LMT','ScheduledPaymentDate':'BILL_DT',
                                            'ActualPaymentAmount':'ACT_PMT','RecentPayDate':'LST_PMT_DTE','OverdueOver180Amount':'M6ABV_AMT',
                                            'EndMonth':'LST_MONTH','Latest24State':'PMT_STATUS'})    
        qcard_info['CREDIT_TYPE']='准贷记卡'
        qcard_info_names_obj=list(set(card_info_names_t).intersection(set(qcard_info.columns)))
        qcard_info=qcard_info[qcard_info_names_obj]
        
        #3.合并数据
        card_info_t=pd.concat([card_info_t,card_info,qcard_info],axis=0,ignore_index=True)
        
        #4.数据清洗
        #4.1日期处理
        card_info_t['OPEN_DT']=card_info_t['OPEN_DT'].apply(lambda x:StrToDate3(x))
        card_info_t['STAT_EXPIRE_DT']=card_info_t['STAT_EXPIRE_DT'].apply(lambda x:StrToDate3(x))
        card_info_t['BILL_DT']=card_info_t['BILL_DT'].apply(lambda x:StrToDate1(x))
        card_info_t['LST_PMT_DTE']=card_info_t['LST_PMT_DTE'].apply(lambda x:StrToDate1(x))
        card_info_t['LST_MONTH']=card_info_t['LST_MONTH'].apply(lambda x:StrToDate2(x))
        #4.2金额处理
        amt_list_1=['CREDIT_LMT','SHARE_LMT','USED_LMT','AVG_6MTH_BAL','MAX_USE_LMT','DESERVED_PMT','ACT_PMT','CRT_DUE_AMT','M6ABV_AMT']
        amt_list_2=['CRT_DUE_MTHS']
        for i in amt_list_1:
            card_info_t[i]=card_info_t[i].apply(lambda x:StrToFloat(x))
        for i in amt_list_2:
            card_info_t[i]=card_info_t[i].apply(lambda x:StrToInt(x))
        #4.3文本处理
        text_list=list(set(card_info_names_t).difference(set(amt_list_1+amt_list_2)))
        for i in text_list:
            card_info_t[i]=card_info_t[i].apply(lambda x:StrOutlierModify(x))
            
    except:
        pass

    return(card_info_t)


#==========================================================================
#说明：贷款明细信息解析至数据框，输入内容为字典，输出为数据框
def LoaninfoToDf(PbocDict):
    js=dict_str(PbocDict)
    #贷款明细初始化
    loan_info_names_t=['REPORT_NUMBER','LOAN_ORG','BIZ_NO','LOAN_TYPE','CURRENCY_TYPE','ISSUE_DT','MATURE_DT','CONTRACT_AMT',
                       'ASSU_METHOD','PAY_FREQ','PMT_TERM','ACCT_STAT','ORG_TYPE','STAT_EXPIRE_DT','FIVE_LVL_CLASS','PRINCIPAL_BAL',
                       'UNPAY_TERM','DESERVED_PMT','PMT_DAY','ACT_PMT','LST_PMT_DTE','CRT_DUE_MTHS','CRT_DUE_AMT','M2_AMT',
                       'M3_AMT','M4M6_AMT','M6ABV_AMT','LST_MONTH','PMT_STATUS']
    loan_info_t=pd.DataFrame([],columns=loan_info_names_t)
    
    try:
        #1.贷款
        loan_list=js.get('ReportMessage').get('CreditDetail').get('Loan')
        loan_info=pd.DataFrame()
        cnt=0
        for k in range(len(loan_list) if type(loan_list)==list else 1):
            cnt=cnt+1
            try:
                loan_dict_temp=loan_list[k]
            except:
                loan_dict_temp=loan_list
            if 'SpecialTrade' in loan_dict_temp.keys():
                del loan_dict_temp['SpecialTrade']
            else:
                pass
            loan_df_temp=DictToDataframe(loan_dict_temp)
            loan_df_temp['Account']='X_LOAN_'+str(cnt)
            loan_info=loan_info.append(loan_df_temp,ignore_index=True)
        
        loan_info['ReportSN']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
        loan_info=loan_info.rename(columns={'ReportSN':'REPORT_NUMBER','FinanceOrg':'LOAN_ORG','Account':'BIZ_NO','Type':'LOAN_TYPE','Currency':'CURRENCY_TYPE',
                                            'OpenDate':'ISSUE_DT','EndDate':'MATURE_DT','CreditLimitAmount':'CONTRACT_AMT','GuaranteeType':'ASSU_METHOD',
                                            'PaymentRating':'PAY_FREQ','PaymentCyc':'PMT_TERM','State':'ACCT_STAT','FinanceType':'ORG_TYPE',
                                            'StateEndDate':'STAT_EXPIRE_DT','Class5State':'FIVE_LVL_CLASS','Balance':'PRINCIPAL_BAL','RemainPaymentCyc':'UNPAY_TERM',
                                            'ScheduledPaymentAmount':'DESERVED_PMT','ScheduledPaymentDate':'PMT_DAY','ActualPaymentAmount':'ACT_PMT',
                                            'RecentPayDate':'LST_PMT_DTE','CurrOverdueCyc':'CRT_DUE_MTHS','CurrOverdueAmount':'CRT_DUE_AMT','Overdue31To60Amount':'M2_AMT',
                                            'Overdue61To90Amount':'M3_AMT','Overdue91To180Amount':'M4M6_AMT','OverdueOver180Amount':'M6ABV_AMT',
                                            'EndMonth':'LST_MONTH','Latest24State':'PMT_STATUS'})    
        
        loan_info_names_obj=list(set(loan_info_names_t).intersection(set(loan_info.columns)))
        loan_info=loan_info[loan_info_names_obj]
        
        #2.合并数据
        loan_info_t=pd.concat([loan_info_t,loan_info],axis=0,ignore_index=True)
        
        #4.数据清洗
        #4.1日期处理
        loan_info_t['ISSUE_DT']=loan_info_t['ISSUE_DT'].apply(lambda x:StrToDate3(x))
        loan_info_t['MATURE_DT']=loan_info_t['MATURE_DT'].apply(lambda x:StrToDate3(x))
        loan_info_t['STAT_EXPIRE_DT']=loan_info_t['STAT_EXPIRE_DT'].apply(lambda x:StrToDate3(x))
        loan_info_t['PMT_DAY']=loan_info_t['PMT_DAY'].apply(lambda x:StrToDate1(x))
        loan_info_t['LST_PMT_DTE']=loan_info_t['LST_PMT_DTE'].apply(lambda x:StrToDate1(x))
        loan_info_t['LST_MONTH']=loan_info_t['LST_MONTH'].apply(lambda x:StrToDate2(x))
        #4.2金额处理
        amt_list_1=['CONTRACT_AMT','PRINCIPAL_BAL','DESERVED_PMT','ACT_PMT','CRT_DUE_AMT','M2_AMT','M3_AMT','M4M6_AMT','M6ABV_AMT']
        amt_list_2=['UNPAY_TERM','CRT_DUE_MTHS']
        for i in amt_list_1:
            loan_info_t[i]=loan_info_t[i].apply(lambda x:StrToFloat(x))
        for i in amt_list_2:
            loan_info_t[i]=loan_info_t[i].apply(lambda x:StrToInt(x))
        #4.3文本处理
        text_list=list(set(loan_info_names_t).difference(set(amt_list_1+amt_list_2)))
        for i in text_list:
            loan_info_t[i]=loan_info_t[i].apply(lambda x:StrOutlierModify(x))
    
    except:
        pass
    
    return(loan_info_t)

#==========================================================================
#说明：查询明细信息解析至数据框，输入内容为字典，输出为数据框
def DetailqryToDf(PbocDict):
    js=dict_str(PbocDict)
    detail=['REPORT_NUMBER','QRY_OPER_ID', 'QRY_DTE', 'QRY_RSN','SEQ_ID','QRY_TYPE']    
    df=pd.DataFrame(columns=detail)
    da={}
	
    #1、信贷审批查询

    t=js.get('ReportMessage').get('QueryRecord').get('RecordInfo')[0]
    
    ##多条记录
    if 'RecordDetail' in t.keys() and type(t['RecordDetail'])==list:
        tt=t['RecordDetail']   
        query=pd.DataFrame(tt)
        query.columns = ['QRY_OPER_ID','QRY_DTE','QRY_RSN']
        query['REPORT_NUMBER']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
        query['SEQ_ID']=[i+1 for i in range(len(query))]
        query['QRY_TYPE']=t['QueryReqFormat']
        query1=pd.DataFrame(query,columns=detail)
    
    ##一条记录    
    elif 'RecordDetail' in t.keys() and type(t['RecordDetail'])==dict:
        A=js.get('ReportMessage').get('Header').get('MessageHeader')
        tt=t['RecordDetail'] 
        da.update({'REPORT_NUMBER':A['ReportSN']})
        da.update({'QRY_OPER_ID':tt['Querier'],'QRY_DTE':tt['QueryDate'],'QRY_RSN':tt['QueryReason'],'QRY_TYPE':t['QueryReqFormat']})
        query1=df.append(da,ignore_index=True)
        query1['SEQ_ID']=[i+1 for i in range(len(query1))]
        
    ##空值
    else:
        query1=df  

    #2、其他自然人查询

    t=js.get('ReportMessage').get('QueryRecord').get('RecordInfo')[1]
    
    
    ##多条记录
    if 'RecordDetail' in t.keys() and type(t['RecordDetail'])==list:
        tt=t['RecordDetail']   
        query=pd.DataFrame(tt)
        query.columns = ['QRY_OPER_ID','QRY_DTE','QRY_RSN']
        query['REPORT_NUMBER']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
        query['SEQ_ID']=[i+1 for i in range(len(query))]
        query['QRY_TYPE']=t['QueryReqFormat']
        query2=pd.DataFrame(query,columns=detail)
    
    ##一条记录    
    elif 'RecordDetail' in t.keys() and type(t['RecordDetail'])==dict:
        A=js.get('ReportMessage').get('Header').get('MessageHeader')
        tt=t['RecordDetail'] 
        da.update({'REPORT_NUMBER':A['ReportSN']})
        da.update({'QRY_OPER_ID':tt['Querier'],'QRY_DTE':tt['QueryDate'],'QRY_RSN':tt['QueryReason'],'QRY_TYPE':t['QueryReqFormat']})
        query2=df.append(da,ignore_index=True)
        query2['SEQ_ID']=[i+1 for i in range(len(query2))]

    ##空值
    else:
        query2=df  

    
    #3、本人查询
    t=js.get('ReportMessage').get('QueryRecord').get('RecordInfo')[2]
    
    
    ##多条记录
    if 'RecordDetail' in t.keys() and type(t['RecordDetail'])==list:
        tt=t['RecordDetail']   
        query=pd.DataFrame(tt)
        query.columns = ['QRY_OPER_ID','QRY_DTE','QRY_RSN']
        query['REPORT_NUMBER']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
        query['SEQ_ID']=[i+1 for i in range(len(query))]
        query['QRY_TYPE']=t['QueryReqFormat']
        query3=pd.DataFrame(query,columns=detail)
    
    ##一条记录    
    elif 'RecordDetail' in t.keys() and type(t['RecordDetail'])==dict:
        A=js.get('ReportMessage').get('Header').get('MessageHeader')
        tt=t['RecordDetail'] 
        da.update({'REPORT_NUMBER':A['ReportSN']})
        da.update({'QRY_OPER_ID':tt['Querier'],'QRY_DTE':tt['QueryDate'],'QRY_RSN':tt['QueryReason'],'QRY_TYPE':t['QueryReqFormat']})
        query3=df.append(da,ignore_index=True)
        query3['SEQ_ID']=[i+1 for i in range(len(query3))]

    ##空值
    else:
        query3=df  
    
    ###数据合并
    query4=query1.append(query2).append(query3)
    
    ###修改日期格式
    query4['QRY_DTE']=[i.replace('.','-') for i  in query4['QRY_DTE']]

    return (query4) 

#==========================================================================
#说明：住房公积金信息解析至数据框，输入内容为字典，输出为数据框
def AccfundToDf(PbocDict):
    js=dict_str(PbocDict)
 
    public=['REPORT_NUMBER','AREA', 'REGISTER_DATE', 'FIRST_MONTH','TO_MONTH','STATE','PAY','OWN_PERCENT','COM_PERCENT','ORGAN_NAME','GET_TIME']    
    df=pd.DataFrame(columns=public)
   
    da={}
    t1=js.get('ReportMessage')
    t2=js.get('ReportMessage').get('PublicInfo').get('AccFund')
    
    
    if t2 in ['',None]:
        accfundinfo=df
    
    elif t2!='':
        if type(t2)==dict:
            if 'PublicInfo' in t1.keys():
                A=js.get('ReportMessage').get('Header').get('MessageHeader')
                da.update({'REPORT_NUMBER':A['ReportSN']})
                A=js.get('ReportMessage').get('PublicInfo').get('AccFund')
                da.update({'AREA':A['Area'],'REGISTER_DATE':A['RegisterDate'],'FIRST_MONTH':A['FirstMonth'],'TO_MONTH':A['ToMonth'],'STATE':A['State'],'PAY':A['Pay'],'OWN_PERCENT':A['OwnPercent'],'COM_PERCENT':A['ComPercent'],'ORGAN_NAME':A['Organname'],'GET_TIME':A['GetTime']})
                accfundinfo=df.append(da,ignore_index=True)
            else:
                accfundinfo=df 
            
        elif type(t2)==list:
            a=pd.DataFrame(t2)
            a.columns = ['AREA','COM_PERCENT','FIRST_MONTH','GET_TIME','ORGAN_NAME','OWN_PERCENT','PAY','REGISTER_DATE','STATE','TO_MONTH']
            a['REPORT_NUMBER']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
            accfundinfo=pd.DataFrame(a,columns=public)
			
	###修改格式
    list_1=['REGISTER_DATE','GET_TIME']
    for i in list_1:
        try:
            accfundinfo[i]=[i.replace('.','-') for i  in accfundinfo[i]]
        except:
            pass
        
    accfundinfo['PAY']=accfundinfo['PAY'].apply(lambda x:StrToFloat(x))
	
    return (accfundinfo)


#==========================================================================
#说明：强制执行信息解析至数据框，输入内容为字典，输出为数据框

def ForceinfoToDf(PbocDict):
    js=dict_str(PbocDict)
 
    force=['REPORT_NUMBER','COURT','CASE_REASON','REGISTER_DATE','CLOSED_TYPE','CASE_STATE','CLOSED_DATE','ENFORCE_OBJECT','ENFORCE_MONEY','ALREADY_OBJECT','ALREADY_MONEY']    
    df=pd.DataFrame(columns=force)
   
    da={}
    t1=js.get('ReportMessage')
    t2=js.get('ReportMessage').get('PublicInfo').get('ForceExecution')
    
    if t2 in ['',None]:
        forceinfo=df
    elif t2!='':     
        if type(t2)==dict:
            if 'PublicInfo' in t1.keys():
                A=js.get('ReportMessage').get('Header').get('MessageHeader')
                da.update({'REPORT_NUMBER':A['ReportSN']})
                A=js.get('ReportMessage').get('PublicInfo').get('ForceExecution')
                da.update({'COURT':A['Court'],'CASE_REASON':A['CaseReason'],'REGISTER_DATE':A['RegisterDate'],'CLOSED_TYPE':A['ClosedType'],'CASE_STATE':A['CaseState'],'CLOSED_DATE':A['ClosedDate'],'ENFORCE_OBJECT':A['EnforceObject'],'ENFORCE_MONEY':A['EnforceObjectMoney'],'ALREADY_OBJECT':A['AlreadyEnforceObject'],'ALREADY_MONEY':A['AlreadyEnforceObjectMoney']})
                forceinfo=df.append(da,ignore_index=True)
            else:
                forceinfo=df 
             
        elif type(t2)==list:
            a=pd.DataFrame(t2)
            a.columns = ['ALREADY_OBJECT','ALREADY_MONEY','CASE_REASON','CASE_STATE','CLOSED_DATE','CLOSED_TYPE','Court','ENFORCE_OBJECT','ENFORCE_MONEY','REGISTER_DATE']
            a['REPORT_NUMBER']=js.get('ReportMessage').get('Header').get('MessageHeader').get('ReportSN') 
            forceinfo=pd.DataFrame(a,columns=force)


               
    ###修改格式
    list=['REGISTER_DATE','CLOSED_DATE']
    for i in list:
        try:
            forceinfo[i]=[i.replace('.','-') for i  in forceinfo[i]]
        except:
            pass
        
    forceinfo['ENFORCE_MONEY']=forceinfo['ENFORCE_MONEY'].apply(lambda x:StrToFloat(x))
    forceinfo['ALREADY_MONEY']=forceinfo['ALREADY_MONEY'].apply(lambda x:StrToFloat(x))

    return (forceinfo)

#==========================================================================
#案例测试
#import os
#import json
#
#os.chdir('C:/君正小贷/工作项目/2017.09.30_人行数据集市')
#f = open('周倍倍_解析1.json', encoding='utf8')
#js=json.load(f)
#
#personal=PersonalToDf(pboc_dict)
#summary=SummaryToDf(pboc_dict)
#card_info=CardinfoToDf(pboc_dict)
#loan_info=LoaninfoToDf(pboc_dict)
#detail_qry=DetailqryToDf(pboc_dict)
#acc_fund=AccfundToDf(pboc_dict)

