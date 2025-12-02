from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, func, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import datetime


engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/sintonia_bd')

local_secao = sessionmaker(bind=engine)
Base = declarative_base()


class Artista(Base):
    __tablename__ = 'artista'

    id_artista = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    biografia = Column(String(250))
    foto = Column(String(250))
    musicas = relationship("Musica", back_populates="artista_rel")


class Musica(Base):
    __tablename__ = 'musica'

    id_musica = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(60), nullable=False)
    id_artista = Column(Integer, ForeignKey('artista.id_artista'), nullable=False)
    genero = Column(String(30), nullable=False)
    duracao = Column(String(10), nullable=False)
    data_de_lancamento = Column(Date, nullable=False)
    artista_rel = relationship("Artista", back_populates="musicas")


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    email = Column(String(120))
    senha = Column(String(100))
    data_nascimento = Column(Date)

    playlists = relationship("Playlist", back_populates="usuario")




class Playlist(Base):
    __tablename__ = "playlist"

    id_playlist = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    descricao = Column(String(250))
    data_criacao = Column(Date, nullable=False, default=datetime.date.today)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)


    usuario = relationship("Usuario", back_populates="playlists")




