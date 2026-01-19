# ============================================================================
# DASHBOARD INTERATIVO DE CONTAS A RECEBER
# Compatível com Streamlit
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard Contas a Receber",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título do Dashboard
st.title("💰 Dashboard de Contas a Receber")
st.markdown("---")

# ----------------------------------------------------------------------------
# FUNÇÃO PARA CARREGAR DADOS
# ----------------------------------------------------------------------------

@st.cache_data(ttl=300)  # Cache por 5 minutos
def carregar_dados():
    """
    Carrega e processa os dados da planilha do Google Sheets
    """
    # ID da planilha
    SHEET_ID = "1CbdRno9isBCkLKkGne4KJBUUQ1CVUl9kma5X1l608ng"
    SHEET_NAME = "A%20Receber"
    
    # URL da API de visualização do Google
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    
    # Ler dados
    df = pd.read_csv(url)
    
    # Identificar colunas automaticamente
    colunas_lower = {col.lower().strip(): col for col in df.columns}
    
    mapeamento = {}
    for palavra in ['vencimento', 'data', 'venc']:
        if palavra in colunas_lower:
            mapeamento['Vencimento'] = colunas_lower[palavra]
            break
    
    for palavra in ['valor', 'vlr']:
        if palavra in colunas_lower:
            mapeamento['Valor'] = colunas_lower[palavra]
            break
    
    for palavra in ['pagador', 'cliente']:
        if palavra in colunas_lower:
            mapeamento['Pagador'] = colunas_lower[palavra]
            break
    
    for palavra in ['pago', 'status']:
        if palavra in colunas_lower:
            mapeamento['Pago'] = colunas_lower[palavra]
            break
    
    # Renomear colunas
    df = df.rename(columns=mapeamento)
    
    # Converter valores monetários
    def converter_valor_br(valor):
        if pd.isna(valor):
            return 0.0
        valor_str = str(valor).strip()
        valor_str = valor_str.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        try:
            return float(valor_str)
        except:
            return 0.0
    
    df['Valor'] = df['Valor'].apply(converter_valor_br)
    
    # Converter datas
    df['Vencimento'] = pd.to_datetime(df['Vencimento'], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['Vencimento'])
    df = df.sort_values('Vencimento')
    
    # Tratar coluna Pago (se existir)
    if 'Pago' in df.columns:
        def verificar_pago(valor):
            if pd.isna(valor):
                return False
            valor_str = str(valor).strip().upper()
            return valor_str in ['TRUE', 'SIM', 'PAGO', '1', 'YES', 'S']
        df['Pago'] = df['Pago'].apply(verificar_pago)
    else:
        df['Pago'] = False
    
    return df

# ----------------------------------------------------------------------------
# CARREGAR DADOS
# ----------------------------------------------------------------------------

with st.spinner('📊 Carregando dados da planilha...'):
    try:
        df = carregar_dados()
        st.success(f'✅ {len(df)} registros carregados com sucesso!')
    except Exception as e:
        st.error(f'❌ Erro ao carregar dados: {str(e)}')
        st.stop()

# ----------------------------------------------------------------------------
# SIDEBAR - FILTROS
# ----------------------------------------------------------------------------

st.sidebar.header("🔍 Filtros")

# Filtro de Status de Pagamento
if 'Pago' in df.columns:
    status_options = {
        'Todos': None,
        'Pendentes': False,
        'Pagos': True
    }
    status_selecionado = st.sidebar.selectbox(
        "Status de Pagamento",
        options=list(status_options.keys()),
        index=1  # Padrão: Pendentes
    )
    
    # Aplicar filtro
    if status_options[status_selecionado] is not None:
        df_filtrado = df[df['Pago'] == status_options[status_selecionado]].copy()
    else:
        df_filtrado = df.copy()
else:
    df_filtrado = df.copy()
    status_selecionado = 'Todos'

# Filtro de Período
st.sidebar.markdown("---")
st.sidebar.subheader("📅 Período")

periodo_options = ['Personalizado', 'Hoje', 'Próximos 7 dias', 'Próximos 30 dias', 'Tudo']
periodo = st.sidebar.selectbox("Selecione o período", periodo_options, index=2)

hoje = datetime.now().date()

if periodo == 'Hoje':
    data_inicio = hoje
    data_fim = hoje
elif periodo == 'Próximos 7 dias':
    data_inicio = hoje
    data_fim = hoje + timedelta(days=7)
elif periodo == 'Próximos 30 dias':
    data_inicio = hoje
    data_fim = hoje + timedelta(days=30)
elif periodo == 'Tudo':
    data_inicio = df_filtrado['Vencimento'].min().date()
    data_fim = df_filtrado['Vencimento'].max().date()
