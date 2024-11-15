from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from extensions import app, db
from models.sala import Sala
from models.usuario import Usuario
from models.reserva import Reserva
from functools import wraps
from datetime import datetime

db_session = db.session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Verifica se o usuário está logado
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        senha = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(senha):
            session['user_id'] = usuario.id  # Salva o ID do usuário na sessão
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('menu'))  # Redireciona para o menu principal
        else:
            error = "Email ou senha inválidos."
            flash('Email ou senha inválidos.', 'error')
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)  # Remove o ID do usuário da sessão
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('login'))

notificacoes = []

@app.route('/menu')
@login_required
def menu():
    usuarios = Usuario.query.filter(Usuario.id == session['user_id']).first()
    return render_template('menu.html', notificacoes=notificacoes, usuarios=usuarios)

@app.route('/salas', methods=['GET'])
@login_required
def listar_salas():
    per_page = 10 
    page = request.args.get('page', 1, type=int)
    pagination = Sala.query.paginate(page=page, per_page=per_page, error_out=False)
    salas = pagination.items
    return render_template('salas.html', salas=salas, pagination=pagination)

@app.route('/salas/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_sala():
    if request.method == 'POST':
        nome = request.form['nome']
        localizacao = request.form['localizacao']
        capacidade = int(request.form['capacidade'])
        equipamentos = request.form['equipamentos']
        nova_sala = Sala(nome=nome, localizacao=localizacao, capacidade=capacidade, equipamentos=equipamentos)
        db_session.add(nova_sala)
        db_session.commit()
        return redirect(url_for('menu'))
    return render_template('sala_form.html', titulo="Cadastrar Sala", sala=None, readonly=False, action_url=url_for('cadastrar_sala'))

@app.route('/salas/editar/<int:sala_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def excluir_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    db.session.delete(sala)
    db.session.commit()
    return redirect(url_for('listar_salas'))

@app.route('/salas/visualizar/<int:sala_id>', methods=['GET'])
@login_required
def visualizar_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    return render_template('sala_form.html', titulo="Visualizar Sala", sala=sala, readonly=True, action_url="#")

@app.route('/reservas', methods=['GET'])
@login_required
def listar_reservas():
    pesquisa = request.args.get('pesquisa', '').strip()
    sala_id = request.args.get('sala_id')
    data_reserva = request.args.get('data_reserva')
    page = request.args.get('page', 1, type=int)
    reservas_query = Reserva.query.join(Sala).join(Usuario)
    if pesquisa:
        reservas_query = reservas_query.filter(
            (Usuario.nome.ilike(f'%{pesquisa}%')) |
            (Sala.nome.ilike(f'%{pesquisa}%'))
        )
    if sala_id:
        reservas_query = reservas_query.filter(Reserva.sala_id == sala_id)
    if data_reserva:
        reservas_query = reservas_query.filter(Reserva.data_reserva == data_reserva)
    reservas_query = reservas_query.order_by(Reserva.data_reserva, Reserva.horario_inicio)
    pagination = reservas_query.paginate(page=page, per_page=10)
    reservas = pagination.items
    salas = Sala.query.all()
    return render_template('reservas.html', reservas=reservas, salas=salas, pagination=pagination, pesquisa=pesquisa, sala_id=sala_id, data_reserva=data_reserva)

@app.route('/reservas/criar', methods=['GET', 'POST'])
@login_required
def criar_reserva():
    if request.method == 'POST':
        try:
            salas = Sala.query.all()
            usuarios = Usuario.query.all()
            sala_id = request.form['sala_id']
            usuario_id = request.form['usuario_id']
            data_reserva = datetime.strptime(request.form['data_reserva'], '%Y-%m-%d').date()
            horario_inicio = datetime.strptime(request.form['horario_inicio'], '%H:%M').time()
            horario_fim = datetime.strptime(request.form['horario_fim'], '%H:%M').time()

            conflito = Reserva.query.filter(
                Reserva.sala_id == sala_id,
                Reserva.data_reserva == data_reserva,
                Reserva.horario_inicio < horario_fim,
                Reserva.horario_fim > horario_inicio
            ).first()

            if conflito:
                flash('Conflito de horários para a sala selecionada!', 'error')
                return render_template('reserva_form.html', title='Criar Reserva', modo='criar', salas=salas, usuarios=usuarios, reserva={
                        'sala_id': sala_id,
                        'usuario_id': usuario_id,
                        'data_reserva': data_reserva,
                        'horario_inicio': horario_inicio,
                        'horario_fim': horario_fim
                    }
                )

            nova_reserva = Reserva(
                sala_id=sala_id,
                usuario_id=usuario_id,
                data_reserva=data_reserva,
                horario_inicio=horario_inicio,
                horario_fim=horario_fim
            )
            db.session.add(nova_reserva)
            db.session.commit()
            flash('Reserva criada com sucesso!', 'success')
            return redirect(url_for('listar_reservas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao criar a reserva: {str(e)}', 'error')
        return render_template('reserva_form.html', title='Criar Reserva', modo='criar', salas=salas, usuarios=usuarios, reserva=None)
    salas = Sala.query.all()
    usuarios = Usuario.query.all()
    return render_template('reserva_form.html', title='Criar Reserva', modo='criar', salas=salas, usuarios=usuarios, reserva=None)

@app.route('/reservas/<int:id>')
@login_required
def visualizar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    salas = Sala.query.all()
    usuarios = Usuario.query.all()
    return render_template('reserva_form.html', title='Visualizar Reserva', modo='visualizar', salas=salas, usuarios=usuarios, reserva=reserva)

@app.route('/reservas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    salas = Sala.query.all()
    usuarios = Usuario.query.all()
    if request.method == 'POST':
        try:
            reserva.sala_id = request.form['sala_id']
            reserva.usuario_id = request.form['usuario_id']
            reserva.data_reserva = datetime.strptime(request.form['data_reserva'], '%Y-%m-%d').date()
            reserva.horario_inicio = datetime.strptime(request.form['horario_inicio'], '%H:%M').time()
            reserva.horario_fim = datetime.strptime(request.form['horario_fim'], '%H:%M').time()
            db.session.commit()
            flash('Reserva atualizada com sucesso!', 'success')
            return redirect(url_for('listar_reservas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao atualizar a reserva: {str(e)}', 'danger')
    return render_template('reserva_form.html', title='Editar Reserva', modo='editar', salas=salas, usuarios=usuarios, reserva=reserva)

@app.route('/reservas/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    db.session.delete(reserva)
    db.session.commit()
    flash('Reserva excluída com sucesso!', 'success')
    return redirect(url_for('listar_reservas'))

@app.route('/criar_usuario')
def criar_usuario():
    novo_usuario = Usuario(
        nome="Admin",
        email="admin@gmail.com",
        data_nascimento=datetime.strptime("2001-07-20", "%Y-%m-%d").date(),
        cpf="12312312378",
        telefone="47999999999",
        tipo_usuario="ADMIN"
    )
    novo_usuario.set_password("1234")
    db.session.add(novo_usuario)
    try:
        db.session.commit()
        flash("Usuário criado com sucesso!", 'success')
    except Exception as e:
        flash(f'Erro ao criar o usuário: {str(e)}', 'error')
    return redirect(url_for('login'))

@app.route('/conta/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes_conta():
    usuario = Usuario.query.get_or_404(current_user.id)

    if request.method == 'POST':
        try:
            # Atualizar informações pessoais
            usuario.email = request.form['email']
            usuario.telefone = request.form['telefone']
            db.session.commit()
            flash('Informações pessoais atualizadas!', 'success')

            # Alterar senha
            if 'nova_senha' in request.form and 'confirmar_senha' in request.form:
                nova_senha = request.form['nova_senha']
                confirmar_senha = request.form['confirmar_senha']
                if nova_senha == confirmar_senha:
                    usuario.senha = generate_password_hash(nova_senha)
                    db.session.commit()
                    flash('Senha alterada com sucesso!', 'success')
                else:
                    flash('As senhas não coincidem!', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro: {str(e)}', 'danger')

    return render_template('configuracoes_conta.html', usuario=usuario)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    usuario = Usuario.query.get(session['user_id'])

    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.telefone = request.form.get('telefone')
        usuario.endereco = request.form.get('endereco')
        usuario.data_nascimento = datetime.strptime(request.form['data_nascimento'], "%Y-%m-%d").date()

        try:
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('menu'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar o perfil: {str(e)}', 'danger')
            db.session.rollback()
        return redirect(url_for('editar_perfil'))
    return render_template('editar_perfil.html', usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)