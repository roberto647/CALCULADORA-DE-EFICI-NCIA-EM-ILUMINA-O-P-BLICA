import streamlit as st
import os

st.set_page_config(page_title='Eficiência Energética em Iluminação-Vitális Energia', layout='wide')

if os.path.exists('logo.jpg'):
    st.image('logo.jpg', width=250)

st.title('Eficiência Energética em Iluminação Pública')

benchmarks = {
    'Norte / Nordeste': {'Pequeno': 4.05, 'Médio': 4.95, 'Grande': 6.30},
    'Sudeste / Centro-Oeste': {'Pequeno': 3.60, 'Médio': 4.40, 'Grande': 5.60},
    'Sul': {'Pequeno': 3.24, 'Médio': 3.96, 'Grande': 5.04}
}

tarifas = {
    'Norte / Nordeste': 0.52,
    'Sudeste / Centro-Oeste': 0.46,
    'Sul': 0.41
}

st.sidebar.header('Parâmetros do Município')
regiao = st.sidebar.selectbox('Região', list(benchmarks.keys()))
habitantes = st.sidebar.number_input('Número de Habitantes', min_value=1, value=10000)
gasto_total = st.sidebar.number_input('Gasto Mensal Total (R$)', min_value=0.0, value=50000.0)
pontos = st.sidebar.number_input('Número Total de Pontos de Iluminação', min_value=1, value=500)

if habitantes < 50000:
    porte = 'Pequeno'
    meta_kwh = 20
elif habitantes <= 500000:
    porte = 'Médio'
    meta_kwh = 24
else:
    porte = 'Grande'
    meta_kwh = 28

tarifa = tarifas[regiao]
consumo_total_kwh = gasto_total / tarifa
kwh_por_ponto = consumo_total_kwh / pontos
watts_por_ponto = (kwh_por_ponto / 360) * 1000
gasto_por_hab = gasto_total / habitantes
meta_financeira_hab = benchmarks[regiao][porte]
gasto_ideal_total = meta_financeira_hab * habitantes

col1, col2, col3, col4 = st.columns(4)
col1.metric('Consumo/Ponto', f'{kwh_por_ponto:.2f} kWh')
col2.metric('Gasto/Habitante', f'R$ {gasto_por_hab:.2f}')
col3.metric('Potência Média', f'{watts_por_ponto:.2f} W')
col4.metric('Porte', porte)

st.divider()

if gasto_por_hab <= meta_financeira_hab:
    st.success('Diagnóstico: Município Eficiente')
else:
    st.error('Diagnóstico: Município Ineficiente')
    desvio = ((gasto_por_hab - meta_financeira_hab) / meta_financeira_hab) * 100
    st.warning(f'Prejuízo estimado: R$ {gasto_total - gasto_ideal_total:.2f} (Desvio de {desvio:.2f}%)')
    st.info(f'Gasto ideal para o seu porte e região: R$ {gasto_ideal_total:.2f}')

st.markdown("---")
st.markdown(
    """
    ### 📞 Próximos Passos
    Para saber como melhorar a gestão de energia do seu município, entre em contato com a **VITÁLIS ENERGIA**:
    *   **WhatsApp:** [19-997970002](https://wa.me/5519997970002)
    *   **E-mail:** [comercial@vitalisenergia.com](mailto:comercial@vitalisenergia.com)
    """
)
