import pandas as pd
import streamlit as st
import plotly.express as px

# ===== CARREGAR ARQUIVOS ===== #
df_cobranca = pd.read_csv('COBRANÇA.csv', delimiter=';', encoding='latin-1')
df_saldo_devedor = pd.read_csv('SALDO DEVEDOR.csv', delimiter=';', encoding='latin-1')

# ==== CRIAÇÃO DE ABAS ==== #
aba1, aba2 = st.tabs(['Saldo Devedor', 'Cobrança'])

# ==== FUNÇÃO DE CONVERSÃO DE NÚMERO EM STRING COM MOEDA ==== #
def format_number(value, prefix=''):
    is_negative = value < 0
    value = abs(value)

    for unit in ['', 'mil']:
        if value < 1000:
            formatted_value = f'{value:.3f}'.replace('-', '')
            return f'{prefix}{"-" if is_negative else ""}{formatted_value} {unit}'
        value /= 1000

    formatted_value = f'{value:.3f}'.replace('-', '')
    return f'{prefix}{"-" if is_negative else ""}{formatted_value} milhões'

# ==== FUNÇÃO DE SIDEBAR ==== #
def sidebar_saldo_devedor(saldo_devedor):
    # ===== BARRA LATERAL ==== #
    num_contrato = saldo_devedor['CONTRATO'].unique().tolist()
    filtro_num_contrato = st.sidebar.multiselect('NÚMERO DO CONTRATO', num_contrato)

    titular = saldo_devedor['TITULAR'].unique().tolist()
    filtro_titular = st.sidebar.multiselect('NOME DO TITULAR', titular)

    parc_financidas = saldo_devedor['N°PARC. FINANC'].unique().tolist()
    filtro_parc_financiadas = st.sidebar.multiselect('NÚMERO DE PARCELAS FINANCIADAS', parc_financidas)

    loteamento = saldo_devedor['LOTEAMENTO'].unique().tolist()
    filtro_loteamento = st.sidebar.multiselect('EMPREENDIMENTOS', loteamento)

    df_saldo_devedor_filtrado = saldo_devedor

    if filtro_num_contrato:
        df_saldo_devedor_filtrado = df_saldo_devedor_filtrado[df_saldo_devedor_filtrado['CONTRATO'].isin(filtro_num_contrato)]

    if filtro_titular:
        df_saldo_devedor_filtrado = df_saldo_devedor_filtrado[df_saldo_devedor_filtrado['TITULAR'].isin(filtro_titular)]

    if filtro_parc_financiadas:
        df_saldo_devedor_filtrado = df_saldo_devedor_filtrado[df_saldo_devedor_filtrado['N°PARC. FINANC'].isin(filtro_parc_financiadas)]

    if filtro_loteamento:
        df_saldo_devedor_filtrado = df_saldo_devedor_filtrado[df_saldo_devedor_filtrado['LOTEAMENTO'].isin(filtro_loteamento)]

    return df_saldo_devedor_filtrado

def sidebar_cobranca(cobranca):
    num_contrato = cobranca['Nº CONTR.'].unique().tolist()
    filtro_num_contrato = st.sidebar.multiselect('NÚMERO DO CONTRATO', num_contrato)

    titular = cobranca['NOME DO TITULAR'].unique().tolist()
    filtro_titular = st.sidebar.multiselect('NOME DO TITULAR', titular)

    loteamento = cobranca['LOTEAMENTO'].unique().tolist()
    filtro_loteamento = st.sidebar.multiselect('EMPREEENDIMENTO', loteamento)

    dias_atraso = cobranca['DIAS DE ATRASO'].unique().tolist()
    filtro_dias_atraso = st.sidebar.multiselect('DIAS DE ATRASO', dias_atraso)

    nparcelas_atraso = cobranca['Nº DE PARCELAS ATRASADAS'].unique().tolist()
    filtro_nparcelas_atraso = st.sidebar.multiselect('NÚMERO DE PARCELAS ATRASADAS', nparcelas_atraso)

    df_cobranca_filtrado = cobranca

    if filtro_num_contrato:
        df_cobranca_filtrado = df_cobranca_filtrado[df_cobranca_filtrado['Nº CONTR.'].isin(filtro_num_contrato)]

    if filtro_titular:
        df_cobranca_filtrado = df_cobranca_filtrado[df_cobranca_filtrado['NOME DO TITULAR'].isin(filtro_titular)]

    if filtro_dias_atraso:
        df_cobranca_filtrado = df_cobranca_filtrado[df_cobranca_filtrado['DIAS DE ATRASO'].isin(filtro_dias_atraso)]

    if filtro_loteamento:
        df_cobranca_filtrado = df_cobranca_filtrado[df_cobranca_filtrado['LOTEAMENTO'].isin(filtro_loteamento)]

    if filtro_nparcelas_atraso:
        df_cobranca_filtrado = df_cobranca_filtrado[df_cobranca_filtrado['Nº DE PARCELAS ATRASADAS'].isin(filtro_nparcelas_atraso)]

    return df_cobranca_filtrado
    
