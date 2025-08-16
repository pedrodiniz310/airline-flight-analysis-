import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Análise de Voos - Companhias Aéreas",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNÇÃO PARA CARREGAR E PREPARAR OS DADOS ---
@st.cache_data
def load_data():
    # Carregar o DataFrame
    df = pd.read_csv('airlines_flights_data.csv')
    # Limpeza e pré-processamento dos dados (do seu notebook)
    df['price'] = df['price'].astype('float64')
    mapeamento_nomes = {
        'Air_India': 'Air India',
        'GO_FIRST': 'Go First'
    }
    # Corrigindo nomes de companhias aéreas
    df['airline'] = df['airline'].replace(mapeamento_nomes, regex=False)
    mapeamento_horarios = {
        'Early_Morning': 'Early Morning',
        'Late_Night': 'Late Night' # Corrigido para 'Late Night'
    }
    
    df['departure_time'] = df['departure_time'].replace(mapeamento_horarios, regex=False)
    
    return df

# --- INÍCIO DA INTERFACE DO APLICATIVO ---
# Título principal
st.title("✈️ Painel de Análise de Voos")
st.markdown("Este é um painel interativo criado para analisar os dados de voos das principais companhias aéreas da India, "
"com base na análise exploratória desenvolvida a partir de dados públicos."
"")

# Carregar os dados e tratar erros de carregamento
try:
    df = load_data()
except FileNotFoundError:
    st.error("Erro: O arquivo 'airlines_flights_data.csv' não foi encontrado. Por favor, certifique-se de que ele está na mesma pasta que o arquivo `app.py`.")
    st.stop() #Interrompe a execução se o arquivo não for encontrado

# --- PALETA DE CORES FIXAS POR COMPANHIA ---
cores_por_companhia = {
    'Air India': '#1F4E79',
    'IndiGo': '#2E8B57',
    'SpiceJet': '#8B0000',
    'Vistara': '#4B0082',
    'Go First': '#696969',
    'Akasa Air': '#3B3B3B'
}

# --- BARRA LATERAL PARA NAVEGAÇÃO ---
st.sidebar.header("Menu de Análise")
pagina_selecionada = st.sidebar.radio(
    "Escolha uma seção para visualizar:",
    [
        "Visão Geral dos Dados", 
        "Análise das Companhias Aéreas", 
        "Análise de Preços", 
        "Análise Geográfica e Temporal",
        "Calculadora de Preço Médio (Interativo)"
    ]
)

# --- SEÇÃO: VISÃO GERAL DOS DADOS ---
if pagina_selecionada == "Visão Geral dos Dados":
    st.header("Visão Geral do Conjunto de Dados")
    st.markdown("Abaixo estão as primeiras linhas do conjunto de dados, que contém informações sobre voos, preços, duração e outros atributos.")
    
    if st.checkbox("Mostrar dados brutos"):
        st.dataframe(df)

    st.subheader("Informações Gerais")
    st.markdown(f"""
    - **Total de Registros:** O conjunto de dados possui **{df.shape[0]:,}** registros de voos.
    - **Colunas:** Inclui informações como companhia aérea, cidades de origem e destino, horários, classe de voo, duração, dias restantes para o voo e preço.
    """)
    
    st.subheader("Estatísticas Descritivas")
    st.write(df.describe())

