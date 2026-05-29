import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import urllib.parse

# ==========================================
# 1. SETUP DE ALTA PERFORMANCE E CSS
# ==========================================
st.set_page_config(page_title="Sincro | Portal Executivo", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    html, body, [class*="css"]  { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0B0E14;}
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} 
    
    div[data-testid="metric-container"] { background: linear-gradient(145deg, #151923, #1A1F2B); border-top: 3px solid #00E676; padding: 15px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    div[data-testid="metric-container"] label { color: #8A98AC !important; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;}
    div[data-testid="metric-container"] div { color: #FFFFFF !important; font-size: 26px; font-weight: 900;}
    
    .block-container { padding-top: 0rem; padding-bottom: 1rem; max-width: 98%; }
    .streamlit-expanderHeader { font-size: 15px !important; color: #00E676 !important; font-weight: 600 !important; }
    .ai-summary-box { background: rgba(0, 230, 118, 0.05); border-left: 4px solid #00E676; border-radius: 4px; padding: 15px 20px; margin-bottom: 25px; color: #E2E8F0; font-size: 15px; line-height: 1.5; }
    [data-testid="stSidebar"] { background-color: #12161E; border-right: 1px solid #1F2937; }
    
    .ticker-container { width: 100%; overflow: hidden; background-color: #1A1F2B; border-bottom: 2px solid #00E676; padding: 12px 0; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);}
    .ticker-text { display: inline-block; white-space: nowrap; animation: scrolling-left 35s linear infinite; font-size: 15px; color: #E2E8F0; font-weight: 600;}
    .ticker-text span { color: #00E676; }
    .ticker-text .alert { color: #FF4B4B; }
    @keyframes scrolling-left { 0% { transform: translateX(100vw); } 100% { transform: translateX(-100vw); } }
    
    .filter-bar { background-color: #151923; padding: 15px; border-radius: 8px; border: 1px solid #1F2937; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. O LETREIRO DESLIZANTE & CABEÇALHO DO USUÁRIO
# ==========================================
col_logo_top, col_user_top = st.columns([1, 1])
with col_user_top:
    st.markdown("<div style='text-align: right; color: #8A98AC; font-size: 14px; padding-top: 10px;'>👤 Admin: <b>Leandro</b> | 🟢 Sistema Online</div>", unsafe_allow_html=True)

st.markdown("""
<div class="ticker-container">
    <div class="ticker-text">
        🌐 SELIC ATUAL: <span>10.50%</span> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        🚨 INADIMPLÊNCIA: <strong class="alert">R$ 4.300 em contas vencidas de clientes.</strong> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        🎯 META MENSAL: Faltam R$ 12.500 para atingir o alvo. &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        💡 ALERTA SINCRO: Despesa com combustível subiu 8% este mês.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. MOTOR DE DADOS REAIS
# ==========================================
meses_ordem = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
mapa_meses = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
status_conexao = "🔴 A usar dados de demonstração (Falha na conexão)"

def limpar_moeda(x):
    x = str(x).strip()
    if ',' in x and '.' in x:
        x = x.replace('.', '').replace(',', '.') 
    elif ',' in x:
        x = x.replace(',', '.') 
    return float(x) if x != 'nan' and x != '' else 0.0

@st.cache_data(ttl=30)
def puxar_base_mestre():
    try:
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTTiSDMnchwFBa1NWybL1B1zxH6V2tNfxqYm2vI-oHCiCGGRnmYee9UMqyrlQ8Iff42Bihzxg5qBTbx/pub?gid=0&single=true&output=csv"
        df = pd.read_csv(url, sep=None, engine='python')
        df['Valor'] = df['Valor'].apply(limpar_moeda)
        df['Data_Pagamento'] = pd.to_datetime(df['Data_Pagamento'], errors='coerce')
        df['Mês_Nome'] = df['Data_Pagamento'].dt.month.map(mapa_meses)
        df['Status'] = df['Status'].astype(str).str.strip().str.upper()
        df['Tipo_Movimento'] = df['Tipo_Movimento'].astype(str).str.strip().str.upper()
        df['Categoria'] = df['Categoria'].astype(str)
        return df
    except Exception as e:
        return str(e) 

df_bruto = puxar_base_mestre()
base_sucesso = isinstance(df_bruto, pd.DataFrame) and not df_bruto.empty

dias = np.arange(1, 31)
recebimentos_diarios = np.random.uniform(2000, 8000, 30)
pagamentos_diarios = np.random.uniform(1000, 9000, 30)
df_aging = pd.DataFrame({"Vencimento": ["No Prazo", "1-15 Dias", "16-30 Dias", "31-60 Dias", "+60 Dias"], "A Receber": [85, 22, 15, 8, 5], "A Pagar": [60, 10, 5, 2, 0]})
df_funnel = pd.DataFrame(dict(etapa=["Visitantes na Loja", "Orçamentos Solicitados", "Negociações", "Vendas Fechadas"], valores=[5400, 1200, 450, 210]))

# ==========================================
# 4. MENU LATERAL
# ==========================================
with st.sidebar:
    st.write("") 
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_logo = os.path.join(diretorio_atual, "logo.png")
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        if os.path.exists(caminho_logo):
            st.image(caminho_logo, use_container_width=True)
        else:
            st.markdown("<h2 style='text-align: center; color: #00E676; font-weight: 900;'>SINCRO</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = option_menu(None, ["Cockpit Gerencial", "Saúde Financeira e Caixa", "Frota e Logística", "Cofre (Metas Futuras)", "CRM e Cobrança", "Simulador de Cenários"],
        icons=["speedometer", "cash-stack", "truck", "safe", "whatsapp", "sliders"], default_index=0,
        styles={"container": {"background-color": "transparent", "padding": "0"}, "icon": {"color": "#8A98AC", "font-size": "16px"}, "nav-link": {"font-size": "14px", "color": "#E2E8F0", "margin":"2px", "border-radius": "5px", "--hover-color": "#1A1F2B"}, "nav-link-selected": {"background-color": "#00E676", "color": "#000000", "font-weight": "bold"}})

# ==========================================
# 5. ROTEAMENTO DAS TELAS
# ==========================================
if menu == "Cockpit Gerencial":
    st.markdown("<div class='filter-bar'>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        ano_filtro = st.selectbox("📅 Exercício (Ano)", ["Todos", "2026"])
    with f_col2:
        meses_disponiveis = ["Visão Geral (Todos)"] + meses_ordem
        mes_filtro = st.selectbox("📆 Mês de Análise", meses_disponiveis)
    with f_col3:
        conta_filtro = st.selectbox("🏢 Conta/Unidade", ["Consolidado DRE", "Loja Física", "Digital"])
    st.markdown("</div>", unsafe_allow_html=True)

    if base_sucesso:
        status_conexao = "✅ Conectado à Base Mestre (Dados Reais do Google Sheets)"
        df_filtrado = df_bruto.copy()
        if mes_filtro != "Visão Geral (Todos)":
            df_filtrado = df_filtrado[df_filtrado['Mês_Nome'] == mes_filtro]
            
        df_concluido = df_filtrado[df_filtrado['Status'] == 'CONCLUÍDO']
        
        receita_total = df_concluido[df_concluido['Tipo_Movimento'] == 'ENTRADA']['Valor'].sum()
        df_saidas = df_concluido[df_concluido['Tipo_Movimento'] == 'SAÍDA']
        custo_fixo_total = df_saidas[df_saidas['Categoria'].str.contains('Despesas Fixas', case=False, na=False)]['Valor'].sum()
        custo_var_total = df_saidas[df_saidas['Categoria'].str.contains('Custos Variáveis', case=False, na=False)]['Valor'].sum()
        lucro_total = receita_total - custo_fixo_total - custo_var_total
        margem_total = (lucro_total / receita_total * 100) if receita_total > 0 else 0
        
        df_evolucao = df_bruto[df_bruto['Status'] == 'CONCLUÍDO']
        faturamento_evol = df_evolucao[df_evolucao['Tipo_Movimento'] == 'ENTRADA'].groupby('Mês_Nome')['Valor'].sum().reindex(meses_ordem).fillna(0).tolist()
        custos_fixos_evol = df_evolucao[(df_evolucao['Tipo_Movimento'] == 'SAÍDA') & (df_evolucao['Categoria'].str.contains('Despesas Fixas', case=False, na=False))].groupby('Mês_Nome')['Valor'].sum().reindex(meses_ordem).fillna(0).tolist()
        custos_var_evol = df_evolucao[(df_evolucao['Tipo_Movimento'] == 'SAÍDA') & (df_evolucao['Categoria'].str.contains('Custos Variáveis', case=False, na=False))].groupby('Mês_Nome')['Valor'].sum().reindex(meses_ordem).fillna(0).tolist()
        top_despesas = df_saidas.groupby('Categoria')['Valor'].sum().sort_values(ascending=True).tail(5).reset_index()
        todas_despesas_donut = df_saidas.groupby('Categoria')['Valor'].sum().reset_index()
    else:
        receita_total, custo_fixo_total, lucro_total, margem_total = 160000, 50000, 60000, 37.5
        faturamento_evol = [110, 125, 130, 145, 160, 155, 175, 190, 210, 205, 230, 260] 
        custos_fixos_evol = [45, 45, 48, 48, 50, 50, 52, 52, 55, 55, 58, 60]
        custos_var_evol = [30, 35, 40, 42, 50, 45, 55, 60, 65, 62, 70, 85]
        top_despesas = pd.DataFrame({"Categoria": ["Energia", "Marketing", "Logística", "Impostos", "Folha"], "Valor": [8, 12, 18, 25, 45]})
        todas_despesas_donut = pd.DataFrame({"Categoria": ["Folha", "Impostos", "Logística", "Marketing", "Sistemas", "Materiais"], "Valor": [45, 25, 18, 12, 8, 15]})

    st.markdown(f"<p style='color: {'#00E676' if '✅' in status_conexao else '#FF4B4B'}; font-size: 12px; margin-bottom: 0px;'>{status_conexao}</p>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FFFFFF; font-weight: 800; margin-top:0px;'>Painel de Resultados Operacionais</h2>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Faturação (Entradas)", f"R$ {receita_total:,.2f}")
    with c2: st.metric("Custo Fixo Total", f"R$ {custo_fixo_total:,.2f}", delta_color="inverse")
    with c3: st.metric("Lucro Líquido (Sobrou)", f"R$ {lucro_total:,.2f}")
    with c4: st.metric("Margem Real (%)", f"{margem_total:.1f}%")

    st.write("---")
    
    col_master, col_ofensores = st.columns([2.5, 1.5])
    with col_master:
        fig_master = go.Figure()
        fig_master.add_trace(go.Bar(x=meses_ordem, y=custos_fixos_evol, name="Custos Fixos", marker_color="#1F2937"))
        fig_master.add_trace(go.Bar(x=meses_ordem, y=custos_var_evol, name="Custos Variáveis", marker_color="#FF4B4B"))
        fig_master.add_trace(go.Bar(x=meses_ordem, y=faturamento_evol, name="Receitas", marker_color="#00E676", opacity=0.7, text=faturamento_evol, textposition='outside'))
        fig_master.update_layout(title="📈 Evolução Mensal (Receitas vs Saídas)", barmode='overlay', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.1), yaxis=dict(showticklabels=False, showgrid=False))
        st.plotly_chart(fig_master, use_container_width=True)

    with col_ofensores:
        if not top_despesas.empty:
            fig_top = px.bar(top_despesas, x='Valor', y='Categoria', orientation='h', title="🔥 Maiores Despesas (Top 5)", text_auto='.2s')
            fig_top.update_traces(marker_color='#FF4B4B', textfont_size=12, textangle=0, textposition="outside")
            fig_top.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showticklabels=False, showgrid=False), yaxis=dict(title=""))
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.warning("Sem despesas lançadas no período.")

    st.write("---")
    c_aging, c_donut, c_gauge = st.columns(3)
    with c_aging:
        fig_aging = go.Figure()
        fig_aging.add_trace(go.Bar(x=df_aging["Vencimento"], y=df_aging["A Receber"], name="A Receber", marker_color="#3B82F6"))
        fig_aging.add_trace(go.Bar(x=df_aging["Vencimento"], y=df_aging["A Pagar"], name="A Pagar", marker_color="#FF4B4B"))
        fig_aging.update_layout(title="⚖️ Fôlego de Caixa Diário", barmode='group', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=-0.2), yaxis=dict(gridcolor="#1F2937"))
        st.plotly_chart(fig_aging, use_container_width=True)
            
    with c_donut:
        if not todas_despesas_donut.empty:
            fig_donut = px.pie(todas_despesas_donut, values='Valor', names='Categoria', hole=0.65, title="🍰 Divisão de Custos")
            fig_donut.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#0B0E14', width=2)))
            fig_donut.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_donut, use_container_width=True)
        
    with c_gauge:
        fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = 85, title = {'text': "% da Meta de Vendas", 'font': {'color': '#8A98AC', 'size': 14}}, number = {'font': {'color': '#00E676', 'size': 40}, 'suffix': "%"}, gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00E676"}, 'bgcolor': "#151923", 'steps': [{'range': [0, 50], 'color': "#FF4B4B"}, {'range': [50, 80], 'color': "#F59E0B"}, {'range': [80, 100], 'color': "rgba(0, 230, 118, 0.2)"}], 'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 80}}))
        fig_gauge.update_layout(margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor="rgba(0,0,0,0)", height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)


# ==========================================
# NOVO: MÓDULO CRM E COBRANÇA (FIM DO FIADO)
# ==========================================
elif menu == "CRM e Cobrança":
    st.markdown("<h2 style='color: #00E676; font-weight: 800;'>Central de Recuperação de Crédito</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8A98AC; font-size: 16px;'>Identifique rapidamente quem está devendo e dispare lembretes educados de cobrança com apenas 1 clique.</p>", unsafe_allow_html=True)
    
    # Criando dados fictícios para o exemplo (no futuro, vêm do Excel)
    dados_inadimplencia = {
        "Cliente": ["João Silva (Oficina Centro)", "Fazenda São José", "Mercadinho do Bairro", "Carlos Eduardo"],
        "Valor": [1450.00, 3200.00, 890.50, 450.00],
        "Dias de Atraso": [12, 28, 5, 45],
        # Telefones com DDD, mas sem formatação, para a URL funcionar. Coloque um número de teste válido seu no lugar para testar!
        "Telefone_WPP": ["5534999999999", "5534988888888", "5534977777777", "5534966666666"]
    }
    df_devedores = pd.DataFrame(dados_inadimplencia)
    
    st.write("---")
    
    # Construção da Lista Visual de Cobrança
    for index, row in df_devedores.iterrows():
        cliente = row['Cliente']
        valor = row['Valor']
        atraso = row['Dias de Atraso']
        telefone = row['Telefone_WPP']
        
        # O Texto da Mensagem já pronto para o cliente não pensar
        mensagem = f"Olá, tudo bem? Aqui é do financeiro da empresa. Notamos em nosso sistema que há uma pendência no valor de R$ {valor:,.2f} referente aos dias anteriores. Podemos te ajudar com algo para regularizarmos isso? Qualquer dúvida estou à disposição!"
        
        # Transforma o texto para um formato que o link da internet entende (URL Encoded)
        mensagem_codificada = urllib.parse.quote(mensagem)
        link_whatsapp = f"https://wa.me/{telefone}?text={mensagem_codificada}"
        
        # A Caixa visual do devedor
        st.markdown(f"""
        <div style="background-color: #1A1F2B; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #FF4B4B; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
            <div>
                <h4 style="color: #E2E8F0; margin: 0; font-size: 18px;">{cliente}</h4>
                <p style="color: #8A98AC; margin: 5px 0 0 0; font-size: 15px;">Dívida: <strong style="color: #FF4B4B; font-size: 18px;">R$ {valor:,.2f}</strong> &nbsp;|&nbsp; Atraso: <strong style="color: #F59E0B;">{atraso} dias</strong></p>
            </div>
            <div>
                <a href="{link_whatsapp}" target="_blank" style="background-color: #25D366; color: #000000; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px; display: inline-block;">💬 Cobrar via WhatsApp</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with st.expander("💡 Como esta tela aumenta meu faturamento?"):
        st.markdown("O brasileiro tem vergonha de cobrar. Esta tela tira a emoção do jogo. Você entra, vê a dívida, clica no botão verde e o sistema faz o trabalho 'chato' de escrever a cobrança de forma educada e profissional. A inadimplência costuma cair pela metade nos dois primeiros meses de uso.")

# ==========================================
# DEMAIS MÓDULOS INTACTOS
# ==========================================
elif menu == "Saúde Financeira e Caixa":
    st.markdown("<h2 style='color: #00E676; font-weight: 800;'>Radiografia da Semana</h2>", unsafe_allow_html=True)
    col_alert, col_action = st.columns([1, 1.5])
    with col_alert:
        st.markdown("""<div style="background-color: #251012; border: 1px solid #FF4B4B; padding: 25px; border-radius: 8px;">
            <h4 style="color: #FF4B4B; margin-top: 0; font-weight: 800;">🚨 O QUE EU PAGO ESTA SEMANA?</h4>
            <h1 style="color: #FFFFFF; font-size: 45px; margin: 10px 0;">R$ 18.450</h1>
            <p style="color: #E2E8F0; font-size: 15px;">Deste total, <strong>R$ 8.200</strong> são para Folha.</p></div>""", unsafe_allow_html=True)
    with col_action:
        st.markdown("""<div style="background-color: #1A1F2B; border: 1px solid #3B82F6; padding: 25px; border-radius: 8px;">
            <h4 style="color: #3B82F6; margin-top: 0; font-weight: 800;">🧠 PLANO DE AÇÃO SINCRO</h4>
            <ul style="color: #E2E8F0; font-size: 15px; padding-left: 20px;">
                <li><strong>Dinheiro em Caixa:</strong> R$ 12.000 disponíveis hoje.</li>
                <li><strong>Furo:</strong> Faltam <span style="color: #FF4B4B; font-weight: bold;">R$ 6.450</span>.</li>
                <li><strong>Ação:</strong> Cobre os R$ 4.300 em atraso hoje e negocie o restante. Evite cheque especial!</li></ul></div>""", unsafe_allow_html=True)
    st.write("---")
    st.markdown("#### 📅 Calendário de Contas: Entradas vs Saídas Diárias")
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Bar(x=dias, y=recebimentos_diarios, name="Dinheiro que Entra", marker_color="#00E676"))
    fig_daily.add_trace(go.Bar(x=dias, y=-pagamentos_diarios, name="Contas a Pagar", marker_color="#FF4B4B"))
    fig_daily.update_layout(barmode='relative', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", hovermode="x unified", yaxis=dict(gridcolor="#1F2937"))
    st.plotly_chart(fig_daily, use_container_width=True)

elif menu == "Frota e Logística":
    st.markdown("<h2 style='color: #00E676; font-weight: 800;'>Auditoria de Frota e Operação</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Gasto com Diesel (Mês)", "R$ 18.400", "▲ 8%", delta_color="inverse")
    with c2: st.metric("Custo de Manutenção", "R$ 4.200", "Troca Pneus", delta_color="inverse")
    with c3: st.metric("Média KM/Litro", "6.2 km/L", "▼ -0.5", delta_color="inverse")
    st.write("---")
    st.markdown("#### 🚚 Evolução Mensal: Custo de Combustível vs KM Rodado")
    fig_frota = go.Figure()
    fig_frota.add_trace(go.Bar(x=meses_ordem[:6], y=[12, 13, 12, 15, 16, 18], name="Custo Diesel (Mil)", marker_color="#F59E0B"))
    fig_frota.add_trace(go.Scatter(x=meses_ordem[:6], y=[2000, 2100, 2050, 2200, 2150, 2100], name="KM Rodado", yaxis="y2", line=dict(color="#3B82F6", width=3)))
    fig_frota.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", hovermode="x unified", yaxis=dict(gridcolor="#1F2937"), yaxis2=dict(overlaying="y", side="right"))
    st.plotly_chart(fig_frota, use_container_width=True)

elif menu == "Cofre (Metas Futuras)":
    st.markdown("<h2 style='color: #00E676; font-weight: 800;'>Cofre de Provisionamento</h2>", unsafe_allow_html=True)
    st.progress(0.4) 
    st.caption("R$ 18.000 guardados para 13º Salário (Faltam R$ 27.000)")
    st.write("---")
    st.progress(0.85)
    st.caption("R$ 10.200 guardados para Seguro Frota (Faltam R$ 1.800)")

elif menu == "Simulador de Cenários":
    st.markdown("<h2 style='color: #00E676; font-weight: 800;'>Simulador de Impacto Financeiro</h2>", unsafe_allow_html=True)
    col_controles, col_grafico = st.columns([1, 2])
    with col_controles:
        var_vendas = st.slider("Aumentar/Cair Vendas (%)", min_value=-30, max_value=50, value=0, step=1)
        var_custo = st.slider("Aumento no Custo (%)", min_value=-20, max_value=40, value=0, step=1)
        nova_receita = 150000 * (1 + var_vendas/100)
        novo_custo = 90000 * (1 + var_vendas/100) * (1 + var_custo/100)
        st.write("---")
        st.metric("Lucro Final da Simulação", f"R$ {nova_receita - novo_custo:,.2f}")
    with col_grafico:
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(name='Hoje', x=['Vendas', 'Custos', 'Lucro'], y=[150000, 90000, 60000], marker_color='#1F2937'))
        fig_sim.add_trace(go.Bar(name='Simulado', x=['Vendas', 'Custos', 'Lucro'], y=[nova_receita, novo_custo, nova_receita-novo_custo], marker_color=['#00E676', '#FF4B4B', '#3B82F6']))
        fig_sim.update_layout(barmode='group', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#1F2937"))
        st.plotly_chart(fig_sim, use_container_width=True)