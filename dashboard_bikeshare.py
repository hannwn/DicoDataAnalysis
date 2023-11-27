# Libraries used
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Data Read by Pandas
hour_st = pd.read_csv('hour_quarter.csv')


# Helper functions
def total_users_df(df):
    user_year0 = df[df['yr'] == 0].groupby(by = 'quarter').agg({
        'registered' : 'sum',
        'casual' : 'sum'
    })
    user_year0['yr'] = 0
    user_year1 = df[df['yr'] == 1].groupby(by = 'quarter').agg({
        'registered' : 'sum',
        'casual' : 'sum'
    })
    user_year1['yr'] = 1
    total_users_st = pd.concat([user_year0, user_year1])

    return total_users_st, user_year0, user_year1

def compare_users_df(df):
    diff_reg = []
    increase_reg = []
    for q in range(len(user_year1['registered'])):
        diff_reg.append(user_year1['registered'][q] - user_year0['registered'][q])
        increase_reg.append((user_year1['registered'][q] * 100 - user_year0['registered'][q])/user_year0['registered'][q])

    diff_cas = []
    increase_cas = []
    for q in range(len(user_year1['casual'])):
        diff_cas.append(user_year1['casual'][q] - user_year0['casual'][q])
        increase_cas.append((user_year1['casual'][q] * 100 - user_year0['casual'][q])/user_year0['casual'][q])

    zipped = list(zip(diff_reg, increase_reg, diff_cas, increase_cas))
    indeq = ['q1', 'q2', 'q3', 'q4']

    compare_st = pd.DataFrame(zipped, columns = ['diff_reg', 'increase_reg', 'diff_cas', 'increase_cas'], index= indeq)
    compare_st.index.name = 'quarter'

    return compare_st

def percent_df(df):
    b = df.groupby('season').agg({
        'casual' : 'sum',
        'registered' : 'sum',
        'cnt' :'sum'
    }).sort_values(by = 'cnt', ascending= False).reset_index()
    b['season'] = b['season'].apply(lambda x: 'Spring' if x == 1 else ('Summer' if x == 2 else ('Fall' if x == 3 else 'Winter')))


    per = []
    for i in range(len(b['cnt'])):
        per.append(b['cnt'][i] * 100 / b['cnt'].sum())

    b['percentage'] = per

    return b

# Function Call
total_users_st, user_year0, user_year1 = total_users_df(hour_st)
compare_st = compare_users_df(hour_st)
percent_st = percent_df(hour_st)


# Dashboard Construct First Tab
st.header('Bikeshare Dashboard')

tab1, tab2 = st.tabs(['Users per Quarter', 'Users per Season'])

# Registered Users Graph
with tab1:
    st.subheader('Registered User by Quarter (YoY)')
    colm1, colm2 = st.columns(2)
        
    with colm1:
        total_users = hour_st.cnt.sum()
        st.metric("Total users in 2011-2012", value=total_users)
        
    with colm2:
        total_regis = hour_st.registered.sum() 
        st.metric("Total Registered User", value=total_regis)

    fig = plt.figure(figsize=(16, 8))
    sns.lineplot(
        x = 'quarter',
        y = 'registered',
        data = total_users_st,
        hue = 'yr',
        style = 'yr',
        markers = True
    )
    plt.xlabel('Quarter')
    plt.ylabel('Amount of Registered Users')
    plt.title('Registered Users by Quarter (YoY)')  
    st.pyplot(fig)

    # Casual Users Graph
    st.subheader('Casual User by Quarter (YoY)')
    colm1, colm2 = st.columns(2)
        
    with colm1:
        total_users = hour_st.cnt.sum()
        st.metric("Total users in 2011-2012", value=total_users)
        
    with colm2:
        total_regis = hour_st.registered.sum() 
        st.metric("Total Casual User", value=total_regis)

    fig = plt.figure(figsize=(16, 8))
    sns.lineplot(
        x = 'quarter',
        y = 'casual',
        data = total_users_st,
        hue = 'yr',
        style = 'yr',
        markers = True
    )
    plt.xlabel('Quarter')
    plt.ylabel('Amount of Casual Users')
    plt.title('Casual Users by Quarter (YoY)')
    st.pyplot(fig)

    # Comparison of Growth
    st.subheader('Comparison of Percent Increase of Users per Quarter (YoY')

    fig = plt.figure(figsize=(10,5))
    plt.plot(
        compare_st.index,
        compare_st['increase_reg'],
        '-go',
        compare_st['increase_cas'],
        '-bo'
    )
    plt.title('Comparison of Percent Increase of Users per Quarter (YoY)')
    plt.xlabel('Quarter')
    plt.ylabel('Percent')
    plt.legend(['Regular user','Casual User'])
    st.pyplot(fig)

# Tab 2
with tab2:
    fig = plt.figure(figsize=(8,10))
    ax = sns.barplot(
        x = 'season',
        y = 'cnt',
        data = percent_st.sort_values(by = 'cnt', ascending= False),
        palette = 'Blues_r'
    )
    plt.xlabel('Seasons')
    plt.ylabel('Count of Users')
    plt.title('Total Users per Season in 2011-2012')
    abs_values = percent_st['cnt']
    rel_values = percent_st['percentage']
    lbls = [f'{p[0]} ({p[1]:.0f}%)' for p in zip(abs_values, rel_values)]

    ax.bar_label(container=ax.containers[0], labels = abs_values)
    st.pyplot(fig)
