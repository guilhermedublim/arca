from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from urllib.parse import quote
from extensions import app, db
from models.sala import Sala

db_session = db.session

with app.app_context():
    db.create_all()

# Dados simulados
salas = [{"nome": "Sala A", "localizacao": "Andar 1", "capacidade": 10, "equipamentos": "Projetor, Wi-Fi"}]
reservas = []
notificacoes = ["Lembrete: Reunião em 1 hora", "Confirmação de reserva"]

@app.context_processor
def inject_notifications():
    return dict(notificacoes=notificacoes)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aqui você pode verificar as credenciais do usuário.
        # Se estiverem corretas, redirecione para o menu.
        if username == "admin" and password == "1234":  # Exemplo de validação simples
            return redirect(url_for('menu'))
        else:
            return "Usuário ou senha incorretos", 401
    return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', notificacoes=notificacoes)

@app.route('/salas', methods=['GET'])
def listar_salas():
    per_page = 10  # Número de registros por página
    page = request.args.get('page', 1, type=int)
    pagination = Sala.query.paginate(page=page, per_page=per_page, error_out=False)
    salas = pagination.items
    return render_template('salas.html', salas=salas, pagination=pagination)

@app.route('/salas/cadastrar', methods=['GET', 'POST'])
def cadastrar_sala():
    if request.method == 'POST':
        # Captura os dados do formulário
        nome = request.form['nome']
        localizacao = request.form['localizacao']
        capacidade = int(request.form['capacidade'])
        equipamentos = request.form['equipamentos']

        # Cria uma nova instância do modelo Sala
        nova_sala = Sala(nome=nome, localizacao=localizacao, capacidade=capacidade, equipamentos=equipamentos)

        # Adiciona e faz commit no banco de dados usando db_session
        db_session.add(nova_sala)
        db_session.commit()

        return redirect(url_for('menu'))

    return render_template('sala_form.html', titulo="Cadastrar Sala", sala=None, readonly=False, action_url=url_for('cadastrar_sala'))

@app.route('/salas/editar/<int:sala_id>', methods=['GET', 'POST'])
def editar_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    if request.method == 'POST':
        sala.nome = request.form['nome']
        sala.localizacao = request.form['localizacao']
        sala.capacidade = int(request.form['capacidade'])
        sala.equipamentos = request.form['equipamentos']
        db.session.commit()

        return redirect(url_for('listar_salas'))

    return render_template('sala_form.html', titulo="Alterar Sala", sala=sala, readonly=False, action_url=url_for('editar_sala', sala_id=sala_id))

@app.route('/salas/excluir/<int:sala_id>', methods=['POST'])
def excluir_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    db.session.delete(sala)
    db.session.commit()

    return redirect(url_for('listar_salas'))

@app.route('/salas/visualizar/<int:sala_id>', methods=['GET'])
def visualizar_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    return render_template('sala_form.html', titulo="Visualizar Sala", sala=sala, readonly=True, action_url="#")

@app.route('/reservas')
def reservas_salas():
    return render_template('reservas.html', salas=salas, reservas=reservas)

@app.route('/reservar/<nome_sala>')
def reservar(nome_sala):
    reserva = {"sala": nome_sala, "usuario": "Usuário Exemplo"}
    reservas.append(reserva)
    return redirect(url_for('reservas_salas'))

if __name__ == '__main__':
    app.run(debug=True)