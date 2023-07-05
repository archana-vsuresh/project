import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/archa/OneDrive/Documents/Python class/Project data/Mental health Depression disorder Data.csv")
df.head()
df.shape
df.info()
print(df.shape) #Shape of data before droping rows that are not countries
df = df.loc[~df.Entity.str.match('Australasia|Andean Latin America|Caribbean|Central African Republic|Central Asia|Central Europe|Central Europe, Eastern Europe, and Central Asia|Central Latin America|Central Sub-Saharan Africa|East Asia|Eastern Europe|Eastern Sub-Saharan Africa|High-income Asia Pacific|High-middle SDI|Latin America and Caribbean|Low SDI|Low-middle SDI|Middle SDI|North Africa and Middle East|North America|South Asia|South Asia|Southeast Asia, East Asia, and Oceania|Southern Latin America|Southern Sub-Saharan Africa|Tropical Latin America|Western Europe|Western Sub-Saharan Africa')] #Select everyhting except this zones that are not countries 
print(df.shape)
df = df.rename(columns= {'Entity' : 'Country'})
#df['Year'] = pd.to_numeric(df['Year'])
df[5705:5720]#index error
df = df.drop(columns=['index']).reset_index()
df.loc[df['Year'] == 'Year']
df1 = df[:5712] #First table of dataset
df2 = df[5712:52478] #Second table of dataset
df3 = df[52478:99244] #Third table of dataset
df4 = df[99244:] #Third table of dataset
df2, df2.columns = df2[1:] , df2.iloc[0] #df2[1:] to setting row from 1 to last and df2.iloc[0] to lock the first row as a header. 
df2 = df2.iloc[:, 1:7]
df2 = df2.rename(columns= {'Entity' : 'Country'}) #Changing column Entity to Country as well

df3, df3.columns = df3[1:] , df3.iloc[0] #df2[1:] to setting row from 1 to last and df2.iloc[0] to lock the first row as a header. 
df3 = df3.iloc[:, 1:7]
df3 = df3.rename(columns= {'Entity' : 'Country'}) #Changing column Entity to Country as well

df4, df4.columns = df4[1:] , df4.iloc[0] #df2[1:] to setting row from 1 to last and df2.iloc[0] to lock the first row as a header. 
df4 = df4.iloc[:, 1:5]
df4 = df4.rename(columns= {'Entity' : 'Country'}) #Changing column Entity to Country as well

dff =pd.merge(df1, df2, how='left', on=['Country', 'Code', 'Year']) #We use left join concatenate them with these three columns that have in common.
dff1 = pd.merge(dff, df3, how='left', on=['Country', 'Code', 'Year'])
c_data = pd.merge(dff1, df4, how='left', on=['Country', 'Code', 'Year'])
c_data = c_data.drop(columns=['Population_y', 'Code', 'index']).rename(columns={'Population_x' : 'Population'}).dropna()
c_data.info()
c_data = c_data.astype({'Year': 'int', 'Schizophrenia (%)': 'float', 'Bipolar disorder (%)' : 'float', 'Eating disorders (%)' : 'float', 'Prevalence in males (%)' : 'float', 'Prevalence in females (%)' : 'float', 'Population' : 'float', 'Suicide rate (deaths per 100,000 individuals)' : 'float', 'Depressive disorder rates (number suffering per 100,000)' : 'float', 'Prevalence - DD' : 'float' })
c_data.describe()

import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import*
root=Tk()#window
root.title('data visualization')
root.iconbitmap('Mental health Depression disorder Data.csv')
root.geometry('400x400')

def graph1():
    plot_df = c_data.iloc[:, 2:9].mean().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(6, 5))
    ax = plt.axes()
    ax.spines['bottom'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.spines[['right', 'top']].set_visible(False)
    sns.barplot(y= plot_df['index'], x = plot_df[0], orient='h', palette='Blues_r')
    plt.title('Percentage of each disorder between 1990 - 2017')
    plt.ylabel('')
    plt.xlabel('Percentage', loc='left')
    plt.show()
    
def graph2():
    plot_mw = c_data.iloc[:, 9:11].mean().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(6, 5))
    ax = plt.axes()
    ax.spines['bottom'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.spines[['right', 'top']].set_visible(False)
    sns.barplot(y= plot_mw[0], x = plot_mw['index'], palette='Blues_r', orient='v')
    plt.title('Prevalence of disorders by gender')
    plt.ylabel('Percentage')
    plt.xlabel('')
    plt.show()

map = df1.iloc[:, [1, 2, 9]].groupby(['Code', 'Country']).median().reset_index()
map2 = df1.iloc[:, [1, 2, 7]].groupby(['Code', 'Country']).median().reset_index()
import plotly.graph_objects as go
import pandas as pd

def graph3():
    fig = go.Figure(data=go.Choropleth(
    locations = map2['Code'],
    z = map2['Anxiety disorders (%)'],
    text = map2['Country'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Anxiety disorders Rate(%)',
    ))

    fig.update_layout(
    title_text='Anxiety disorders Rate(%)',
    geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
        ),
    )
    fig.layout.template = None
    fig.show()
    
def graph4():
    plt.figure(figsize=(12, 8))
    plt.title('Correlation between disorders', fontdict={'size': 14})
    corr_val = c_data.iloc[:, 2:9].corr()
    sns.heatmap(corr_val, 
                xticklabels = corr_val.columns.values,
                yticklabels = corr_val.columns.values,
                annot = True, cmap="Blues");
    plt.show()

def graph5():    
    ax = plt.axes()
    ax.spines['bottom'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.spines[['right', 'top']].set_visible(False)
    plt.plot("Depression (%)", "Suicide rate (deaths per 100,000 individuals)", data=c_data, linestyle='none', marker='o')
    plt.title('Correlation')
    plt.ylabel('Suicide rate (deaths per 100,000 individuals)', loc='top', multialignment='center')
    plt.xlabel('Depression (%)', loc='left')
    plt.show()

l=Label(root,text="plotting").pack()    
my_button1=Button(root,text='Percentage of each disorder between 1990 - 2017',command=graph1)
my_button1.pack()
my_button2=Button(root,text='Prevalence of disorders by gender',command=graph2)
my_button2.pack()
my_button3=Button(root,text='Anxiety disorders Rate',command=graph3)
my_button3.pack()
my_button4=Button(root,text='Correlation between disorders',command=graph4)
my_button4.pack()
my_button5=Button(root,text='correlation with Suicide rate',command=graph5)
my_button5.pack()

root.mainloop()
