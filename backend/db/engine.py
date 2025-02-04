from sqlmodel import create_engine, SQLModel, Session

DB_URL = "postgresql+psycopg2://postgres:example@localhost:5432/postgres"  # TODO change to env var

engine = create_engine(DB_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
