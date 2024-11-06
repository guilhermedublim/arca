from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/cadastro_sala', methods=['GET', 'POST'])
def cadastro_sala():
    if request.method == 'POST':
        nova_sala = {
            "nome": request.form['nome'],
            "localizacao": request.form['localizacao'],
            "capacidade": request.form['capacidade'],
            "equipamentos": request.form['equipamentos']
        }
        salas.append(nova_sala)
        return redirect(url_for('menu'))
    return render_template('cadastro_sala.html')

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