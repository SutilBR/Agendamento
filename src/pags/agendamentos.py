import streamlit as st
import sqlite3
from database import Database
import time
from datetime import date
import xml.etree.ElementTree as ET
from database import DB_NAME

# Essa tela é para o cadastro de agendamentos
# Adicionar a leitura do xml em outra tabela com as infos do xml e foreing key do id

class Agendamentos:
    def __init__(self):
        self.db = Database()
        self.hoje = date.today().isoformat()

    def show(self):
        st.title("Agendamentos")

        user_id = st.session_state["auth_user"]["id"]
        user_tipo = st.session_state["auth_user"]["tipo"]

        if user_tipo == "admin":
            query = "SELECT id, usuario_id, placa, descricao, data, cliente FROM agendamentos WHERE data = ?"
            params = (self.hoje,)
        else:
            query = "SELECT id, usuario_id, placa, descricao, data, cliente FROM agendamentos WHERE usuario_id = ? AND data = ?"
            params = (user_id, self.hoje)

        # Criar novo agendamento
        with st.form("Novo Agendamento"):
            placa = st.text_input("Placa Cavalo")
            placa_carreta = st.text_input("Placa Carreta 1")
            placa_carreta2 = st.text_input("Placa Carreta 2")
            cliente = st.selectbox("Escolha o Cliente", ["Cliente 1", "Cliente 2"])
            terminal = st.selectbox("Escolha o Terminal", ["Terminal 1", "Terminal 2"])
            produto = st.selectbox("Escolha o Produto", ["Produto 1", "Produto 2"])
            nome_motorista = st.text_input("Nome do motorista")
            telefone_motorista = st.text_input("Telefone do motorista")
            documento_motorista = st.text_input("Documento do motorista")
            tipo_cms = st.selectbox("Escolha o tipo do caminhão", ["Tipo 1", "Tipo 2"])
            descricao = st.text_area("Descrição")
            data = st.date_input("Data")
            nf_xml = st.file_uploader("Por favor, selecione o XML da nota", type=["xml"], accept_multiple_files=True)

            if st.form_submit_button("Salvar"):
                if all([placa, cliente, terminal, nome_motorista, telefone_motorista, 
                    documento_motorista, tipo_cms, data, produto, placa_carreta, placa_carreta2, nf_xml]):
                    try:
                        if user_tipo == "admin":
                            placa = "ADMIN_" + str(user_id) + " " + placa
                        self.db.cursor.execute(
                            "INSERT INTO agendamentos (usuario_id, placa, placa_carreta, placa_carreta2, descricao, data, data_cadastro, cliente, terminal, tipo_cms, nome_motorista, telefone_motorista, documento_motorista, produto) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (user_id, placa, placa_carreta, placa_carreta2, descricao, data, time.time(), cliente, terminal, tipo_cms, nome_motorista, telefone_motorista, documento_motorista, produto),
                        )
                        print("aqui-teste")
                        self.db.conn.commit()
                        id_agendamento = self.db.cursor.lastrowid

                        self.ler_xml(nf_xml, id_agendamento)
                        st.success("Agendamento criado com sucesso!")
                        self.db.conn.commit()
                        time.sleep(3)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro, por favor, tente novamente mais tarde {e}")
                else:
                    st.error("Por favor, preencha todas as informações")

        self.db.cursor.execute(query, params)
        agendamentos = self.db.cursor.fetchall()

        col1, col2 = st.columns(2)

        agendamentos_cliente1 = [ag for ag in agendamentos if ag[5] == "Cliente 1"]
        agendamentos_cliente2 = [ag for ag in agendamentos if ag[5] == "Cliente 2"]

        with col1:
            st.subheader("Agendamentos Cliente 1")
            if agendamentos_cliente1:
                for ag in agendamentos_cliente1:
                    st.write(f"**Placa:** {ag[2]}")
                    st.write(f"**Descrição:** {ag[3]}")
                    st.write(f"**Data:** {ag[4]}")
                    st.write("---")
            else:
                st.write("Nenhum agendamento encontrado.")

        with col2:
            st.subheader("Agendamentos Cliente 2")
            if agendamentos_cliente2:
                for ag in agendamentos_cliente2:
                    st.write(f"**Placa:** {ag[2]}")
                    st.write(f"**Descrição:** {ag[3]}")
                    st.write(f"**Data:** {ag[4]}")
                    st.write("---")
            else:
                st.write("Nenhum agendamento encontrado.")

    def ler_xml(self, nf_xml, id_agendamento):
        try:
            for xml_file in nf_xml:
                xml_nome = xml_file.name
                xml_content = xml_file.read()
                try:
                    root = ET.fromstring(xml_content)
                    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
                    # chave de acesso
                    try:
                        chave_acesso = root.find(".//{http://www.portalfiscal.inf.br/nfe}infNFe", namespaces=ns).attrib["Id"]
                    except Exception as e:
                        chave_acesso == "No Info"

                    # Número da nota
                    try:
                        numero_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}nNF", namespaces=ns).text
                    except Exception as e:
                        numero_nota == "No Info"
                    
                    # Série da nota
                    try:
                        serie_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}serie", namespaces=ns).text
                    except Exception as e:
                        serie_nota == "No Info"

                    # Produto da nota - Supondo que a estrutura seja algo assim (ajustar conforme necessário)
                    try:
                        produtos = root.findall(".//{http://www.portalfiscal.inf.br/nfe}det", namespaces=ns)
                        produto_nota = [prod.find("{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}xProd", namespaces=ns).text for prod in produtos]
                        prod_nome = produto_nota[0]
                    except Exception as e:
                        produtos == "No Info"
                        produto_nota == "No Info"
                        prod_nome == "No Info"

                    # Quantidade do produto
                    try:
                        quantidade_nota = [prod.find("{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}qCom", namespaces=ns).text for prod in produtos]
                        quantidade = quantidade_nota[0]
                    except Exception as e:
                        quantidade == "No Info"

                    # CNPJ do exportador, emitente, retirada, transportador, entrega
                    try:
                        exportador_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}CNPJ", namespaces=ns)
                        if exportador_nota is None:
                            exportador_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}CPF", namespaces=ns)

                        # Se encontrar a tag, acessa o texto, caso contrário, define como "No Info"
                        exportador_nota = exportador_nota.text if exportador_nota is not None else "No Info"
                    except Exception as e:
                        exportador_nota == "No Info"
                        
                    # CNPJ emitente
                    try:
                        emitente_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}CNPJ", namespaces=ns)
                        if emitente_nota is None:
                            emitente_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}CPF", namespaces=ns)

                        # Se encontrar a tag, acessa o texto, caso contrário, define como None
                        emitente_nota = emitente_nota.text if emitente_nota is not None else "No Info"
                    except Exception as e:
                        emitente_nota == "No Info"

                    # CNPJ retirada
                    try:
                        retirada_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}retirada/{http://www.portalfiscal.inf.br/nfe}CNPJ", namespaces=ns)
                        if retirada_nota is None:
                            retirada_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}retirada/{http://www.portalfiscal.inf.br/nfe}CPF", namespaces=ns)

                        # Se encontrar a tag, acessa o texto, caso contrário, define como None
                        retirada_nota = retirada_nota.text if retirada_nota is not None else "No Info"
                    except Exception as e:
                        retirada_nota == "No Info"
                    
                    # CNPJ transportadora
                    try:
                        transportador_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}transportador/{http://www.portalfiscal.inf.br/nfe}CNPJ", namespaces=ns)
                        if transportador_nota is None:
                            transportador_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}transportador/{http://www.portalfiscal.inf.br/nfe}CPF", namespaces=ns)

                        # Se encontrar a tag, acessa o texto, caso contrário, define como None
                        transportador_nota = transportador_nota.text if transportador_nota is not None else "No Info"
                    except Exception as e:
                        transportador_nota == "No Info"
                        
                    # CNPJ entrega
                    try:
                        entrega_nota = root.find(".//{http://www.portalfiscal.inf.br/nfe}entrega/{http://www.portalfiscal.inf.br/nfe}CNPJ", namespaces=ns).text if root.find(".//{http://www.portalfiscal.inf.br/nfe}entrega", namespaces=ns) else "No Info"
                    except Exception as e:
                        entrega_nota == "No Info"

                    # Informações complementares
                    try:
                        info_cpl = root.find(".//{http://www.portalfiscal.inf.br/nfe}infCpl", namespaces=ns).text if root.find(".//{http://www.portalfiscal.inf.br/nfe}infCpl", namespaces=ns) else "No Info"
                    except Exception as e:
                        info_cpl == "No Info" 

                    print(chave_acesso, numero_nota, serie_nota, prod_nome, quantidade, exportador_nota, emitente_nota, retirada_nota, transportador_nota,
                          entrega_nota, info_cpl)
                    user_id = st.session_state["auth_user"]["id"]
                    self.db.cursor.execute("INSERT INTO arquivos (usuario_id, id_agendamento, chave_acesso, numero_nota, serie_nota, produto_nota, quantidade_nota, exportador_nota, emitente_nota, retirada_nota, transportador_nota, entrega_nota, info_cpl) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, id_agendamento, chave_acesso, numero_nota, serie_nota, prod_nome, quantidade, exportador_nota, emitente_nota, retirada_nota, transportador_nota, entrega_nota, info_cpl))
                except Exception as e: # Erro para encontrar alguma info
                    self.db.cursor.execute("INSERT INTO arquivos (usuario_id, id_agendamento, chave_acesso, numero_nota, serie_nota, produto_nota, quantidade_nota, exportador_nota, emitente_nota, retirada_nota, transportador_nota, entrega_nota, info_cpl) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, id_agendamento, chave_acesso, numero_nota, serie_nota, prod_nome, quantidade, exportador_nota, emitente_nota, retirada_nota, transportador_nota, entrega_nota, info_cpl))
                    st.error(f"Erro para encontrar informações no arquivo {xml_nome}, não é necessário reenviar no momento. {e}")
        except Exception as e: # erro na leitura de algum xmls
            self.db.cursor.execute("INSERT INTO arquivos (usuario_id, id_agendamento, chave_acesso, numero_nota, serie_nota, produto_nota, quantidade_nota, exportador_nota, emitente_nota, retirada_nota, transportador_nota, entrega_nota, info_cpl) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, id_agendamento, chave_acesso, numero_nota, serie_nota, prod_nome, quantidade, exportador_nota, emitente_nota, retirada_nota, transportador_nota, entrega_nota, info_cpl))
            st.error(f"Erro na leitura do arquivo {xml_nome}, não é necessário reenviar. {e}")
        

        # Continuar para inserir as informacoes no banco de dados.