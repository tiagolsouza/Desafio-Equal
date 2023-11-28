import streamlit as st
import pandas as pd
#import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

#st.set_page_config(layout="wide")
#st.set_page_config(page_title="Meu dashboard", )

#st.title("disgraça de site")

# Carregar os dados
fato_vendas = pd.read_excel('fato_vendas.xlsx')
dim_produtos = pd.read_excel('dim_produtos.xlsx')
dim_familia_produtos = pd.read_excel('dim_familia_produtos.xlsx')
dim_vendedor = pd.read_excel('dim_vendedor.xlsx')

# Visualização do total vendido no ano e vendas ao longo do tempo
total_vendido = fato_vendas.groupby('data_venda')['valor_monetario_total'].sum().reset_index()
#total_vendido.plot(label='Total Vendido', marker='o')
#plt.title('Total Vendido ao Longo do Ano')
#plt.xlabel('Data da Venda')
#plt.ylabel('Valor Monetário Total')

total_vendido["Month"] = total_vendido["data_venda"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", total_vendido["Month"].unique())

total_vendido_filtrado = total_vendido[total_vendido["Month"] == month]

col1, col2 = st.columns(2)

col1= total_vendido_filtrado.plot(label='Total Vendido', marker='o')
plt.title('Total Vendido ao Longo do Ano')
plt.xlabel('Data da Venda')
plt.ylabel('Valor Monetário Total')

#fig_prod = px.line(total_vendido_filtrado, x='data_venda', y='valor_monetario_total',
#                   title='grafico 1')
#col1.plotly_chart(fig_prod)

#total_vendido

#fig_prod = px.line(df_filtered, x="Date", y="Product line", 
#                  color="City", title="Faturamento por tipo de produto",
#                  orientation="h")
#col1.plotly_chart(fig_prod, use_container_width=True)

#3city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
#fig_city = px.bar(city_total, x="City", y="Total",
#                   title="Faturamento por filial")
#col3.plotly_chart(fig_city, use_container_width=True)