st.sidebar.write('Última atualização: 01/07/2024')

with aba1:
    st.sidebar.header(':blue[SALDO DEVEDOR]', divider='blue')
    df_saldo_devedor_filtrado = sidebar_saldo_devedor(df_saldo_devedor)

    # ==== FUNÇÃO DE CONVERSÃO DE NÚMERO EM FLOAT ==== #
    colunas = [' VALOR PARC. ATUAL','BALÕES','SALDO DEVEDOR (ATUALIZADO)']

    for coluna in colunas:
        df_saldo_devedor_filtrado[coluna] = df_saldo_devedor_filtrado[coluna].astype(str).str.replace('.', '', regex=False)
        df_saldo_devedor_filtrado[coluna] = df_saldo_devedor_filtrado[coluna].str.replace(',', '.', regex=False).astype(float)

    st.header(':blue[Métricas de Negócios]', divider='blue')

    # === QUANTIDADE DE CONTRATOS === #
    qtd_contratos = df_saldo_devedor_filtrado['CONTRATO'].count()

    # === QUANTIDADE DE CLIENTES === #
    qtd_clientes = df_saldo_devedor_filtrado['TITULAR'].nunique()

    # ==== QUANTIDADE DE LOTEAMENTOS ==== #
    qtd_loteamentos = df_saldo_devedor_filtrado['LOTEAMENTO'].nunique()

    # ==== VALORES DE PARCELAS ==== #
    vlr_parcelas = df_saldo_devedor_filtrado[' VALOR PARC. ATUAL'].sum()

    # ==== VALOR DE BALÕES ==== #
    vlr_baloes = df_saldo_devedor_filtrado['BALÕES'].sum()

    # ==== VALOR DE SALDO DEVEDOR ATUALIZADO ==== #
    vlr_saldo_devedor = df_saldo_devedor_filtrado['SALDO DEVEDOR (ATUALIZADO)'].sum()

    # ==== VALOR DE PARCELAS PAGAS ==== #
    df_saldo_devedor_filtrado.rename(columns={' VALOR PARC. ATUAL': 'VALOR PARC. ATUAL'}, inplace=True)
    df_saldo_devedor_filtrado['VALOR PAGO'] = df_saldo_devedor_filtrado['PARCELA PAGAS'] * df_saldo_devedor_filtrado['VALOR PARC. ATUAL']
    total_pago = df_saldo_devedor_filtrado['VALOR PAGO'].sum()
    
    # ==== IMPRIMIR NA TELA ==== #
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric('Quantidade de Contratos', qtd_contratos)
        st.metric('Somatório de Parcelas', format_number(vlr_parcelas, 'R$'))
        st.metric('Somatório de Balões', format_number(vlr_baloes, 'R$'))
    with coluna2:
        st.metric('Quantidade de Clientes', qtd_clientes)
        st.metric('Valor de Parcelas Pagas', format_number(total_pago,'R$'))        
    with coluna3:
        st.metric('Quantidade de Empreendimentos', qtd_loteamentos)
        st.metric('Somatório de Saldo Devedor', format_number(vlr_saldo_devedor, 'R$'))
        

    st.divider()
    st.header(':blue[Base de Dados]', divider='blue')
    st.dataframe(df_saldo_devedor_filtrado, use_container_width=True)
        
    st.divider()
    st.header(':blue[Análise Gráfica]', divider='blue')

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        # ==== GRÁFICO CONTAGEM DE LOTEAMENTOS ==== #
        contagem_loteamentos = df_saldo_devedor_filtrado['LOTEAMENTO'].value_counts().reset_index()
        contagem_loteamentos.columns = ['Empreendimento', 'Quantidade']
        contagem_loteamentos = contagem_loteamentos.sort_values(by='Quantidade', ascending=False)

        grafico_qtd_loteamento = px.bar(
            contagem_loteamentos.head(10), 
            x='Empreendimento', 
            y='Quantidade', 
            color_discrete_sequence=[px.colors.qualitative.Prism[1]],
            text_auto = True,
            title='Quantidade de Contratos por Empreendimento'
        )
        st.plotly_chart(grafico_qtd_loteamento, use_container_width=True)

        # ==== SALDO DEVEDOR POR LOTEAMENTO ==== #
        df_sd_lote = df_saldo_devedor_filtrado.groupby('LOTEAMENTO')['SALDO DEVEDOR (ATUALIZADO)'].sum().reset_index()
        df_sd_lote = df_sd_lote.sort_values(by = 'SALDO DEVEDOR (ATUALIZADO)', ascending=False)
        df_sd_lote['SALDO DEVEDOR (ATUALIZADO) Formatado'] = df_sd_lote['SALDO DEVEDOR (ATUALIZADO)'].apply(format_number)

        grafico_sd_lote = px.bar(
            df_sd_lote.head(10),
            x = 'LOTEAMENTO',
            y = 'SALDO DEVEDOR (ATUALIZADO)',
            color_discrete_sequence=[px.colors.qualitative.Prism[1]],
            text = 'SALDO DEVEDOR (ATUALIZADO) Formatado',
            title = 'Saldo Devedor por Empreendimento'
        )
        st.plotly_chart(grafico_sd_lote, use_container_width = True)

        # ==== VALOR PAGO POR LOTEAMENTO ==== #
        df_vlr_pg_lote = df_saldo_devedor_filtrado.groupby('LOTEAMENTO')['VALOR PAGO'].sum().reset_index()
        df_vlr_pg_lote = df_vlr_pg_lote.sort_values(by = 'VALOR PAGO', ascending=False)
        df_vlr_pg_lote['VALOR PAGO FORMATADO'] = df_vlr_pg_lote['VALOR PAGO'].apply(format_number)

        grafico_vlr_pg_lote = px.bar(
            df_vlr_pg_lote.head(10),
            x = 'LOTEAMENTO',
            y = 'VALOR PAGO',
            color_discrete_sequence=[px.colors.qualitative.Prism[1]],
            text = 'VALOR PAGO FORMATADO',
            title = 'Valor Pago por Empreendimento'
        )
        st.plotly_chart(grafico_vlr_pg_lote, use_container_width = True)

        # ==== GRÁFICO CONTAGEM DE PARCELAS ==== #
        contagem_parcelas = df_saldo_devedor_filtrado['N°PARC. FINANC'].value_counts().reset_index()
        contagem_parcelas.columns = ['Nº de Parcelas', 'Quantidade']
        contagem_parcelas = contagem_parcelas.sort_values(by='Quantidade', ascending=False)

        grafico_qtd_parcelas = px.bar(
            contagem_parcelas.head(10), 
            x='Nº de Parcelas', 
            y='Quantidade', 
            color_discrete_sequence=[px.colors.qualitative.Prism[1]],
            text_auto = True,
            title='Quantidade de Parcelas'
        )
        st.plotly_chart(grafico_qtd_parcelas, use_container_width=True)

        # ==== SALDO DEVEDOR POR Nº DE PARCELAS ==== #
        df_sd_parcelas = df_saldo_devedor_filtrado.groupby('N°PARC. FINANC')['SALDO DEVEDOR (ATUALIZADO)'].sum().reset_index()
        df_sd_parcelas = df_sd_parcelas.sort_values(by = 'SALDO DEVEDOR (ATUALIZADO)', ascending=False)
        df_sd_parcelas['SALDO DEVEDOR (ATUALIZADO) Formatado'] = df_sd_parcelas['SALDO DEVEDOR (ATUALIZADO)'].apply(format_number)

        grafico_sd_parcelas = px.bar(
            df_sd_parcelas.head(10),
            x = 'N°PARC. FINANC',
            y = 'SALDO DEVEDOR (ATUALIZADO)',
            color_discrete_sequence=[px.colors.qualitative.Prism[1]],
            text = 'SALDO DEVEDOR (ATUALIZADO) Formatado',
            title = 'Saldo Devedor por Número de Parcelas'
        )
        st.plotly_chart(grafico_sd_parcelas, use_container_width = True)

    with coluna2:
        # ==== REPRESENTATIVIDADE POR LOTEAMENTO ==== #
        repres_loteamento = df_saldo_devedor_filtrado['LOTEAMENTO'].value_counts().reset_index()
        repres_loteamento.columns = ['Empreendimento', 'Quantidade']

        grafico_repres_lote = px.pie(
            repres_loteamento.head(10),
            names='Empreendimento',
            values='Quantidade',
            hole = 0.3,
            title='TOP 10 Distribuição dos Empreendimentos'
        )

        st.plotly_chart(grafico_repres_lote, use_container_width = True)

        # ==== REPRESENTATIVIDADE SALDO DEVEDOR POR LOTEAMENTO ==== #
        grafico_repres_sd_lote = px.pie(
            df_sd_lote.head(10),
            values='SALDO DEVEDOR (ATUALIZADO)',
            names='LOTEAMENTO',
            hole=0.3,
            title='Representatividade de Saldo Devedor por Empreendimento'
        )
        st.plotly_chart(grafico_repres_sd_lote, use_container_width=True)

        # ==== REPRESENTATIVIDADE VALOR PAGO POR LOTEAMENTO ==== #
        grafico_repres_vlr_pg_lote = px.pie(
            df_vlr_pg_lote.head(10),
            values='VALOR PAGO',
            names='LOTEAMENTO',
            hole=0.3,
            title='Representatividade de Valor Pago por Loteamento'
        )
        st.plotly_chart(grafico_repres_vlr_pg_lote, use_container_width=True)

        # ==== REPRESENTATIVIDADE POR Nº PARCELAS ==== #
        repres_parcelas = df_saldo_devedor_filtrado['N°PARC. FINANC'].value_counts().reset_index()
        repres_parcelas.columns = ['Nº Parcelas', 'Quantidade']

        grafico_repres_parcelas = px.pie(
            repres_parcelas.head(10),
            names='Nº Parcelas',
            values='Quantidade',
            hole = 0.3,
            title='TOP 10 Distribuição do Número de Parcelas'
        )

        st.plotly_chart(grafico_repres_parcelas, use_container_width = True)

        # ==== REPRESENTATIVIDADE SALDO DEVEDOR POR PARCELAS ==== #
        grafico_repres_sd_parcelas = px.pie(
            df_sd_parcelas.head(10),
            values='SALDO DEVEDOR (ATUALIZADO)',
            names='N°PARC. FINANC',
            hole=0.3,
            title='Representatividade de Saldo Devedor por Número de Parcelas'
        )
        st.plotly_chart(grafico_repres_sd_parcelas, use_container_width=True)

