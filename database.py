from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Word(Base):
    __tablename__ = "Words"

    banned_word = Column("banned_word", String, primary_key=True)

    def __init__(self, banned_word: str) -> None:
        self.banned_word = banned_word

    def __repr__(self) -> str:
        return f"{self.banned_word=}"


class Violations(Base):
    __tablename__ = "Violations"

    volation_id = Column("volation_id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", String)
    timestamp = Column("timestamp", Integer)
    word = Column("word", String)

    def __repr__(self) -> str:
        return (
            f"{self.volation_id=} & {self.user_id=} & {self.timestamp=} & {self.word=}"
        )


engine = create_engine("sqlite:///mydb.sqlite", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

db = Session()

# db.add(Word(banned_word="ANOTHER_WORD"))

# db.commit()
