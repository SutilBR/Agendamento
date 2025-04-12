import streamlit as st
from database import Database
import pandas as pd
import sqlite3
from datetime import date
# Precisa criar o historico dos agendamentos, aqui precisa aparecer TODOS os agendamentos feitos por esse usuario (lembrando, cada usuario pode ver apenas o agendamento de seu user)
DB_NAME = "agendamentos.db"
class Historico:
    def __init__(self):
        self.db = Database()
        self.user_id = st.session_state["auth_user"]["id"]
        self.user_tipo = st.session_state["auth_user"]["tipo"]
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
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
        if self.user_tipo == "admin":
            query = "SELECT * FROM agendamentos WHERE 1=1"
            params = []
        else:
            query = "SELECT * FROM agendamentos WHERE usuario_id = ?"
            params = [self.user_id]

        dict_query = {
            "data_inicio_descarga": self.data_inicial_descarga.strftime("%Y-%m-%d") if isinstance(self.data_inicial_descarga, date) else self.data_inicial_descarga,
            "data_fim_descarga": self.data_final_descarga.strftime("%Y-%m-%d") if isinstance(self.data_final_descarga, date) else self.data_final_descarga,
            "terminal": self.terminal,
            "tipo_cms": self.tipo_cms,
            "status": self.status,
            "clientes": self.clientes,
            "produtos": self.produtos,
            "placa": self.placa,
            "nome_motorista": self.nome_motorista,
            "documento_motorista": self.documento_motorista,
        }

        for coluna, valor in dict_query.items():
            if valor and valor != "Todos":
                if coluna == "data_inicio_descarga":
                    query += " AND data_inicio_descarga >= ?"
                    params.append(valor)

                elif coluna == "data_fim_descarga":
                    query += " AND (data_fim_descarga <= ? OR data_fim_descarga IS NULL)"
                    params.append(valor)

                else:
                    query += f" AND {coluna} = ?"
                    params.append(valor)
        all_agendamentos = pd.read_sql(query, self.conn, params=tuple(params))
        st.write(all_agendamentos)
    def exportar_excel(self):
        pass