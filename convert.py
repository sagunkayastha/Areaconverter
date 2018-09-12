# -*- coding: utf-8 -*-

#import libraries
import pandas as pd
import numpy as np

files = pd.ExcelFile('okay.xlsx')           
sheet1= files.parse(files.sheet_names[0])
sheet2= files.parse(files.sheet_names[1])

#Data selection
rowstart=[7,7]   #for both sheets
rowsend=[255,255] 
columnstart='Unnamed: 2'
columnend='Unnamed: 5'

df= sheet2.ix[:,columnstart:columnend].iloc[rowstart[0]:rowsend[0]].reset_index(drop=True)
df2= sheet1.ix[:,columnstart:columnend].iloc[rowstart[0]:].reset_index(drop=True)
df.columns=df2.columns=['Area1','RAPD1','Area2','RAPD2']

#Dataset Cleaning
df=df.reset_index(drop=True)            #Depends on data in the spreadsheet
df['Area1'][df['Area1'].isna()]=''
df['Area2'][df['Area2'].isna()]=''
df['RAPD1'][df['RAPD1'].isna()]=''
df['RAPD2'][df['RAPD2'].isna()]=''
#
df2['Area1'][df2['Area1'].isna()]=''
df2['Area2'][df2['Area2'].isna()]=''
df2['RAPD1'][df2['RAPD1'].isna()]=''
df2['RAPD2'][df2['RAPD2'].isna()]=''

def convArea2R(value):  # Converts Square meters to Ropani-Anna-Paisa-Dam
    if value =='':
        return('')
    else:
        rop = value/508.996
        anna = (rop - int(rop))*16
        paisa = (anna-int(anna))*4
        dam = (paisa -int(paisa))*4 
        return(str(int(rop))+'-'+str(int(anna))+'-'+str(int(paisa))+'-'+str(round(dam)))

def convRAPD2A(value):
    if value =='':   # Converts Ropani-Anna-Paisa-Dam to  Squarem 
        return ('')  #Depends on 
    else:
        v=value.split('-')
        cv=508.996
        r,a,p,d=int(v[0]),int(v[1]),int(v[2]),float(v[3])
        return(r*cv + a *(cv/16) + p *(cv/16/4) + d *(cv/16/16))

       
#Function for sheet1
df['RAPD2']=df['Area2'].apply(convArea2R)
df['Area1']=df['RAPD1'].apply(convRAPD2A)

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'sheet1')

#Function for sheet1
df2['RAPD2']=df2['Area2'].apply(convArea2R)
df2['Area1']=df2['RAPD1'].apply(convRAPD2A)



df2.to_excel(writer,'sheet2')
writer.save()