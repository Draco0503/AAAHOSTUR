from datetime import datetime as dt, timedelta

from flask import Flask, request, session, json, render_template, Response, redirect, url_for
from models import db
from models import Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language, \
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review
from config import config
from aaahostur.security import security

app = Flask(__name__, template_folder='templates')
conf = config['development']
sec = security.Security(conf.SECRET_KEY, conf.ALGORITHM)


def check_auth() -> bool:
    return 'auth' not in request.headers or request.headers['auth'] is None


def get_privileges_from_token(token: str) -> Role.Role or None:
    payload = sec.decode_jwt(token)
    if payload is None or len(payload) != 4:
        return None
    else:
        return Role.Role.query.filter_by(ID_ROLE=int(payload.get('user-role')))


# metodo de prueba de conexion
@app.route('/prueba')
def index():
    return render_template('t-login.html', prueba='holka')


# -------------------------------Language-------------------------------#

@app.route('/api_v0/language-list', methods=['GET'])
def language_list():
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [language.to_json() for language in Language.Language.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"languages": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/language/<id>', methods=['GET'])
def language_by_id(id: int):
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [language.to_json() for language in Language.Language.query.filter_by(ID_LANGUAGE=id)]
    if len(list) == 0:
        return not_found()
    msg = {"languages": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/language/<name>', methods=['GET'])
def language_by_name(name):
    # comprobacion de roles
    # no roles inadequate_Permits
    list = [language.to_json() for language in Language.Language.query.filter_by(Name=name)]
    if len(list) == 0:
        return not_found()
    msg = {"languages": list}
    return Response(json.dumps(
        msg,
    ), status=200)


# -------------------------------Job_Category-------------------------------#
@app.route('/api_v0/job_category-list', methods=['GET'])
def job_category_list():
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [job_Category.to_json() for job_Category in Job_Category.Job_Category.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"job_Category": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/job_category/<id>', methods=['GET'])
def job_category_by_id(id: int):
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [job_Category.to_json() for job_Category in Job_Category.Job_Category.query.filter_by(ID_JOB_CATEGORY=id)]
    if len(list) == 0:
        return not_found()
    msg = {"job_Category": list}
    return Response(json.dumps(
        msg,
    ), status=200)


# -------------------------------Qualification-------------------------------#

@app.route('/api_v0/qualification-list', methods=['GET'])
def qualification_list():
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [qualification.to_json() for qualification in Qualification.Qualification.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"qualification": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/qualification/<id>', methods=['GET'])
def job_qualification_by_id(id: int):
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [qualification.to_json() for qualification in
            Qualification.Qualification.query.filter_by(ID_QUALIFICATION=id)]
    if len(list) == 0:
        return not_found()
    msg = {"qualification": list}
    return Response(json.dumps(
        msg,
    ), status=200)


# -------------------------------User-------------------------------#

@app.route('/api_v0/user-list', methods=['GET'])
def user_list():
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [user.to_json() for user in User.User.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"user": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/user/<id>', methods=['GET'])
def user_by_id(id: int):
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [user.to_json() for user in User.User.query.filter_by(ID_USER=id)]
    if len(list) == 0:
        return not_found()
    msg = {"user": list}
    return Response(json.dumps(
        msg,
    ), status=200)


# -------------------------------Section-------------------------------#


# section-list
# section/<category>
# section/<category>/<name>
# section (ADD) (SE NECESITAN PERMISOS)
@app.route('/api_v0/section-list', methods=['GET'])
def section_list():
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [section.to_json() for section in Section.Section.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"section": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/section/<category>', methods=['GET'])
def section_by_category(category):
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [section.to_json() for section in Section.Section.query.filter_by(Category=category)]
    if len(list) == 0:
        return not_found()
    msg = {"company": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/section', methods=['POST'])
def section_add(section):
    try:
        # comprobar permisos
        Section.Section.query.add(section)
        Section.Section.query.commit()
        msg = {"new offer": section.to_json()}
    except:
        Offer.Offer.query.rollback()
        msg = {"fuck new offer": section.to_json()}

    return Response(json.dumps(msg), status=200)


# -------------------------------Company-------------------------------#

@app.route('/api_v0/company-list', methods=['GET'])
def company_list():
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [company.to_json() for company in Company.Company.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"company": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/company/<id>', methods=['GET'])
def company_by_id(id: int):
    # comprobacion de roles

    # no roles inadequate_Permits

    # si tiene permisos
    list = [company.to_json() for company in Company.Company.query.filter_by(ID_COMPANY=id)]
    if len(list) == 0:
        return not_found()
    msg = {"company": list}
    return Response(json.dumps(
        msg,
    ), status=200)


# TODO
# -------------------------------ACADEMIC PROFILE-------------------------------#
@app.route('/api_v0/academic_profile', methods=['POST'])
def academic_profile_add():
    data = request.form
    if data is None or (5 > len(data) > 8):
        return bad_request("offer_add() - data len()")
    if data['company_name'] is None:
        return "[ERROR] - offer_add() - insert: company_name"
    if data['address'] is None:
        return "[ERROR] - offer_add() - insert: address"
    if data['contact_name'] is None:
        return "[ERROR] - offer_add() - insert: contact_name"
    if data['contact_phone'] is None:
        return "[ERROR] - offer_add() - insert: contact_phone"
    if data['contact_email'] is None:
        return "[ERROR] - offer_add() - insert: contact_email"

    contact_name2 = "" if data['contact_name_2'] is None else data["contact_name_2"]
    contact_phone2 = "" if data['contact_phone_2'] is None else data["contact_phone_2"]
    contact_email2 = "" if data['contact_email_2'] is None else data["contact_email_2"]
    offer = Offer.Offer(Company_Name=data['company_name'], Address=data['address'], Contact_Name=data['contact_name'],
                        Contact_Phone=data['contact_phone'], Contact_Email=data['contact_email'],
                        Contact_Name_2=contact_name2, Contact_Phone_2=contact_phone2, Contact_Email_2=contact_email2)
    try:
        # comprobar permisos
        Offer.Offer.query.add(offer)
        Offer.Offer.query.commit()
        msg = {"new offer": offer.to_json()}
        status_code = 200
    except:
        try:
            Offer.Offer.query.rollback()
        except:
            pass
        msg = {"fuck new offer": offer.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------COMPANY ACCOUNT-------------------------------#


# -------------------------------COMPANY-------------------------------#


# -------------------------------JOB CATEGORY-------------------------------#
@app.route('/api_v0/job_category', methods=['POST'])
def job_category_add():
    data = request.form
    if data is None or (2 > len(data) > 2):
        return "[ERROR] - job_category_add() - data len()"
    if data['name'] is None:
        return "[ERROR] - job_category_add() - insert: name"
    if data['description'] is None:
        return "[ERROR] - job_category_add() - insert: description"

    job_category = Job_Category.Job_Category(Name=data['name'], Description=data['description'])
    try:
        # comprobar permisos
        Job_Category.Job_Category.query.add(job_category)
        Job_Category.Job_Category.query.commit()
        msg = {"new job_category": job_category.to_json()}
        status_code = 200
    except:
        try:
            Job_Category.Job_Category.query.rollback()
        except:
            pass
        msg = {"fuck new job_category": job_category.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------JOB_DEMAND_CATEGORY-------------------------------#
@app.route('/api_v0/job_demand_category-list', methods=['GET'])
def job_demand_category_list():
    # comprobar permisos
    list = [job_demand_category.to_json() for job_demand_category in
            Job_Demand_Category.Job_Demand_Category.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"job_demand_categories": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_category/<id>', methods=['GET'])
def job_demand_category_by_id(id: int):
    # comprobar permisos
    list = [job_demand_category.to_json() for job_demand_category in
            Job_Demand_Category.Job_Demand_Category.query.filter_by(Id_Job_Demand=id)]
    if len(list) == 0:
        return not_found()
    msg = {"job_demand_categories": list}  # there can be job_demand_categories with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND_LANGUAGE-------------------------------#
@app.route('/api_v0/job_demand_language-list', methods=['GET'])
def job_demand_language_list():
    # comprobar permisos
    list = [job_demand_language.to_json() for job_demand_language in
            Job_Demand_Language.Job_Demand_Language.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"job_demand_languages": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_language/<id>', methods=['GET'])
def job_demand_language_by_id(id: int):
    # comprobar permisos
    list = [job_demand_language.to_json() for job_demand_language in
            Job_Demand_Language.Job_Demand_Language.query.filter_by(Id_Job_Demand=id)]
    if len(list) == 0:
        return not_found()
    msg = {"job_demand_languages": list}  # there can be job_demand_languages with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND_QUALIFICATION-------------------------------#
@app.route('/api_v0/job_demand_qualification-list', methods=['GET'])
def job_demand_qualification_list():
    # comprobar permisos
    list = [job_demand_qualification.to_json() for job_demand_qualification in
            Job_Demand_Qualification.Job_Demand_Qualification.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"job_demand_qualifications": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_qualification/<id>', methods=['GET'])
def job_demand_qualification_by_id(id: int):
    # comprobar permisos
    list = [job_demand_qualification.to_json() for job_demand_qualification in
            Job_Demand_Qualification.Job_Demand_Qualification.query.filter_by(Id_Job_Demand=id)]
    if len(list) == 0:
        return not_found()
    msg = {"job_demand_qualifications": list}  # there can be job_demand_qualifications with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND-------------------------------#
@app.route('/api_v0/job_demand-list', methods=['GET'])
def job_demand_list():
    # comprobar permisos
    list = [job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"job_demands": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand/<id>', methods=['GET'])
def job_demand_by_id(id: int):
    # comprobar permisos
    list = [job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.filter_by(Id_Offer=id)]
    if len(list) == 0:
        return not_found()
    msg = {"job_demands": list}  # there can be job_demands with the same id_offer
    return Response(json.dumps(msg), status=200)


# -------------------------------LANGUAGE-------------------------------#
@app.route('/api_v0/language', methods=['POST'])
def language_add():
    data = request.form
    if data is None or (5 > len(data) > 8):
        return "[ERROR] - offer_add() - data len()"
    if data['company_name'] is None:
        return "[ERROR] - offer_add() - insert: company_name"
    if data['address'] is None:
        return "[ERROR] - offer_add() - insert: address"
    if data['contact_name'] is None:
        return "[ERROR] - offer_add() - insert: contact_name"
    if data['contact_phone'] is None:
        return "[ERROR] - offer_add() - insert: contact_phone"
    if data['contact_email'] is None:
        return "[ERROR] - offer_add() - insert: contact_email"

    contact_name2 = "" if data['contact_name_2'] is None else data["contact_name_2"]
    contact_phone2 = "" if data['contact_phone_2'] is None else data["contact_phone_2"]
    contact_email2 = "" if data['contact_email_2'] is None else data["contact_email_2"]
    offer = Offer.Offer(Company_Name=data['company_name'], Address=data['address'], Contact_Name=data['contact_name'],
                        Contact_Phone=data['contact_phone'], Contact_Email=data['contact_email'],
                        Contact_Name_2=contact_name2, Contact_Phone_2=contact_phone2, Contact_Email_2=contact_email2)
    try:
        # comprobar permisos
        Offer.Offer.query.add(offer)
        Offer.Offer.query.commit()
        msg = {"new offer": offer.to_json()}
        status_code = 200
    except:
        try:
            Offer.Offer.query.rollback()
        except:
            pass
        msg = {"fuck new offer": offer.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------MEMBER_ACCOUNT-------------------------------#


# -------------------------------MEMBER_LANGUAGE-------------------------------#


# -------------------------------MEMBER_OFFER-------------------------------#
@app.route('/api_v0/member_offer-list', methods=['GET'])
def member_offer_list():
    # comprobar permisos
    list = [member_offer.to_json() for member_offer in Member_Offer.Member_Offer.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"member_offers": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/member_offer/<id>', methods=['GET'])
def member_offer_by_id(id: int):
    # comprobar permisos
    list = [member_offer.to_json() for member_offer in Member_Offer.Member_Offer.query.filter_by(Id_Member=id)]
    if len(list) == 0:
        return not_found()
    msg = {"member_offers": list}  # there can be member_offers with the same id_member
    return Response(json.dumps(msg), status=200)


# -------------------------------MEMBER-------------------------------#


# -------------------------------OFFER-------------------------------#
@app.route('/api_v0/offer-list', methods=['GET'])
def offer_list():
    # comprobar permisos
    list = [offer.to_json() for offer in Offer.Offer.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"offers": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/offer/<id>', methods=['GET'])
def offer_by_id(id: int):
    # comprobar permisos
    list = [offer.to_json() for offer in Offer.Offer.query.filter_by(ID_OFFER=id)]
    if len(list) == 0:
        return not_found()
    elif len(list) > 1:
        return internal_server_error()  # there can't be offers with the same id
    msg = {"offers": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/offer', methods=['POST'])
def offer_add():
    data = request.form
    if data is None or (5 > len(data) > 8):
        return "[ERROR] - offer_add() - data len()"
    if data['company_name'] is None:
        return "[ERROR] - offer_add() - insert: company_name"
    if data['address'] is None:
        return "[ERROR] - offer_add() - insert: address"
    if data['contact_name'] is None:
        return "[ERROR] - offer_add() - insert: contact_name"
    if data['contact_phone'] is None:
        return "[ERROR] - offer_add() - insert: contact_phone"
    if data['contact_email'] is None:
        return "[ERROR] - offer_add() - insert: contact_email"

    contact_name2 = "" if data['contact_name_2'] is None else data["contact_name_2"]
    contact_phone2 = "" if data['contact_phone_2'] is None else data["contact_phone_2"]
    contact_email2 = "" if data['contact_email_2'] is None else data["contact_email_2"]
    offer = Offer.Offer(Company_Name=data['company_name'], Address=data['address'], Contact_Name=data['contact_name'],
                        Contact_Phone=data['contact_phone'], Contact_Email=data['contact_email'],
                        Contact_Name_2=contact_name2, Contact_Phone_2=contact_phone2, Contact_Email_2=contact_email2)
    try:
        # comprobar permisos
        Offer.Offer.query.add(offer)
        Offer.Offer.query.commit()
        msg = {"new offer": offer.to_json()}
        status_code = 200
    except:
        try:
            Offer.Offer.query.rollback()
        except:
            pass
        msg = {"fuck new offer": offer.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------PROFESSIONAL_PROFILE-------------------------------#


# -------------------------------QUALIFICATION-------------------------------#
@app.route('/api_v0/qualification', methods=['POST'])
def qualification_add():
    data = request.form
    if data is None or (5 > len(data) > 8):
        return "[ERROR] - offer_add() - data len()"
    if data['company_name'] is None:
        return "[ERROR] - offer_add() - insert: company_name"
    if data['address'] is None:
        return "[ERROR] - offer_add() - insert: address"
    if data['contact_name'] is None:
        return "[ERROR] - offer_add() - insert: contact_name"
    if data['contact_phone'] is None:
        return "[ERROR] - offer_add() - insert: contact_phone"
    if data['contact_email'] is None:
        return "[ERROR] - offer_add() - insert: contact_email"

    contact_name2 = "" if data['contact_name_2'] is None else data["contact_name_2"]
    contact_phone2 = "" if data['contact_phone_2'] is None else data["contact_phone_2"]
    contact_email2 = "" if data['contact_email_2'] is None else data["contact_email_2"]
    offer = Offer.Offer(Company_Name=data['company_name'], Address=data['address'], Contact_Name=data['contact_name'],
                        Contact_Phone=data['contact_phone'], Contact_Email=data['contact_email'],
                        Contact_Name_2=contact_name2, Contact_Phone_2=contact_phone2, Contact_Email_2=contact_email2)
    try:
        # comprobar permisos
        Offer.Offer.query.add(offer)
        Offer.Offer.query.commit()
        msg = {"new offer": offer.to_json()}
        status_code = 200
    except:
        try:
            Offer.Offer.query.rollback()
        except:
            pass
        msg = {"fuck new offer": offer.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------REVIEW-------------------------------#


# -------------------------------ROLE-------------------------------#
@app.route('/api_v0/role-list', methods=['GET'])
def role_list():
    # 1º conseguir header de la peticion
    # 2º si tiene permisos hacer la logica tal cual esta definida
    #    si no tiene permisos return inadequate_Permits()
    list = [role.to_json() for role in Role.Role.query.all()]
    if len(list) == 0:
        return not_found()
    msg = {"roles": list}
    return Response(json.dumps(
        msg,
    ), status=200)



# LOGIN
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not check_auth():  # and security.validate(request.headers['auth']):
            return redirect('/', code=200)  # todo
        return render_template('t-login.html')
    elif request.method == 'POST':
        if len(request.form) != 2:
            return bad_request()
        else:
            if request.form['user-login'] is not None:
                username = request.form['user-login']
                if username == "":
                    return bad_request()  # Usuario vacio
                else:
                    if request.form['user-passwd'] is not None:
                        passwd = request.form['user-passwd']
                        if passwd == "":
                            return bad_request()
                        else:
                            user = User.User.query.filter_by(Email=username)
                            if user is not None:
                                if sec.verify_password(passwd, user.Passwd):
                                    token_info = sec.generate_jwt({
                                        "user": user.Email,
                                        "user-role": user.Id_Role,
                                        "curr": dt.now(),
                                        "exp": dt.now() + timedelta(minutes=30)
                                    })
                                    # TODO pasar el token generado a todas las cabeceras de petición y redirect a index
                                    auth_header = {'auth': sec.generate_jwt(token_info)}
                                    redirect()
                                else:
                                    return "Contraseña incorrecta"
                            else:
                                return "Email incorrecto"

            else:
                return bad_request()

    else:
        return {}   # empty response


@app.route('/api_v0/role/<id>', methods=['GET'])
def role_by_id(id: int):
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None or not role.CanSeeApiRole:
        return forbidden()
    list = [role.to_json() for role in Role.Role.query.filter_by(ID_ROLE=id)]
    if len(list) == 0:
        return not_found()
    msg = {"roles": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/role/<name>', methods=['GET'])
def role_by_name(name):
    #comprobacion de roles
    #no roles inadequate_Permits
    list = [role.to_json() for role in Role.Role.query.filter_by(Name=name)]
    if len(list) == 0:
        return not_Found()
    msg = {"roles": list}
    return Response(json.dumps(
        msg,
    ), status=200)

#-------------------------------Language-------------------------------#

@app.route('/api_v0/language-list', methods=['GET'])
def language_list():
    #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [language.to_json() for language in Language.Language.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"languages": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/language/<id>', methods=['GET'])
def language_by_id(id: int):
     #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [language.to_json() for language in Language.Language.query.filter_by(ID_LANGUAGE=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"languages": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/language/<name>', methods=['GET'])
def language_by_name(name):
    #comprobacion de roles
    #no roles inadequate_Permits
    list = [language.to_json() for language in Language.Language.query.filter_by(Name=name)]
    if len(list) == 0:
        return not_Found()
    msg = {"languages": list}
    return Response(json.dumps(
        msg,
    ), status=200)

#-------------------------------Job_Category-------------------------------#
@app.route('/api_v0/job_category-list', methods=['GET'])
def job_category_list():
    #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [job_Category.to_json() for job_Category in Job_Category.Job_Category.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"job_Category": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/job_category/<id>', methods=['GET'])
def job_category_by_id(id: int):
     #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [job_Category.to_json() for job_Category in Job_Category.Job_Category.query.filter_by(ID_JOB_CATEGORY=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"job_Category": list}
    return Response(json.dumps(
        msg,
    ), status=200)

#-------------------------------Qualification-------------------------------#

@app.route('/api_v0/qualification-list', methods=['GET'])
def qualification_list():
    #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [qualification.to_json() for qualification in Qualification.Qualification.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"qualification": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/qualification/<id>', methods=['GET'])
def job_qualification_by_id(id: int):
     #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [qualification.to_json() for qualification in Qualification.Qualification.query.filter_by(ID_QUALIFICATION=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"qualification": list}
    return Response(json.dumps(
        msg,
    ), status=200)


#-------------------------------User-------------------------------#

@app.route('/api_v0/user-list', methods=['GET'])
def user_list():
    #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [user.to_json() for user in User.User.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"user": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/user/<id>', methods=['GET'])
def user_by_id(id: int):
     #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [user.to_json() for user in User.User.query.filter_by(ID_USER=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"user": list}
    return Response(json.dumps(
        msg,
    ), status=200)



#-------------------------------Section-------------------------------#


# section-list
# section/<category>
# section (ADD) (SE NECESITAN PERMISOS)
@app.route('/api_v0/section-list', methods=['GET'])
def section_list():
    #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [section.to_json() for section in Section.Section.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"section": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/section/<category>', methods=['GET'])
def section_by_category(category):
     #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [section.to_json() for section in Section.Section.query.filter_by(Category=category)]
    if len(list) == 0:
        return not_Found()
    msg = {"company": list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/section', methods=['POST'])
def offer_add():
    data = request.form
    if data is None or (6 > len(data) > 6):
        return "[ERROR] - section_add() - data len()"
    if data['category'] is None:
        return "[ERROR] - job_category_add() - insert: category"
    if data['description'] is None:
        return "[ERROR] - job_category_add() - insert: description"
    if data['publication_date'] is None:
        return "[ERROR] - job_category_add() - insert: publication_date"
    if data['schedule'] is None:
        return "[ERROR] - job_category_add() - insert: schedule"
    if data['img_resource'] is None:
        return "[ERROR] - job_category_add() - insert: img_resource"
    if data['price'] is None:
        return "[ERROR] - job_category_add() - insert: price"

    section = Section.Section(Category=data['category'], Description=data['description'], Publication_Date=data['publication_date'],
                               Schedule=data['schedule'], Img_Resource=data['img_resource'], Price=data['price'])

    try:
        # comprobar permisos
        Section.Section.query.add(section)
        Section.Section.query.commit()
        msg = {"new offer": section.to_json()}
        status_code = 200
    except:
        try:
            Offer.Offer.query.rollback()
        except:
            pass
        msg = {"fuck new offer": section.to_json()}
        status_code = 500
    return Response(json.dumps(msg), status=status_code)




def job_category_add():
    data = request.form
    if data is None or (2 > len(data) > 2):
        return "[ERROR] - job_category_add() - data len()"
    if data['name'] is None:
        return "[ERROR] - job_category_add() - insert: name"
    if data['description'] is None:
        return "[ERROR] - job_category_add() - insert: description"
    
    job_category = Job_Category.Job_Category(Name=data['name'], Description=data['description'])
    try:
        # comprobar permisos
        Job_Category.Job_Category.query.add(job_category)
        Job_Category.Job_Category.query.commit()
        msg = {"new job_category": job_category.to_json()}
        status_code = 200
    except:
        try:
            Job_Category.Job_Category.query.rollback()
        except:
            pass
        msg = {"fuck new job_category": job_category.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)




#-------------------------------Company-------------------------------#

@app.route('/api_v0/company-list', methods=['GET'])
def company_list():
    #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [company.to_json() for company in Company.Company.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"company": list}
    return Response(json.dumps(
        msg,
    ), status=200)

@app.route('/api_v0/company/<id>', methods=['GET'])
def company_by_id(id: int):
     #comprobacion de roles

    #no roles inadequate_Permits

    #si tiene permisos
    list = [company.to_json() for company in Company.Company.query.filter_by(ID_COMPANY=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"company": list}
    return Response(json.dumps(
        msg,
    ), status=200)




#-------------------------------MEMBER-------------------------------#


# -------------------------------SECTION-------------------------------#


# -------------------------------USER-------------------------------#


# FUNCIONES PARA LOS ERRORES MAS COMUNES


# Error 404-not found
def not_found():
    return Response(json.dumps({
        "title": "Not found",
        "message": "Item not found, check the parameters given"
    }), status=404)


# Error 403-forbidden
def forbidden():
    return Response(json.dumps({
        "title": "Forbidden",
        "message": "You are not allowed to access"
    }), status=403)


# Error 429-Too many request
def too_many_request():
    return Response(json.dumps({
        "title": "Too many request",
        "message": "You have "
    }), status=429)


# Error 500-Internal server error
def internal_server_error():
    return Response(json.dumps({
        "message": "An error has occurred, please try again"
    }), status=500)


# Error 504 Gateway Timeout
def gateway_timeout():
    return Response(json.dumps({
        "title": "Gateway Timeout",
        "message": "Request time out"
    }), status=504)


def bad_request(msg: str):
    return Response(json.dumps({
        "message": msg
    }), status=400)


# inicio del main
if __name__ == '__main__':
    # acceso al diccionario con las credenciales para acceder a la base de datos
    app.config.from_object(conf)
    # Conexion con la base de datos
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # para manegar los errores
    # app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(429, too_many_request)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(504, gateway_timeout)
    # run
    app.run(host='0.0.0.0', port=5000)
