from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

# Função para criar a tabela 'postagens' no banco de dados
def criar_tabela():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS postagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            conteudo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rota da página inicial (Home)
@app.route('/')
def home():
    return render_template('home.html')

# Rota da página Sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota da página Contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Rota da página de postagens
@app.route('/postagens')
def postagens():
    criar_tabela()
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM postagens')
    postagens = cursor.fetchall()
    conn.close()
    return render_template('postagens.html', postagens=postagens)

# Rota para adicionar uma nova postagem
@app.route('/nova_postagem', methods=['GET', 'POST'])
def nova_postagem():
    if 'usuario' not in session or session['usuario'] != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']

        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO postagens (titulo, conteudo) VALUES (?, ?)', (titulo, conteudo))
        conn.commit()
        conn.close()

    return redirect(url_for('postagens'))

# Rota para fazer login como administrador
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Verifique se as credenciais são corretas (por exemplo, usuário=admin, senha=admin)
        if usuario == 'admin' and senha == 'admin':
            session['usuario'] = 'admin'
            return redirect(url_for('postagens'))

    return render_template('login.html')

# Rota para fazer logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

