import sqlite3
import hashlib

# Criando o banco de dados, é util para manter o código organizado e sempre encontrar a tabela que precisamos. qlqr alteração aqui precisa ser revisada

DB_NAME = "agendamentos.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Cria as tabelas no banco de dados"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('comum', 'admin')) DEFAULT 'comum'
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                placa TEXT NOT NULL,
                placa_carreta TEXT NOT NULL,
                placa_carreta2 TEXT NOT NULL,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                data_cadastro TEXT NOT NULL,
                data_inicio_descarga TEXT NULL,
                data_fim_descarga TEXT NULL,
                cliente TEXT NOT NULL,
                terminal TEXT NOT NULL,
                tipo_cms TEXT NOT NULL,
                nome_motorista TEXT NOT NULL,
                telefone_motorista TEXT NOT NULL,
                documento_motorista TEXT NOT NULL,
                produto TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('ativo', 'cancelado', 'concluído')) DEFAULT 'ativo',
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS arquivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                id_agendamento INTEGER NOT NULL,
                chave_acesso TEXT NOT NULL,
                numero_nota TEXT NOT NULL,
                serie_nota TEXT NOT NULL,
                produto_nota TEXT NOT NULL,
                quantidade_nota TEXT NOT NULL,
                exportador_nota TEXT NOT NULL,
                emitente_nota TEXT NOT NULL,
                retirada_nota TEXT NOT NULL,
                transportador_nota TEXT NOT NULL,
                entrega_nota TEXT NOT NULL,
                info_cpl TEXT NOT NULL,
                FOREIGN KEY (id_agendamento) REFERENCES agendamentos(id)
            )
        ''')
        self.conn.commit()

    def insert_usuario(self, nome, email, senha, tipo="comum"):
        """Função para criar um usuário manualmente"""
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo),
            )
            self.conn.commit()
            print(f"Usuário {nome} criado com sucesso!")
        except sqlite3.IntegrityError:
            print(f"Erro: Email {email} já está em uso.")
    def get_usernames(self):
        select_users = "SELECT nome FROM usuarios"
        self.cursor.execute(select_users)
        users = self.cursor.fetchall()
        users = [user[0] for user in users]
        return users
    def close(self):
        self.conn.close()