# --- SEÇÃO: ANÁLISE DAS COMPANHIAS AÉREAS ---
elif pagina_selecionada == "Análise das Companhias Aéreas":
    st.header("Quais são as companhias aéreas mais populares?")

    st.markdown("O gráfico abaixo mostra o número total de voos registrados para cada companhia aérea no conjunto de dados. **Vistara** e **Air India** dominam em volume.")
    
    # Criamos 3 colunas. Usaremos a do meio (col2) para o gráfico.
    # Os números definem a proporção da largura. 0.1 para as margens, 0.8 para o gráfico.
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2: # Todo o código do gráfico vai aqui dentro
        fig1, ax1 = plt.subplots(figsize=(7, 4))
        sns.set_palette("deep")
        sns.countplot(data=df, y='airline', order=df['airline'].value_counts().index, ax=ax1)
        ax1.set_title('Número de Voos por Companhia Aérea', fontsize=16)
        ax1.set_xlabel('Número de Voos', fontsize=12)
        ax1.set_ylabel('Companhia Aérea', fontsize=12)
        st.pyplot(fig1)

    # --- Gráfico 2: Preço Médio por Companhia ---
    st.subheader("Qual o preço médio das passagens por companhia?")
    st.markdown("Analisando o preço médio, vemos que a **Vistara** e a **Air India** também possuem os tickets mais caros, o que pode estar relacionado à oferta de mais voos em classe executiva.")
    
    col4, col5, col6 = st.columns([0.2, 0.6, 0.2])
    
    with col5: # Colocando o segundo gráfico na coluna do meio
        media_precos_por_companhia = df.groupby('airline')['price'].mean().sort_values(ascending=False)
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        sns.barplot(x=media_precos_por_companhia.values, y=media_precos_por_companhia.index, ax=ax2, palette="viridis")
        ax2.set_title('Preço Médio por Companhia Aérea', fontsize=16)
        ax2.set_xlabel('Preço Médio (₹)', fontsize=12, labelpad=10)
        ax2.set_ylabel('Companhia Aérea', fontsize=12, labelpad=10)
        st.pyplot(fig2)

# --- SEÇÃO: ANÁLISE DE PREÇOS ---
elif pagina_selecionada == "Análise de Preços":
    st.header("Como os preços das passagens estão distribuídos?")
    st.markdown("A maioria das passagens se concentra na faixa de preço mais baixa (abaixo de 20.000₹). A longa cauda à direita indica a presença de voos mais caros, provavelmente de classe executiva.")
    
    col7, col8, col9 = st.columns([0.2, 0.6, 0.2])
    with col8:
    # Gráfico 3: Distribuição de Preços
        fig3, ax3 = plt.subplots(figsize=(7, 4))
        sns.histplot(data=df, x='price', bins=50, kde=True, ax=ax3, color="skyblue")
        ax3.set_title('Distribuição de Preços das Passagens Aéreas', fontsize=16)
        ax3.set_xlabel('Preço (₹)', fontsize=12, labelpad=10)
        ax3.set_ylabel('Frequência', fontsize=12, labelpad=10)
        st.pyplot(fig3)

    # Gráfico 4: Preços por Classe de Voo
    st.subheader("Relação de Preços por Classe de Voo")
    st.markdown("Como esperado, a classe Executiva (`Business`) tem um preço médio e uma variação de valores significativamente maiores em comparação com a classe Econômica (`Economy`).")
    col10, col11, col12 = st.columns([0.2, 0.6, 0.2])
    with col11:
        fig4, ax4 = plt.subplots(figsize=(7, 4)) # Tamanho ajustado para consistência
        sns.boxplot(data=df, x='class', y='price', ax=ax4, palette="coolwarm")
        ax4.set_title('Relação de Preços por Classe de Voo', fontsize=16)
        ax4.set_xlabel('Classe de Voo', fontsize=12, labelpad=10)
        ax4.set_ylabel('Preço (₹)', fontsize=12,labelpad=10)
        st.pyplot(fig4)

    # Gráfico 5 e 6: Relação com Duração e Dias Restantes
    st.subheader("Fatores que Influenciam o Preço")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Preço vs. Duração do Voo**")
        st.markdown("Há uma correlação positiva clara: voos mais longos tendem a ser mais caros.")
        fig5, ax5 = plt.subplots(figsize=(5, 4))
        sns.scatterplot(data=df, x='duration', y='price', alpha=0.5, s=20, ax=ax5)
        ax5.set_title('Preço vs. Duração do Voo')
        ax5.set_xlabel('Duração (horas)', labelpad=10)
        ax5.set_ylabel('Preço (₹)', labelpad=10)
        st.pyplot(fig5)
    
    with col2:
        st.markdown("**Preço vs. Dias Restantes**")
        st.markdown("O preço tende a aumentar quando a data do voo se aproxima.")
        fig6, ax6 = plt.subplots(figsize=(5, 4))
        sns.scatterplot(data=df, x='days_left', y='price', alpha=0.5, s=20, ax=ax6)
        ax6.set_title('Preço vs. Dias Restantes')
        ax6.set_xlabel('Dias Restantes para o Voo', labelpad=10)
        ax6.set_ylabel('Preço (₹)', labelpad=10)
        st.pyplot(fig6)
    
    # Gráfico 7: Mapa de Calor
    st.subheader("Mapa de Calor de Correlações")
    st.markdown("O mapa de calor confirma visualmente as correlações entre as variáveis numéricas.")
    col13, col14, col15 = st.columns([0.2, 0.6, 0.2])
    with col14:
        colunas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
        corrmat = df[colunas_numericas].corr()
        fig7, ax7 = plt.subplots(figsize=(7, 4)) # Tamanho ajustado para consistência
        mask = np.triu(np.ones_like(corrmat, dtype=bool))
        sns.heatmap(corrmat, vmax=.8, mask=mask, square=True, annot=True, cmap="YlGnBu", ax=ax7)
        st.pyplot(fig7)

