"""Beverage data models"""



# System Imports.
import os

# First Party Imports
from errors import DatabaseNotCreatedError

# Third Party Imports
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Float, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
    active = Column(Boolean(), nullable=False)

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

    def __str__(self):
        """String method"""
        self.__check_if_database_exists()
        return_string = ""
        beverages = self._query_database_for_all_beverages()
        for beverage in beverages:
            return_string += f"{beverage}{os.linesep}"
        return return_string

    def add(self, beverage):
        """Add a new beverage to the collection"""
        self.__check_if_database_exists()
        session.add(beverage)
        session.commit()

    def find_by_id(self, id_):
        """Find a beverage by it's id"""
        self.__check_if_database_exists()
        beverage = session.query(Beverage).get(id_)
        return beverage

    def create_beverage(self, id_, name, pack, price, active) -> Beverage:
        """create beverage from parameters"""
        return Beverage(id_, name, pack, price, active)

    def update_name(self, beverage_to_update: Beverage, new_name: str) -> None:
        """method to update name"""
        self.__check_if_database_exists()
        beverage_to_update.name = new_name
        session.commit()

    def update_pack(self, beverage_to_update: Beverage, new_pack: str) -> None:
        """method to update pack"""
        self.__check_if_database_exists()
        beverage_to_update.pack = new_pack
        session.commit()

    def update_price(self, beverage_to_update: Beverage, new_price: str) -> None:
        """method to update pack"""
        self.__check_if_database_exists()
        beverage_to_update.price = new_price
        session.commit()

    def update_active(self, beverage_to_update: Beverage, new_active: str) -> None:
        """method to update active"""
        self.__check_if_database_exists()
        beverage_to_update.active = new_active
        session.commit()

    def _query_database_for_all_beverages(self) -> object:
        """method to get iterable of all beverages in database"""
        self.__check_if_database_exists()
        result = session.query(Beverage).all()
        return result

    def delete_beverage(self, beverage: Beverage) -> None:
        """method to delete beverage from database"""
        self.__check_if_database_exists()
        session.delete(beverage)
        session.commit()

    def delete_inactive_beverages(self) -> None:
        """method to delete inactive beverages from database"""
        self.__check_if_database_exists()
        inactive_beverages = self.query_for_all_inactive()
        for beverage in inactive_beverages:
            self.delete_beverage(beverage)

    def query_for_all_inactive(self) -> object:
        """method to query for inactive"""
        self.__check_if_database_exists()
        return session.query(Beverage).filter(Beverage.active == 0).all()

    def query_for_one_inactive(self) -> object:
        """look for at least one inactive beverage"""
        self.__check_if_database_exists()
        return session.query(Beverage).filter(Beverage.active == 0).first()

    def __check_if_database_exists(self):
        """method to check if database exists"""
        if not os.path.exists("./db.sqlite3"):
            raise DatabaseNotCreatedError
