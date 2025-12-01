import datetime

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models import Artista, Musica, local_secao

app = Flask(__name__)
app.secret_key = "shhhh"


@app.route("/")
def index():
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

@app.route("/artista", methods=["GET", "POST"])
def artista_detalhe():
    artistas_sql = select(Artista)
    return render_template('artista_detalhe.html', artista=artistas_sql)


if __name__ == "__main__":
    app.run(debug=True, port=5001)