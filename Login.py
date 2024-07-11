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
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout('Logout', 'main')
    show_imobiliaria()    
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

