import streamlit as st
from auth import Auth
from pags.dashboard import Dashboard
from pags.agendamentos import Agendamentos
from pags.suporte import Suporte
from pags.historico import Historico

# Tela principal para rodar o código, ela que faz a "Distribuição" para as outras páginas. Importante manter o controle do versionamento dessa página.
st.set_page_config(page_title="Agendamentos", layout="centered")

class App:
    def __init__(self):
        self.auth = Auth()
        # Verifica se o usuário está autenticado na sessão
        if "auth_user" not in st.session_state:
            st.session_state["auth_user"] = None
        if "page" not in st.session_state:
            st.session_state["page"] = "Dashboard"  # Página inicial após login

    def run(self):
        """Executa a aplicação"""
        if st.session_state["auth_user"] is None:
            self.show_auth_screen()
        else:
            self.show_dashboard()

    def show_auth_screen(self):
        """Tela de autenticação"""
        st.title("Login")
        email = st.text_input("Email", placeholder="Digite seu email")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

        if st.button("Entrar"):
            user = self.auth.login_user(email, senha)
            if user:
                user_id, nome, tipo = user
                st.session_state["auth_user"] = {"id": user_id, "nome": nome, "email": email, "tipo": tipo}
                st.session_state["page"] = "Dashboard"  # Página inicial após login
                st.success(f"Bem-vindo, {nome}!")
                st.rerun()  # Recarregar a página após login
            else:
                st.error("Email ou senha inválidos!")

    def show_dashboard(self):
        """Painel de navegação após login"""
        user_tipo = st.session_state["auth_user"]["tipo"]

        # Exibe o nome do usuário logado
        st.sidebar.title(f"Bem-vindo, {st.session_state['auth_user']['nome']}!")

        # Menu de navegação
        if user_tipo == "admin":
            paginas = ["Dashboard", "Agendamentos", "Suporte", "Histórico"]
        else:
            paginas = ["Dashboard", "Agendamentos", "Suporte", "Histórico"]

        # Navegação entre as páginas usando radio buttons
        page = st.sidebar.radio("Navegação", paginas)

        # Controlando a navegação
        if page == "Dashboard":
            Dashboard().show()
        elif page == "Agendamentos":
            Agendamentos().show()
        elif page == "Suporte":
            Suporte().show()
        elif page == "Histórico":
            Historico().show()

        # Botão para sair da conta
        if st.sidebar.button("Sair"):
            st.session_state["auth_user"] = None
            st.session_state["page"] = "Dashboard"  # Volta para a tela inicial
            st.rerun()  # Recarregar a página após logout

if __name__ == "__main__":
    app = App()
    app.run()