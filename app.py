import streamlit as st

def main():
    st.title('Calculadora de Eficiência Energética - Iluminação Pública')
    
    st.sidebar.header('Parâmetros do Município')
    porte = st.sidebar.selectbox('Porte do Município', ['Pequeno', 'Médio', 'Grande'])
    regiao = st.sidebar.selectbox('Região', ['Norte/Nordeste', 'Sudeste/Centro-Oeste', 'Sul'])
    gasto_mensal = st.sidebar.number_input('Gasto Mensal Total (R$)', min_value=0.0, value=10000.0)
    pontos = st.sidebar.number_input('Número de Pontos de Iluminação', min_value=1, value=100)

    tarifas = {'Norte/Nordeste': 0.52, 'Sudeste/Centro-Oeste': 0.46, 'Sul': 0.41}
    benchmarks = {'Pequeno': 20, 'Médio': 24, 'Grande': 28}
    
    tarifa = tarifas[regiao]
    benchmark = benchmarks[porte]
    
    consumo_total_kwh = gasto_mensal / tarifa
    consumo_real_por_ponto = consumo_total_kwh / pontos
    potencia_media_real = (consumo_real_por_ponto * 1000) / 360
    
    st.subheader('Resultados')
    col1, col2 = st.columns(2)
    col1.metric('Consumo Real (kWh/ponto)', f'{consumo_real_por_ponto:.2f}')
    col2.metric('Potência Média Real (W)', f'{potencia_media_real:.2f}')
    
    if consumo_real_por_ponto <= benchmark:
        st.success('Status: Eficiente (Dentro do benchmark)')
    else:
        st.error('Status: Ineficiente (Acima do benchmark)')
        excesso_kwh = (consumo_real_por_ponto - benchmark) * pontos
        prejuizo = excesso_kwh * tarifa
        st.write(f'Prejuízo Mensal Estimado: R$ {prejuizo:,.2f}')

if __name__ == '__main__':
    main()