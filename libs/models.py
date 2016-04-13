from redisorm.core import PersistentData, Column


class Thread(PersistentData):
    id = Column()
    name = Column()


class Comment(PersistentData):
    id = Column()
    body = Column()
    thread = Column()
    author = Column()
    remote_addr = Column()


class Anonymous(PersistentData):
    id = Column()
    remote_addr = Column()
    avatar_url = Column()
