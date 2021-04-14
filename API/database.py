from flask_sqlalchemy import SQLAlchemy

# Create database using SQLAlchemy ORM
db = SQLAlchemy()


class BaseModel:
    '''
        Common methods for managing data tables
    '''

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, ide):
        return cls.query.get(ide)

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()