# --- SEÇÃO: ANÁLISE GEOGRÁFICA E TEMPORAL ---
elif pagina_selecionada == "Análise Geográfica e Temporal":
    st.header("Distribuição de Voos por Localização e Horário")

    col1, col2 = st.columns(2)
    with col1:
        # Gráfico 8: Cidades de Origem
        st.subheader("Voos por Cidade de Origem")
        fig8, ax8 = plt.subplots(figsize=(8, 6))
        sns.countplot(data=df, y='source_city', order=df['source_city'].value_counts().index, ax=ax8, palette="crest")
        ax8.set_title('Distribuição por Cidade de Origem')
        ax8.set_xlabel('Número de Voos', labelpad=10)
        ax8.set_ylabel('Cidade de Origem', labelpad=10)
        st.pyplot(fig8)

    with col2:
        # Gráfico 9: Cidades de Destino
        st.subheader("Voos por Cidade de Destino")
        fig9, ax9 = plt.subplots(figsize=(8, 6))
        sns.countplot(data=df, y='destination_city', order=df['destination_city'].value_counts().index, ax=ax9, palette="flare")
        ax9.set_title('Distribuição por Cidade de Destino')
        ax9.set_xlabel('Número de Voos', labelpad=10)
        ax9.set_ylabel('Cidade de Destino', labelpad=10)
        st.pyplot(fig9)
    
    # Gráfico 10: Horários de Partida
    st.subheader("Distribuição de Voos por Horário de Partida")
    fig10, ax10 = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='departure_time', order=df['departure_time'].value_counts().index, ax=ax10, palette="magma")
    ax10.set_title('Distribuição por Horário de Partida')
    ax10.set_xlabel('Horário de Partida', labelpad=10)
    ax10.set_ylabel('Número de Voos', labelpad=10)
    plt.xticks(rotation=45)
    st.pyplot(fig10)

# --- SEÇÃO: CALCULADORA INTERATIVA ---
elif pagina_selecionada == "Calculadora de Preço Médio (Interativo)":
    st.header("🔍 Calcule o Preço Médio para um Voo Específico")
    st.markdown("Utilize os filtros abaixo para selecionar os parâmetros e descobrir o preço médio da passagem.")

    # Filtros para o usuário
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        companhia = st.selectbox("Companhia Aérea:", sorted(df['airline'].unique()))
    with col2:
        origem = st.selectbox("Cidade de Origem:", sorted(df['source_city'].unique()))
    with col3:
        destino = st.selectbox("Cidade de Destino:", sorted(df['destination_city'].unique()))
    with col4:
        classe = st.selectbox("Classe de Voo:", sorted(df['class'].unique()))

    # Botão para calcular
    if st.button("Calcular Preço Médio"):
        voos_filtrados = df[
            (df['airline'] == companhia) &
            (df['source_city'] == origem) &
            (df['destination_city'] == destino) &
            (df['class'] == classe)
        ]

        if not voos_filtrados.empty:
            preco_medio = voos_filtrados['price'].mean()
            st.success(f"O preço médio para esta rota é: **{preco_medio:.2f}₹**")
        else:
            st.error("Não foram encontrados voos com os critérios selecionados. Por favor, tente outra combinação.")

# --- RODAPÉ ---
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido a partir de um notebook de uma análise.")