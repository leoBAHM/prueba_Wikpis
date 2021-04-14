from API.database import db, BaseModel


class Persons(BaseModel, db.Model):
    '''
        Class in charge of building the table "person" and storing data in it.
    '''
    # table attributes
    id = db.Column(db.Integer, primary_key=True)
    id_person = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __init__(self, id_person, name, last_name):
        '''
            Constructor of Persons class
        '''
        self.id_person = id_person
        self.name = name
        self.last_name = last_name


class Relationship(BaseModel, db.Model):
    '''
        Class in charge of building the table "relationships" and storing data in it.
    '''
    # table attributes
    id = db.Column(db.Integer, primary_key=True)
    relationship = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, relationship):
        '''
            Constructor of Relationships class
        '''
        self.relationship = relationship


class PersonsRelationship(BaseModel, db.Model):
    '''    
        Class that relates the data of the Persons and Relationships tables by means of foreign keys
    '''
    __tablename__ = "persons_relationships"

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)

    main_person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    secundary_person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    relationship_id = db.Column(db.Integer, db.ForeignKey('relationship.id'))

    main_person = db.relationship("Persons", foreign_keys=[main_person_id])
    secundary_person = db.relationship("Persons", foreign_keys=[secundary_person_id])
    relationship = db.relationship("Relationship", foreign_keys=[relationship_id])

    def __init__(self, main_person_id, secundary_person_id, relationship_id):
        '''
            Constructor of PersonsRelationship class
        '''
        self.main_person_id = main_person_id
        self.secundary_person_id = secundary_person_id
        self.relationship_id = relationship_id


class Studies(BaseModel, db.Model):
    '''
        Class in charge of building the table "studies" and storing data in it.
    '''

    # Table attributes
    id = db.Column(db.Integer, primary_key=True)
    study = db.Column(db.String(50), nullable=False)

    def __init__(self, study):
        '''
            Constructor of Studies class
        '''
        self.study = study


class PersonsStudies(BaseModel, db.Model):
    '''    
        Class that relates the data of the Persons and Studies tables by means of foreign keys
    '''
    __tablename__ = "persons_studies"

    #Table attributes
    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    study_id = db.Column(db.Integer, db.ForeignKey('studies.id'))

    person = db.relationship("Persons", foreign_keys=[person_id])
    study = db.relationship("Studies", foreign_keys=[study_id])

    def __init__(self, person_id, study_id):
        '''
            Constructor of PersonsStudies class
        '''
        self.person_id = person_id
        self.study_id = study_id



    
