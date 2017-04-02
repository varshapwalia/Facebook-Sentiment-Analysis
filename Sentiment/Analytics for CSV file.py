import matplotlib.pyplot as plt
import csv

a=[]
b=[]
c=[]
d=[]
e=[]

with open('E:\Sentiment\posts.txt','r') as csvfile: #posts from post.py script
	plots=csv.reader(csvfile, delimiter=',')
	for row in plots:
		a.append(int(row[7]))#num of reaction
		b.append(int(row[8]))#num of comments
		c.append(int(row[9]))#num of shares
		d.append(int(row[10]))#num of likes
		e.append(int(row[14]))#num of sads
		
plt.plot([],[],colors='m',label='reaction')
plt.plot([],[],colors='c',label='comments')
plt.plot([],[],colors='r',label='shares')
plt.plot([],[],colors='k',label='likes')
plt.plot([],[],colors='o',label='sads')
plt.stackplot(a,b,c,d,e, colors =['m','c','r','k','o'])
'''
Second Method we can use: but i am still learning Numpy and pandas:

import numpy as np
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,=np.loattext('FILE_NAME',delimiter=',',unpack=True)
plt.plot([],[],colors='m',label='reaction')
plt.plot([],[],colors='c',label='comments')
plt.plot([],[],colors='r',label='shares')
plt.plot([],[],colors='k',label='likes')
plt.plot([],[],colors='o',label='sads')
plt.stackplot(h,i,j,0,p, colors =['m','c','r','k','o'])
'''
plt.xlabel("TimeLine")
plt.ylabel("Stack ploted values")
plt.title("Sentiment")
plt.legend()
plt.show()