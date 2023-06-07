import uuid
from base64 import b64encode, b64decode
from datetime import datetime as dt, timedelta
from user_agents import parse
import requests
from flask import Flask, request, session, json, render_template, Response, redirect, url_for, make_response
from models import db
from models import Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language, \
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review, Shift, Working_Day, Schedule
from config import config
from security import security
import utils
from enum import IntEnum

# region CONSTANTS

ERROR_400_DEFAULT_MSG = "The server cannot or will not process the request."
ERROR_403_DEFAULT_MSG = "You are not allowed to access to this endpoint."
ERROR_404_DEFAULT_MSG = "The requested URL was not found on the server. " \
                        "If you entered the URL manually please check your spelling and try again."
ERROR_429_DEFAULT_MSG = "You have sent too many requests in a given amount of time."
ERROR_500_DEFAULT_MSG = "Something was wrong, please try it again later. " \
                        "If the problem persists please contact with the service provider."
ERROR_504_DEFAULT_MSG = "The server did not get a response in time."

# endregion
# ==================================================================================================================== #

# region app declaration and its first settings

app = Flask(__name__, template_folder='templates')
conf = config['development']
sec = security.Security(conf.SECRET_KEY, conf.ALGORITHM)


# endregion
# ==================================================================================================================== #

# region should be in utils

def not_auth_header() -> bool:
    """True if 'auth' header not found or empty"""
    return request.cookies.get('auth') is None


def get_user_from_token(token: str) -> tuple[str, Role.Role or str]:
    """Gets the role from the validated token"""
    try:
        # Getting the payload from the stored token
        payload = sec.decode_jwt(token)
        # Check for correct payload's length
        if payload is None or len(payload) != 4:
            return "", "Payload format not correct"
        # Check if token has not expired
        if dt.now() > dt.strptime(payload.get("exp_time"), "%y-%m-%d %H:%M:%S"):
            return "", "Token expired, please log in again"
        # Check if the user exists
        user = User.User.query.filter_by(Email=payload.get("user")).first()
        if user is None:
            return "", "User not found"
        # Check if the user's role and the role given are the same
        if user.Id_Role != int(payload.get("user-role")):
            return "", "This user have not this role..."
        return user.Email, Role.Role.query.filter_by(ID_ROLE=int(payload.get("user-role"))).first()
    except Exception as ex:
        return "", "The server could not process your token info"


def user_privileges() -> tuple[Role.Role or Response, str]:
    # Check if auth cookie exists
    if not_auth_header():
        return redirect(url_for(".login", _method='GET')), "Not header"
    # Then it gets user's email and role from the token stored
    user, role = get_user_from_token(request.cookies.get('auth'))
    # Its defined that when user is "" an error has occurred
    if user == "" or type(role) == str:
        resp = bad_request(role)
        resp.delete_cookie('auth')
        return resp, "Not found"
    return role, user


def key_in_request_form(key) -> bool:
    return key in request.form and request.form[key] is not None


def navigator_user_agent() -> bool:
    uas = request.user_agent.string
    user_agent = parse(uas)
    return user_agent.is_pc or user_agent.is_mobile or user_agent.is_tablet


def valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


# endregion
# ==================================================================================================================== #

# ============================================ COMMON ERROR RESPONSES ================================================ #
# region COMMON ERROR RESPONSES

# 400-Bad Request
def bad_request(msg: str = ERROR_400_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "message": "{}".format(msg)
    }), status=400)


# 403-forbidden
def forbidden(msg: str = ERROR_403_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Forbidden",
        "message": "{}".format(msg)
    }), status=403)


# 404-not found
def not_found(msg: str = ERROR_404_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Not found",
        "message": "{}".format(msg)
    }), status=404)


# 429-Too many request
def too_many_request(msg: str = ERROR_429_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Too many request",
        "message": "{}".format(msg)
    }), status=429)


# 500-Internal server error
def internal_server_error(msg: str = ERROR_500_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "message": "{}".format(msg)
    }), status=500)


# 504 Gateway Timeout
def gateway_timeout(msg: str = ERROR_504_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Gateway Timeout",
        "message": "{}".format(msg)
    }), status=504)


# endregion
# ==================================================================================================================== #

# region testing
# method for testing purposes
@app.route('/prueba')
def prueba():
    return render_template('addoffer.html', prueba='holka')


# endregion
# ==================================================================================================================== #
# =========================================================  API  ==================================================== #
# region API

