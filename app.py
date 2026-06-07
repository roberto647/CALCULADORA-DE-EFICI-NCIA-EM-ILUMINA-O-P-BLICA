import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="Eficiência Energética - Vitalis Energia", layout="wide")

# --- EXIBIÇÃO DO LOGO CENTRALIZADO ---
# Certifique-se de que o arquivo no GitHub se chama exatamente "logo.jpg"
logo_path = "logo.jpg"
if os.path.exists(logo_path):
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.image(logo_path, width=250)

st.title("⚡ Eficiência Energética em Iluminação Pública")
st.markdown("---")

# --- BENCHMARKS ATUALIZADOS (Conforme Tabelas) ---
# Benchmarks Financeiros (R$/hab)
benchmarks_financeiros = {
    "Norte / Nordeste": {"Pequeno": 3.15, "Médio": 3.85, "Grande": 4.90},
    "Sudeste / Centro-Oeste": {"Pequeno": 2.80, "Médio": 3.42, "Grande": 4.36},
    "Sul": {"Pequeno": 2.52, "Médio": 3.08, "Grande": 3.92}
}

# Tarifas B4a (R$/kWh)
tarifas = {
    "Norte / Nordeste": 0.52,
    "Sudeste / Centro-Oeste": 0.46,
    "Sul": 0.41
}

# --- ENTRADAS (Barra Lateral) ---
st.sidebar.header("Parâmetros do Município")
regiao = st.sidebar.selectbox("Selecione a Região:", list(benchmarks_financeiros.keys()))
habitantes = st.sidebar.number_input("Número de Habitantes:", min_value=1, value=154000)
gasto_total = st.sidebar.number_input("Gasto Mensal Total (R$):", min_value=0.0, value=656000.0)
pontos = st.sidebar.number_input("Número Total de Pontos de Iluminação:", min_value=1, value=21000)

# --- LÓGICA DE PORTE E BENCHMARK DE CONSUMO (kWh) ---
if habitantes < 50000:
    porte = "Pequeno"
    meta_kwh = 20
elif habitantes <= 500000:
    porte = "Médio"
    meta_kwh = 24
else:
    porte = "Grande"
    meta_kwh = 28

# --- CÁLCULOS ---
tarifa = tarifas[regiao]
consumo_total_kwh = gasto_total / tarifa
kwh_por_ponto = consumo_total_kwh / pontos
watts_por_ponto = (kwh_por_ponto / 360) * 1000

# Benchmark Financeiro para referência
gasto_por_hab = gasto_total / habitantes
meta_financeira_hab = benchmarks_financeiros[regiao][porte]
gasto_ideal_total = meta_financeira_hab * habitantes

# --- RESULTADOS EM COLUNAS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Consumo/Ponto", f"{kwh_por_ponto:.2f} kWh")
col2.metric("Gasto/Habitante", f"R$ {gasto_por_hab:.2f}")
col3.metric("Potência Média", f"{watts_por_ponto:.2f} W")
col4.metric("Porte", porte)

st.divider()

# --- DIAGNÓSTICO BASEADO NO CONSUMO (kWh/ponto) ---
# Conforme solicitado: o critério de eficiência agora é o kWh/ponto
if kwh_por_ponto <= meta_kwh:
    st.success(f"✅ Diagnóstico: Município Eficiente! O consumo de {kwh_por_ponto:.2f} kWh/ponto está dentro da meta de {meta_kwh} kWh.")
else:
    st.error(f"❌ Diagnóstico: Município Ineficiente! O consumo de {kwh_por_ponto:.2f} kWh/ponto está acima da meta de {meta_kwh} kWh.")
    
    # Cálculos de desvio e prejuízo financeiro para contexto comercial
    desvio_financeiro = ((gasto_por_hab - meta_financeira_hab) / meta_financeira_hab) * 100
    prejuizo = max(0, gasto_total - gasto_ideal_total)
    
    st.warning(f"💸 Prejuízo mensal estimado: R$ {prejuizo:,.2f} (Desvio de {desvio_financeiro:.2f}% do benchmark financeiro)")
    st.info(f"💡 Para atingir a eficiência financeira, o gasto total deveria ser de no máximo R$ {gasto_ideal_total:,.2f}")

# --- SEÇÃO DE CONTATO (CTA) ---
st.markdown("---")
st.markdown(
    """
    ### 📞 Próximos Passos
    Para saber como melhorar a gestão de energia do seu município, entre em contato com a **VITÁLIS ENERGIA**:
    *   **WhatsApp:** [19-997970002](https://wa.me/5519997970002)
    *   **E-mail:** [comercial@vitalisenergia.com](mailto:comercial@vitalisenergia.com)
    """
)
