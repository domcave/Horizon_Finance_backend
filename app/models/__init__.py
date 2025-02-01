from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .thread import Thread
from .code_migration import CodeMigration