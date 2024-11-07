"""Beverage data models"""

# Walter Podewil
# CIS 226
# November 6, 2024

# System Imports.
import os


# Third Party Imports
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Float, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


# NOTE: added
Base = declarative_base()
engine = create_engine("sqlite:///db.sqlite3", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Database:
    """database class"""

    def create_database(self) -> None:
        """method to create database"""
        Base.metadata.create_all(engine)

    def populate_database(self, data_to_add) -> None:
        """populate database from list of beverages"""
        session.add(data_to_add)
        session.commit()


class Beverage(Base):
    """Beverage class"""

    # NOTE: added
    __tablename__ = "beverages"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    pack = Column(String(255), nullable=False)
    price = Column(Float(4), nullable=False)
    active = Column(Boolean(5), nullable=False)

    def __init__(self, id_, name, pack, price, active):
        """Constructor"""
        self.id = id_
        self.name = name
        self.pack = pack
        self.price = price
        self.active = active

    def __str__(self):
        """String method"""
        active = "True" if self.active else "False"
        return f"| {self.id:>6} | {self.name:<56} | {self.pack:<15} | {self.price:>6.2f} | {active:<6} |"


# NOTE: renamed
class BeverageRepository(Database):
    """BeverageRepository class"""

    def __init__(self):
        """Constructor"""
        self.__beverages = []

    def __str__(self):
        """String method"""
        return_string = ""
        beverages = self._query_database_for_all_beverages()
        for beverage in beverages:
            return_string += f"{beverage}{os.linesep}"
        return return_string

    def add(self, id_, name, pack, price, active):
        """Add a new beverage to the collection"""
        self.__beverages.append(Beverage(id_, name, pack, price, active))

    def find_by_id(self, id_):
        """Find a beverage by it's id"""
        beverage = session.query(Beverage).get(id_)
        return beverage

    def create_beverage(self, id_, name, pack, price, active) -> Beverage:
        """create beverage from parameters"""
        return Beverage(id_, name, pack, price, active)

    def _query_database_for_all_beverages(self) -> object:
        """method to get iterable of all beverages in database"""
        result = session.query(Beverage).all()
        return result
