import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import matplotlib.dates as mdates

sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='date').agg({
        'total_rent': 'sum'
    }).reset_index()
     
    return daily_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'total_rent': 'sum' 
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'total_rent': 'sum'
    }).reset_index()
    return weekday_rent_df

def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return holiday_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_condition').agg({
        'total_rent': 'sum'
    })
    return weather_rent_df

# Load cleaned data
all_df = pd.read_csv("./dashboard/main_data.csv")

datetime_columns = ["date"]
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    st.image("./dashboard/bike_rental.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

filtered_df = main_df[(main_df['date'] >= pd.to_datetime(start_date)) & (main_df['date'] <= pd.to_datetime(end_date))]


# Menyiapkan berbagai dataframe
daily_df = create_daily_rent_df(main_df)
daily_casual_df = create_daily_casual_rent_df(main_df)
daily_registered_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_df = create_monthly_rent_df(main_df)
weekday_df = create_weekday_rent_df(main_df)
holiday_df = create_holiday_rent_df(main_df)
weather_df = create_weather_rent_df(main_df)

st.header('Bike Rentals')
st.subheader('Daily Orders')

col1, col2, col3 = st.columns(3)

with col1:
    daily_casual = daily_casual_df['casual'].sum()
    st.metric('Casual User', value=f"{daily_casual:,}")

with col2:
    daily_registered = daily_registered_df['registered'].sum()
    st.metric('Registered User', value=f"{daily_registered:,}")

with col3:
    daily_rent_total = daily_df['total_rent'].sum()
    st.metric('Total User', value=f"{daily_rent_total:,}")


#Total semua rental sepanjang waktu
st.subheader('Total Daily Users Over Time')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_df["date"],
    daily_df["total_rent"],
    markersize=2,
    linewidth=2,
    color="#90CAF9"
)
ax.set_xticks(daily_df["date"][::30])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_xlabel("Date", fontsize=18)
ax.set_ylabel("Total Users", fontsize=18)
ax.tick_params(axis='y', labelsize=16)
ax.tick_params(axis='x', labelsize=14, rotation=45)

st.pyplot(fig)

#Visualisasi berdasarkan Bulan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_df.index,
    monthly_df['total_rent'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)
for index, row in enumerate(monthly_df['total_rent']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=17)
ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)


#Visualisasi berdasarkan musim
st.subheader('Seasonly Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Visualisasi berdasarkan kondisi cuaca
st.subheader('Weatherly Rentals')
fig, ax = plt.subplots(figsize=(16, 8))
colors=["tab:blue", "tab:orange", "tab:red"]
sns.barplot(
    x=weather_df.index,
    y=weather_df['total_rent'],
    palette=colors,
    ax=ax
)
for index, row in enumerate(weather_df['total_rent']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan weekday dan holiday
st.subheader('Weekday and Holiday Rentals')

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15,10)) 

colors2 = ["tab:blue", "tab:orange"]
colors3 = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

# Berdasarkan holiday
holiday_melt = holiday_df.melt(
    id_vars='holiday', 
    value_vars=['registered', 'casual'],
    var_name='user_type', 
    value_name='total_rent'
)

sns.barplot(
    x='holiday',
    y='total_rent',
    hue='user_type',
    data=holiday_melt,
    palette=colors2, 
    ax=axes[0]
)
for p in axes[0].patches:
    axes[0].annotate(
        format(int(p.get_height()), ','),
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='bottom',
        fontsize=12,
        xytext=(0, 5),
        textcoords='offset points'
    )
axes[0].set_title('Number of Rents (Registered vs Casual) based on Holiday')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)
axes[0].legend(title="User Type", loc='upper right')


#Visuali weekday
sns.barplot(
    x='weekday',
    y='total_rent',
    data=weekday_df,
    hue=colors3,
    palette=colors3,
    ax=axes[1]
)

for index, row in enumerate(weekday_df['total_rent']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Weekday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)