with aba2:
    st.sidebar.header(':orange[COBRANÇA]', divider='orange')
    df_cobranca_filtrado = sidebar_cobranca(df_cobranca)

    # ==== FUNÇÃO DE CONVERSÃO DE NÚMERO EM FLOAT ==== #
    colunas = ['VALOR DA PARCELA','VALOR TOTAL']

    for coluna in colunas:
        df_cobranca_filtrado[coluna] = df_cobranca_filtrado[coluna].astype(str).str.replace('.', '', regex=False)
        df_cobranca_filtrado[coluna] = df_cobranca_filtrado[coluna].str.replace(',', '.', regex=False).astype(float)

    st.header(':orange[Métricas de Negócios]', divider='orange')

    # ==== QUANTIDADE DE CONTRATOS COM ATRASO ==== #
    qtd_contratos_atraso = df_cobranca_filtrado['Nº CONTR.'].count()

    # === QUANTIDADE DE CLIENTES EM ATRASO === #
    qtd_clientes_atraso = df_cobranca_filtrado['NOME DO TITULAR'].nunique()

    # ==== QUANTIDADE DE LOTEAMENTOS EM ATRASO ==== #
    qtd_loteamentos_atraso = df_cobranca_filtrado['LOTEAMENTO'].nunique()

    # ==== QUANTIDADE DE PARCELAS ATRASASDAS ==== #
    qtd_parcelas_atraso = df_cobranca_filtrado['N°PAC ATRAS'].sum()

    # ==== VALOR POR PARCELA ==== #
    vlr_parcela_atraso = df_cobranca_filtrado['VALOR DA PARCELA'].sum()

    # ==== VALOR POR PARCELA ==== #
    vlr_parcela_total_atraso = df_cobranca_filtrado['VALOR TOTAL'].sum()

    coluna1, coluna2, coluna3 = st.columns(3)

    # ==== IMPRIMIR NA TELA ==== #
    with coluna1:
        st.metric('Quantidade de Contratos em Atraso', qtd_contratos_atraso)
        st.metric('Quantidade de Parcelas em Atraso', qtd_parcelas_atraso)
    with coluna2:
        st.metric('Quantidade de Clientes em Atraso', qtd_clientes_atraso)
        st.metric('Somatório de Valores Individuais de Parcelas em Atraso', format_number(vlr_parcela_atraso,'R$'))
    with coluna3:
        st.metric('Quantidade de Loteamentos em Atraso', qtd_loteamentos_atraso)
        st.metric('Somatório de Valores Totais de Parcelas em Atraso', format_number(vlr_parcela_total_atraso,'R$'))

    st.divider()
    st.header(':orange[Base de Dados]', divider='orange')
    st.dataframe(df_cobranca_filtrado, use_container_width=True)
    st.divider()

    st.header(':orange[Análise Gráfica]', divider='orange')

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        # ==== QUANTIDADE DE ATRASO POR LOTEAMENTO ==== #
        ctg_loteamentos_atraso = df_cobranca_filtrado['LOTEAMENTO'].value_counts().reset_index()
        ctg_loteamentos_atraso.columns = ['Empreendimento', 'Quantidade']
        ctg_loteamentos_atraso = ctg_loteamentos_atraso.sort_values(by='Quantidade', ascending=False)

        graf_ctg_lote_atraso = px.bar(
            ctg_loteamentos_atraso.head(10),
            x = 'Empreendimento',
            y = 'Quantidade',
            color_discrete_sequence=[px.colors.qualitative.Prism[7]],
            text_auto = True,
            title = 'Quantidade de Contratos com Inadimplência por Empreendimento'
        )
        st.plotly_chart(graf_ctg_lote_atraso, use_container_width = True)

        # ==== VALOR TOTAL DE ATRASO POR LOTEAMENTO ==== #
        df_atraso_lote = df_cobranca_filtrado.groupby('LOTEAMENTO')['VALOR TOTAL'].sum().reset_index()
        df_atraso_lote = df_atraso_lote.sort_values(by = 'VALOR TOTAL', ascending=False)
        df_atraso_lote['VALOR TOTAL FORMATADO'] = df_atraso_lote['VALOR TOTAL'].apply(format_number)

        grafico_atraso_lote = px.bar(
            df_atraso_lote.head(10),
            x = 'LOTEAMENTO',
            y = 'VALOR TOTAL',
            color_discrete_sequence=[px.colors.qualitative.Prism[7]],
            text = 'VALOR TOTAL FORMATADO',
            title = 'Inadimplência por Empreendimento'
        )
        st.plotly_chart(grafico_atraso_lote, use_container_width = True)

        # ==== QUANTIDADE DE DIAS DE ATRASO ==== #
        ctg_dias_atraso = df_cobranca_filtrado['DIAS DE ATRASO'].value_counts().reset_index()
        ctg_dias_atraso.columns = ['Dias de Atraso', 'Quantidade']
        ctg_dias_atraso = ctg_dias_atraso.sort_values(by='Quantidade', ascending=False)

        graf_ctg_dias_atraso = px.bar(
            ctg_dias_atraso,
            x = 'Dias de Atraso',
            y = 'Quantidade',
            color_discrete_sequence=[px.colors.qualitative.Prism[7]],
            text_auto = True,
            title = 'Quantidade Dias por Contratos Atrasados'
        )
        st.plotly_chart(graf_ctg_dias_atraso, use_container_width = True)

        # ==== VALOR TOTAL DE ATRASO POR QUANTIDADE DE DIAS ==== #
        df_atraso_dias = df_cobranca_filtrado.groupby('DIAS DE ATRASO')['VALOR TOTAL'].sum().reset_index()
        df_atraso_dias = df_atraso_dias.sort_values(by = 'VALOR TOTAL', ascending=False)
        df_atraso_dias['VALOR TOTAL FORMATADO'] = df_atraso_dias['VALOR TOTAL'].apply(format_number)

        grafico_atraso_dias = px.bar(
            df_atraso_dias,
            x = 'DIAS DE ATRASO',
            y = 'VALOR TOTAL',
            color_discrete_sequence=[px.colors.qualitative.Prism[7]],
            text = 'VALOR TOTAL FORMATADO',
            title = 'Inadimplência por Dias de Atraso'
        )
        st.plotly_chart(grafico_atraso_dias, use_container_width = True)

    with coluna2:
        # ==== REPRESENTATIVIDADE POR LOTEAMENTO ==== #
        repres_loteamento_atraso = df_cobranca_filtrado['LOTEAMENTO'].value_counts().reset_index()
        repres_loteamento_atraso.columns = ['Empreendimento', 'Quantidade']

        grafico_repres_lote_atraso = px.pie(
            repres_loteamento_atraso.head(10),
            names='Empreendimento',
            values='Quantidade',
            hole = 0.3,
            title='TOP 10 Distribuição dos Empreendimentos com Atraso'
        )
        st.plotly_chart(grafico_repres_lote_atraso, use_container_width = True)

        # ==== REPRESENTATIVIDADE INADIMPLÊNCIA POR LOTEAMENTO ==== #
        grafico_repres_vlr_atraso_lote = px.pie(
            df_atraso_lote.head(10),
            values='VALOR TOTAL',
            names='LOTEAMENTO',
            hole=0.3,
            title='Representatividade de Inadimplência por Empreendimento'
        )
        st.plotly_chart(grafico_repres_vlr_atraso_lote, use_container_width=True)

        # ==== REPRESENTATIVIDADE POR DIAS DE ATRASO ==== #
        repres_dias_atraso = df_cobranca_filtrado['DIAS DE ATRASO'].value_counts().reset_index()
        repres_dias_atraso.columns = ['Dias de Atraso', 'Quantidade']

        grafico_repres_dias_atraso = px.pie(
            repres_dias_atraso,
            names='Dias de Atraso',
            values='Quantidade',
            hole = 0.3,
            title='Representatividade dos Dias Atraso'
        )
        st.plotly_chart(grafico_repres_dias_atraso, use_container_width = True)

        # ==== REPRESENTATIVIDADE VALOR TOTAL POR DIAS DE ATRASO ==== #
        grafico_repres_vlr_dias_atraso = px.pie(
            df_atraso_dias,
            values='VALOR TOTAL',
            names='DIAS DE ATRASO',
            hole=0.3,
            title='Representatividade de Inadimplência por Dias de Atraso'
        )
        st.plotly_chart(grafico_repres_vlr_dias_atraso, use_container_width=True)
