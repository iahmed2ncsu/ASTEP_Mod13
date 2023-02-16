# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 19:01:04 2022

@author: Ishtiak
"""
#updates from previous version
#1. I
# description	: one script for all the scenarios created by Mehedi for Task 6. 
# update(s) from previous version: added options for users to choose either defauly % increase/shift/reduction or their own input
# version		:1.0
# python_version: 3.8
# status		: in progress

import streamlit as st
from PIL import Image
import os
import pandas as pd
pd.options.mode.chained_assignment = None  #removes a warning message
import csv
import numpy as np
from numpy import genfromtxt
import time

version = 4.2
#set page config
st.set_page_config(page_title=None, page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="auto", menu_items=None)

#define tab names and numbers
tab1, tab2, tab3, tab4 = st.tabs(["About", "Module 1 Input","Module 2 & 3 Inputs", "Run Model"])

# %% dataframe conversion function
#this function converts the output data to utf-8 encoded data. It is important to download the outputs
@st.cache
def convert_df(df):
    
   return df.to_csv().encode('utf-8')

# %% Read hard-coded files
#working directory. Change if necessary
direct = 'G:\\.shortcut-targets-by-id\\1m_vWVSXCB3I9mQi1vuOqJsIjp9HUbG1y\\Rail Decarbonization\\Task 6 Demand Estimation\\sample_code\\streamlit version\\Hardcoded Input\\'
#Read hard-coded pdf files
with open('dummy.pdf', "rb") as pdf_file:
    PDFbyte = pdf_file.read()
image1 = Image.open(f"{direct}sample output.png")
image2 = Image.open(f"{direct}faf zones.png")


temoa_region =  pd.read_csv(f'{direct}temoa_faf.csv')   

# %% description of scenarios
descrip = """1. Population shift
Recent migration trends in the U.S. have reported that the metropolitan regions of the sunbelt states are experiencing higher net migration gains. This scenario assumes that the future population distribution will follow this trend. The user can specify the proportion of population that will shift to the metropolitan regions of the 18 sunbelt states. The default assumption is a 10% population shift towards sunbelt states. 

2. Reduced fossil fuel
This scenario focuses on a future where U.S. energy dependence will be diverted from fossil fuels toward renewable energy systems. More dependence on renewable energy will reduce the demand for fossil fuels and reduce the total tons transported by rail. The sub-scenarios under this scenario will be developed based on Temoa outputs: (a) business as usual - where no constraints are placed on the emissions limits; (b) a CO2 emissions reduction target of 50% of 2020 emissions is to be achieved by 2050; (c) CO2 emissions are constrained to be reduced to 0 by 2050.

3. Agricultural shift 
This scenario addresses the impact of climate change on agricultural production, which may result in a northward shift of crop and livestock production. Based on past studies, the default assumption for this scenario includes a 10% shift in agricultural production from southern states (Texas, Oklahoma, Kansas) of the Great Plains to the northern states (Nebraska, South Dakota, North Dakota) of the Great Plains by 2050. 

