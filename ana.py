#Import dependencies
import pandas as pd
import matplotlib.pyplot as plt
import math

#Import Data in environment - Change the file path as required
WindData = pd.read_csv("wind--data--file--path")
SiteEnergy = pd.read_csv("actual--output--for--comparison")
pcurve = pd.read_csv("turbine--power--curve--file--path")

#Select only windData for height at 50m, the height of windmill is 80m
WindData = WindData.drop(columns = ['NW_spd_2m', 'NW_dir_2m', 'NW_spd_10m', 'NW_dir_10m',
       'NW_t2m'])

#Plot the power curve for onsite turbine
x = pcurve["WindSpeed.ms"]
y = pcurve["Power.kW"]
plt.title("Power Curve")
plt.plot(x,y)
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Power (kW)")

#Use time column to set dataframe index as time series index
WindData.index = pd.to_datetime(WindData['Time'])

#Select Date range from year 2007 to 2015
mask = (WindData.index > '2006-12-31 23:00:00') & (WindData.index <= '2015-12-31')

#Wind Data for logan site from 2007 to 2015
dfl = WindData[mask]

#Empty dataframe to store estimated power generation
p_est = pd.DataFrame(columns = ['Time','Power'])

#Search the Wind data in power curve and appending to new dataframe
for speed, time in zip(dfl['NW_spd_50m'],dfl['Time']):
    #print('Speed is'+' '+str(speed))
    #print('Time is'+' '+str(time))
    #rounding off the windspeed to nearest quarter
    k = math.ceil(speed*4)/4
    #get location of windspeed in dataframe
    loc = pcurve[pcurve['WindSpeed.ms'] == k].index[0] 
    #use location to get power at that windspeed
    data = pd.DataFrame({'Time': time, 'Power' : pcurve['Power.kW'][loc]},index=[0]) 
    p_est = p_est.append(data)

#Use time column to set dataframe index as time series index    
p_est.index = pd.to_datetime(p_est['Time'])

#Group Data by month and aggregating 
apdm = p_est.groupby(pd.TimeGrouper("M")).sum()

#Drop last row as October 2015 data is not required for comparison
apdm = apdm.drop(apdm.index[len(apdm)-1])
s = SiteEnergy['Energy.MWh']
apdm['Site_Energy'] = s.tolist()
apdm = apdm.drop(columns='Time')

#Convert kWh to MWh
apdm['Power'] = apdm['Power']/1000

#Calculate Output for 134 no of turbines
apdm['Power'] = apdm['Power']*134

#Select Actual output and Anticipated Output to plot
list = ['Power','Site_Energy']

#Plot Size
apdm[list].plot(figsize=(25,10), grid=True)

#Plot labels
plt.title("Power Output(actual) v/s Anticipated Output")
plt.xlabel("Time")
plt.ylabel("Monthly Energy (MWh)")
plt.legend(["Anticipated Output", "Power Output(actual)"])

#Show Plot
plt.show()
    


    



