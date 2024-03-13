import utilities
from sqlalchemy import Text, create_engine, select
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.orm import mapped_column, sessionmaker
from typing_extensions import Annotated

DATABASE_URL = "mysql+pymysql://root:bZrglcZvXEFAmqMtlmsaQMexpgnCWaET@monorail.proxy.rlwy.net:58091/railway"
# CA_CERT_PATH = "./cert.pem"
# ssl_args = {"ssl": {"ca": CA_CERT_PATH}}
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


u_bigint_pk = Annotated[
    int, mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[u_bigint_pk]
    email = mapped_column(Text)
    amplifyId = mapped_column(Text)


def use_ffmpeg():
    utilities.check_ffmpeg()
    utilities.check_ffmpeg_opt()


def get_users_from_db(session: SessionType):
    print("querying users")

    users = session.execute(select(User)).scalars().all()

    return users
