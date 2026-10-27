import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

db = SQLAlchemy()

class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""
    pass

class Category(db.Enum):
    """Enumeration of valid Product Categories"""
    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4

class Product(db.Model):
    """Class that represents a Product"""

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(
        db.Enum(Category), nullable=False, server_default=(Category.UNKNOWN.name)
    )

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Product to the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Product to the database"""
        logger.info("Updating %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Product from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data: dict):
        """Deserializes a Product from a dictionary"""
        try:
            self.name = data["name"]
            self.description = data.get("description")
            self.price = data["price"]
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + type(data["available"])
                )
            self.category = getattr(Category, data["category"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid product missing parameter: " + error.args[0])
        except TypeError as error:
            raise DataValidationError("Invalid product type: " + error.args[0])
        return self

    @classmethod
cat << 'EOF' > service/models.py
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

db = SQLAlchemy()

class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""
    pass

class Category(db.Enum):
    """Enumeration of valid Product Categories"""
    UNKNOWN = 0
    CLOTHS = 1
    FOOD = 2
    HOUSEWARES = 3
    AUTOMOTIVE = 4

class Product(db.Model):
    """Class that represents a Product"""

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(
        db.Enum(Category), nullable=False, server_default=(Category.UNKNOWN.name)
    )

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Creates a Product to the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Product to the database"""
        logger.info("Updating %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Product from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data: dict):
        """Deserializes a Product from a dictionary"""
        try:
            self.name = data["name"]
            self.description = data.get("description")
            self.price = data["price"]
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + type(data["available"])
                )
            self.category = getattr(Category, data["category"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid product missing parameter: " + error.args[0])
        except TypeError as error:
            raise DataValidationError("Invalid product type: " + error.args[0])
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database app"""
        logger.info("Initializing database")
        db.init_app(app)
        with app.app_context():
            db.create_all()

    @classmethod
    def all(cls):
        """Returns all of the Products in the database"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """Finds a Product by its ID"""
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Products with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """Returns all Products in a category"""
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """Returns all Products by availability"""
        logger.info("Processing availability query for %s ...", available)
        return cls.query.filter(cls.available == available)
