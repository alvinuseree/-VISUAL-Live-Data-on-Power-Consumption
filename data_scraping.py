import requests													#Request HTML 										
import bs4														#Beatufiul Soup to see source clearly
from decimal import *											#Easier floating point arithmetic

import matplotlib.pyplot as plt 								#To plot the data visually

import time
import datetime

getcontext().prec = 5											#set arithmetic precision to 5 sig figs 

def get_livedata():
	re = requests.get("http://gridwatch.co.uk/")				#request HTML from GridWatch
	soup = bs4.BeautifulSoup(re.text, 'lxml')					#Convert to a readable sourcefile

	#find the numerical data we need 
	spans = soup.find_all('span', {'style' : 'color:white;'})	#find all data with span , style:color white

	demand_data = [span.get_text() for span in spans]			#extract data needed 

																#demand_data contains: all strings with:
																#><span style='color:white;'

	consumption = Decimal(demand_data[0][0:6])					#read first string in demand_data and converts first 
	frequency = Decimal(demand_data[0][10:16])					#7 elements into float

	#find the titles for the numerical data				
	spans_titles = soup.find_all('span', {'style' : 'color:black;font-weight:800;'}) + soup.find_all('span', {'style' : 'color:black;font-weight:800;font-size:12px;'})
																#titles are in black hence color:black; etc
	titles = [span.get_text() for span in spans_titles]			#extract titles needed
	title = []
	place_holder = []

	for x in range(len(titles)):
		if(x<8 or x>11):
			title.append(titles[x])
		else:
			place_holder.append(titles[x])
	for x in range(len(place_holder)):
		title.append(place_holder[x])

	return demand_data, title 									#returns demand and their corresponding  										 #Reads live data from gridwatch and splits into numerical & titles
def data_splitting(numerical_data):
	consumption = []											#Arrays containing
	frequency = []
	percentage = []

	for x in range (len(numerical_data)):
		#check to see if the any of the data is 0 GW
		characters = len(numerical_data[x])						#number of characters in the entire data set
		
		if(numerical_data[x][characters-1]!="%"):
			if(x>0):
				percentage.append(0)

		for i in range (len(numerical_data[x])):
			#3 cases we look at: "GW","hz","%" 
			if(numerical_data[x][i]=="W"):
				consumption_character = i 						#number of chracters in consumption
				consumption.append(numerical_data[x][0:i-1])

			if(numerical_data[x][i]=="z"):
				frequency.append(numerical_data[x][consumption_character+2:i-1])
			
			if(numerical_data[x][i]=="%"):
				percentage.append(numerical_data[x][consumption_character+2:i])
			
	return consumption, frequency, percentage 						 #Split numerical data into categories (GW, Hz, %)


#										script to run functions
important_data = get_livedata()									#important_data[0] contains the data
																#important_data[1] contains the titles

data = data_splitting(important_data[0])						#data[0] contains all the consumption levels
																#data[1] contains system frequency
																#data[2] contains the percentage of consumption per technology

# Pie chart
labels = []														#label used for the legend
sizes = []														#the actual consumption data
label=[]														#label used for the actual pie chart

renewables = ["Biomass","Wind","Solar","Hydro"]					#list of renewables
renewable_techs = []
sizesax3=[]

legend_label=[]

for x in range (2,len(important_data[1]),1):	
	if(float(data[0][x])>0):	
		label.append(important_data[1][x])
		sizes.append(data[0][x])
		legend_label.append(important_data[1][x] + ": "+ str(data[0][x]) + "GW")

	ren_check = important_data[1][x] in renewables 				#checks to see if the technology is a renewable
	if(ren_check == True):
		renewable_techs.append(important_data[1][x])
		sizesax3.append(data[0][x])
	
labelax2= ["Renewables","Non-Renewables"]						#percentage of renewable usage 			
sizesax2=[float(data[2][0]),100-float(data[2][0])]

current_time = str(datetime.datetime.now())						#find the current date and time 
datetime = []

for x in range(0,4,1):											#split probelm into 4 parts: day,month,year and time
	if(x==0):
		datetime.append(current_time[8]+current_time[9]+"/")
	if(x==1):
		datetime.append(current_time[5]+current_time[6]+"/")
	if(x==2):
		datetime.append(current_time[0]+current_time[1]+current_time[2]+current_time[3])		
	if(x==3):
		datetime.append(" "+current_time[11]+current_time[12]+current_time[13]+current_time[14]+current_time[15])

datetime=''.join(datetime)										#join all the elements of the array together without spaces ('')


fig = plt.figure()

#Renewable techs
ax1 = fig.add_axes([0.55, -0.05, .5, .5], aspect=1)				#position of chart 1
ax1.pie(sizesax3, labels=renewable_techs, radius = 0.9,autopct='%1.0f%%')

#% renewables
ax2 = fig.add_axes([.55, 0.45, .5, .5], aspect=1)					#pos chart 2
ax2.pie(sizesax2, labels=labelax2, radius = 0.9,autopct='%1.0f%%')

#all technologies
ax3 = fig.add_axes([0.15, 0.225, .5, .5], aspect=1)					#pos chart 2
ax3.pie(sizes, labels=label, radius = 1.8)


ax1.set_title('Renewable Technologies',fontweight="bold")									
ax2.set_title('% Renewable Usage',fontweight="bold",y=0.9)
ax3.set_title('Technologies',fontweight="bold",y=1.35)

fig.suptitle('UK Consumption Data',fontsize=25,x=0.16,fontweight="bold")

fig.text(x=0.006, y=0.87, s="System Frequency:", fontsize=22)
fig.text(x=0.225, y=0.87, s=float(data[1][0]), fontsize=22)
fig.text(x=0.305, y=0.87, s="Hz", fontsize=22)

fig.text(x=0.006, y=0.82, s="Demand:", fontsize=22)
fig.text(x=0.11, y=0.82, s=float(data[0][0]), fontsize=22)
fig.text(x=0.19, y=0.82, s="GW", fontsize=22)

fig.text(x=0.006, y=0.76, s=datetime, fontsize=18)

plt.legend(labels=legend_label, loc=[-0.9,0.15])




plt.show()