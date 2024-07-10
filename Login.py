import streamlit as st
import streamlit_authenticator as stauth
from imobiliaria import show_imobiliaria
from yaml.loader import SafeLoader
import yaml

# ===== CONFIGURAÇÃO INICIAL DE PÁGINA ==== #
st.set_page_config(page_title="📊 Análise Estatística de Saldos Devedores e Cobranças", layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 Análise Estatística de Saldos Devedores e Cobranças</h1>", unsafe_allow_html=True)
st.divider()

# ==== ABRIR ARQUIVO DE CONFIGURAÇÃO ==== #
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# ==== INICIALIZAR O AUTENTICATOR ==== #
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# ==== FAZER O LOGIN ==== #
name, authentication_status, username = authenticator.login()

# ==== LÓGICA PARA MOSTRAR A PÁGINA SELECIONADA ==== #
if authentication_status:
    st.button("Logout", on_click=authenticator.logout)
    show_imobiliaria()  # Substitua por sua lógica específica
elif authentication_status is False:
    st.error('Usuário/Senha está inválido.')
elif authentication_status is None:
    st.warning('Por favor, utilize seu usuário e senha!')

# ==== LÓGICA PARA REMOVER O BOTÃO DE LOGOUT APÓS LOGOUT ==== #
if 'authentication_status' in st.session_state and not st.session_state['authentication_status']:
    st.experimental_rerun()  # Força um recarregamento da página

# ==== FORÇAR RECARGA DA PÁGINA APÓS O LOGIN ==== #
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if authentication_status and not st.session_state['logged_in']:
    st.session_state['logged_in'] = True
    st.experimental_rerun()

if not authentication_status and st.session_state['logged_in']:
    st.session_state['logged_in'] = False
