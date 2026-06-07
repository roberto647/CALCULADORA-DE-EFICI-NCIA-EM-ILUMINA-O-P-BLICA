import streamlit as st
import os

# Configuração da página
st.set_page_config(page_title="Eficiência Energética - Vitalis Energia", layout="centered")

# --- EXIBIÇÃO DO LOGO ---
# O código procura pelo arquivo exato que você anexou
logo_path = "logo vitalis (6).jpg"
if os.path.exists(logo_path):
    st.image(logo_path, width=250)

# Tabela de Benchmarks (R$/hab)
benchmarks = {
    "Norte / Nordeste": {"Pequeno": 4.05, "Médio": 4.95, "Grande": 6.30},
    "Sudeste / Centro-Oeste": {"Pequeno": 3.60, "Médio": 4.40, "Grande": 5.60},
    "Sul": {"Pequeno": 3.24, "Médio": 3.96, "Grande": 5.04}
}

# Tarifas B4a por região
tarifas_b4a = {
    "Norte / Nordeste": 0.52,
    "Sudeste / Centro-Oeste": 0.46,
    "Sul": 0.41
}

st.title("⚡ Calculadora de Eficiência Energética")
st.subheader("Iluminação Pública Municipal")

# --- ENTRADAS ---
st.sidebar.header("Parâmetros do Município")
regiao = st.sidebar.selectbox("Selecione a Região:", list(benchmarks.keys()))
habitantes = st.sidebar.number_input("Número de Habitantes:", min_value=1, value=154000)
gasto_total = st.sidebar.number_input("Gasto Mensal Total (R$):", min_value=0.0, value=656000.0)
pontos = st.sidebar.number_input("Número Total de Pontos de Iluminação:", min_value=1, value=21000)

# --- LÓGICA DE PORTE ---
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
tarifa = tarifas_b4a[regiao]
consumo_total_kwh = gasto_total / tarifa
kwh_por_ponto = consumo_total_kwh / pontos
watts_por_ponto = (kwh_por_ponto / 360) * 1000

# Benchmark Financeiro
gasto_por_hab = gasto_total / habitantes
meta_financeira_hab = benchmarks[regiao][porte]
gasto_ideal_total = meta_financeira_hab * habitantes

st.divider()

# --- RESULTADOS ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Consumo por Ponto", f"{kwh_por_ponto:.2f} kWh")
    st.metric("Gasto por Habitante", f"R$ {gasto_por_hab:.2f}")

with col2:
    st.metric("Potência Média", f"{watts_por_ponto:.2f} W")
    st.metric("Porte do Município", porte)

# --- DIAGNÓSTICO ---
desvio = ((gasto_total - gasto_ideal_total) / gasto_ideal_total) * 100
prejuizo = max(0, gasto_total - gasto_ideal_total)

if gasto_por_hab <= meta_financeira_hab:
    st.success(f"✅ Município Eficiente! O gasto está dentro do benchmark de R$ {meta_financeira_hab:.2f}/hab.")
else:
    st.error(f"❌ Município Ineficiente! O gasto está {desvio:.1f}% acima do ideal.")
    st.warning(f"💸 Prejuízo mensal estimado: R$ {prejuizo:,.2f}")

st.info(f"💡 Para ser eficiente, o gasto total deveria ser de no máximo R$ {gasto_ideal_total:,.2f}")

# --- SEÇÃO DE CONTATO (CTA) ---
st.divider()
st.markdown("### 📞 Próximos Passos")
st.write("Para saber como melhorar a gestão de energia do seu município entre em contato através do:")
st.markdown("- **WhatsApp:** [19-997970002](https://wa.me/5519997970002)")
st.markdown("- **E-mail:** [comercial@vitalisenergia.com](mailto:comercial@vitalisenergia.com)")
