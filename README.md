# ARCA - Sistema de Gestão de Salas Corporativas

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/) 
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

ARCA é um sistema web desenvolvido para facilitar a gestão de salas corporativas, permitindo reservas, visualização de disponibilidade e gerenciamento eficiente. O objetivo é oferecer uma interface moderna e intuitiva para usuários e administradores.

---

## 🚀 **Funcionalidades**

- **Cadastro de Salas**: Criação e edição de informações detalhadas sobre cada sala corporativa.
- **Reserva de Salas**: Agendamento e visualização de horários disponíveis.
- **Filtros e Pesquisa**: Busca avançada por data, sala ou disponibilidade.
- **Gerenciamento de Usuários**: Permite atribuir usuários às reservas de forma segura e rápida.
- **Alertas de Conflito**: Identifica e alerta automaticamente sobre conflitos de horário.

---

## 🛠️ **Tecnologias Utilizadas**

- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Python (Flask)
- **Banco de Dados**: SQLite (ambos suportados)
- **Outras Ferramentas**:
  - SQLAlchemy para ORM
  - Flask-WTF para validação de formulários
  - Jinja2 para templates HTML

---

## 📦 **Instalação**

### **Pré-requisitos**
Certifique-se de ter instalado:
- Python 3.11+
- PostgreSQL ou SQLite

### **Passos**
1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/arca.git
    cd arca
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:
    - A configuração padrão será usada.

5. Inicialize o banco de dados:
    ```bash
    flask db upgrade
    ```

6. Inicie o servidor:
    ```bash
    flask run
    ```

7. Acesse o sistema em [http://localhost:5000](http://localhost:5000).

---

## 🌟 **Capturas de Tela**

1. **Tela de Listagem de Salas**  
   ![Listagem de Salas](docs/screenshots/listagem_salas.png)

2. **Tela de Cadastro de Reserva**  
   ![Cadastro de Reserva](docs/screenshots/cadastro_reserva.png)

3. **Dashboard com Estatísticas**
   ![Dashboard](docs/screenshots/dashboard.png)

---
🔒 Licença

Este projeto é licenciado sob a MIT License.

---
📧 Contato
- Autor: Guilherme Moreira Dublim
- E-mail: gdublim@gmail.com
- LinkedIn: https://www.linkedin.com/in/guilherme-moreira-dublim-4092271a5/

---
📌 To-Do (Roadmap)
- Implementar autenticação baseada em OAuth.
- Adicionar suporte para exportar relatórios em PDF.
- Criar uma API para integração com sistemas externos.
- Melhorar as notificações de conflito de horários.
