import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. SETUP DE ALTA PERFORMANCE E CSS PREMIUM
# ==========================================
st.set_page_config(page_title="Sincro | Gestão Premium", page_icon="logo.png", layout="wide", initial_sidebar_state="expanded")

# Injeção de CSS para transformar o Streamlit em um WebApp de Luxo (Light Clean)
st.markdown("""
<style>
    /* Cor de fundo de todo o sistema (Off-white elegante) */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Esconde o menu padrão do Streamlit e o rodapé */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Customização da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Títulos e Textos globais */
    h1, h2, h3, p {
        color: #1E293B;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Cartão Principal Escuro (Estilo a imagem de referência) */
    .main-card {
        background-color: #1E293B;
        padding: 25px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .main-card h2, .main-card p { color: white !important; }
    
    /* Cartões Brancos de Métricas */
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    
    /* Cor Verde Sincro para destaques */
    .sincro-green { color: #00B37E; font-weight: bold; }
    .sincro-red { color: #EF4444; font-weight: bold; }
    
    /* Linha sutil de divisão */
    hr { border-top: 1px solid #E5E7EB; margin-top: 10px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. GERAÇÃO DE DADOS MOCK (Simulação para o visual)
# (Futuramente vamos conectar isso de volta à sua planilha real)
# ==========================================
mes_atual = "Junho 2026"
receitas = 45500.00
compromissos = 28600.00
ja_pago = 15200.00
em_aberto = compromissos - ja_pago
sobra_prevista = receitas - compromissos
indice_saude = int((sobra_prevista / receitas) * 100) if receitas > 0 else 0

# ==========================================
# 3. MENU LATERAL (SIDEBAR)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3592/3592885.png", width=60) # Ícone provisório caso a logo não carregue
st.sidebar.markdown("<h2 style='color: #00B37E;'>Sincro Gestão</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size: 12px; color: #64748B;'>Controle Premium Privado</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    ["📊 Dashboard Executivo", "📈 Análise Gráfica", "🗓️ Lançamentos", "⚙️ Configurações"]
)

# ==========================================
# 4. TELA 1: DASHBOARD EXECUTIVO (A Visão Limpa)
# ==========================================
if menu == "📊 Dashboard Executivo":
    st.markdown(f"<p style='color: #64748B; font-weight: bold; margin-bottom: -15px;'>FINANCEIRO PRIVADO | {mes_atual.upper()}</p>", unsafe_allow_html=True)
    st.markdown("<h1>Dashboard Executivo</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B;'>Organização inteligente. Receitas, contas e alertas em um painel pensado para decisão rápida.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # BLOCO PRINCIPAL: Leitura do Mês (Estilo Referência)
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        st.markdown(f"""
        <div class="main-card">
            <p style='font-size: 14px; color: #94A3B8 !important; text-transform: uppercase;'>Leitura do Mês</p>
            <h2 style='font-size: 32px; margin-top: -10px;'>Sobra prevista de R$ {sobra_prevista:,.2f}</h2>
            <p style='font-size: 14px; color: #CBD5E1 !important;'>O painel cruza receitas, contas abertas e limites antes do dinheiro sair da conta.</p>
            <div style='display: flex; gap: 40px; margin-top: 20px;'>
                <div>
                    <span style='font-size: 12px; color: #94A3B8;'>Receitas Confirmadas</span><br>
                    <span style='font-size: 18px; font-weight: bold;'>R$ {receitas:,.2f}</span>
                </div>
                <div>
                    <span style='font-size: 12px; color: #94A3B8;'>Compromissos Totais</span><br>
                    <span style='font-size: 18px; font-weight: bold;'>R$ {compromissos:,.2f}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style='text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
            <p style='font-size: 14px; color: #64748B; font-weight: bold;'>ÍNDICE DE CONTROLE</p>
            <h1 style='color: #00B37E; font-size: 48px; margin: 0;'>{indice_saude}</h1>
            <p style='font-size: 12px; color: #94A3B8;'>Quanto maior, menor o risco de surpresa no mês.</p>
        </div>
        """, unsafe_allow_html=True)

    # LINHA DE MÉTRICAS SECUNDÁRIAS (Quatro bloquinhos limpos)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card'><span style='font-size: 12px; color: #64748B;'>TOTAL RECEITAS</span><br><span class='sincro-green' style='font-size: 22px;'>R$ {receitas:,.2f}</span></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><span style='font-size: 12px; color: #64748B;'>JÁ PAGO</span><br><span style='font-size: 22px; color: #1E293B;'>R$ {ja_pago:,.2f}</span></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><span style='font-size: 12px; color: #64748B;'>EM ABERTO</span><br><span class='sincro-red' style='font-size: 22px;'>R$ {em_aberto:,.2f}</span></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card'><span style='font-size: 12px; color: #64748B;'>SOBRA PROTEGIDA</span><br><span style='font-size: 22px; color: #1E293B;'>R$ {sobra_prevista:,.2f}</span></div>", unsafe_allow_html=True)

    # INSIGHTS INTELIGENTES
    st.markdown("<h3>Insights Inteligentes ✨</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14px; color: #64748B;'>O que merece a sua atenção imediata hoje:</p>", unsafe_allow_html=True)
    
    i1, i2, i3 = st.columns(3)
    i1.info("**Aviso de Vencimento:** Há 3 boletos de fornecedores vencendo hoje no valor de R$ 4.200,00.")
    i2.success("**Meta Atingida:** A receita de vendas ultrapassou a meta de segurança do mês.")
    i3.warning("**Alerta de Categoria:** Os gastos com Logística estão 15% acima da média histórica.")

# ==========================================
# 5. TELA 2: ANÁLISE GRÁFICA (Aprofundamento)
# ==========================================
elif menu == "📈 Análise Gráfica":
    st.markdown("<h1>Análise Profunda e Gráficos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B;'>Explore visualmente para onde o dinheiro está indo.</p><hr>", unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Fluxo de Caixa (Últimos 6 meses)</h4>", unsafe_allow_html=True)
        # Gráfico de Barras Elegante (Plotly)
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        rec = [35000, 38000, 32000, 41000, 44000, 45500]
        desp = [28000, 29000, 31000, 27000, 28500, 28600]
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=meses, y=rec, name='Receitas', marker_color='#00B37E'))
        fig1.add_trace(go.Bar(x=meses, y=desp, name='Despesas', marker_color='#EF4444'))
        fig1.update_layout(barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_g2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Composição de Custos (Neste Mês)</h4>", unsafe_allow_html=True)
        # Gráfico de Rosca Elegante
        categorias = ['Folha Pagamento', 'Impostos', 'Logística', 'Marketing', 'Manutenção']
        valores = [12000, 5000, 4500, 3000, 4100]
        
        fig2 = go.Figure(data=[go.Pie(labels=categorias, values=valores, hole=.5)])
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. TELA 3 E 4: PLACEHOLDERS
# ==========================================
elif menu == "🗓️ Lançamentos":
    st.markdown("<h1>Lançamentos e Base de Dados</h1>", unsafe_allow_html=True)
    st.info("Aqui entrará a tabela inteligente com os dados da sua planilha. Área de controle minucioso.")
    
elif menu == "⚙️ Configurações":
    st.markdown("<h1>Configurações do Sistema</h1>", unsafe_allow_html=True)
    st.warning("Área restrita. Ajustes de metas, troca de logo e configuração de e-mails automáticos.")