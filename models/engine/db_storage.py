#!/usr/bin/python3
"""This is the file DBStorage class for AirBnB"""
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class seria
    lizes instances to a JSON file and
    deserializes JSON fi
    le to instances
    Attributes:
        __engine path to the JSON file
        __session: objects will be stored
    """
    __engine = None
    __session = None
    __classes = {'BaseModel': BaseModel,
                 'User': User,
                 'Place': Place,
                 'State': State,
                 'City': City,
                 'Amenity': Amenity,
                 'Review': Review}

    def __init__(self):
        """Instantiation of base model DBStorage"""
        ENV = os.getenv('HBNB_ENV')
        USER = os.getenv('HBNB_MYSQL_USER')
        PWD = os.getenv('HBNB_MYSQL_PWD')
        HOST = os.getenv('HBNB_MYSQL_HOST')
        DB = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HOST, DB),
                                      pool_pre_ping=True)
        if ENV == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Query of object depending of the class name
         if cls=none query of all type of objects """
        my_session = self.__session
        dic = {}
        if not cls:
            class_to_return = [State, City, User, Place, Review, Amenity]
        else:
            class_to_return = [DBStorage.__classes[cls]]
        
        for class_to_print in class_to_return:
            class_list = my_session.query(class_to_print).all()
            for item in class_list:
                key = "{}.{}".format(item.__class__.__name__, item.id)
                dic[key] = item
        return dic

    def new(self, obj):
        """Add new obj
        Args:
            obj: given object
        """
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Save to database
        """
        self.__session.commit()

    def reload(self):
        """Create the current database session
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(Session)
        self.__session = session()

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside"""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """Close method on the private session attribute on class Session"""
        self.__session.close()