else:  # Personalizado
    col1, col2 = st.sidebar.columns(2)
    with col1:
        data_inicio = st.date_input(
            "De",
            value=hoje,
            min_value=df_filtrado['Vencimento'].min().date(),
            max_value=df_filtrado['Vencimento'].max().date()
        )
    with col2:
        data_fim = st.date_input(
            "Até",
            value=hoje + timedelta(days=7),
            min_value=df_filtrado['Vencimento'].min().date(),
            max_value=df_filtrado['Vencimento'].max().date()
        )

# Aplicar filtro de período
df_filtrado = df_filtrado[
    (df_filtrado['Vencimento'].dt.date >= data_inicio) &
    (df_filtrado['Vencimento'].dt.date <= data_fim)
]

# ----------------------------------------------------------------------------
# MÉTRICAS PRINCIPAIS
# ----------------------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    total_valor = df_filtrado['Valor'].sum()
    st.metric(
        "💰 Valor Total",
        f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    )

with col2:
    qtd_registros = len(df_filtrado)
    st.metric("📋 Quantidade", qtd_registros)

with col3:
    if len(df_filtrado) > 0:
        valor_medio = df_filtrado['Valor'].mean()
        st.metric(
            "📊 Valor Médio",
            f"R$ {valor_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )

st.markdown("---")

# ----------------------------------------------------------------------------
# GRÁFICO DE BARRAS EMPILHADAS
# ----------------------------------------------------------------------------

if len(df_filtrado) > 0:
    # Formatar dados para tooltips
    df_filtrado['Data_Formatada'] = df_filtrado['Vencimento'].dt.strftime('%d/%m/%Y')
    df_filtrado['Valor_Formatado'] = df_filtrado['Valor'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    )
    
    # Criar gráfico
    fig = px.bar(
        df_filtrado,
        x='Vencimento',
        y='Valor',
        color='Pagador',
        title=f'📊 Contas a Receber - {status_selecionado}',
        labels={
            'Vencimento': 'Data de Vencimento',
            'Valor': 'Valor (R$)',
            'Pagador': 'Cliente/Pagador'
        },
        template='plotly_dark',
        text='Valor',
        custom_data=['Pagador', 'Data_Formatada', 'Valor_Formatado']
    )
    
    # Configurar tooltips e rótulos
    fig.update_traces(
        texttemplate='R$ %{text:,.0f}',
        textposition='inside',
        textfont_size=10,
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                      'Valor: %{customdata[2]}<br>' +
                      '<extra></extra>'
    )
    
    # Calcular totais por data para referência
    totais_por_data = df_filtrado.groupby('Vencimento')['Valor'].sum().reset_index()
    totais_por_data['Total_Formatado'] = totais_por_data['Valor'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    )
    
    # Configurar layout
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='Data de Vencimento',
        yaxis_title='Valor (R$)',
        font=dict(size=12),
        height=600,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        margin=dict(r=150),
        xaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikedash='solid'
        )
    )
    
    # Formatar eixo Y
    fig.update_yaxes(
        tickprefix='R$ ',
        tickformat=',.0f'
    )
    
    # Configurar eixo X com botões de seleção rápida
    fig.update_xaxes(
        range=[data_inicio, data_fim],
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="Dia", step="day", stepmode="backward"),
                dict(count=7, label="Semana", step="day", stepmode="backward"),
                dict(count=1, label="Mês", step="month", stepmode="backward"),
                dict(count=3, label="3 Meses", step="month", stepmode="backward"),
                dict(step="all", label="Tudo")
            ]),
            x=0,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
        hoverformat='%d/%m/%Y'
    )
    
    # Exibir gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    # ----------------------------------------------------------------------------
    # TABELA DE DETALHES
    # ----------------------------------------------------------------------------
    
    st.markdown("---")
    st.subheader("📋 Detalhamento")
    
    # Preparar dados para exibição
    df_display = df_filtrado[['Vencimento', 'Pagador', 'Valor']].copy()
    df_display['Vencimento'] = df_display['Vencimento'].dt.strftime('%d/%m/%Y')
    df_display['Valor'] = df_display['Valor'].apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    )
    
    if 'Pago' in df_filtrado.columns:
        df_display['Status'] = df_filtrado['Pago'].apply(lambda x: '✅ Pago' if x else '⏳ Pendente')
    
    # Exibir tabela
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
else:
    st.warning("⚠️ Nenhum registro encontrado para os filtros selecionados.")

# ----------------------------------------------------------------------------
# RODAPÉ
# ----------------------------------------------------------------------------

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Dashboard desenvolvido com Streamlit | Dados atualizados automaticamente
    </div>
    """,
    unsafe_allow_html=True
)
