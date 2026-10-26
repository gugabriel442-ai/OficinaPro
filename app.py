
from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import Error
from database import conectar

app = Flask(__name__)
app.secret_key = "chave-temporaria-oficinapro"


# =========================================================
# FUNÇÕES AUXILIARES DO BANCO DE DADOS
# =========================================================

def buscar_um(sql, parametros=()):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        return cursor.fetchone()

    except Error as erro:
        print(f"Erro no banco de dados: {erro}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def buscar_todos(sql, parametros=()):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        return cursor.fetchall()

    except Error as erro:
        print(f"Erro no banco de dados: {erro}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def executar(sql, parametros=()):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(sql, parametros)
        conexao.commit()
        return True

    except Error as erro:
        if conexao:
            conexao.rollback()

        print(f"Erro no banco de dados: {erro}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


# =========================================================
# DASHBOARD E PESQUISA DE CLIENTES
# =========================================================

@app.route("/")
def inicio():
    total_clientes = buscar_um(
        "SELECT COUNT(*) AS total FROM clientes"
    )

    total_veiculos = buscar_um(
        "SELECT COUNT(*) AS total FROM veiculos"
    )

    ordens_pendentes = buscar_um(
        """
        SELECT COUNT(*) AS total
        FROM ordens_servico
        WHERE status IN ('Pendente', 'Em andamento')
        """
    )

    ordens_concluidas = buscar_um(
        """
        SELECT COUNT(*) AS total
        FROM ordens_servico
        WHERE status = 'Concluída'
        """
    )

    pesquisa_cliente = request.args.get(
        "pesquisa_cliente", ""
    ).strip()

    sql_clientes = """
        SELECT id, nome, telefone, email
        FROM clientes
    """

    parametros = []

    if pesquisa_cliente:
        sql_clientes += """
            WHERE nome LIKE %s
               OR telefone LIKE %s
               OR email LIKE %s
        """

        termo = f"%{pesquisa_cliente}%"
        parametros = [termo, termo, termo]

    sql_clientes += " ORDER BY id DESC"

    clientes = buscar_todos(
        sql_clientes, tuple(parametros)
    )

    return render_template(
        "index.html",
        total_clientes=total_clientes["total"] if total_clientes else 0,
        total_veiculos=total_veiculos["total"] if total_veiculos else 0,
        ordens_pendentes=ordens_pendentes["total"] if ordens_pendentes else 0,
        ordens_concluidas=ordens_concluidas["total"] if ordens_concluidas else 0,
        clientes=clientes,
        pesquisa_cliente=pesquisa_cliente
    )


# =========================================================
# CLIENTES
# =========================================================

@app.route("/clientes/cadastrar", methods=["POST"])
def cadastrar_cliente():
    nome = request.form.get("nome", "").strip()
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip()

    if not nome:
        flash("O nome do cliente é obrigatório.", "erro")
        return redirect(url_for("inicio") + "#cadastro-cliente")

    sucesso = executar(
        """
        INSERT INTO clientes (nome, telefone, email)
        VALUES (%s, %s, %s)
        """,
        (nome, telefone, email)
    )

    if sucesso:
        flash("Cliente cadastrado com sucesso!", "sucesso")
    else:
        flash("Não foi possível cadastrar o cliente.", "erro")

    return redirect(url_for("inicio") + "#clientes")


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    cliente = buscar_um(
        "SELECT * FROM clientes WHERE id = %s",
        (id,)
    )

    if not cliente:
        flash("Cliente não encontrado.", "erro")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome:
            flash("O nome do cliente é obrigatório.", "erro")
            return redirect(url_for("editar_cliente", id=id))

        sucesso = executar(
            """
            UPDATE clientes
            SET nome = %s, telefone = %s, email = %s
            WHERE id = %s
            """,
            (nome, telefone, email, id)
        )

        if sucesso:
            flash("Cliente atualizado com sucesso!", "sucesso")
            return redirect(url_for("inicio") + "#clientes")

        flash("Não foi possível atualizar o cliente.", "erro")

    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/clientes/excluir/<int:id>", methods=["POST"])
def excluir_cliente(id):
    cliente = buscar_um(
        "SELECT id FROM clientes WHERE id = %s",
        (id,)
    )

    if not cliente:
        flash("Cliente não encontrado.", "erro")
        return redirect(url_for("inicio") + "#clientes")

    veiculo = buscar_um(
        "SELECT id FROM veiculos WHERE cliente_id = %s LIMIT 1",
        (id,)
    )

    if veiculo:
        flash(
            "Não é possível excluir este cliente porque ele possui veículos cadastrados.",
            "erro"
        )
        return redirect(url_for("inicio") + "#clientes")

    sucesso = executar(
        "DELETE FROM clientes WHERE id = %s",
        (id,)
    )

    if sucesso:
        flash("Cliente excluído com sucesso!", "sucesso")
    else:
        flash("Não foi possível excluir o cliente.", "erro")

    return redirect(url_for("inicio") + "#clientes")


# =========================================================
# VEÍCULOS E PESQUISA
# =========================================================

@app.route("/veiculos")
def listar_veiculos():
    pesquisa = request.args.get("pesquisa", "").strip()

    sql = """
        SELECT
            v.id,
            v.cliente_id,
            c.nome AS cliente,
            v.marca,
            v.modelo,
            v.ano,
            v.placa
        FROM veiculos v
        INNER JOIN clientes c ON c.id = v.cliente_id
    """

    parametros = []

    if pesquisa:
        sql += """
            WHERE v.placa LIKE %s
               OR v.marca LIKE %s
               OR v.modelo LIKE %s
        """

        termo = f"%{pesquisa}%"
        parametros = [termo, termo, termo]

    sql += " ORDER BY v.id DESC"

    veiculos = buscar_todos(sql, tuple(parametros))

    clientes = buscar_todos(
        "SELECT id, nome FROM clientes ORDER BY nome"
    )

    return render_template(
        "veiculos.html",
        veiculos=veiculos,
        clientes=clientes,
        pesquisa=pesquisa
    )


@app.route("/veiculos/cadastrar", methods=["POST"])
def cadastrar_veiculo():
    cliente_id = request.form.get("cliente_id", "").strip()
    marca = request.form.get("marca", "").strip()
    modelo = request.form.get("modelo", "").strip()
    ano = request.form.get("ano", "").strip()
    placa = request.form.get("placa", "").strip().upper()

    if not all([cliente_id, marca, modelo, ano, placa]):
        flash("Preencha todos os campos do veículo.", "erro")
        return redirect(url_for("listar_veiculos"))

    try:
        cliente_id = int(cliente_id)
        ano = int(ano)
    except ValueError:
        flash("Cliente e ano devem ser valores válidos.", "erro")
        return redirect(url_for("listar_veiculos"))

    cliente = buscar_um(
        "SELECT id FROM clientes WHERE id = %s",
        (cliente_id,)
    )

    if not cliente:
        flash("Selecione um cliente cadastrado.", "erro")
        return redirect(url_for("listar_veiculos"))

    sucesso = executar(
        """
        INSERT INTO veiculos
            (cliente_id, marca, modelo, ano, placa)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (cliente_id, marca, modelo, ano, placa)
    )

    if sucesso:
        flash("Veículo cadastrado com sucesso!", "sucesso")
    else:
        flash(
            "Não foi possível cadastrar o veículo. Verifique se a placa já existe.",
            "erro"
        )

    return redirect(url_for("listar_veiculos"))


@app.route("/veiculos/editar/<int:id>", methods=["GET", "POST"])
def editar_veiculo(id):
    veiculo = buscar_um(
        "SELECT * FROM veiculos WHERE id = %s",
        (id,)
    )

    if not veiculo:
        flash("Veículo não encontrado.", "erro")
        return redirect(url_for("listar_veiculos"))

    if request.method == "POST":
        cliente_id = request.form.get("cliente_id", "").strip()
        marca = request.form.get("marca", "").strip()
        modelo = request.form.get("modelo", "").strip()
        ano = request.form.get("ano", "").strip()
        placa = request.form.get("placa", "").strip().upper()

        if not all([cliente_id, marca, modelo, ano, placa]):
            flash("Preencha todos os campos do veículo.", "erro")
            return redirect(url_for("editar_veiculo", id=id))

        try:
            cliente_id = int(cliente_id)
            ano = int(ano)
        except ValueError:
            flash("Cliente e ano devem ser valores válidos.", "erro")
            return redirect(url_for("editar_veiculo", id=id))

        cliente = buscar_um(
            "SELECT id FROM clientes WHERE id = %s",
            (cliente_id,)
        )

        if not cliente:
            flash("Selecione um cliente cadastrado.", "erro")
            return redirect(url_for("editar_veiculo", id=id))

        sucesso = executar(
            """
            UPDATE veiculos
            SET cliente_id = %s,
                marca = %s,
                modelo = %s,
                ano = %s,
                placa = %s
            WHERE id = %s
            """,
            (cliente_id, marca, modelo, ano, placa, id)
        )

        if sucesso:
            flash("Veículo atualizado com sucesso!", "sucesso")
            return redirect(url_for("listar_veiculos"))

        flash(
            "Não foi possível atualizar o veículo. Verifique se a placa já existe.",
            "erro"
        )

    clientes = buscar_todos(
        "SELECT id, nome FROM clientes ORDER BY nome"
    )

    return render_template(
        "editar_veiculo.html",
        veiculo=veiculo,
        clientes=clientes
    )


@app.route("/veiculos/excluir/<int:id>", methods=["POST"])
def excluir_veiculo(id):
    veiculo = buscar_um(
        "SELECT id FROM veiculos WHERE id = %s",
        (id,)
    )

    if not veiculo:
        flash("Veículo não encontrado.", "erro")
        return redirect(url_for("listar_veiculos"))

    ordem = buscar_um(
        """
        SELECT id
        FROM ordens_servico
        WHERE veiculo_id = %s
        LIMIT 1
        """,
        (id,)
    )

    if ordem:
        flash(
            "Não é possível excluir este veículo porque ele possui ordens de serviço.",
            "erro"
        )
        return redirect(url_for("listar_veiculos"))

    sucesso = executar(
        "DELETE FROM veiculos WHERE id = %s",
        (id,)
    )

    if sucesso:
        flash("Veículo excluído com sucesso!", "sucesso")
    else:
        flash("Não foi possível excluir o veículo.", "erro")

    return redirect(url_for("listar_veiculos"))


# =========================================================
# ORDENS DE SERVIÇO E PESQUISA POR CLIENTE
# =========================================================

@app.route("/ordens-servico")
def listar_ordens():
    pesquisa = request.args.get("pesquisa", "").strip()
    status_filtro = request.args.get("status", "").strip()

    sql = """
        SELECT
            os.id,
            os.veiculo_id,
            os.descricao,
            os.valor,
            os.status,
            os.data_abertura,
            v.marca,
            v.modelo,
            v.placa,
            c.nome AS cliente
        FROM ordens_servico os
        INNER JOIN veiculos v ON v.id = os.veiculo_id
        INNER JOIN clientes c ON c.id = v.cliente_id
        WHERE 1 = 1
    """

    parametros = []

    if pesquisa:
        sql += """
            AND (
                v.placa LIKE %s
                OR v.modelo LIKE %s
                OR v.marca LIKE %s
                OR os.descricao LIKE %s
                OR c.nome LIKE %s
            )
        """

        termo = f"%{pesquisa}%"
        parametros.extend([termo] * 5)

    status_permitidos = {
        "Pendente",
        "Em andamento",
        "Concluída"
    }

    if status_filtro in status_permitidos:
        sql += " AND os.status = %s"
        parametros.append(status_filtro)
    else:
        status_filtro = ""

    sql += " ORDER BY os.id DESC"

    ordens = buscar_todos(sql, tuple(parametros))

    veiculos = buscar_todos(
        """
        SELECT id, marca, modelo, placa
        FROM veiculos
        ORDER BY marca, modelo
        """
    )

    return render_template(
        "ordens_servico.html",
        ordens=ordens,
        veiculos=veiculos,
        pesquisa=pesquisa,
        status_filtro=status_filtro
    )

@app.route("/ordens-servico/detalhes/<int:id>")
def detalhes_ordem(id):
    ordem = buscar_um(
        """
        SELECT
            os.id,
            os.descricao,
            os.valor,
            os.status,
            os.data_abertura,
            c.nome AS cliente,
            c.telefone,
            c.email,
            v.marca,
            v.modelo,
            v.ano,
            v.placa
        FROM ordens_servico os
        INNER JOIN veiculos v ON v.id = os.veiculo_id
        INNER JOIN clientes c ON c.id = v.cliente_id
        WHERE os.id = %s
        """,
        (id,)
    )

    if not ordem:
        flash("Ordem de serviço não encontrada.", "erro")
        return redirect(url_for("listar_ordens"))

    return render_template(
        "detalhes_ordem.html",
        ordem=ordem
    )

@app.route("/ordens-servico/cadastrar", methods=["POST"])
def cadastrar_ordem():
    veiculo_id = request.form.get("veiculo_id", "").strip()
    descricao = request.form.get("descricao", "").strip()
    valor = request.form.get("valor", "").strip()

    if not all([veiculo_id, descricao, valor]):
        flash("Preencha todos os campos da ordem de serviço.", "erro")
        return redirect(url_for("listar_ordens"))

    try:
        veiculo_id = int(veiculo_id)
        valor = float(valor.replace(",", "."))
    except ValueError:
        flash("Informe um veículo e um valor válidos.", "erro")
        return redirect(url_for("listar_ordens"))

    if valor < 0:
        flash("O valor não pode ser negativo.", "erro")
        return redirect(url_for("listar_ordens"))

    veiculo = buscar_um(
        "SELECT id FROM veiculos WHERE id = %s",
        (veiculo_id,)
    )

    if not veiculo:
        flash("Selecione um veículo cadastrado.", "erro")
        return redirect(url_for("listar_ordens"))

    sucesso = executar(
        """
        INSERT INTO ordens_servico
            (veiculo_id, descricao, valor)
        VALUES (%s, %s, %s)
        """,
        (veiculo_id, descricao, valor)
    )

    if sucesso:
        flash("Ordem de serviço cadastrada com sucesso!", "sucesso")
    else:
        flash("Não foi possível cadastrar a ordem de serviço.", "erro")

    return redirect(url_for("listar_ordens"))


@app.route(
    "/ordens-servico/atualizar-status/<int:id>",
    methods=["POST"]
)
def atualizar_status_ordem(id):
    status = request.form.get("status", "").strip()

    status_permitidos = {
        "Pendente",
        "Em andamento",
        "Concluída"
    }

    if status not in status_permitidos:
        flash("Status inválido.", "erro")
        return redirect(url_for("listar_ordens"))

    ordem = buscar_um(
        "SELECT id FROM ordens_servico WHERE id = %s",
        (id,)
    )

    if not ordem:
        flash("Ordem de serviço não encontrada.", "erro")
        return redirect(url_for("listar_ordens"))

    sucesso = executar(
        """
        UPDATE ordens_servico
        SET status = %s
        WHERE id = %s
        """,
        (status, id)
    )

    if sucesso:
        flash("Status da ordem atualizado com sucesso!", "sucesso")
    else:
        flash("Não foi possível atualizar o status.", "erro")

    return redirect(url_for("listar_ordens"))


@app.route("/ordens-servico/excluir/<int:id>", methods=["POST"])
def excluir_ordem(id):
    ordem = buscar_um(
        "SELECT id, status FROM ordens_servico WHERE id = %s",
        (id,)
    )

    if not ordem:
        flash("Ordem de serviço não encontrada.", "erro")
        return redirect(url_for("listar_ordens"))

    if ordem["status"] != "Concluída":
        flash(
            "Somente ordens de serviço concluídas podem ser excluídas.",
            "erro"
        )
        return redirect(url_for("listar_ordens"))

    sucesso = executar(
        "DELETE FROM ordens_servico WHERE id = %s",
        (id,)
    )

    if sucesso:
        flash("Ordem de serviço excluída com sucesso!", "sucesso")
    else:
        flash("Não foi possível excluir a ordem de serviço.", "erro")

    return redirect(url_for("listar_ordens"))


# =========================================================
# INICIALIZAÇÃO
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
