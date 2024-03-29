from dataclasses import dataclass
from typing import List
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    uri: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    host = env('DB_HOST')
    password = env.str('DB_PASS')
    user = env.str('DB_USER')
    database = env.str('DB_NAME')

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS')))
        ),
        db=DbConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            uri=f"postgresql://{user}:{password}@{host}/{database}"
        ),
        misc=Miscellaneous()
    )
