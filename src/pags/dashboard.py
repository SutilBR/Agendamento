import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import plotly.express as px
from database import DB_NAME

class Dashboard:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.nome_usuario = self.buscar_nome_usuario()  # Obtém o nome ao inicializar

    def buscar_nome_usuario(self):
        """Busca o nome do usuário no banco de dados"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Busca o nome do usuário pelo ID
        cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (self.usuario_id,))
        resultado = cursor.fetchone()
        conn.close()

        # Retorna o nome do usuário se encontrado, ou uma mensagem padrão
        return resultado[0] if resultado else "Usuário desconhecido"

    def show(self):
        st.title("📋 Painel Principal")
        st.success(f"Bem-vindo, {self.nome_usuario}!")  # Exibe o nome do usuário
        self.mostrar_agendamentos()
        self.mostrar_graficos()

    def mostrar_agendamentos(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT data, descricao 
            FROM agendamentos
            WHERE usuario_id = ?
            ORDER BY data_cadastro DESC
            LIMIT 5
        """, (self.usuario_id,))
        
        agendamentos = cursor.fetchall()
        conn.close()

        st.subheader("📝 Últimos Agendamentos")
        if agendamentos:
            for data, descricao in agendamentos:
                st.write(f"📅 **Data:** {data} | 📝 **Descrição:** {descricao}")
        else:
            st.info("Nenhum agendamento encontrado.")

    def mostrar_graficos(self):
        conn = sqlite3.connect(DB_NAME)

        # Leia os dados do banco para um DataFrame
        df = pd.read_sql_query("""
            SELECT cliente, produto, data_cadastro 
            FROM agendamentos 
            WHERE usuario_id = ?
        """, conn, params=(self.usuario_id,))
        conn.close()

        # Validação para evitar o erro se o DataFrame estiver vazio
        if df.empty:
            st.warning("Ainda não há dados suficientes para gerar gráficos.")
            return

        # Convertendo timestamps Unix na coluna "data_cadastro" para datas legíveis
        df["data_cadastro"] = pd.to_datetime(df["data_cadastro"], unit="s")
        df["dia"] = df["data_cadastro"].dt.date

        st.subheader("📊 Gráficos de Agendamentos")

        # Gráfico 1: Agendamentos por dia
        ag_por_dia = df.groupby("dia").size().reset_index(name="quantidade")
        fig1 = px.bar(ag_por_dia, x="dia", y="quantidade", title="Agendamentos por Dia")
        st.plotly_chart(fig1, use_container_width=True)

        # Gráfico 2: Clientes mais frequentes
        clientes = df["cliente"].value_counts().reset_index()
        clientes.columns = ["cliente", "quantidade"]
        fig2 = px.bar(clientes, x="cliente", y="quantidade", title="Top Clientes")
        st.plotly_chart(fig2, use_container_width=True)

        # Gráfico 3: Produtos mais agendados
        produtos = df["produto"].value_counts().reset_index()
        produtos.columns = ["produto", "quantidade"]
        fig3 = px.pie(produtos, names="produto", values="quantidade", title="Distribuição por Produto")
        st.plotly_chart(fig3, use_container_width=True)
