from sqlalchemy.exc import SQLAlchemyError
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import select
from models import *

app = Flask(__name__)
app.secret_key = "shhhh"


@app.route("/")
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))
    db_session = local_secao()
    artistas_sql = select(Artista).order_by(Artista.nome)
    artistas = db_session.execute(artistas_sql).scalars().all()

    musicas_sql = select(Musica)
    musicas = db_session.execute(musicas_sql).scalars().all()

    print(artistas)
    print(musicas)
    return render_template("index.html", artistas=artistas, musicas=musicas)


@app.route("/cadastro_artista", methods=["GET", "POST"])
def cadastro_artista():
    if "usuario" not in session:
        return redirect(url_for("login"))
    db_session = local_secao()
    if request.method == "POST":
        nome = request.form["nome"]
        biografia = request.form["biografia"]
        foto = request.form["foto"]

        artista = Artista(
            nome=nome,
            biografia=biografia,
            foto=foto
        )

        db_session.add(artista)
        db_session.commit()

        return redirect(url_for("index"))

    return render_template("artistas.html")


@app.route("/cadastro_musica", methods=["GET", "POST"])
def cadastro_musica():
    if "usuario" not in session:
        return redirect(url_for("login"))
    db_session = local_secao()
    artistas_sql = select(Artista)
    artistas = db_session.execute(artistas_sql).scalars().all()

    if request.method == "POST":
        titulo = request.form["titulo"]
        id_artista = request.form["id_artista"]
        genero = request.form["genero"]
        duracao = request.form["duracao"]
        data = request.form["data_de_lancamento"]

        musica = Musica(
            titulo=titulo,
            id_artista= int(id_artista),
            genero=genero,
            duracao=duracao,
            data_de_lancamento= datetime.datetime.strptime(data, "%Y-%m-%d"),
        )

        db_session.add(musica)
        db_session.commit()

        return redirect(url_for("index"))

    return render_template("musicas.html", artistas=artistas)

@app.route("/artista/<id_artista>", methods=["GET", "POST"])
def artista_detalhe(id_artista):
    db_session = local_secao()
    artistas_sql = select(Artista)
    user = db_session.execute(select(Artista).where(Artista.id_artista == id_artista)).scalar_one_or_none()
    return render_template('artista_detalhe.html', artista=artistas_sql, user=user )


@app.route("/cadastro_usuario", methods=["GET", "POST"])
def cadastro_usuario():

    db_session = local_secao()
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        data_nascimento = request.form["data_nascimento"]

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,
            data_nascimento=datetime.datetime.strptime(data_nascimento, "%Y-%m-%d"),
        )

        db_session.add(usuario)
        db_session.commit()

        return redirect(url_for("login"))

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    db_session = local_secao()

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        consulta = select(Usuario).where(
            Usuario.email == email,
            Usuario.senha == senha
        )

        usuario = db_session.execute(consulta).scalar_one_or_none()

        if usuario:
            session["usuario"] = usuario.nome
            session["id_usuario"] = usuario.id_usuario
            return redirect(url_for("index"))
        else:
            return "Usuário ou senha incorretos!"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario")
    return redirect(url_for("index"))

@app.route("/criar_playlist", methods=["GET", "POST"])
def criar_playlist():
    if "usuario" not in session:
        return redirect(url_for("login"))

    db_session = local_secao()

    user = db_session.execute(select(Usuario).where(Usuario.id_usuario == session["id_usuario"])).scalars().one_or_none()

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        playlist = Playlist(
            nome=nome,
            descricao=descricao,
            data_criacao=datetime.date.today(),
            id_usuario=user.id_usuario
        )

        db_session.add(playlist)
        db_session.commit()

        return redirect(url_for("criar_playlist"))

    return render_template("criar_playlist.html")

@app.route("/playlists", methods=["GET", "POST"])
def exibir_playlists():
    if "usuario" not in session:
        return redirect(url_for("login"))
    db_session = local_secao()
    playlist_sql = select(Playlist)
    playlist = db_session.execute(playlist_sql).scalars().all()
    print('yth',playlist)
    # return render_template('playlists.html', playlist=playlist)


    sql_playlist = select(Playlist, Usuario).join(Usuario, Usuario.id_usuario == Playlist.id_usuario)
    playlist2 = db_session.execute(sql_playlist).all()
    print('weq',playlist2)
    return render_template( 'playlists.html',playlists=playlist2)

if __name__ == "__main__":
    app.run(debug=True, port=5001)