import streamlit as st
from database import Database
# Precisa criar o historico dos agendamentos, aqui precisa aparecer TODOS os agendamentos feitos por esse usuario (lembrando, cada usuario pode ver apenas o agendamento de seu user)
class Historico:
    def __init__(self):
        self.db = Database()
        self.user_id = st.session_state["auth_user"]["id"]
        self.user_tipo = st.session_state["auth_user"]["tipo"]
        
    def tela_filtros(self):
        st.write("Selecione os filtros desejados para visualizar os agendamentos.")
        self.data_inicial_descarga = st.date_input("Data Inicial", format="DD/MM/YYYY")
        self.data_final_descarga = st.date_input("Data Final", format="DD/MM/YYYY", max_value="today")
        self.terminal = st.selectbox("Terminal", ["Todos", "Terminal 1", "Terminal 2"])
        self.tipo_cms = st.selectbox("Tipo CMS", ["Todos", "Tipo 1", "Tipo 2"])
        self.status = st.selectbox("Status", ["Todos", "Ativo", "Cancelado", "Concluído"])
        self.clientes = st.selectbox("Cliente", ["Todos", "Cliente 1", "Cliente 2"])
        self.produtos = st.selectbox("Produto", ["Todos", "Produto 1", "Produto 2"])
        self.placa = st.text_input("Placa", placeholder="Digite a placa do veículo")
        self.nome_motorista = st.text_input("Nome do Motorista", placeholder="Digite o nome do motorista")
        self.documento_motorista = st.text_input("Documento do Motorista", placeholder="Digite o documento do motorista")
        if self.user_tipo == "admin":
            self.user_id_filtro = st.selectbox("Usuário", ["Todos"] + self.db.get_usernames())

    def show(self):
        st.title("Histórico de Agendamentos")
        with st.expander("Filtros de Pesquisa", expanded=True):
            self.tela_filtros()
        if st.button("Pesquisar"):
            self.filtrar_agendamentos()
    def filtrar_agendamentos(self):
        selected_filters = f"SELECT * FROM agendamentos WHERE data_inicio_descarga = ? AND data_fim_descarga = ? and terminal = ? and tipo_cms = ? and status = ? and cliente = ? and produto = ? and placa = ? and nome_motorista = ? and documento_motorista = ? and usuario_id = ?"
        params = (self.data_inicial_descarga, self.data_final_descarga, self.terminal, self.tipo_cms, self.status, self.clientes, self.produtos, self.placa, self.nome_motorista, self.documento_motorista, self.user_id)
        query = "select * from agendamentos"
        self.db.cursor.execute(query)
        all_agendamentos = self.db.cursor.fetchall()
        st.write(all_agendamentos)

        # self.db.cursor.execute(selected_filters, params)
        # historico_agendamentos = self.db.cursor.fetchall()
        # st.write(historico_agendamentos)
    def exportar_excel(self):
        pass