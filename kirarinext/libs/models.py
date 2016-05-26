from redisorm.core import Model, Column


class Thread(Model):
    id = Column()
    name = Column()


class Comment(Model):
    id = Column()
    body = Column()
    thread = Column()
    author = Column()
    remote_addr = Column()
    created_at = Column()


class Anonymous(Model):
    id = Column()
    remote_addr = Column()
    avatar_url = Column()


class User(Model):
    id = Column()
    avatar_url = Column()
    username = Column()
    password = Column()
    screen_name = Column()


class Favorite(Model):
    id = Column()
    user_id = Column()
    comment_id = Column()


class Session(Model):
    id = Column()
    session_id = Column()
    data = Column()
