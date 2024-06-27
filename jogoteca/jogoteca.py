from flask import Flask, render_template, request, redirect, session, flash, url_for

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Henrique Bastos", "HB", "Bastos17")
usuario2 = Usuario("Lais Bastos", "LB", "Lala12")
usuario3 = Usuario("Heitor Bastos", "cria", "Heitor24")

usuarios = { usuario1.nickname: usuario1, 
             usuario2.nickname: usuario2, 
             usuario3.nickname: usuario3 }

app = Flask(__name__)
app.secret_key = 'henricao123'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'puzzle', 'Atari')
jogo2 = Jogo('God of War', 'hack n slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'luta', 'PS3')

lista = [jogo1, jogo2, jogo3]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    novo_jogo = Jogo(nome, categoria, console)
    lista.append(novo_jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso! ', 'success')
            proxima_pagina = request.form.get('proxima')
            if proxima_pagina:
                return redirect(proxima_pagina)
            else:
                return redirect(url_for('index'))
    else:
        flash('Usuário não logado.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout executado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
