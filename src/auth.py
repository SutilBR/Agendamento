import sqlite3
import hashlib
from database import DB_NAME

# Código para garantir login e segurança dos usuarios


class Auth:
    def hash_senha(self, senha):
        """Retorna o hash SHA-256 da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()

    def login(self, email, senha):
        """Autentica usuário e retorna os dados se válido"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        senha_hash = self.hash_senha(senha)

        cursor.execute("""
            SELECT id, nome, tipo 
            FROM usuarios 
            WHERE email = ? AND senha = ?
        """, (email, senha_hash))
        
        user = cursor.fetchone()
        conn.close()
        return user