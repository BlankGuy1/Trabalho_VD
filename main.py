import pandas as pd
import plotly.express as px
import streamlit as st

data = pd.read_csv('grocery_store_transactions.csv')
new_data = data["transaction_timestamp"].str.split(" ", n=1, expand=True)

data["Date"] = new_data[0]
data["Time"] = new_data[1]
data.drop(columns=["transaction_timestamp"], inplace=True)

seassons_data = data["Date"].str.split("-", n=1, expand=True)
seassons_data["Dia"] = seassons_data[1]
seassons_data["Ano"] = seassons_data[0]
data_seasson = seassons_data["Dia"].str.split("-", n=1, expand=True)

data["Month"] = data_seasson[0]
data['Date'] = pd.to_datetime(data['Date'])

data_per_day = data.groupby(['Date'], as_index=False).agg(total_sales=('sales_value','sum'),total_quantity=('quantity','sum'))


def estacoes(mes):
    if mes == "01":
        return "Winter"
    if mes == "02":
        return "Winter"
    if mes == "03":
        return "Winter"
    if mes == "04":
        return "Spring"
    if mes == "05":
        return "Spring"
    if mes == "06":
        return "Summer"
    if mes == "07":
        return "Summer"
    if mes == "08":
        return "Summer"
    if mes == "09":
        return "Summer"
    if mes == "10":
        return "Fall"
    if mes == "11":
        return "Fall"
    if mes == "12":
        return "Fall"


data['Seasons'] = data['Month'].map(estacoes)
data_per_season = data.groupby(['Seasons'], as_index=False).agg(total_sales=('sales_value','sum'))
data_per_age = data.groupby(['household_age'], as_index=False).agg(total_sales=('sales_value','sum'))
data_per_store = data.groupby(['store_id'], as_index=False).agg(total_sales=('sales_value','sum'))
print(data)