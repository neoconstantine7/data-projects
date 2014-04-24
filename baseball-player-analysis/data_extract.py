import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import * 



def get_past_x_days(filename , x):
	data = pd.read_csv(filename)
	df = pd.DataFrame(data)
	df.BA.fillna('.000', inplace = True)
	filtered_data = df[df.Split == 'Last %s days' % x]
	ba=filtered_data[filtered_data['PA'] >= 10]['BA']
	so=filtered_data[filtered_data['PA'] >= 10]['SO']
	bavg=[]
	souts=[]
	for x in ba:
		bavg.append(float(x))
	for y in so:
		souts.append(float(y))	
	
	return (bavg,souts)	

def plot(x,y,style,linestyle):
	fit = polyfit(x,y,1)
	fit_fn = poly1d(fit)
	plt.plot(x,y, style , x, fit_fn(x),linestyle)


def show_plots():
	plt.figure()
	plt.show()

plt.figure()
ba,so = get_past_x_days('giants.csv' , '7')
plot(ba,so,'bo', '-')
ba,so = get_past_x_days('giants.csv' , '14')
plot(ba,so,'ro', '-.')
ba,so = get_past_x_days('giants.csv' , '28')
plot(ba,so,'go', ':')
plt.show()
