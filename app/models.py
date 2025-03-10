from .database import Base
from sqlalchemy.sql.expression import text 
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ = 'user_details'

    id = Column(Integer,primary_key = True, nullable = False)
    name = Column(String,nullable = False)
    email = Column(String,nullable = False,unique = True)
    password = Column(String,nullable = False)
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='True')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    user_id = Column(Integer,ForeignKey("user_details.id",ondelete="CASCADE"),nullable=False)

    owner = relationship('User')