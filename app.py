import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="Eficiência Energética - Vitalis Energia", layout="wide")

# --- EXIBIÇÃO DO LOGO CENTRALIZADO ---
logo_path = "logo.jpg"
if os.path.exists(logo_path):
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.image(logo_path, width=250)

st.title("⚡ Eficiência Energética em Iluminação Pública")
st.markdown("---")

# --- PARÂMETROS DAS TABELAS ---
# Tarifas B4a (R$/kWh)
tarifas = {
    "Norte / Nordeste": 0.52,
    "Sudeste / Centro-Oeste": 0.46,
    "Sul": 0.41
}

# --- ENTRADAS (Barra Lateral) ---
st.sidebar.header("Parâmetros do Município")
regiao = st.sidebar.selectbox("Selecione a Região:", list(tarifas.keys()))
habitantes = st.sidebar.number_input("Número de Habitantes:", min_value=1, value=160318)
gasto_total = st.sidebar.number_input("Gasto Mensal Total (R$):", min_value=0.0, value=451699.0)
pontos = st.sidebar.number_input("Número Total de Pontos de Iluminação:", min_value=1, value=21500)

# --- LÓGICA DE PORTE E META DE CONSUMO (kWh) ---
if habitantes < 50000:
    porte = "Pequeno"
    meta_kwh = 20
elif habitantes <= 500000:
    porte = "Médio"
    meta_kwh = 24
else:
    porte = "Grande"
    meta_kwh = 28

# --- CÁLCULOS CORRIGIDOS ---
tarifa = tarifas[regiao]
consumo_total_kwh = gasto_total / tarifa
kwh_por_ponto = consumo_total_kwh / pontos
watts_por_ponto = (kwh_por_ponto / 360) * 1000
gasto_por_hab = gasto_total / habitantes

# AJUSTE DA FÓRMULA: O Gasto Ideal agora é baseado na Meta de kWh (Eficiência Real)
# Gasto Ideal = (Total de Pontos * Meta de kWh por ponto) * Preço da Energia
gasto_ideal_total = (pontos * meta_kwh) * tarifa
prejuizo = max(0, gasto_total - gasto_ideal_total)
desvio_tecnico = ((kwh_por_ponto - meta_kwh) / meta_kwh) * 100

# --- RESULTADOS EM COLUNAS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Consumo/Ponto", f"{kwh_por_ponto:.2f} kWh")
col2.metric("Gasto/Habitante", f"R$ {gasto_por_hab:.2f}")
col3.metric("Potência Média", f"{watts_por_ponto:.2f} W")
col4.metric("Porte", porte)

st.divider()

# --- DIAGNÓSTICO ---
if kwh_por_ponto <= meta_kwh:
    st.success(f"✅ Diagnóstico: Município Eficiente! O consumo de {kwh_por_ponto:.2f} kWh/ponto está dentro da meta de {meta_kwh} kWh.")
else:
    st.error(f"❌ Diagnóstico: Município Ineficiente! O consumo de {kwh_por_ponto:.2f} kWh/ponto está {desvio_tecnico:.2f}% acima da meta.")
    
    st.warning(f"💸 **Potencial de Economia Mensal:** R$ {prejuizo:,.2f}")
    st.info(f"💡 Para atingir a eficiência técnica, o gasto total deveria ser de no máximo **R$ {gasto_ideal_total:,.2f}** (baseado na meta de {meta_kwh} kWh/ponto).")

# --- SEÇÃO DE CONTATO ---
st.markdown("---")
st.markdown(
    """
    ### 📞 Próximos Passos
    Para saber como economizar esses valores na gestão de energia do seu município, entre em contato com a **VITÁLIS ENERGIA**:
    *   **WhatsApp:** [19-997970002](https://wa.me/5519997970002)
    *   **E-mail:** [comercial@vitalisenergia.com](mailto:comercial@vitalisenergia.com)
    """
)
