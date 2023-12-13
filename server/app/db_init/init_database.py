from app.database import engine

from app.api.cominfo.model import ComInfo, ComInfoRT
from app.api.commanage.model import ComManage
from app.api.user.model import User


def create_table():
    ComInfo.metadata.create_all(bind=engine)
    ComInfoRT.metadata.create_all(bind=engine)
    ComManage.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("DB Init")

    create_table()
