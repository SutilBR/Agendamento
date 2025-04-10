import streamlit as st
from database import Database
# Precisa criar o historico dos agendamentos, aqui precisa aparecer TODOS os agendamentos feitos por esse usuario (lembrando, cada usuario pode ver apenas o agendamento de seu user)
class HistoricoAgendamentos:
    def __init__(self):
        self.db = Database()

    def tela_historico(self):
        pass

    def consulta_especifica(self):
        pass

    def exportar_excel(self):
        pass