# -------------------------------ACADEMIC_PROFILE-------------------------------#
# INSERT
@app.route('/api_v0/academic_profile', methods=['POST'])
def academic_profile_add():
    # PARA HACER ESTA LLAMADA HAY QUE ASEGURARSE DE QUE EXISTE EL MIEMBRO
    data = request.form
    # NOT NULL fields
    if data is None or len(data) < 2 or len(data) > 3:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data len()]')
    if not key_in_request_form('school'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <school>]')
    if not key_in_request_form('graduation_date'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <graduation_date>]')

    # NULL fields
    promotion = '' if not key_in_request_form('promotion') else data['promotion']

    academic_profile = Academic_Profile.Academic_Profile(School=data['school'],
                                                         Graduation_Date=data['graduation_date'],
                                                         Promotion=promotion)
    try:
        db.session.add(academic_profile)
        db.session.commit()
        msg = {'NEW academic_profile ADDED': academic_profile.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {ERROR_500_DEFAULT_MSG: academic_profile.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------COMPANY_ACCOUNT-------------------------------#
# TODO not implemented in v.0


# -------------------------------COMPANY-------------------------------#
# READ ALL
@app.route('/api_v0/company-list', methods=['GET'])
def company_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiCompany:
        return forbidden()
    data_list = [company.to_json() for company in Company.Company.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"company": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/company/<id>', methods=['GET'])
def company_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiCompany:
        return forbidden()
    data_list = [company.to_json() for company in Company.Company.query.filter_by(ID_COMPANY=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"company": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/company', methods=['POST'])
def company_add():
    data = request.form
    if data is None or (5 > len(data) > 10):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data len()]')
    if not key_in_request_form('id'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <id>]')
    if not key_in_request_form('company_name'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <company_name>]')
    if not key_in_request_form('type'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <type>')
    if not key_in_request_form('cif'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <cif>]')
    if not key_in_request_form('contact_name'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_name>]')
    if not key_in_request_form('contact_phone'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_phone>]')
    if not key_in_request_form('contact_email'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_email>]')

    address = "" if not key_in_request_form('address') else data['address']
    cp = "" if not key_in_request_form('cp') else data['cp']
    city = "" if not key_in_request_form('city') else data['city']
    province = "" if not key_in_request_form('province') else data['province']
    description = "" if not key_in_request_form('description') else data['description']
    company = Company.Company(ID_COMPANY=data['id'],
                              Name=data['company_name'],
                              Type=data['type'],
                              CIF=data['cif'],
                              Address=address,
                              CP=cp,
                              City=city,
                              Province=province,
                              Contact_Name=data['contact_name'],
                              Contact_Phone=data['contact_phone'],
                              Contact_Email=data['contact_email'],
                              Description=description)

    try:
        db.session.add(company)
        db.session.commit()
        msg = {'company_add': company.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {"company_add": ERROR_500_DEFAULT_MSG}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# UPDATE
@app.route("/api_v0/company/<id>", methods=["GET", "PUT"])
def company_verify_update(id):
    company = Company.Company.query.filter_by(ID_COMPANY=id).first()
    # Check if exists
    if company is None:
        return not_found()
    else:
        if request.method == "GET":
            msg = {"company": company.to_json()}
            return Response(json.dumps(msg), status=200)
        elif request.method == "PUT":
            data = request.form
            # Check that the value given is present
            if not key_in_request_form('verify') and not key_in_request_form('active'):
                return bad_request()
            else:
                status_code = 400
                msg = ERROR_400_DEFAULT_MSG
                try:
                    if key_in_request_form('verify'):
                        if data["verify"] == 'True':
                            company.Verify = True
                        elif data["verify"] == 'False':
                            company.Verify = False
                    if key_in_request_form('active'):
                        if data["active"] == 'True':
                            company.Active = True
                        elif data["active"] == 'False':
                            company.Active = False
                    db.session.commit()
                    msg = {"company": company.to_json()}
                    status_code = 200
                except Exception as ex:
                    print(ex)
                    db.session.rollback()
                if status_code != 200:
                    return internal_server_error("An error has occurred processing PUT query")
                return Response(json.dumps(msg), status=status_code)


# -------------------------------JOB_CATEGORY--------------------------------------#
# READ ALL
@app.route('/api_v0/job_category-list', methods=['GET'])
def job_category_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiJobCategory:
        return forbidden()
    data_list = [job_Category.to_json() for job_Category in Job_Category.Job_Category.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_Category": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/job_category/<id>', methods=['GET'])
def job_category_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiJobCategory:
        return forbidden()
    data_list = [job_Category.to_json() for job_Category in
                 Job_Category.Job_Category.query.filter_by(ID_JOB_CATEGORY=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_Category": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/job_category', methods=['POST'])
def job_category_add():
    data = request.form
    if data is None or (2 > len(data) > 2):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data len()]')
    if not key_in_request_form('name'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data <name>')
    if not key_in_request_form('description'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data <description>]')

    job_category = Job_Category.Job_Category(Name=data['name'],
                                             Description=data['description'])

    try:
        # TODO check role
        db.session.add(job_category)
        db.session.commit()
        msg = {'NEW job_category ADDED': job_category.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {ERROR_500_DEFAULT_MSG: job_category.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------JOB_DEMAND_CATEGORY-------------------------------#
# READ ALL
@app.route('/api_v0/job_demand_category-list', methods=['GET'])
def job_demand_category_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand_category.to_json() for job_demand_category in
                 Job_Demand_Category.Job_Demand_Category.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demand_categories": list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/job_demand_category/<id>', methods=['GET'])
def job_demand_category_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand_category.to_json() for job_demand_category in
                 Job_Demand_Category.Job_Demand_Category.query.filter_by(Id_Job_Demand=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demand_categories": data_list}  # there can be job_demand_categories with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND_LANGUAGE-------------------------------#
# READ ALL
@app.route('/api_v0/job_demand_language-list', methods=['GET'])
def job_demand_language_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand_language.to_json() for job_demand_language in
                 Job_Demand_Language.Job_Demand_Language.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demand_languages": data_list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/job_demand_language/<id>', methods=['GET'])
def job_demand_language_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand_language.to_json() for job_demand_language in
                 Job_Demand_Language.Job_Demand_Language.query.filter_by(Id_Job_Demand=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demand_languages": data_list}  # there can be job_demand_languages with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND_QUALIFICATION-------------------------------#
# READ ALL
@app.route('/api_v0/job_demand_qualification-list', methods=['GET'])
def job_demand_qualification_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand_qualification.to_json() for job_demand_qualification in
                 Job_Demand_Qualification.Job_Demand_Qualification.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demand_qualifications": data_list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/job_demand_qualification/<id>', methods=['GET'])
def job_demand_qualification_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand_qualification.to_json() for job_demand_qualification in
                 Job_Demand_Qualification.Job_Demand_Qualification.query.filter_by(Id_Job_Demand=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demand_qualifications": data_list}  # there can be job_demand_qualifications with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND-------------------------------#
# READ ALL
@app.route('/api_v0/job_demand-list', methods=['GET'])
def job_demand_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demands": data_list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/job_demand/<id>', methods=['GET'])
def job_demand_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.filter_by(Id_Offer=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demands": data_list}  # there can be job_demands with the same id_offer
    return Response(json.dumps(msg), status=200)


# -------------------------------LANGUAGE-------------------------------#
# READ ALL
@app.route('/api_v0/language-list', methods=['GET'])
def language_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiLanguage:
        return forbidden()
    data_list = [language.to_json() for language in Language.Language.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"languages": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/language/<id>', methods=['GET'])
def language_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiLanguage:
        return forbidden()
    data_list = [language.to_json() for language in Language.Language.query.filter_by(ID_LANGUAGE=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"languages": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


@app.route('/api_v0/language/<name>', methods=['GET'])
def language_by_name(name):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiLanguage:
        return forbidden()
    data_list = [language.to_json() for language in Language.Language.query.filter_by(Name=name)]
    if len(data_list) == 0:
        return not_found()
    msg = {"languages": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/language', methods=['POST'])
def language_add():
    # TODO check roles
    data = request.form
    if data is None or (3 > len(data) > 3):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [language_add() - data len()]')
    if not key_in_request_form('name'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [language_add() - data <name>')

    language = Language.Language(Name=data['name'])

    try:
        db.session.add(language)
        db.session.commit()
        msg = {'NEW language ADDED': language.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {ERROR_500_DEFAULT_MSG: language.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------MEMBER_ACCOUNT-------------------------------#
# TODO not implemented in v.0


# -------------------------------MEMBER_LANGUAGE-------------------------------#


# -------------------------------MEMBER_OFFER-------------------------------#
# READ ALL
@app.route('/api_v0/member_offer-list', methods=['GET'])
def member_offer_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiMember:
        return forbidden()
    data_list = [member_offer.to_json() for member_offer in Member_Offer.Member_Offer.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"member_offers": data_list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/member_offer/<id>', methods=['GET'])
def member_offer_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiMember:
        return forbidden()
    data_list = [member_offer.to_json() for member_offer in Member_Offer.Member_Offer.query.filter_by(Id_Member=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"member_offers": data_list}  # there can be member_offers with the same id_member
    return Response(json.dumps(msg), status=200)


# -------------------------------MEMBER-------------------------------#
# READ ALL
@app.route('/api_v0/member-list', methods=['GET'])
def member_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiMember:
        return forbidden()
    data_list = [member.to_json() for member in Member.Member.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"member_list": data_list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/member/<id>', methods=['GET'])
def member_by_id(id):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    # print(type(role))
    if not role.CanSeeApiMember:
        return forbidden()
    member = Member.Member.query.filter_by(ID_MEMBER=id).first()
    if member is None:
        return not_found()
    msg = {"member": member.to_json()}
    return Response(json.dumps(msg), status=200)


# INSERT
@app.route('/api_v0/member', methods=['POST'])
def member_add():
    data = request.form
    if data is None or (18 > len(data) > 21):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data len()]')
    if not key_in_request_form('id'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <id>]')
    if not key_in_request_form('name'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <name>')
    if not key_in_request_form('surname'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <surname>')
    if not key_in_request_form('dni'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <dni>')
    if not key_in_request_form('address'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <address>')
    if not key_in_request_form('cp'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <cp>')
    if not key_in_request_form('city'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <city>')
    if not key_in_request_form('province'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <province>')
    if not key_in_request_form('gender'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <gender>')
    if not key_in_request_form('mobile'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <mobile>')
    # if not key_in_request_form('profile_picture'):
    #     return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <profile_picture>')
    if not key_in_request_form('birth_date'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <birth_date>')
    if not key_in_request_form('join_date'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <join_date>')
    if not key_in_request_form('cancellation_date'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <cancellation_date>')

    pna_address = None
    pna_cp = None
    pna_city = None
    pna_province = None

    if key_in_request_form('pna_data'):
        if not key_in_request_form('pna_address'):
            return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_address")
        if not key_in_request_form('pna_cp'):
            return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_cp")
        if not key_in_request_form('pna_city'):
            return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_city")
        if not key_in_request_form('pna_province'):
            return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_province")
        pna_address = data['pna_address']
        pna_cp = data['pna_cp']
        pna_city = data['pna_city']
        pna_province = data['pna_province']

    try:
        land_line = None if not key_in_request_form('land_line') else data["land_line"]
        vehicle = False if not key_in_request_form('vehicle') or data["vehicle"] else bool(data["vehicle"])
        geographical_mobility = False if not key_in_request_form('geographical_mobility') or data[
            "geographical_mobility"] \
            else bool(data["geographical_mobility"])
        disability_grade = 0 if not key_in_request_form('disability_grade') or data["disability_grade"] \
            else int(data["disability_grade"])
        profile_pic = None if not key_in_request_form('profile_picture') else data["profile_picture"]

        member = Member.Member(ID_MEMBER=data['id'],
                               Name=data['name'],
                               Surname=data['surname'],
                               DNI=data['dni'],
                               Address=data['address'],
                               CP=data['cp'],
                               City=data['city'],
                               Province=data['province'],
                               PNA_Address=pna_address,
                               PNA_CP=pna_cp,
                               PNA_City=pna_city,
                               PNA_Province=pna_province,
                               Gender=data['gender'],
                               Land_Line=land_line,
                               Mobile=data['mobile'],
                               Profile_Picture=profile_pic,
                               Birth_Date=data['birth_date'],
                               Vehicle=vehicle,
                               Geographical_Mobility=geographical_mobility,
                               Disability_Grade=disability_grade,
                               Join_Date=data['join_date'],
                               Cancellation_Date=data['cancellation_date'])

        db.session.add(member)
        db.session.commit()
        msg = {'member_add': member.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {'member_add': ERROR_500_DEFAULT_MSG}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# UPDATE
@app.route("/api_v0/member/<id>", methods=["PUT"])
def member_verify_update(id):
    member = Member.Member.query.filter_by(ID_MEMBER=id)
    # Check if exists
    if member is None or member.count() == 0:
        return not_found()
    if member.count() > 1:
        return internal_server_error()
    else:
        if request.method == "PUT":
            data = request.form
            # Check that the value given is present
            if not key_in_request_form('verify') and not key_in_request_form('active'):
                return bad_request()
            else:
                status_code = 400
                msg = ERROR_400_DEFAULT_MSG
                try:
                    if key_in_request_form('verify'):
                        if data["verify"] == 'True':
                            member.Verify = True
                        elif data["verify"] == 'False':
                            member.Verify = False
                    if key_in_request_form('active'):
                        if data["active"] == 'True':
                            member.Active = True
                        elif data["active"] == 'False':
                            member.Active = False
                except Exception as ex:
                    print(ex)
                    db.session.rollback()
                if status_code != 200:
                    return internal_server_error("An error has occurred processing PUT query")
                return Response(json.dumps(msg), status=status_code)


# -------------------------------OFFER-------------------------------#
# READ ALL
@app.route('/api_v0/offer-list', methods=['GET'])
def offer_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [offer.to_json() for offer in Offer.Offer.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"offers": data_list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/offer/<id>', methods=['GET'])
def offer_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [offer.to_json() for offer in Offer.Offer.query.filter_by(ID_OFFER=id)]
    if len(data_list) == 0:
        return not_found()
    elif len(data_list) > 1:
        return internal_server_error()  # there can't be offers with the same id
    msg = {"offers": data_list}
    return Response(json.dumps(msg), status=200)


# UPDATE
@app.route("/api_v0/offer/<id>", methods=["GET", "PUT"])
def offer_verify_update(id):
    offer = Offer.Offer.query.filter_by(ID_OFFER=id)
    # comprobación de que se almacen un dato
    if offer is None or offer.count() == 0:
        return not_found()
    if offer.count() > 1:
        return internal_server_error()
    else:
        if request.method == "GET":
            msg = {"offer": [off.to_json() for off in offer]}
            return Response(json.dumps(msg), status=200)
        elif request.method == "PUT":
            data = request.form
            # comprobacion que se guarde el valor que queremos cambiar
            if not key_in_request_form('verify') and not key_in_request_form('active'):
                return bad_request()
            else:
                status_code = 400
                msg = ERROR_400_DEFAULT_MSG
                try:
                    if key_in_request_form('verify'):
                        if data["verify"] == 'True':
                            offer.Verify = True
                        elif data["verify"] == 'False':
                            offer.Verify = False
                    if key_in_request_form('active'):
                        if data["active"] == 'True':
                            offer.Active = True
                        elif data["active"] == 'False':
                            offer.Active = False
                except Exception as ex:
                    print(ex)
                    db.session.rollback()
                if status_code != 200:
                    return internal_server_error("An error has occurred processing PUT query")
                return Response(json.dumps(msg), status=status_code)


# -------------------------------PROFESSIONAL_PROFILE-------------------------------#
# TODO not implemented in v.0


# -------------------------------QUALIFICATION-------------------------------#
# READ ALL
@app.route('/api_v0/qualification-list', methods=['GET'])
def qualification_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiQualification:
        return forbidden()
    data_list = [qualification.to_json() for qualification in Qualification.Qualification.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"qualification": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/qualification/<id>', methods=['GET'])
def job_qualification_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiQualification:
        return forbidden()
    data_list = [qualification.to_json() for qualification in
                 Qualification.Qualification.query.filter_by(ID_QUALIFICATION=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"qualification": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/qualification', methods=['POST'])
def qualification_add():
    # TODO check roles
    data = request.form
    if data is None or (2 > len(data) > 2):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data len()]')
    if not key_in_request_form('name'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data <name>')
    if not key_in_request_form('description'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data <description>')

    qualification = Qualification.Qualification(Name=data['name'],
                                                Description=data['description'])

    try:
        db.session.add(qualification)
        db.session.commit()
        msg = {'NEW qualification ADDED': qualification.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {ERROR_500_DEFAULT_MSG: qualification.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------REVIEW-------------------------------#
# TODO not implemented in v.0


# -------------------------------ROLE-------------------------------#
# READ ALL
@app.route('/api_v0/role-list', methods=['GET'])
def role_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiRole:
        return forbidden()
    data_list = [role.to_json() for role in Role.Role.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"roles": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/role/<id>', methods=['GET'])
def role_by_id(id: int):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiRole:
        return forbidden()
    data_list = [role.to_json() for role in Role.Role.query.filter_by(ID_ROLE=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"roles": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# -------------------------------SECTION-------------------------------#
# READ ALL
@app.route('/api_v0/section-list', methods=['GET'])
def section_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiSection:
        return forbidden()
    data_list = [section.to_json() for section in Section.Section.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"section": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/section/<category>', methods=['GET'])
def section_by_category(category):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiSection:
        return forbidden()
    data_list = [section.to_json() for section in Section.Section.query.filter_by(Description=category)]
    if len(data_list) == 0:
        return not_found()
    msg = {"section": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/section', methods=['POST'])
def section_add():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanMakeSection:
        return forbidden()
    data = request.form
    if data is None or (6 > len(data) > 6):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data len()]')
    if not key_in_request_form('category'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <category>')
    if not key_in_request_form('description'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <description>')
    if not key_in_request_form('publication_date'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <publication_date>')
    if not key_in_request_form('schedule'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <schedule>')
    if not key_in_request_form('img_resource'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <img_resource>')
    if not key_in_request_form('price'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <price>')

    section = Section.Section(Category=data['category'],
                              Description=data['description'],
                              Publication_Date=data['publication_date'],
                              Schedule=data['schedule'],
                              Img_Resource=data['img_resource'],
                              Price=data['price'])

    try:
        db.session.add(section)
        db.session.commit()
        msg = {'NEW section ADDED': section.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {ERROR_500_DEFAULT_MSG: section.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# UPDATE
@app.route("/api_v0/section/<id>", methods=["GET", "PUT"])
def section_active_update(id):
    section = Section.Section.query.filter_by(ID_SECTION=id)
    # comprobación de que se almacen un dato
    if section is None or section.count() == 0:
        return not_found()
    if section.count() > 1:
        return internal_server_error()
    else:
        if request.method == "GET":
            msg = {"section": [sect.to_json() for sect in section]}
            return Response(json.dumps(msg), status=200)
        elif request.method == "PUT":
            data = request.form
            # comprobacion que se guarde el valor que queremos cambiar
            if not key_in_request_form('active'):
                return bad_request()
            else:
                status_code = 400
                msg = {"default message"}
                try:
                    if key_in_request_form('active'):
                        if data["active"] == 'True':
                            section.Active = True
                        elif data["active"] == 'False':
                            section.Active = False

                except Exception as ex:
                    db.session.rollback()
                if status_code != 200:
                    return internal_server_error("An error has occurred processing PUT query")
                return Response(json.dumps(msg), status=status_code)


# -------------------------------USER------------------------------- #
# READ ALL
@app.route('/api_v0/user-list', methods=['GET'])
def user_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiUser:
        return forbidden()
    data_list = [user.to_json() for user in User.User.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"user": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/user/<key>', methods=['GET'])
def user_by_id(key: str):
    if request.method == 'GET':
        role, user_token = user_privileges()
        if type(role) is Response:
            return role
        # Now we can ask for the requirement set
        if "%40" in key or "@" in key:
            username = key if "%40" in key else key.replace("%40", "@")
            if user_token != username:
                return forbidden()
            user = User.User.query.filter_by(Email=username).first()
        elif valid_uuid(key):
            if not role.CanSeeApiUser:
                return forbidden()
            user = User.User.query.filter_by(ID_USER=key).first()
        else:
            return bad_request()
        if user is None:
            return not_found()
        json_data = user.to_json()
        if user.member is not None and len(user.member) > 0:
            json_data.update(user.member[0].to_json())
            json_data.pop('id_member')
        elif user.company is not None and len(user.company) > 0:
            json_data.update(user.company[0].to_json())
            json_data.pop('id_company')
        msg = {"user_get": json_data}
        return Response(json.dumps(msg), status=200)


# INSERT
@app.route('/api_v0/user', methods=['POST'])
def user_add():
    data = request.form
    if data is None or len(data) != 3:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data len()]')
    if not key_in_request_form('passwd'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <passwd>')
    if not key_in_request_form('email'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <email>')
    if not key_in_request_form('role'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <role>]')

    user = User.User(Passwd=sec.hashed_password(data['passwd']),
                     Email=data['email'],
                     Id_Role=int(data['role']))

    try:
        db.session.add(user)
        db.session.commit()
        new_user = User.User.query.filter_by(Email=user.Email).first()
        msg = {'user_add': new_user.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {"user_add": ERROR_500_DEFAULT_MSG}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


@app.route("/api_v0/login", methods=["POST"])
def api_login():
    # Check for the length of the form request
    if len(request.form) != 2:
        return bad_request()
    # Check for the 'user-login' field
    if key_in_request_form('user-login'):
        username = request.form['user-login']
        if username == "":
            error = "El nombre de usuario no puede estar vacio"
            return bad_request(error)
        if key_in_request_form('user-passwd'):
            passwd = request.form['user-passwd']
            if passwd == "":
                error = "La contraseña no puede estar vacia"
                return bad_request(error)
            # Search for the user
            user = User.User.query.filter_by(Email=username).first()
            if user is not None:
                # As the method says
                if sec.verify_password(passwd, user.Passwd):
                    # Generate the auth token
                    token_info = sec.generate_jwt({
                        "user": user.Email,
                        "user-role": user.Id_Role,
                        "curr_time": dt.now().strftime("%y-%m-%d %H:%M:%S"),
                        "exp_time": (dt.now() + timedelta(minutes=30)).strftime("%y-%m-%d %H:%M:%S")
                    })
                    # Custom response to add the auth cookie
                    return Response(json.dumps({'auth': token_info}), status=200)
                else:
                    error = "Contraseña incorrecta"
                    return bad_request(error)
            else:
                error = "Usuario incorrecto"
                return bad_request(error)


# REGISTER ROUTES
@app.route("/api_v0/register/member", methods=["POST"])
def api_register_member():
    try:
        data = request.form
        if data is None or len(data) < 15:
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data len()]')
        # USER VALIDATIONS
        if not key_in_request_form('passwd'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <passwd>')
        if not key_in_request_form('email'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <email>')
        if not key_in_request_form('role'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <role>]')

        user_id = uuid.uuid4()
        user = User.User(ID_USER=user_id,
                         Passwd=sec.hashed_password(data['passwd']),
                         Email=data['email'],
                         Id_Role=int(data['role']))
        # MEMBER VALIDATIONS
        if not key_in_request_form('name'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <name>')
        if not key_in_request_form('surname'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <surname>')
        if not key_in_request_form('dni'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <dni>')
        if not key_in_request_form('address'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <address>')
        if not key_in_request_form('cp'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <cp>')
        if not key_in_request_form('city'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <city>')
        if not key_in_request_form('province'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <province>')
        if not key_in_request_form('gender'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <gender>')
        if not key_in_request_form('mobile'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <mobile>')
        if not key_in_request_form('birth_date'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <birth_date>')
        if not key_in_request_form('join_date'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <join_date>')
        if not key_in_request_form('cancellation_date'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <cancellation_date>')
        pna_address = None
        pna_cp = None
        pna_city = None
        pna_province = None
        if key_in_request_form('pna_data'):
            if not key_in_request_form('pna_address'):
                return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_address")
            if not key_in_request_form('pna_cp'):
                return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_cp")
            if not key_in_request_form('pna_city'):
                return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_city")
            if not key_in_request_form('pna_province'):
                return bad_request(ERROR_400_DEFAULT_MSG + "[ERROR] - member_add() - insert: pna_province")
            pna_address = data['pna_address']
            pna_cp = data['pna_cp']
            pna_city = data['pna_city']
            pna_province = data['pna_province']
        land_line = None if not key_in_request_form('land_line') else data["land_line"]
        vehicle = False if not key_in_request_form('vehicle') or data["vehicle"] else bool(data["vehicle"])
        geographical_mobility = False if not key_in_request_form('geographical_mobility') or data[
            "geographical_mobility"] \
            else bool(data["geographical_mobility"])
        disability_grade = 0 if not key_in_request_form('disability_grade') or data["disability_grade"] != "" \
            else int(data["disability_grade"])
        profile_pic = None if not key_in_request_form('profile_picture') else b64decode(data["profile_picture"])
        # BEGINNING OF THE INSERTS
        db.session.add(user)
        # TODO MAYBE WE SHOULD DO A SELECT TO VERIFY THAT THE USER HAS BEEN CREATED
        member = Member.Member(ID_MEMBER=user.ID_USER,
                               Name=data['name'],
                               Surname=data['surname'],
                               DNI=data['dni'],
                               Address=data['address'],
                               CP=data['cp'],
                               City=data['city'],
                               Province=data['province'],
                               PNA_Address=pna_address,
                               PNA_CP=pna_cp,
                               PNA_City=pna_city,
                               PNA_Province=pna_province,
                               Gender=data['gender'],
                               Land_Line=land_line,
                               Mobile=data['mobile'],
                               Profile_Picture=profile_pic,
                               Birth_Date=data['birth_date'],
                               Vehicle=vehicle,
                               Geographical_Mobility=geographical_mobility,
                               Disability_Grade=disability_grade,
                               Join_Date=data['join_date'],
                               Cancellation_Date=data['cancellation_date'])
        db.session.add(member)
        db.session.commit()
        msg = {"register_member": "SUCCESS"}
        return Response(json.dumps(msg), status=200)
    except Exception as ex:
        db.session.rollback()
        return internal_server_error(ERROR_500_DEFAULT_MSG + " :: {}".format(ex))


# method [GET] --> to get object lists for offer form
# method [POST] --> to get data from form and save an offer
@app.route('/api_v0/register/offer', methods=['GET', 'POST'])
def api_register_offer_job_demand():
    if request.method == "GET":
        try:
            print('api_register_offer_job_demand')
            language_data_list= Language.Language.query.all() # quicker query than language_list()
            qualification_data_list= Qualification.Qualification.query.all()
            job_category_data_list= Job_Category.Job_Category.query.all()
            # shift_data_list= [Shift.CONTINUOUS, Shift.SPLIT]
            # schedule_data_list= list(map(int, Schedule))
            # working_day_data_list= list(map(int, Working_Day))
            # print(list(map(int, Shift)))
            # TODO falta el contract type
            # contract_type_data_list= list(map(int, Working_Day))
            response = {
                'offer_add_get': {
                    'language_list': [language.to_json() for language in language_data_list],
                    'qualification_list': [qualification.to_json() for qualification in qualification_data_list],
                    'job_category_list': [job_category.to_json() for job_category in job_category_data_list]
                }
            }
            return Response(json.dumps(response), status=200)
        except Exception as ex:
            return internal_server_error()
    elif request.method == "POST":
        try:
            role, _ = user_privileges()
            if type(role) is Response:
                return role
            # Now we can ask for the requirement set
            if not role.CanMakeOffer:
                return forbidden()
            data = request.form
            if data is None or (5 > len(data) > 8):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data len()]')
            if not key_in_request_form('company_name'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <company_name>')
            if not key_in_request_form('address'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <address>')
            if not key_in_request_form('contact_name'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_name>')
            if not key_in_request_form('contact_phone'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_phone>')
            if not key_in_request_form('contact_email'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_email>')

            contact_name_2 = "" if not key_in_request_form('contact_name_2') else data["contact_name_2"]
            contact_phone_2 = "" if not key_in_request_form('contact_phone_2') else data["contact_phone_2"]
            contact_email_2 = "" if not key_in_request_form('contact_email_2') else data["contact_email_2"]

            offer = Offer.Offer(Company_Name=data['company_name'],
                                Address=data['address'],
                                Contact_Name=data['contact_name'],
                                Contact_Phone=data['contact_phone'],
                                Contact_Email=data['contact_email'],
                                Contact_Name_2=contact_name_2,
                                Contact_Phone_2=contact_phone_2,
                                Contact_Email_2=contact_email_2)

            # job_demand validation
            if not key_in_request_form('vacancies'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <vacancies>')
            if not key_in_request_form('schedule'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <schedule>')
            if not key_in_request_form('working_day'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <working_day>')
            if not key_in_request_form('shift'):
                return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <shift>')

            monthly_salary = "" if not key_in_request_form('monthly_salary') else data['monthly_salary']
            contract_type = "" if not key_in_request_form('contract_type') else data['contract_type']
            holidays = "" if not key_in_request_form('holidays') else data['holidays']
            experience = "" if not key_in_request_form('experience') else data['experience']
            vehicle = False if not key_in_request_form('vehicle') else data['vehicle']
            geographical_mobility = False if not key_in_request_form('geographical_mobility') else data['geographical_mobility']
            others = "" if not key_in_request_form('others') else data['others']

            db.session.add(offer)

            job_demand = Job_Demand.Job_Demand(Vacancies=data['vacancies'],
                                               Monthly_Salary=monthly_salary,
                                               Contract_Type=contract_type,
                                               Schedule=data['schedule'],
                                               Working_Day=data['working_day'],
                                               Shift=data['shift'],
                                               Holidays=holidays,
                                               Experience=experience,
                                               Vehicle=vehicle,
                                               Geographical_Mobility=geographical_mobility,
                                               Others=others)

            db.session.add(job_demand)
            db.session.refresh(job_demand)

            db.session.commit()
            msg = {"add_offer": "SUCCESS"}
            return Response(json.dumps(msg), status=200)
        except Exception as ex:
            db.session.rollback()
            return internal_server_error(ERROR_500_DEFAULT_MSG)


@app.route("/api_v0/register/company", methods=["POST"])
def api_register_company():
    try:
        data = request.form
        if data is None or len(data) < 9:
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data len()]')
        # USER VALIDATIONS
        if not key_in_request_form('passwd'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <passwd>')
        if not key_in_request_form('email'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <email>')
        if not key_in_request_form('role'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <role>]')

        user_id = uuid.uuid4()
        user = User.User(ID_USER=user_id,
                         Passwd=sec.hashed_password(data['passwd']),
                         Email=data['email'],
                         Id_Role=int(data['role']))
        # COMPANY VALIDATIONS
        if not key_in_request_form('company_name'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <company_name>]')
        if not key_in_request_form('type'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <type>')
        if not key_in_request_form('cif'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <cif>]')
        if not key_in_request_form('contact_name'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_name>]')
        if not key_in_request_form('contact_phone'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_phone>]')
        if not key_in_request_form('contact_email'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_email>]')

        address = "" if not key_in_request_form('address') else data['address']
        cp = "" if not key_in_request_form('cp') else data['cp']
        city = "" if not key_in_request_form('city') else data['city']
        province = "" if not key_in_request_form('province') else data['province']
        description = "" if not key_in_request_form('description') else data['description']
        # BEGINNING OF INSERTS
        db.session.add(user)
        # TODO MAYBE WE SHOULD DO A SELECT TO VERIFY THAT THE USER HAS BEEN CREATED
        company = Company.Company(ID_COMPANY=user.ID_USER,
                                  Name=data['company_name'],
                                  Type=data['type'],
                                  CIF=data['cif'],
                                  Address=address,
                                  CP=cp,
                                  City=city,
                                  Province=province,
                                  Contact_Name=data['contact_name'],
                                  Contact_Phone=data['contact_phone'],
                                  Contact_Email=data['contact_email'],
                                  Description=description)
        print(company)
        db.session.add(company)
        db.session.commit()
        msg = {'register_company': 'SUCCESS'}
        return Response(json.dumps(msg), status=200)
        
    except Exception as ex:
        db.session.rollback()
        return internal_server_error(ERROR_500_DEFAULT_MSG + " " + ex)


@app.route("/api_v0/admin/member", methods=["GET"])
def api_get_member_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if role.IsAAAHOSTUR and role.CanSeeApiMember:
        result_set = User.User.query.all()
        data_list = []
        for user in result_set:
            if user.member is not None and len(user.member) > 0:
                json_data = user.to_json()
                json_data['member_name'] = user.member[0].Name
                json_data['member_surname'] = user.member[0].Surname
                json_data['member_dni'] = user.member[0].DNI
                json_data['member_mobile'] = user.member[0].Mobile
                json_data['member_landline'] = user.member[0].Land_Line
                json_data['member_verify'] = user.member[0].Verify
                json_data['member_active'] = user.member[0].Active
                data_list.append(json_data)
        msg = {'adm_member': data_list}
        return Response(json.dumps(msg), status=200)
    else:
        return forbidden()


@app.route("/api_v0/admin/company", methods=["GET"])
def api_get_company_list():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if role.IsAAAHOSTUR and role.CanSeeApiCompany:
        result_set = User.User.query.all()
        data_list = []
        for user in result_set:
            if user.company is not None and len(user.company) > 0:
                json_data = user.to_json()
                json_data['company_name'] = user.company[0].Name
                json_data['company_contact_name'] = user.company[0].Contact_Name
                json_data['company_nif'] = user.company[0].CIF
                json_data['company_contact_email'] = user.company[0].Contact_Email
                json_data['company_contact_mobile'] = user.company[0].Contact_Phone
                json_data['company_verify'] = user.company[0].Verify
                json_data['company_active'] = user.company[0].Active
                data_list.append(json_data)
        msg = {'adm_company': data_list}
        return Response(json.dumps(msg), status=200)
    else:
        return forbidden()


# endregion
# ==================================================================================================================== #
# =======================================================   PAGES   ================================================== #
# region PAGES
# LOGIN
@app.route("/login", methods=['GET', 'POST'])
def login():
    # This definition can be called from some methods
    if request.method == 'GET':
        # Check if the user is already logged
        if not not_auth_header():
            return redirect(url_for("index", _method="GET"))  # Redirect to index if True
        return render_template('login.html')  # Load login if False
    elif request.method == 'POST':
        # Check for the length of the form request
        if len(request.form) != 2:
            return bad_request()
        # Check for the 'user-login' field
        if key_in_request_form('user-login'):
            username = request.form['user-login']
            if username == "":
                error = "El nombre de usuario no puede estar vacio"
                if navigator_user_agent():  # Empty user
                    return render_template('login.html', error=error)
                return bad_request(error)
            if key_in_request_form('user-passwd'):
                passwd = request.form['user-passwd']
                if passwd == "":
                    error = "La contraseña no puede estar vacia"
                    if navigator_user_agent():  # Empty password
                        return render_template('login.html', error=error)
                    return bad_request(error)
                login_data = {
                    'user-login': request.form['user-login'],
                    'user-passwd': request.form['user-passwd']  # TODO !IMPORTANT SE NECESITA UN CERTIFICADO HTTPS
                }
                login_response = requests.post("http://localhost:5000/api_v0/login", data=login_data)
                if login_response.status_code != 200:
                    error = login_response.json()['message']
                    if navigator_user_agent():
                        return render_template('login.html', error=error)
                    return bad_request(error)
                    # Custom response to add the auth cookie
                token_info = login_response.json()['auth']
                success_resp = make_response(redirect(url_for("index", _method="GET")))
                success_resp.set_cookie('auth', token_info)
                return success_resp
        else:
            return bad_request()
    else:
        return bad_request("{} method not supported".format(request.method))


@app.route("/logout", methods=["GET"])
def logout():
    if not_auth_header():
        return redirect(url_for("index", _method="GET"))
    resp = make_response(redirect(url_for("index", _method="GET")))
    resp.delete_cookie('auth')
    return resp


@app.route("/", methods=["GET"])
def index():
    if not_auth_header():
        return render_template("index.html", code=200)
    payload = sec.decode_jwt(request.cookies.get('auth'))
    return render_template("index.html", payload=payload, code=200)


def check_member_params(form) -> str:
    """Validations of the member form"""
    # USER INFO
    if 'user-email' not in form or form['user-email'] is None or form['user-email'] == "":
        return "Email no valido"
    if 'user-pwd' not in form or form['user-pwd'] is None or sec.check_valid_passwd(form['user-pwd']) is None:
        return "Contraseña no valida"
    # MEMBER INFO
    if 'member-name' not in form or form['member-name'] is None or form['member-name'] == "":
        return "Nombre no valido"
    if 'member-surname' not in form or form['member-name'] is None or form['member-name'] == "":
        return "Apellidos no valido"
    # TODO Check for valid DNI, at least sth like 8 digits and 1 letter, it can be a NIE...
    if 'member-dni' not in form or form['member-dni'] is None or not utils.validate_nif(form['member-dni']):
        return "DNI no valido"
    if 'member-address' not in form or form['member-address'] is None or form['member-address'] == "":
        return "Direccion no valido"
    if 'member-cp' not in form or form['member-cp'] is None or form['member-cp'] == "":
        return "Codigo Postal no valido"
    if 'member-city' not in form or form['member-city'] is None or form['member-city'] == "":
        return "Ciudad no valido"
    if 'member-province' not in form or form['member-province'] is None or form['member-province'] == "":
        return "Provincia no valida"
    if 'rb-group-gender' not in form or form['rb-group-gender'] is None or form['rb-group-gender'] == "":
        return "Genero no valido"
    if 'member-mobile' not in form or form['member-mobile'] is None or form['member-mobile'] == "":
        return "Tlf. Movil no valido"
    if 'member-birthdate' not in form or form['member-birthdate'] is None or form['member-birthdate'] == "":
        return "F. Nacimiento no valido"
    if key_in_request_form('pna_cb') and (not key_in_request_form('member-pna-address') or form['member-pna-address']):
        return "Direccion PNA no valido"
    if key_in_request_form('pna_cb') and (not key_in_request_form('member-pna-cp') or form['member-pna-cp']):
        return "Codigo Postal PNA no valido"
    if key_in_request_form('pna_cb') and (not key_in_request_form('member-pna-city') or form['member-pna-city']):
        return "Ciudad PNA no valido"
    if key_in_request_form('pna_cb') and (
            not key_in_request_form('member-pna-province') or form['member-pna-province']):
        return "Provincia PNA no valida"
    if 'member-landline' not in form:
        return "F. Nacimiento no valido"
    return ""


@app.route("/register/member", methods=["GET", "POST"])
def register_member():
    if request.method == "POST":
        error = "Las contraseñas no coinciden"
        data = request.form
        try:
            files = request.files['member-profilepic']
        except:
            files = None
        if data["user-pwd"] == data["user-pwd-2"]:
            # print(data)
            error = check_member_params(data)
            if error != "":
                if navigator_user_agent():
                    return render_template("signinmember.html", error=error)
                return bad_request(error)
            user_member_data_form = {
                "email": data["user-email"],
                "passwd": data["user-pwd"],
                "role": 104,
                "name": data["member-name"],
                "surname": data["member-surname"],
                "dni": data["member-dni"],
                "address": data["member-address"],
                "cp": data["member-cp"],
                "city": data["member-city"],
                "province": data["member-province"],
                "gender": data["rb-group-gender"],
                "mobile": data["member-mobile"],
                "profile_picture": None if files is None else b64encode(files.read()),
                "birth_date": data["member-birthdate"],
                "join_date": dt.now().strftime("%y-%m-%d %H:%M:%S"),
                "cancellation_date": "",
                "pna_data": None if not key_in_request_form('pna_cb') or data['pna_cb'] == "" else data["pna_cb"],
                "pna_address": data["member-pna-address"],
                "pna_cp": data["member-pna-cp"],
                "pna_city": data["member-pna-city"],
                "pna_province": data["member-pna-province"],
                "land_line": data["member-landline"],
                "vehicle": True if not key_in_request_form('rb-group-car') or data["rb-group-car"] == "y" else False,
                "geographical_mobility": True if not key_in_request_form('rb-group-mov') or data[
                    "rb-group-mov"] == "y" else False,
                "disability_grade": 0 if not key_in_request_form("member-handicap") or data[
                    "member-handicap"] == "" else int(data["member-handicap"])
            }

            # print(user_member_data_form)
            user_created = requests.post('http://localhost:5000/api_v0/register/member', data=user_member_data_form,
                                         cookies=request.cookies)
            # Check if the user has been created
            if user_created.status_code == 200:
                return redirect(url_for("login"))  # TODO redirect to success-register-page
            else:
                if 'user_add' in user_created.json():
                    error = user_created.json()["user_add"]
                elif 'message' in user_created.json():
                    error = user_created.json()["message"]
                else:
                    error = 'DEFAULT ERROR MESSAGE'
        return render_template("signinmember.html", error=error)
    elif request.method == "GET":
        return render_template("signinmember.html")
    else:
        return bad_request("{} method not supported".format(request.method))


@app.route("/profile", methods=["GET"])
def profile():
    role, user_token = user_privileges()
    if type(role) is Response:
        return role
    payload = sec.decode_jwt(request.cookies.get('auth'))
    user_token = user_token.replace("@", "%40")
    user_info = requests.get("http://localhost:5000/api_v0/user/{}".format(user_token), cookies=request.cookies)

    if user_info.status_code == 200:
        json_data = user_info.json()['user_get']
        if role.IsMember:
            context = {
                'user': {
                        'email': json_data['email']
                    },
                'member': {
                        'name': json_data['name'],
                        'surname': json_data['surname'],
                        'dni': json_data['dni'],
                        'gender': 'Hombre' if json_data['gender'] == 'H' else (
                            'Mujer' if json_data['gender'] == 'M' else 'Otro'),
                        'profilepic': "" if json_data['profile_picture'] is None
                                            or json_data['profile_picture'] == "" else
                        json_data['profile_picture'],
                        'birthdate': json_data['birth_date'],
                        'mobile': json_data['mobile'],
                        'landline': json_data['land_line'],
                        'address': json_data['address'],
                        'cp': json_data['cp'],
                        'city': json_data['city'],
                        'province': json_data['province'],
                        'pna_address': '' if 'pna_address' not in json_data or json_data['pna_address'] == '' else json_data['pna_address'],
                        'pna_cp': '' if 'pna_cp' not in json_data or json_data['pna_cp'] == '' else json_data['pna_cp'],
                        'pna_city': '' if 'pna_city' not in json_data or json_data['pna_city'] == '' else json_data['pna_city'],
                        'pna_province': '' if 'pna_province' not in json_data or json_data['pna_province'] == '' else json_data['pna_province'],
                        'vehicle': 'SI' if json_data['vehicle'] or
                                           json_data['vehicle'] == 'True' else 'NO',
                        'mov': 'SI' if json_data['geographical_mobility'] or
                                       json_data['geographical_mobility'] == 'True' else 'NO',
                        'handicap': json_data['disability_grade']
                    }
            }
        elif role.IsCompany:
            context = {
                'user': {
                    'email': json_data['email']
                },
                'company': {
                    'company_name': json_data['name'],
                    'company_type': json_data['type'],
                    'company_nif': json_data['cif'],
                    'company_address': "" if json_data['address'] is None else json_data['address'],
                    'company_cp': "" if json_data['cp'] is None else json_data['cp'],
                    'company_city': "" if json_data['city'] is None else json_data['city'],
                    'company_province': "" if json_data['province'] is None else json_data['province'],
                    'company_contact_name': json_data['contact_name'],
                    'company_contact_phone': json_data['contact_phone'],
                    'company_contact_email': json_data['contact_email'],
                    'company_description': "" if json_data['description'] is None else json_data['description']
                }
            }
        elif role.IsAAAHOSTUR:
            context = {
                'user': {
                    'email': json_data['email']
                }
            }
            if role.CanVerifyMember and role.CanActiveMember:
                context['admin_member'] = True
            if role.CanVerifyCompany and role.CanActiveCompany:
                context['admin_company'] = True
            if role.CanVerifyOffer and role.CanActiveOffer:
                context['admin_offer'] = True
            if role.CanMakeSection and role.CanVerifyOffer and role.CanActiveOffer:
                context['publisher'] = True
        else:
            context = {}
        # print(context)
        return render_template("profile.html", context=context, payload=payload, profile=True)
    return render_template("profile.html")


@app.route("/register/company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        error = "Las contraseñas no coinciden"
        data = request.form
        if data["user-pwd"] == data["user-pwd-2"]:
            user_company_data_form = {
                "email": request.form["user-email"],
                "passwd": request.form["user-pwd"],
                "role": 105,
                "company_name": data["company-name"],
                "type": data["rb-group-company-type"],
                "cif": data["company-cif"],
                "address": data["company-address"],
                "cp": data["company-cp"],
                "city": data["company-city"],
                "province": data["company-province"],
                "contact_name": data["company-contact1-name"],
                "contact_phone": data["company-contact1-tlf"],
                "contact_email": data["company-contact1-email"],
                "description": data["company-desc"]
            }
            # Check if the user has been created
            user_created = requests.post('http://localhost:5000/api_v0/register/company', data=user_company_data_form,
                                         cookies=request.cookies)
            # Check if the user has been created
            if user_created.status_code == 200:
                return redirect(url_for("login"))  # TODO
            else:
                if 'user_add' in user_created.json():
                    error = user_created.json()["user_add"]
                elif 'message' in user_created.json():
                    error = user_created.json()["message"]
                else:
                    error = 'DEFAULT ERROR MESSAGE'
                print(user_created.json())
                error = user_created.json()["message"]
        return render_template("signincompany.html", error=error)
    elif request.method == "GET":
        return render_template("signincompany.html")
    else:
        return bad_request("{} method not supported".format(request.method))


# TODO
def check_offer_params() -> str:
    pass


@app.route("/register/offer", methods=["GET", "POST"])
def register_offer_job_demand():
    if request.method == "POST":
        data = request.form
        error = check_offer_params()
        if error != "":
            if navigator_user_agent():
                return render_template("addoffer.html", error=error)
            return bad_request(error)
        offer_job_demand_data_form = {
            "workplace_name": data["offer-workplace-name"],
            "workplace_address": data["offer-workplace-address"],
            "contact_name": data["offer-contact-name"],
            "contact_phone": data["offer-contact-phone"],
            "contact_email": data["member-surname"],
            "extra-data": None if not key_in_request_form('pna_cb') or data['pna_cb'] == "" else data["pna_cb"],
            "contact_name_2": data["offer-contact-name-2"],
            "contact_phone_2": data["offer-contact-phone-2"],
            "contact_email_2": data["offer-contact-email-2"],           
            "vacancies": data["job-demand-vacancies"],
            "monthly_salary": data["job-demand-monthly-salary"],
            "contract_type": data["job-demand-contract-type"],
            "schedule": data["rb-group-job-demand-schedule"],
            "working_day": data["rb-group-job-demand-working-day"],
            "shift": data["rb-group-job-demand-shift"],
            "holidays": data["job-demand-holidays"],
            "experience": data["job-demand-experience"],
            "vehicle": True if not key_in_request_form('rb-group-car') or data["rb-group-car"] == "y" else False,
            "geographical_mobility": True if not key_in_request_form('rb-group-mov') or data[
                "rb-group-mov"] == "y" else False,
            "others": data["job-demand-others"]
        }
        print(offer_job_demand_data_form)
        offer_created = requests.post('http://localhost:5000/api_v0/register/offer', data=offer_job_demand_data_form,
                                      cookies=request.cookies)
        # Check if the user has been created
        if offer_created.status_code == 200:
            return redirect(url_for("login"))  # TODO redirect to success-register-page
        else:
            error = offer_created.json()["offer_add"] or offer_created.json()["message"]
            return render_template("addoffer.html", error=error)
    elif request.method == "GET":
        offer_data_request = requests.get("http://localhost:5000/api_v0/register/offer", 
                                          cookies=request.cookies)
        if offer_data_request.status_code == 200:
            return render_template("addoffer.html", 
                                   language_list= offer_data_request.json()['offer_add_get']['language_list'],
                                   qualification_list= offer_data_request.json()['offer_add_get']['qualification_list'],
                                   job_category_list= offer_data_request.json()['offer_add_get']['job_category_list'])
        
        error = offer_data_request.json()['message']
        return render_template("addoffer.html", error=error)
    else:
        return bad_request("{} method not supported".format(request.method))


@app.route("/admin/member", methods=["GET"])
def admin_member():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    payload = sec.decode_jwt(request.cookies.get('auth'))
    # Now we can ask for the requirement set
    if role.IsAAAHOSTUR and role.CanSeeApiMember:
        member_list_request = requests.get("http://localhost:5000/api_v0/admin/member", cookies=request.cookies)
        if member_list_request.status_code == 200:
            context = {'member': member_list_request.json()['adm_member']}
            return render_template('admin.html', context=context, payload=payload)
        else:
            if navigator_user_agent():
                return render_template('admin.html', payload=payload)
            return bad_request()
    else:
        return forbidden()


@app.route("/admin/member/<uid>", methods=["GET"])
def admin_single_member(uid: str):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    payload = sec.decode_jwt(request.cookies.get('auth'))
    if role.IsAAAHOSTUR and role.CanSeeApiMember:
        member_get_request = requests.get("http://localhost:5000/api_v0/user/{}".format(uid), cookies=request.cookies)
        if member_get_request.status_code == 200:
            json_data = member_get_request.json()['user_get']
            context = {
                'user': {
                    'email': json_data['email']
                },
                'member': {
                    'name': json_data['name'],
                    'surname': json_data['surname'],
                    'dni': json_data['dni'],
                    'gender': 'Hombre' if json_data['gender'] == 'H' else (
                        'Mujer' if json_data['gender'] == 'M' else 'Otro'),
                    'profilepic': "" if json_data['profile_picture'] is None
                                    or json_data['profile_picture'] == "" else
                        json_data['profile_picture'],
                    'birthdate': json_data['birth_date'],
                    'mobile': json_data['mobile'],
                    'landline': json_data['land_line'],
                    'address': json_data['address'],
                    'cp': json_data['cp'],
                    'city': json_data['city'],
                    'province': json_data['province'],
                    'pna_address': '' if 'pna_address' not in json_data or json_data['pna_address'] == '' else
                    json_data['pna_address'],
                    'pna_cp': '' if 'pna_cp' not in json_data or json_data['pna_cp'] == '' else json_data['pna_cp'],
                    'pna_city': '' if 'pna_city' not in json_data or json_data['pna_city'] == '' else json_data[
                        'pna_city'],
                    'pna_province': '' if 'pna_province' not in json_data or json_data['pna_province'] == '' else
                    json_data['pna_province'],
                    'vehicle': 'SI' if json_data['vehicle'] or
                                       json_data['vehicle'] == 'True' else 'NO',
                    'mov': 'SI' if json_data['geographical_mobility'] or
                                   json_data['geographical_mobility'] == 'True' else 'NO',
                    'handicap': json_data['disability_grade']
                }
            }
            return render_template('profile.html', context=context, payload=payload)
        else:
            if navigator_user_agent():
                return render_template('profile.html')
            return bad_request()
    else:
        return forbidden()


@app.route("/admin/company", methods=["GET"])
def admin_company():
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    payload = sec.decode_jwt(request.cookies.get('auth'))
    if role.IsAAAHOSTUR and role.CanSeeApiCompany:
        company_list_request = requests.get("http://localhost:5000/api_v0/admin/company", cookies=request.cookies)
        if company_list_request.status_code == 200:
            context = {'company': company_list_request.json()['adm_company']}
            return render_template('admin.html', context=context, payload=payload)
        else:
            if navigator_user_agent():
                return render_template('admin.html', payload=payload)
            return bad_request()
    else:
        return forbidden()


@app.route("/admin/company/<uid>", methods=["GET"])
def admin_single_company(uid: str):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    payload = sec.decode_jwt(request.cookies.get('auth'))
    if role.IsAAAHOSTUR and role.CanSeeApiCompany:
        company_get_request = requests.get("http://localhost:5000/api_v0/user/{}".format(uid), cookies=request.cookies)
        if company_get_request.status_code == 200:
            json_data = company_get_request.json()['user_get']
            context = {
                'user': {
                    'email': json_data['email']
                },
                'company': {
                    'company_name': json_data['name'],
                    'company_type': json_data['type'],
                    'company_nif': json_data['cif'],
                    'company_address': "" if json_data['address'] is None else json_data['address'],
                    'company_cp': "" if json_data['cp'] is None else json_data['cp'],
                    'company_city': "" if json_data['city'] is None else json_data['city'],
                    'company_province': "" if json_data['province'] is None else json_data['province'],
                    'company_contact_name': json_data['contact_name'],
                    'company_contact_phone': json_data['contact_phone'],
                    'company_contact_email': json_data['contact_email'],
                    'company_description': "" if json_data['description'] is None else json_data['description']
                }
            }
            return render_template('profile.html', context=context, payload=payload)
        else:
            if navigator_user_agent():
                return render_template('profile.html', payload=payload)
            return bad_request()
    else:
        return forbidden()


@app.route('/admin/offer', methods=['GET'])
def admin_offer():
    pass


@app.route('/admin/offer/<uid>', methods=['GET'])
def admin_single_offer(uid):
    pass


@app.route('/admin/section', methods=['GET'])
def admin_section():
    pass


@app.route('/admin/section/<uid>', methods=['GET'])
def admin_single_section(uid):
    pass


@app.route('/job', methods=['GET'])
def job_opportunities():
    return "<h1> IN PROGRESS :S </h1>"


@app.route("/privacy", methods=["GET"])
def privacy():
    return "<h1>IN PROGRESS</h1>"


@app.route("/legal", methods=["GET"])
def legal():
    return "<h1>IN PROGRESS</h1>"


# endregion
# ==================================================================================================================== #
# ========================================================= MAIN ===================================================== #
# region MAIN

if __name__ == '__main__':
    # Conf contains DB settings
    app.config.from_object(conf)
    # DB Connection (if db exists and not(table models) it will create the tables without data)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # HTTP Common errors handlers
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(429, too_many_request)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(504, gateway_timeout)
    # run
    app.run(host='0.0.0.0', port=5000)

# endregion
# ==================================================================================================================== #
