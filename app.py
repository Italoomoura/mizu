from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações do banco de dados MySQL
db = mysql.connector.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database=os.getenv("database"),
    port=int(os.getenv("port"))
)
cursor = db.cursor()

# Rotas
@app.route('/')
def index():
    # Listar todos os usuários
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template('index.html', usuarios=usuarios)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        # Inserir novo usuário no banco de dados
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
        db.commit()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        # Atualizar usuário no banco de dados
        cursor.execute("UPDATE usuarios SET nome = %s, email = %s WHERE id = %s", (nome, email, id))
        db.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', usuario=usuario)

@app.route('/deletar/<int:id>')
def deletar(id):
    # Deletar usuário do banco de dados
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