4. Decrease in agricultural production 
This scenario addresses the impact of climate change on agricultural production, which may result in a decrease in agricultural production. Based on past studies, the default assumption for this scenario includes a 10% reduction in the amount of agricultural commodities coming from the southern Great Plains by 2050, assuming that the shortage will be covered with imported goods. """  
   
# %% About page
page_title = "A-STEP: Achieving Sustainable Train Energy Pathways"
body = "A-STEP: Achieving Sustainable Train Energy Pathways"
subhead = f"Module 1-3: Decarbonization Pathway-Freight Demand-Economic Scenario (v{version})"

with tab1:
    #st.set_page_config(page_title=page_title)
    st.header(body)
    st.subheader(subhead)

    #add Description pdf
    st.download_button(
       label = "📕 Download User Guide",
       data = PDFbyte,
       file_name = "Demand Model Documentation.pdf",
       mime='application/octet-stream',
       key='Description'
    )
    c1, c2 = st.columns(2)
    with c1:
        st.write('**🗺️ FAF Zone MAP**')
        st.image(image2, caption='FAF Zones', use_column_width=True)
    with c2:
        st.write('📈 Sample Output')
        st.image(image1, caption='Sample output: Net Tons from and to different FAF Zones')


# %%Module 1
body2 = "Module 1 : Decarbonization Pathways"
with tab2:    
    st.header(body2)
    deco2 = st.radio(
    "Choose a decarbonization pathway",
    ('Reference/business as usual', '50% CO2 reduction by 2050', '100% CO2 reduction by 2050'))
# %%Module 2 and 3
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        
        st.header("Module 2: Economic Scenarios")
        
        # input parameters by user
        #choose a scenario for economic growth
        econ_scn = st.selectbox(
            label='Economic scenario', options=('Low (pessimistic)', 'High (optimistic)', 'Baseline (business as usual)'), key=2, 
            format_func=lambda x: str(x) + " economic growth", help = "For more details, see https://faf.ornl.gov/faf5/Documentation.aspx")
        
        #choose a scenario for economic activity change
        scen = st.selectbox(
        label='Choose Change in Economic Activity', options=("Population Shift","Maritime Activity Reduction",
                                            "Agricultural Shift",
                                            "Agricultural Reduction"), key=4)
        with st.expander("See explanation"):
            st.write(descrip)
   
    with col2:
        st.header("Module 3: Freight Demand Scenarios")
        analy_yr = st.selectbox(
            label='Analysis Year', options=(2025, 2030,2035,2040,2045,2050), key=1)
        prcnt_choice = st.selectbox(label=f"Option for selecting proportion of {scen}", 
                                    options= ('Default (see table below)',
                                    'User-specified'))
        if prcnt_choice == 'Default (see table below)':
            
            prcnt_default = {2025: 0.018, 2030: 0.0357, 2035 : 0.0529, 2040 : 0.0695, 2045 : 0.0851, 2050 : 0.1}
            st.table(pd.DataFrame(prcnt_default, index = ['Proportion']))
            prcnt = prcnt_default[analy_yr]
            
        else:
            prcnt = st.slider(label = f"Proportion of {scen} (0 to 0.5)",min_value = 0.0, max_value = 0.5)
        
        #Reduced fossil fuel %
        prcnt_ffc = st.slider(label = "Proportion of coal reduction (0 to 0.999)",
                             min_value = 0.0, max_value = 0.999)
        prcnt_ffp = st.slider(label = "Proportion of petrolium reduction (0 to 0.999)",
                             min_value = 0.0, max_value = 0.999)
   
        if econ_scn == 'Baseline (business as usual)':
            ton_year = 'tons' + '_' + str(analy_yr)
        if econ_scn == 'Low (pessimistic)':
            ton_year = 'tons' + '_' + str(analy_yr) + '_' + str('low')
        if econ_scn == 'High (optimistic)':
            ton_year = 'tons' + '_' + str(analy_yr) + '_' + str('high')
           
        colnames=['dms_orig', 'dms_dest', 'cat_grp', 'trade_type', 'sctg2',ton_year,'cat_grp_mod']     
    
        
        faf_rail = pd.read_csv(f'{direct}FAF5.3_alltrades_byrail_7_Cat.csv',usecols=colnames)
        originrail = faf_rail['dms_orig'].unique().tolist() #all origin faf zones with rail mode
        originrail.sort()
        destrail = faf_rail['dms_dest'].unique().tolist() #all destination faf zones with rail mode
        destrail.sort()
        #sctgrail = faf_rail['sctg2'].unique().tolist() #all commodity types shipped by rail mode
        comm_cat = faf_rail['cat_grp'].unique().tolist()  #predefined categories of commodities;used in scen 1
        catrail = faf_rail['cat_grp'].unique().tolist() #all category types shipped by rail mode;used in scen 2,3 & 4
        agr_sctg = faf_rail[faf_rail['cat_grp']==1]['sctg2'].unique().tolist() #used in scen 3 & 4
        agr_sctg.sort() #sctg commodity types in category 1 (agricultural) #used in scen 3 & 4
     
        #multiply faf_rail ton_year column by 1-a, where a is the reduction in fossil fuel
        red_ff = np.where(faf_rail['cat_grp_mod'] == 3.1, (1-prcnt_ffc), 
                          np.where(faf_rail['cat_grp_mod'] == 3.2, (1-prcnt_ffp),1)
                          )
        faf_rail_red = pd.concat(
            [faf_rail[['dms_orig','dms_dest','cat_grp','trade_type','sctg2','cat_grp_mod']],
             faf_rail[ton_year].multiply(red_ff,axis=0)], axis=1
            )
    
        #faf zones corresponding to the sunbelt metropolitan areas
        #This input is only for pop shift
        sunbelt_metro = [11,50,41,42,61,62,63,64,65,81,122,123,124,131,132,201,202,221,222,223,280,371,372,373,350,321,401,402,451,
                         452,471,472,473,481,482,483,484,485,486,487,488,491] #used in scen 1
        nonsunbelt = list(set(destrail) - set(sunbelt_metro)) #non sunbelt zone numbers
    
        
        #the next four lines are only for Agricultural shift and reduction (sc = 3 & 4) except  2nd line is not used for sc = 4
        
        South_GP = [481,482,483,484,485,486,487,488,489,491,499,201,202,203,401,402,409] #Texas, Kansas, Oklahoma in great plain
        North_GP = [311,319,360,380] #Nebraska, South & North Dakota in great plain
        
        
        #required dataframe. becomes too clumsy if I define these inside the function
        faf_agri_nonimport = faf_rail_red[(faf_rail_red['cat_grp'] == 1) & (faf_rail_red['trade_type'] != 2)]
        faf_agri_import = faf_rail_red[(faf_rail_red['cat_grp'] == 1) & (faf_rail_red['trade_type'] == 2)] 
        
        #the following for loop is only for sc = 4
        Non_South_Orig = []
        for i in originrail:
            if i not in South_GP:
                if i not in Non_South_Orig:
                    Non_South_Orig.append(i)


   
# %% main function for population shift scenario
def demand_rearr(catg, a, year):  # sctg= commodity code, a = % increase in demand, year='tons_year'
    cat_flow =  faf_rail_red[faf_rail_red['cat_grp']== catg]
    existing_flow = cat_flow.pivot_table(values=year, index='dms_orig', columns= 'dms_dest',fill_value=0, aggfunc='sum')
    #index --> dest & column --> origin, the calling goes as column than row, so mat[i][j] is value in column i and row j. 
     
    #Dns = 0 #Estimated demand in non-sunbelt
    #Ds = 0 #Estimated demand in sunbelt
    df_sb = existing_flow.loc[:,sunbelt_metro] #subset dataframe for all destinations w/ sunbelt metro zones
    df_nsb = existing_flow.loc[:,nonsunbelt]
        
    Dns = df_nsb.sum().sum() #Estimated demand in non-sunbelt    
    Ds = df_sb.sum().sum() #Estimated demand in sunbelt
   # Ds_add = Ds*a #added demand to sunbelt states
    
    df_sb*= (1+a)
    df_nsb*= 1-(a*(Ds/Dns))
    df_final = pd.concat([df_sb, df_nsb], axis=1)
    return(df_final)

# %% main function for Maritime activity reduction
def reduceMari(catg,a, tonyear): 
    cat_flow =  faf_rail_red[faf_rail_red['cat_grp_mod']== catg]
    existing_flow = cat_flow.pivot_table(values=tonyear, index='dms_orig', columns= 'dms_dest',
                                         fill_value=0, aggfunc='sum')
    
    if catg == 7.1:
        #print(catg, existing_flow.sum().sum())
        existing_flow *= (1-a)
    else: #all other commodity types will remain unchanged
        pass
    return(existing_flow)
# %% All functions for agricultural shift scenario
#create dictionary to distribute demand for zones which already recieve agricultural products from North GP
def supp_1 (sctg,tonyear,south_gp,north_gp): #different for each sctg type, each data year
   
    sctg_flow =  faf_agri_nonimport[faf_agri_nonimport['sctg2']== sctg]
    existing_flow = sctg_flow.pivot_table(values=tonyear, index='dms_orig', columns= 'dms_dest',fill_value=0, aggfunc='sum')
    dest_red=[]
    for i in south_gp:
        for j in destrail:
            try:
                flow = existing_flow.loc[i,j]
                if flow > 0:
                    if j not in dest_red: #gets the unique value of j for which there is a non-zero flow
                        dest_red.append(j)
            except:
                pass
    
    redistribut= {} #[destination][north_gp]--> flow from north_gp origin to destination
    redistribut_tot ={}
    dest_red_1 = [] #to check that the destination zones in dest_red has alternative flow of the same item from north gp
    for j in dest_red:
        k = 0
        for i in north_gp:
            try:
                flow = existing_flow.loc[i,j]
                if flow > 0:
                    if j not in redistribut:
                        redistribut[j] = {i:flow}
                    else:
                        if i not in redistribut[j]:
                            redistribut[j][i]=(flow)

                    k = k+ flow
            except:
                pass

        if j not in redistribut_tot:
            redistribut_tot[j]= (k)
        if k > 0:
            if j not in dest_red_1:
                    dest_red_1.append(j)
   
    supp_frac_dest_1 ={} #supp_frac_dest_1[desti][nouth gp origin]-->fraction of supply from that nouth gp to that destination
    for i in redistribut.keys(): #to be consistent, it should have used j instead of i
        for k in redistribut[i].keys():
            frac = redistribut[i][k]/redistribut_tot[i]
            if i not in supp_frac_dest_1:
                supp_frac_dest_1[i]={k:frac}
            else:
                if k not in supp_frac_dest_1[i]:
                     supp_frac_dest_1[i][k]=(frac)

    dest_red_2=[]
    for i in dest_red:
        if i not in dest_red_1:
            dest_red_2.append(i)
      
    return(supp_frac_dest_1,dest_red,dest_red_1,dest_red_2)

#creat dictionary to distribute demand for zones which does not recieve agricultural products from North GP, but will receive now
#deficit due to reduced supply from South will be met by additional (new) supply from North. This is to make sure that agricultural production
#strictly shifts from South GP to North GP regions.
def supp_2(agr_sctg,tonyear,north_gp):#different for each data year
    
    supp_frac_dest_2 = {} #supp_frac_dest_2[sctg type][north_np origin] to get fraction of total supply from that origi
    #st = time.time()
    for sctg in agr_sctg: #this should also come from non-imports, as we assume shift of production within USA
        faf_agri_fromnorth = faf_agri_nonimport[(faf_agri_nonimport['dms_orig'].isin(north_gp)) & 
                                                (faf_agri_nonimport['sctg2']==sctg)]
        sum_rail = faf_agri_fromnorth.groupby(['dms_orig']).sum().reset_index()
     
        for i in sum_rail['dms_orig'].unique().tolist():
            ton_i = sum_rail[(sum_rail['dms_orig'] == i)][tonyear]
            r = float(ton_i/sum_rail[tonyear].sum())
          
            if sctg not in supp_frac_dest_2:
                supp_frac_dest_2[sctg]= {i:r}
            else:
                if i not in supp_frac_dest_2[sctg]:
                    supp_frac_dest_2[sctg][i]= (r)
    #en = time.time()
    return (supp_frac_dest_2)

#shift agri prod (non imports) from South to North
def agricultural_shift(sctg,tonyear,south_gp,north_gp,a):
    agr_sctg=[1,2,3,4,5,6,7,8,9] 
    OD_flow= pd.DataFrame(0.00,index=destrail, columns =originrail)
    
    sctg_flow =  faf_agri_nonimport[faf_agri_nonimport['sctg2']== sctg]
    existing_flow = sctg_flow.pivot_table(values=tonyear, index='dms_orig', 
                                          columns= 'dms_dest',fill_value=0, aggfunc='sum')
    modified_flow = existing_flow.copy()
    
    suppl_fact_1, dest, dest_set_1, dest_set_2 = supp_1(sctg,tonyear,south_gp,north_gp)
    
    suppl_fact_2 = supp_2(agr_sctg,ton_year,north_gp)
    
    
    red_dict = {}  
    #st = time.time()
    for j in dest:
        sm = 0

        for i in south_gp:
            try:
                flow = existing_flow.loc[i,j]
                if flow > 0:
                    red =  float(existing_flow.loc[i,j]*a)
                    modified_flow.loc[i,j] = existing_flow.loc [i,j] - red
                    OD_flow[i][j] = OD_flow[i][j] + modified_flow[i][j]
                    sm = sm+red
            except:
                pass
        if j not in red_dict:
            red_dict[j] = sm
    #en = time.time()

    #st = time.time()

    for j in red_dict.keys():
        total_add =float(red_dict[j])
        
        if j in dest_set_1:
            for i in north_gp:
                try:
                    add = float(total_add*suppl_fact_1[j][i])
                    modified_flow.loc[i,j] = existing_flow.loc[i,j] + add
                    OD_flow.loc[i,j] = OD_flow.loc[i,j]  + modified_flow.loc[i,j]
                    #print(j,total_add, add)
                except:
                    pass

        if j in dest_set_2:
            for i in north_gp:
                try:
                    add = float(total_add*suppl_fact_2[sctg][i]) #sctg type ==2
                    modified_flow.loc[i,j] = existing_flow.loc[i,j] + add
                    OD_flow.loc[i,j] = OD_flow.loc[i,j]  + OD_flow.loc[i,j] 
                    #print(j,total_add, add)
                except:
                    pass

    #en = time.time()
    
    #st = time.time()

    for j in destrail:
        for i in originrail:
            if i not in south_gp:
                try:
                    OD_flow.loc[i,j]  = modified_flow.loc[i,j]
                except:
                    pass
    #en = time.time()

    return(OD_flow)

#keeps the imported agricultural flow the same as before
def distribute_agri_import(df_agri_import, tonyear):
    #faf_agri_import = faf_rail_red[(faf_rail_red['cat_grp']==1)&(faf_rail_red['trade_type']==2)]
    agri_import = df_agri_import.pivot_table(values = tonyear, index='dms_orig', 
                                             columns= 'dms_dest',fill_value=0, aggfunc='sum')
    return (agri_import)


#keeps the other categories (non-agricultural)  same as before
def distribute_other(catg, df_rail,tonyear):
    cat_flow =  df_rail[df_rail['cat_grp']== catg]
    existing_flow = cat_flow.pivot_table(values=tonyear, index='dms_orig', 
                                         columns= 'dms_dest',fill_value=0, aggfunc='sum')
    return (existing_flow)




# %% All main functions for the agricultural reduction scenario
#creat dictionary to distribute demand for zones which already recieve agricultural products from North GP
def supp_1_red (sctg,tonyear,south_gp,non_south_orig): #different for each sctg type, each data year
    sctg_flow =  faf_agri_nonimport[faf_agri_nonimport['sctg2']== sctg]
    existing_flow = sctg_flow.pivot_table(values=tonyear, index='dms_orig', columns= 'dms_dest',fill_value=0, aggfunc='sum')
    
    dest_red=[]
    for i in south_gp:
        for j in destrail:
            try:
                flow = existing_flow.loc[i,j]
                if flow > 0:
                    if j not in dest_red:
                        dest_red.append(j)
            except:
                pass
    
    import_flow = faf_agri_import.pivot_table(values = tonyear, index='dms_orig', 
                                          columns= 'dms_dest',fill_value=0, aggfunc='sum')
    redistribut= {} #[destination][non_south_orig]--> flow from non_south_orig origin to destination
    redistribut_tot ={}
    #dest_red_1 = [] #to check that the destination zones in dest_red has alternative flow of the same item from north gp
    
    for j in dest_red:
        k = 0
        for i in non_south_orig:
            try:
                flow = import_flow.loc[i,j]
                if flow > 0:
                    if j not in redistribut:
                        redistribut[j] = {i:flow}
                    else:
                        if i not in redistribut[j]:
                            redistribut[j][i]=(flow)

                    k = k+ flow
            except:
                pass

        if j not in redistribut_tot:
            redistribut_tot[j]= (k)

    supp_frac_dest_1 ={} #supp_frac_dest_1[desti][nouth gp origin]-->fraction of supply from that nouth gp to that destination
    for i in redistribut.keys():
        for k in redistribut[i].keys():
            frac = redistribut[i][k]/redistribut_tot[i]
            if i not in supp_frac_dest_1:
                supp_frac_dest_1[i]={k:frac}
            else:
                if k not in supp_frac_dest_1[i]:
                     supp_frac_dest_1[i][k]=(frac)
            
    return(supp_frac_dest_1,dest_red)


#shift agri prod (non imports) from South to North
def agricultural_shift_red(sctg,tonyear,south_gp,non_south_orig,a):
   
    OD_flow= pd.DataFrame(0.00,index=destrail, columns =originrail)
    
    sctg_flow =  faf_agri_nonimport[faf_agri_nonimport['sctg2']== sctg]
    existing_flow = sctg_flow.pivot_table(values=tonyear, index='dms_orig', 
                                          columns= 'dms_dest',fill_value=0, aggfunc='sum')
    modified_flow = existing_flow.copy()
    
    suppl_fact_1, dest = supp_1_red(sctg,tonyear,south_gp,non_south_orig)
    
    
    red_dict = {}   
    for j in dest:
        sm = 0

        for i in south_gp:
            try:
                flow = existing_flow.loc[i,j]
                if flow > 0:
                    red =  float(existing_flow.loc[i,j]*a)
                    modified_flow.loc[i,j] = existing_flow.loc[i,j] - red
                    OD_flow.loc[i,j] = OD_flow.loc[i,j] + modified_flow.loc[i,j]
                    sm = sm+red
            except:
                pass
        if j not in red_dict:
            red_dict[j] = sm


    for j in red_dict.keys():
        total_add =float(red_dict[j])
 
        for i in non_south_orig:
            try:
                add = float(total_add*suppl_fact_1[j][i])
                modified_flow.loc[i,j] = existing_flow.loc[i,j] + add
                OD_flow.loc[i,j] = OD_flow.loc[i,j] + modified_flow.loc[i,j]
                #print(j,total_add, add)
            except:
                pass

    for j in destrail:
        for i in originrail:
            if i not in south_gp:
                try:
                    OD_flow.loc[i,j] = modified_flow.loc[i,j]
                except:
                    pass

    return(OD_flow)


#keeps the imported agricultural flow the same as before
def distribute_agri_import_red(df_agri_import, tonyear):
    
    #faf_agri_import = faf_rail_red[(faf_rail_red['cat_grp']==1)&(faf_rail_red['trade_type']==2)]
    agri_import = df_agri_import.pivot_table(values = tonyear, index='dms_orig', 
                                             columns= 'dms_dest',fill_value=0, aggfunc='sum')
    return (agri_import)


#keeps the other categories (non-agricultural)  same as before
def distribute_other_red(catg, df_rail,tonyear):
    cat_flow =  df_rail[df_rail['cat_grp']== catg]
    existing_flow = cat_flow.pivot_table(values=tonyear, index='dms_orig', 
                                         columns= 'dms_dest',fill_value=0, aggfunc='sum')
    return (existing_flow)
    

# %% Simulation run page
with tab4:
    st.title("Run Simulation")
    
    @st.experimental_memo(suppress_st_warning = True)
    def computation():
        start = time.time()
        total_flow = pd.DataFrame(0.00,index=destrail, columns =originrail) #empty matrix, will hold the total flow for all categories            
        #Run function for population shift scenario
        if scen == "Population Shift":
            for i in comm_cat:
                OD_flow = demand_rearr(i, prcnt, ton_year) #sctg and %change can be inlcuded as tuple if we have different % for different commodity
                #OD_flow.to_csv('CommCategory_%s_estimate_for_%s_tons.csv' % (i,analy_yr))
                total_flow = total_flow + OD_flow
                del (OD_flow)
                
        #Run function for maritime activity reduction scenario
        if scen == "Maritime Activity Reduction":
            for i in faf_rail_red['cat_grp_mod'].unique().tolist():
                flow = reduceMari(i, prcnt, ton_year)
                #flow.to_csv('CommCategory_%s_estimate_for_%s_tons.csv' % (i,ton_year))
                total_flow = total_flow + flow
                del (flow)        
                    
        #Run function for Agriculatural shift           
        elif scen == "Agricultural Shift":
            total_flow_agri = pd.DataFrame(0.00,index=destrail, columns =originrail)
            
            for i in catrail:
                if i ==1:
                    for sctg in agr_sctg:
                        flow = agricultural_shift(sctg, ton_year,South_GP,North_GP,prcnt)
                        total_flow_agri = total_flow_agri+flow
                        #print(i, sctg, flow.sum().sum())
                    import_flow = distribute_agri_import(faf_agri_import, ton_year)
                    total_flow_agri=total_flow_agri+import_flow
                    #total_flow_agri.to_csv('CommCategory_%s_estimate_for_thousand_%s.csv' % (i,ton_year))
                    total_flow=total_flow + total_flow_agri

                if i !=1:
                    flow = distribute_other(i,faf_rail_red,ton_year)
                    #flow.to_csv('CommCategory_%s_estimate_for_thousand_%s.csv' % (i,ton_year))
                    total_flow = total_flow + flow
                    #print(i, flow.sum().sum())
                    
         #Run function for Agriculatural reduction           
        elif scen == "Agricultural Reduction":
            total_flow_agri = pd.DataFrame(0.00,index=destrail, columns =originrail)
            for i in catrail:
                if i ==1:
                    for sctg in agr_sctg:
                        flow = agricultural_shift_red(sctg, ton_year,South_GP,Non_South_Orig,prcnt)
                        total_flow_agri = total_flow_agri+flow
                        #print(i, sctg, flow.sum().sum())
                    import_flow = distribute_agri_import_red(faf_agri_import, ton_year)
                    total_flow_agri=total_flow_agri+import_flow
                    #total_flow_agri.to_csv('CommCategory_%s_estimate_for_thousand_%s.csv' % (i,ton_year))
                    total_flow=total_flow + total_flow_agri

                if i !=1:
                    flow = distribute_other_red(i,faf_rail_red,ton_year)
                    #flow.to_csv('CommCategory_%s_estimate_for_thousand_%s.csv' % (i,ton_year))
                    total_flow = total_flow + flow
                    #print(i, flow.sum().sum())
                    
        
        #this portion is similar in other scenarios    
        #convert the OD matrix to list to match with the temoa regions [this one takes about 70 sec]
        df_list = pd.DataFrame(columns = ['origin_faf', 'dest_faf', 'thousand_tons'])
        for i in originrail:
            for j in destrail:
                val = total_flow[i][j]
                df_list=df_list.append({'origin_faf' : i, 'dest_faf' : j,'thousand_tons': val},ignore_index=True)
        #df_list.head()
        df_list = df_list[(df_list[['thousand_tons']] != 0).all(axis=1)] #remove 0 entries
        
        
        #merging with Temoa region and saving in csv (OD tons by Temoa region)
        merged = pd.merge(df_list,temoa_region[['FAF_Zone','Temoa_Description']], left_on = ['origin_faf'], right_on='FAF_Zone',how='left')
        merged.rename({"Temoa_Description": "Temoa_Origin"}, axis=1, inplace=True)
        merged = pd.merge(merged,temoa_region[['FAF_Zone','Temoa_Description']], left_on = ['dest_faf'], right_on='FAF_Zone',how='left')
        merged.rename({"Temoa_Description": "Temoa_Destination"}, axis=1, inplace=True)
        merged = merged.groupby(['Temoa_Origin','Temoa_Destination']).sum().reset_index()
        merged= merged.drop(['origin_faf', 'dest_faf','FAF_Zone_x','FAF_Zone_y'], axis=1)
        
        total_flow_df = convert_df(total_flow)
        merged_df = convert_df(merged)
        
        end = time.time()
        return total_flow,merged,start,end,total_flow_df,merged_df
    
    if 'run' not in st.session_state:
         st.session_state.run = 0
    st.info(f"state = {st.session_state.run}")     

    
    run = st.button('▶️ Press to run the simulation')
    if run:
        st.session_state.run = 1
    if st.session_state.run == 1:  
        total_flow,merged,start,end,total_flow_df,merged_df = computation()
        st.info(
           f"Run time = {round(end-start,ndigits = 2)} seconds"
        )
        st.download_button(
            "Download FAF Zone Flow Data",
            total_flow_df,
            f"total_flow_{version}_{scen}.csv",
            "text/csv",
            key='download-csv'
        )
        st.download_button(
            "Download TEMOA Related Flow Data",
            merged_df,
            f"Merged_{version}_{scen}.csv",
            "text/csv",
            key='download-merge'
        )
        
        