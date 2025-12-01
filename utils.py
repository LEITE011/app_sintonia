from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models import local_secao, Artista, Musica

def criar_musica():
    db_session = local_secao()
    try:
        titulo_musica = input("Digite o título da música: ")
        artista_nome = input("Digite o artista da música: ")
        genero_musica = input("Digite o gênero da música: ")
        duracao_musica = input("Digite a duração da música (MM:SS): ")
        data_de_lancamento_str = input("Digite a data de lançamento (AAAA-MM-DD): ")

        # Converter string para date
        try:
            data_de_lancamento = datetime.strptime(data_de_lancamento_str, '%Y-%m-%d').date()
        except ValueError:
            print("Formato de data inválido. Use AAAA-MM-DD.")
            return

        # Verificar se o artista existe
        artista_obj = db_session.query(Artista).filter_by(nome=artista_nome).first()
        if not artista_obj:
            print("Artista não encontrado. Cadastre o artista primeiro.")
            return

        # Criar música
        nova_musica = Musica(
            titulo=titulo_musica,
            artista=artista_obj.nome,
            genero=genero_musica,
            duracao=duracao_musica,
            data_de_lancamento=data_de_lancamento
        )

        db_session.add(nova_musica)
        db_session.commit()
        print("Música cadastrada com sucesso!")

    except SQLAlchemyError as e:
        print(f"Erro ao cadastrar música: {e}")
        db_session.rollback()

    finally:
        db_session.close()


if __name__ == '__main__':
    criar_musica()