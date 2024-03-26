#!/usr/bin/env python
# coding: utf-8

# In[115]:


#IMPORT LIBRARIES
import pandas as pd
import seaborn as sns


# In[116]:


#LOAD DATASET
df=pd.read_csv('Downloads/UMRACES.csv')


# In[117]:


#CHECKOUT DATASET
df.head()


# In[118]:


#CHECK NUMBER OF ROWS AND COLUMNS
df.shape


# In[119]:


#CHECK DATA TYPES
df.dtypes


# In[120]:


df.info()


# In[ ]:


#CLEAN DATASET
#PURPOSE OF THIS ACTIVITY IS TO CHECK FOR USA 50KM AND 50MILES RACES IN 2020


# In[121]:


#VERIFY IF 50KM AND 50MI
df[df['Event distance/length']=='50mi']


# In[13]:


#COMBINE 50KM AND 50MI WITH ISIN
df[df['Event distance/length'].isin(['50km', '50mi'])]


# In[122]:


#EXTRACT JUST 2020 RACES
df[(df['Event distance/length'].isin(['50km', '50mi'])) & (df['Year of event']==2020)]


# In[123]:


#SPLIT USA FROM EVENT NAME
df[df['Event name']== 'Everglades 50 Mile Ultra Run (USA)']['Event name'].str.split('(').str.get(1).str.split(')').str.get(0)


# In[124]:


#EXTRACT ONLY USA EVENTS
df[df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0)=='USA']


# In[125]:


#COMBINE ALL FILTERS
df2 = df[(df['Event distance/length'].isin(['50km', '50mi'])) & (df['Year of event']==2020) & (df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0)=='USA')]


# In[126]:


df2.shape


# In[127]:


#REMOVE USA FROM EVENT NAME
df2['Event name']=df2['Event name'].str.split('(').str.get(0)


# In[128]:


df2.head()


# In[129]:


#CLEAN UP ATHLETE AGE
df2['Athlete_age']= 2020- df2['Athlete year of birth']


# In[130]:


df2.head()


# In[131]:


#REMOVE h FROM ATHLETE PERFORMANCE
df2['Athlete performance']= df2['Athlete performance'].str.split(' ').str.get(0)


# In[132]:


df2.head()


# In[133]:


#DROP COLUMNS: ATHLETE COUNTRY, ATHLETE CLUB, Athlete year of birth, Athlete age category
df2= df2.drop(['Athlete age category', 'Athlete year of birth', 'Athlete club', 'Athlete country'], axis=1)
df2.head()


# In[134]:


#CHECK FOR NULL IN DATASET
df2.isna().sum()


# In[135]:


df2[df2['Athlete_age'].isna()==1]


# In[136]:


#DROP NAN
df2=df2.dropna()


# In[137]:


#NAN HAS BEEN DROPPED
df2.isna().sum()


# In[138]:


#Check for duplicates
df2[df2.duplicated()==True]


# In[139]:


#RESET INDEX
df2.reset_index(drop=True)


# In[140]:


#FIX DATA TYPES
df2.dtypes


# In[141]:


#CHANGE ATHLETE AGE TO INT & ATHLETE AVERAGE SPEED TO FLOAT
df2['Athlete_age']= df2['Athlete_age'].astype(int)
df2['Athlete average speed']= df2['Athlete average speed'].astype(float)


# In[142]:


df2.dtypes


# In[143]:


#RENAME COLUMS
df2=df2.rename(columns={'Year of event': 'year',
                        'Event dates': 'race_date',
                        'Event name': 'race_name',
                        'Event distance/length': 'race_length',
                        'Event number of finishers': 'race_number_of_finishers',
                        'Athlete performance': 'athlete_performance',
                        'Athlete gender': 'athlete_gender',
                        'Athlete average speed': 'athlete_average_speed',
                        'Athlete ID': 'athlete_id',
                        'Athlete_age': 'athlete_age'
                       })


# In[144]:


#FIND RACE NUMBER OF ATHLETE WHO RUN 9:19:09 IN Everglades 50 Mile Ultra Run
df2[df2['race_name']== 'Everglades 50 Mile Ultra Run ']


# In[145]:


#FIND ALL RACES RUN BY ATHLETE ID 222509
df2[df2['athlete_id']==222509]


# In[146]:


#VISUALIZE DATA: CHECK NUMBER OF RACES RUN BY BOTH GENDER FOR 50M AND 50KM
sns.histplot(df2['race_length'])


# In[147]:


#VISUALIZE DATA: CHECK NUMBER OF RACES RUN BY BOTH GENDER SPLIT FOR 50M AND 50KM
sns.histplot(df2, x='race_length', hue='athlete_gender')


# In[148]:


#VISUALIZE DATA: CHECK THE ATHLETE AVERAGE SPEED 
sns.displot(df2[df2['race_length']=='50mi']['athlete_average_speed'])


# In[149]:


#VISUALIZE DATA: VISUALIZE THE AVERAGE SPEED AND RACE LENGTH FOR MALE AND FEMALE
sns.violinplot(df2, x='race_length', y= 'athlete_average_speed', hue='athlete_gender', split=True, inner='quart', linewidth=1)


# In[150]:


#VISUALIZE DATA: VISUALIZE ATHLETE AVERAGE SPEED PER ATHLETE AGE
sns.lmplot(df2, x='athlete_age', y='athlete_average_speed', hue='athlete_gender')


# In[151]:


#QUESTIONS ANSWERED FROM DATA
#1. DIFFERENCE IN SPEED FOR MALE AND FEMALE
df2.groupby(['race_length','athlete_gender'])['athlete_average_speed'].mean()


# In[152]:


#WHAT AGE GROUPS ARE THE BEST IN 50MI RACE
df2.query('race_length== "50mi"').groupby('athlete_age')['athlete_average_speed'].agg(['mean','count']).sort_values('mean', ascending=False).query('count>19').head(10)


# In[153]:


#CREATE A NEW COLUMN FOR RACE MONTH
df2['race_month']=df2['race_date'].str.split('.').str.get(1).astype(int)


# In[154]:


df2


# In[155]:


#CREATE A COLUMN FOR RACE SEASONS
df2['race_season'] = df2['race_month'].apply(lambda x: 'Winter' if x > 11 else 'Fall' if x > 8 else 'Summer' if x > 5 else 'Spring' if x > 2 else 'Winter')


# In[156]:


df2.head()


# In[157]:


#MORE RACES WERE RUN IN THE WINTER AND LESS IN THE SUMMER
df2.groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending=False)


# In[158]:


#WITH 50 MILER ONLY, MORE RACES OCCURED IN THE FALL AND LESS IN THE SUMMER
df2.query('race_length=="50mi"').groupby('race_season')['athlete_average_speed'].agg(['mean', 'count']).sort_values('mean', ascending=False)


# In[ ]:


#REFERENCE: https://www.kaggle.com/datasets/aiaiaidavid/the-big-dataset-of-ultra-marathon-running/discussion/420633


# In[ ]:





# In[ ]:




