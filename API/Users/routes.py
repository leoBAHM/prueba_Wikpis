
from flask import jsonify, request, current_app

from . import user_bp
from .models import Persons, Relationship, PersonsRelationship, Studies, PersonsStudies
from .schema import PersonsSchema, StudiesSchema

person_schema = PersonsSchema()
study_schema = StudiesSchema()

@user_bp.route("/api/add", methods=["POST"])
def add_person():
    '''
        Obtains the data sent through a post request and stores it in the respective database 
        as appropriate.
    '''
    data = request.json
    try:
        user_info = get_information(data) # Get data
        if not Persons.simple_filter(id_person=user_info[0]): # Person not in persons table
            # Add the information within persons table
            main_user = Persons(user_info[0], user_info[1], user_info[2])
            main_user.save()
            save_studies(main_user.id, user_info[3]) # Save studies
            family_data = data.get("family_data", None) # About your family
            if family_data: # If contains data
                # obtain one by one the data
                for family in family_data: 
                    user_info = get_information(family) # Get information
                    user = Persons.simple_filter(id_person=user_info[0])
                    # Person not in persons table
                    if not user:
                        user = Persons(user_info[0], user_info[1], user_info[2])
                        user.save()
                        save_studies(user.id, user_info[3])
                    else: user = user[0]
                    # Search the relationship in relationship table
                    relationship = Relationship.simple_filter(relationship=user_info[4])
                    #if relationship not found 
                    if not relationship:
                        # Add the new relationship within relationship table 
                        relationship = Relationship(user_info[4])
                        relationship.save()
                    else: relationship = relationship[0]
                    # create the relationship between the user and the family member
                    person_relationship = PersonsRelationship(main_user.id, user.id, relationship.id)
                    person_relationship.save()
            return jsonify({'msg': 'Information added', 'status': 200}), 200
        else: 
            return jsonify({'msg': 'Document is already registered', 'status': 200}), 200
    except:
        return jsonify({'msg': 'Error', 'status': 500}), 500


def get_information(data):
    '''
        Get the fields inside json structure
    '''
    id_person = data.get("id", None)
    name = data.get("name", None).title()
    last_name = data.get("last_name", None).title()
    studies = data.get("studies", None)
    if data.get("relationship", None):
        return id_person, name, last_name, studies, data.get("relationship", None).title()
    return id_person, name, last_name, studies


def save_studies(user_id, studies):
    '''
        Take a list of studies and add them inside the stuidies table if they are not found and create 
        the relationship between Persons and Studies.
    '''
    for s in studies:
        # Search studies within studies table
        study = Studies.simple_filter(study=s.title())
        if not study:
            # Add new studies
            study = Studies(s.title())
            study.save()
        else: study = study[0]
        # Create relationship between Person and Studies
        person_studies = PersonsStudies(user_id, study.id)
        person_studies.save()


@user_bp.route("/api/users")
@user_bp.route("/api/users/<id>")
def get_users(id=None):
    '''       
        Shows all the persons stored in the persons table if "id" is not sent as a parameter or the 
        respective information to the person, if the entered document is associated with a subject 
        within the persons table
    '''
    if id: #If id is send as parameter
        # Search the document within persons tabñe
        main_user = Persons.simple_filter(id_person=id)
        if main_user: 
            data = get_all_relationship(main_user[0]) #get all information associated
            return jsonify({"data": data})
        else:
            return jsonify({'msg': 'Document not found', 'status': 404}), 404
    else:
        users = Persons.get_all()
        data = person_schema.dump(users, many=True)
        return jsonify({"data": data})


def get_all_relationship(main_user):
    '''
        Get all the information associated with a subject from the relationships with other 
        stored tables.
    '''
    # Get relationship with other persons
    relationship = PersonsRelationship.simple_filter(main_person_id=main_user.id)
    family_data = [] # To stored family data
    for i in relationship:
        # get personal data of family
        data = person_schema.dump(i.secundary_person)
        study = [] # to stores studies
        # Get studies of family
        studies = PersonsStudies.simple_filter(person_id=data['id'])
        for j in studies:
            # Search studies and append
            study.append(study_schema.dump(j.study)["study"])
        data["studies"] = study # new field in data of family
        data['id'] = data.get("id_person", None)
        data.pop('id_person', None)
        family_data.append(data) # add family data 
    study = [] # to stores studies
    # Get studies
    studies = PersonsStudies.simple_filter(person_id=main_user.id)
    for j in studies:
        study.append(study_schema.dump(j.study)["study"])
    main_user = person_schema.dump(main_user)
    main_user['id'] = main_user.get("id_person", None)
    main_user.pop('id_person', None)
    main_user["studies"] = study
    main_user["family_data"] = family_data
    return main_user
    
