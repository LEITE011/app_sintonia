from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, func, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base



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


