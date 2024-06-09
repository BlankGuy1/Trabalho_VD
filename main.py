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

#Streamlit




st.session_state['data'] = data



def ordenaQuantidade(values):
    def convert(value):
        try:
            return float(value)
        except ValueError:
            return float(value.replace('+', '')) + 0.1
    return sorted(values, key=convert)

def ordenaRenda(value):
    try:
        return float(value.split('-')[0].replace('K', '').replace('$', ''))
    except:
        return float('inf')

def ordenaIdade(value):
    try:
        return int(value.split('-')[0])
    except:
        return float('inf')

st.set_page_config(
    page_title="Análise de Clientes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title('📊 Análise de Clientes')

    # Filtro de data
    min_date = data['Date'].min()
    max_date = data['Date'].max()
    selected_start_date, selected_end_date = st.date_input(
        "Selecione o intervalo de datas:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Filtro estações
    seassons = data['Seasons']
    selected_seassons = st.multiselect('Estação do Ano', seassons, default=None)
    select_all_seassons = st.checkbox('Selecionar todos', value=True, key='seassons')
    if select_all_seassons:
        selected_seassons = seassons

#Filtro produto
    pr_departamento = data['product_department']
    selected_pr_departamento = st.multiselect('Estação do Ano', pr_departamento, default=None)
    selected_all_pr_departamento = st.checkbox('Selecionar todos', value=True, key='produto')
    if selected_all_pr_departamento:
        selected_pr_departamento = pr_departamento

# Filtro faixa etária
    household_ages = sorted(data['household_age'].unique().tolist(), key=ordenaIdade)
    selected_ages = st.multiselect('Faixas Etárias', household_ages, default=None)
    select_all_ages = st.checkbox('Selecionar todos', value=True, key='ages')
    if select_all_ages:
        selected_ages = household_ages

    # Filtro faixa de renda
    household_incomes = sorted(data['household_income'].unique().tolist(), key=ordenaRenda)
    selected_incomes = st.multiselect('Faixas de Renda', household_incomes, default=None)
    select_all_incomes = st.checkbox('Selecionar todos', value=True, key='incomes')
    if select_all_incomes:
        selected_incomes = household_incomes

    # Filtro tamanho da família
    household_sizes = ordenaQuantidade(data['household_size'].unique().tolist())
    selected_sizes = st.multiselect('Tamanho das Famílias', household_sizes, default=None)
    select_all_sizes = st.checkbox('Selecionar todos', value=True, key='sizes')
    if select_all_sizes:
        selected_sizes = household_sizes

    # Filtro número de crianças
    household_kids_counts = ordenaQuantidade(data['household_kids_count'].unique().tolist())
    selected_kids_counts = st.multiselect('Número de Crianças', household_kids_counts, default=None)
    select_all_kids_counts = st.checkbox('Selecionar todos', value=True, key='kids_counts')
    if select_all_kids_counts:
        selected_kids_counts = household_kids_counts

    # Filtro de Lojas
    unique_store_ids = sorted(data['store_id'].unique().tolist())
    selected_store_ids = st.multiselect('Selecione IDs de Loja', unique_store_ids, default=None)
    select_all_stores = st.checkbox('Selecionar todos', value=True, key='stores')
    if select_all_stores:
        selected_store_ids = unique_store_ids

# Filtragem dos dados com base nas seleções e datas
filtros = data[
    (data['Date'] >= pd.to_datetime(selected_start_date)) &
    (data['Date'] <= pd.to_datetime(selected_end_date)) &
    data['household_age'].isin(selected_ages) &
    data['household_income'].isin(selected_incomes) &
    data['household_size'].isin(selected_sizes) &
    data['household_kids_count'].isin(selected_kids_counts) &
    data['store_id'].isin(selected_store_ids) &
    data['Seasons'].isin(selected_seassons) &
    data['product_department'].isin(selected_pr_departamento)
]

st.header('Navegue e descubra o perfil de seus clientes')
'\n'

col1, col2, col3 = st.columns([1.1, 1.5, 1.5])

with col1:
    # Total ao longo do Ano
    st.metric("Total de Vendas ao longo do Ano ", value=f"${filtros['sales_value'].sum():.2f}")
    '\n'

    # Total de Vendas ao longo do Ano
    st.markdown('###### **Total de vendas ao longo do ano**')
    Anual_sales = filtros.groupby(['Date'], as_index=False).agg(total_sales=('sales_value','sum'),total_quantity=('sales_value','sum'))
    Anual_sales = Anual_sales.sort_values(by='Date', ascending=False)
    AnualSales = px.scatter(Anual_sales,
                           y='total_quantity',
                           x='Date',
                           trendline="ols",
                            labels={'Date':'Data', 'total_quantity':'Vendas'})
    AnualSales.update_layout(
        xaxis=dict(
            showgrid=True,
            gridcolor='#3B3B3B'
        ),
        showlegend=False
    )

    st.plotly_chart(AnualSales)

with col2:
    # Total de vendas por estação
    st.metric("Total de Vendas por estação ", value=f"${filtros['sales_value'].sum():.2f}")
    '\n'

    # Total de Vendas por estação
    st.markdown('###### **Total de vendas por estação**')
    season_sales = filtros.groupby(['Seasons'], as_index=False).agg(total_sales=('sales_value','sum'),total_quantity=('sales_value','sum'))
    season_sales = season_sales.sort_values(by='Seasons', ascending=False)
    seasonSales = px.pie(season_sales, names='Seasons', color='Seasons')
    seasonSales.update_traces(textinfo='label+percent', showlegend=False, rotation=340, direction='clockwise')

    st.plotly_chart(seasonSales)

with col3:
    st.metric("Produtos que vendem mais por estação ", value=f"${filtros['sales_value'].sum():.2f}")
    '\n'

    st.markdown('###### **Produtos que vendem mais por estação**')
    Pr_estacao= px.histogram(filtros, x="Seasons", y="sales_value", color="product_department", width=500, height=400,
             labels = {'Seasons':'Seasons', 'Sales_value':'Vendas', 'product_department':'Produto'},
            )
    st.table(Pr_estacao)

col4 = st.columns([1])

with col4:
    '\n'
    # Idade que compra mais
    st.markdown('###### **Idade que compra mais**')
    household_sale = filtros.groupby(['household_age'], as_index=False).agg(total_sales=('sales_value','sum'))

    householdsale = px.bar(household_sale, x='household_age', y='total_sales', color='household_age',
                        labels={'household_age': 'Idade da Família', 'sales_value': 'Vendas'},
                        barmode='h')
    st.plotly_chart(householdsale)

    #End