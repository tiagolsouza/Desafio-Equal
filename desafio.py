import streamlit as st
import pandas as pd
import plotly.express as px
from millify import millify

st.set_page_config(layout="wide")
st.title('DASHBOARD')

@st.cache_data
def carrega_data(nome):
    tabela = pd.read_excel(nome)
    return tabela

# Carregar os dados
fato_vendas = carrega_data('fato_vendas.xlsx')
dim_produtos = carrega_data('dim_produtos.xlsx')
dim_familia_produtos = carrega_data('dim_familia_produtos.xlsx')
dim_vendedor = carrega_data('dim_vendedor.xlsx')

# Visualização do total vendido no ano e vendas ao longo do tempo
total_vendido = fato_vendas.groupby('data_venda')['valor_monetario_total'].sum().reset_index()

total_vendido["Month"] = total_vendido["data_venda"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", total_vendido["Month"].unique())

#=======Filtro mensal======
total_vendido_filtrado = total_vendido[total_vendido["Month"] == month]

#======Criando cards=======
col1, col2 = st.columns([2, 1])

total = float(fato_vendas['valor_monetario_total'].sum())
total_formatado = 'R$ ' + str(millify(total, precision=3))
total_mensal = float(total_vendido_filtrado['valor_monetario_total'].sum())
total_mensal = 'R$ ' + str(millify(total_mensal, precision=3))

col1 =  st.metric(label='TOTAL ARRECADADO ANUAL', value= total_formatado)
col2 = st.metric(label='TOTAL ARRECADADO MENSAL', value= total_mensal)

#======Criando graficos=======
col3, col4 = st.columns(2)

# Grafico de arrecadacao mensal
grafico1 = px.line(total_vendido_filtrado, x='data_venda', y='valor_monetario_total',
                   title='Arrecadação Mensal', labels= {'data_venda': 'Data de venda', 'valor_monetario_total': 'Total Arrecadado'})
col3.plotly_chart(grafico1, use_container_width=True)

#grafico de arrecadacao por familia
top_familias = fato_vendas.merge(dim_produtos, on='codigo_produto').merge(
    dim_familia_produtos, on='codigo_familia').groupby('descricaofamilia')['valor_monetario_total'].sum().nlargest(5).reset_index()

grafico2 = px.bar(top_familias, x="valor_monetario_total", y="descricaofamilia", 
                  title="Top 5 Famílias de Produtos para Campanhas em Dezembro",
                  labels= {'valor_monetario_total': 'Total Arrecadado', 'descricaofamilia': 'Familia de produtos'} )
col4.plotly_chart(grafico2, use_container_width=True)

# Proposição de três indicadores de performance de vendas por vendedor
indicadores_por_vendedor = fato_vendas.merge(dim_vendedor, on='codigo_vendedor')

# Exemplo de indicadores: média de valor monetário total, quantidade média de produtos vendidos, e total de vendas por vendedor
indicadores_vendedor = indicadores_por_vendedor.groupby('nome_vendedor').agg({'valor_monetario_total': ['mean', 'count', 'sum']}).reset_index()
indicadores_vendedor.columns = ['nome_vendedor', 'media_valor', 'quantidade', 'total_vendas']

# Identificação dos 5 melhores vendedores de 2022
top_vendedores_venda = indicadores_vendedor.nlargest(5, 'total_vendas')
top_vendedores_qtdade = indicadores_vendedor.nlargest(5, 'quantidade')
top_vendedores_media = indicadores_vendedor.nlargest(5, 'media_valor')

col5, col6, col7 = st.columns(3)

grafico3 = px.bar(top_vendedores_venda, x="total_vendas", y="nome_vendedor", 
                  title="Top 5 Vendedores  Totais",
                  labels= {'total_vendas': 'Vendas Totais', 'nome_vendedor': 'Vendedor'} )
col5.plotly_chart(grafico3, use_container_width=True)

grafico4 = px.bar(top_vendedores_qtdade, x="quantidade", y="nome_vendedor", 
                  title="Top 5 Vendedores por Quantidade",
                  labels= {'quantidade': 'Quantidade Vendida', 'nome_vendedor': 'Vendedor'} )
col6.plotly_chart(grafico4, use_container_width=True)

grafico5 = px.bar(top_vendedores_media, x="media_valor", y="nome_vendedor", 
                  title="Top 5 Vendedores por Média Vendida",
                  labels= {'media_valor': 'Média de vendas', 'nome_vendedor': 'Vendedor'} )
col7.plotly_chart(grafico5, use_container_width=True)
