import uuid
from base64 import b64encode, b64decode
from datetime import datetime as dt, timedelta
from user_agents import parse
import requests
from flask import Flask, request, json, render_template, Response, redirect, url_for, make_response
from models import db, Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language, \
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review, Shift, Schedule, Working_Day, \
    Contract_Type
from config import config
from security import security
import utils

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
# ==================================================================================================================== #
# region app declaration and its first settings

app = Flask(__name__)
conf = config['development']
sec = security.Security(conf.SECRET_KEY, conf.ALGORITHM)


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
        "title": "Internal Server Error",
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
# ==================================================================================================================== #
# region should be in utils

def not_auth_header() -> bool:
    """True if 'auth' header not found or empty"""
    return request.cookies.get('auth') is None


def get_user_from_token(token: str) -> tuple:
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


def user_privileges() -> tuple:
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
# =========================================================  API  ==================================================== #
# region API

# -------------------------------ACADEMIC_PROFILE-------------------------------#
# INSERT
@app.route('/api_v0/academic_profile', methods=['POST'])
def academic_profile_add():
    try:
        role, _ = user_privileges()
        if type(role) is Response:
            return role
        # Now we can ask for the requirement set
        if not role.CanSeeApiMember:
            return forbidden()
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

        db.session.add(academic_profile)
        db.session.commit()
        msg = {'academic_profile_add': academic_profile.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {'academic_profile_add': ERROR_500_DEFAULT_MSG}
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
    msg = {"company_list": data_list}
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
    company = Company.Company.query.filter_by(ID_COMPANY=id).first()
    if company is None:
        return not_found()
    data_list = company.to_json()
    msg = {"company": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/company', methods=['POST'])
def company_add():
    try:
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
@app.route("/api_v0/company/<id>", methods=["PUT"])
def company_verify_update(id):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiCompany or not role.CanVerifyCompany or not role.CanActiveCompany:
        return forbidden()
    company = Company.Company.query.filter_by(ID_COMPANY=id).first()
    # Check if exists
    if company is None:
        return not_found()
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
                        company.Verify = True
                    elif data["verify"] == 'False':
                        company.Verify = False
                if key_in_request_form('active'):
                    if data["active"] == 'True':
                        company.Active = True
                    elif data["active"] == 'False':
                        company.Active = False
                db.session.commit()
                msg = {"company_upd": company.to_json()}
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
    data_list = [job_Category.to_json() for job_Category in Job_Category.Job_Category.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_category_list": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/job_category/<id>', methods=['GET'])
def job_category_by_id(id: int):
    job_category = Job_Category.Job_Category.query.filter_by(ID_JOB_CATEGORY=id).first()
    if job_category is None:
        return not_found()
    data_list = job_category.to_json()
    msg = {"job_category": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/job_category', methods=['POST'])
def job_category_add():
    try:
        role, _ = user_privileges()
        if type(role) is Response:
            return role
        # Now we can ask for the requirement set
        if not role.CanSeeApiJobCategory:
            return forbidden()
        data = request.form
        if data is None or (2 > len(data) > 2):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data len()]')
        if not key_in_request_form('name'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data <name>')
        if not key_in_request_form('description'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data <description>]')

        job_category = Job_Category.Job_Category(Name=data['name'],
                                                 Description=data['description'])

        db.session.add(job_category)
        db.session.commit()
        msg = {'job_category_add': job_category.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {'job_category_add': ERROR_500_DEFAULT_MSG}
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
    msg = {"job_demand_category_list": list}
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
    job_demand_category = Job_Demand_Category.Job_Demand_Category.query.filter_by(Id_Job_Demand=id).first()
    if job_demand_category is None:
        return not_found()
    data_list = job_demand_category.to_json()
    msg = {"job_demand_category": data_list}  # there can be job_demand_categories with the same id_job_demand
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
    msg = {"job_demand_language_list": data_list}
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
    job_demand_language = Job_Demand_Language.Job_Demand_Language.query.filter_by(Id_Job_Demand=id).first()
    if job_demand_language is None:
        return not_found()
    data_list = job_demand_language.to_json()
    msg = {"job_demand_language": data_list}  # there can be job_demand_languages with the same id_job_demand
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
    msg = {"job_demand_qualification_list": data_list}
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
    job_demand_qualification = Job_Demand_Qualification.Job_Demand_Qualification.query.filter_by(
        Id_Job_Demand=id).first()
    if job_demand_qualification is None:
        return not_found()
    data_list = job_demand_qualification.to_json()
    msg = {"job_demand_qualification": data_list}  # there can be job_demand_qualifications with the same id_job_demand
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
    msg = {"job_demand_list": data_list}
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
    job_demand = Job_Demand.Job_Demand.query.filter_by(Id_Offer=id).first()
    if job_demand is None:
        return not_found()
    data_list = job_demand.to_json()
    msg = {"job_demand": data_list}  # there can be job_demands with the same id_offer
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
    msg = {"language_list": data_list}
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
    language = Language.Language.query.filter_by(ID_LANGUAGE=id).first()
    if language is None:
        return not_found()
    data_list = language.to_json()
    msg = {"language": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/language', methods=['POST'])
def language_add():
    # TODO check roles
    data = request.form
    if data is None or len(data) != 1:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [language_add() - data len()]')
    if not key_in_request_form('name'):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [language_add() - data <name>')

    language = Language.Language(Name=data['name'])

    try:
        db.session.add(language)
        db.session.commit()
        msg = {'language_add': language.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {'language_add': ERROR_500_DEFAULT_MSG}
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
    msg = {"member_offer_list": data_list}
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
    member_offer = Member_Offer.Member_Offer.query.filter_by(Id_Member=id).first()
    if member_offer is None:
        return not_found()
    data_list = member_offer.to_json()
    msg = {"member_offer": data_list}  # there can be member_offers with the same id_member
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
    try:
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
    member = Member.Member.query.filter_by(ID_MEMBER=id).first()
    # Check if exists
    if member is None:
        return not_found()
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
                msg = {"member_upd": member.to_json()}
                status_code = 200
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
    msg = {"offer_list": data_list}
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
    offer = Offer.Offer.query.filter_by(ID_OFFER=id).first()
    if offer is None:
        return not_found()
    data_list = offer.to_json()
    msg = {"offer": data_list}
    return Response(json.dumps(msg), status=200)


# UPDATE
@app.route("/api_v0/offer/<id>", methods=["PUT"])
def offer_verify_update(id):
    offer = Offer.Offer.query.filter_by(ID_OFFER=id).first()
    # comprobación de que se almacen un dato
    if offer is None:
        return not_found()
    if request.method == "PUT":
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
    data_list = [qualification.to_json() for qualification in Qualification.Qualification.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"qualification_list": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# READ BY
@app.route('/api_v0/qualification/<id>', methods=['GET'])
def job_qualification_by_id(id: int):
    qualification = Qualification.Qualification.query.filter_by(ID_QUALIFICATION=id).first()
    if qualification is None:
        return not_found()
    data_list = qualification.to_json()
    msg = {"qualification": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/qualification', methods=['POST'])
def qualification_add():
    try:
        role, _ = user_privileges()
        if type(role) is Response:
            return role
        # Now we can ask for the requirement set
        if not role.CanSeeApiQualification:
            return forbidden()
        data = request.form
        if data is None or (2 > len(data) > 2):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data len()]')
        if not key_in_request_form('name'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data <name>')
        if not key_in_request_form('description'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data <description>')

        qualification = Qualification.Qualification(Name=data['name'],
                                                    Description=data['description'])

        db.session.add(qualification)
        db.session.commit()
        msg = {'qualification_add': qualification.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {'qualification_add': ERROR_500_DEFAULT_MSG}
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
    msg = {"role_list": data_list}
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
    role_get = Role.Role.query.filter_by(ID_ROLE=id).first()
    if role_get is None:
        return not_found()
    data_list = role_get.to_json()
    msg = {"role": data_list}
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
    msg = {"section_list": data_list}
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
    section = Section.Section.query.filter_by(Description=category).first()
    if section is None:
        return not_found()
    data_list = section.to_json()
    msg = {"section": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/section', methods=['POST'])
def section_add():
    try:
        role, _ = user_privileges()
        if type(role) is Response:
            return role
        # Now we can ask for the requirement set
        if not role.CanMakeSection:
            return forbidden()
        data = request.form
        if data is None or len(data) != 6:
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

        db.session.add(section)
        db.session.commit()
        msg = {'section_add': section.to_json()}
        status_code = 200

    except Exception as ex:
        db.session.rollback()
        msg = {'section_add': ERROR_500_DEFAULT_MSG}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# UPDATE
@app.route("/api_v0/section/<id>", methods=["PUT"])
def section_active_update(id):
    role, _ = user_privileges()
    if type(role) is Response:
        return role
    # Now we can ask for the requirement set
    if not role.CanSeeApiSection or not role.CanActiveSection:
        return forbidden()
    section = Section.Section.query.filter_by(ID_SECTION=id).first()
    # comprobación de que se almacen un dato
    if section is None:
        return not_found()
    if request.method == "PUT":
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
    msg = {"user_list": data_list}
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
        msg = {"user": json_data}
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
        print("INSERTANDO MIEMBRO")
        data = request.form
        if data is None or len(data) < 15:
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data len()]')
        # USER VALIDATIONS
        if not key_in_request_form('passwd'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <passwd>')
        if not key_in_request_form('email'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <email>')

        user_id = uuid.uuid4()
        user = User.User(ID_USER=user_id,
                         Passwd=sec.hashed_password(data['passwd']),
                         Email=data['email'],
                         Id_Role=104)
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
        print(member)
        db.session.add(member)
        db.session.commit()
        msg = {"register_member": "SUCCESS"}
        return Response(json.dumps(msg), status=200)
    except Exception as ex:
        db.session.rollback()
        return internal_server_error(ERROR_500_DEFAULT_MSG + " :: {}".format(ex))


@app.route('/api_v0/register/offer', methods=['GET', 'POST'])
def api_register_offer_job_demand():
    if request.method == "GET":
        try:
            language_data_list = Language.Language.query.all()
            qualification_data_list = Qualification.Qualification.query.all()
            job_category_data_list = Job_Category.Job_Category.query.all()
            shift_data_list = [shift.value for shift in Shift.Shift]
            schedule_data_list = [schedule.value for schedule in Schedule.Schedule]
            working_day_data_list = [working_day.value for working_day in Working_Day.Working_Day]
            contract_type_data_list = [contract_type.value for contract_type in Contract_Type.Contract_Type]

            response = {
                'offer_data': {
                    'language_list': [language.to_json() for language in language_data_list],
                    'qualification_list': [qualification.to_json() for qualification in qualification_data_list],
                    'job_category_list': [job_category.to_json() for job_category in job_category_data_list],
                    'shift_list': shift_data_list,
                    'schedule_list': schedule_data_list,
                    'working_day_list': working_day_data_list,
                    'contract_type_list': contract_type_data_list
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
            print(data)
            if data is None or (5 > len(data) > 9):
                print("error de lenght")
                return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data len()]')
            if not key_in_request_form('workplace_name'):
                print("companyu")
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <company_name>')
            if not key_in_request_form('workplace_address'):
                print("addres")
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <address>')
            if not key_in_request_form('contact_name'):
                print("contact")
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_name>')
            if not key_in_request_form('contact_phone'):
                print("contac_phone")
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_phone>')
            if not key_in_request_form('contact_email'):
                print("contact_email")
                return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_email>')
            print("antes d los if d contacto")
            contact_name_2 = "" if not key_in_request_form('contact_name_2') else data["contact_name_2"]
            contact_phone_2 = "" if not key_in_request_form('contact_phone_2') else data["contact_phone_2"]
            contact_email_2 = "" if not key_in_request_form('contact_email_2') else data["contact_email_2"]

            offer = Offer.Offer(Workplace_Name=data['workplace_name'],
                                Workplace_Address=data['workplace_address'],
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
            vehicle = False if not key_in_request_form('vehicle') or data["vehicle"] else bool(data["vehicle"])
            geographical_mobility = False if not key_in_request_form('geographical_mobility') or data[
                "geographical_mobility"] \
                else bool(data["geographical_mobility"])
            others = "" if not key_in_request_form('others') else data['others']

            db.session.add(offer)

            inserted_offer = Offer.Offer.query.filter_by(Workplace_Name=data['workplace_name'],
                                                         Workplace_Address=data['workplace_address'],
                                                         Contact_Phone=data['contact_phone'],
                                                         Contact_Email=data['contact_email']).first()

            offer_id = inserted_offer.ID_OFFER
            print(offer_id)
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
                                               Others=others,
                                               Id_Offer=offer_id)

            db.session.add(job_demand)

            # Refrescar job_demand  para obtener el ID actualizado de la base de datos
            # db.session.refresh(job_demand)
            # job_demand_id = job_demand.ID_JOB_DEMAND
            # print(job_demand_id)
            # o con esto
            # para poder pillar el id de la job-demand que se ha insertado

            inserted_job_demand = Job_Demand.Job_Demand.query.filter_by(Vacancies=data['vacancies'],
                                                                        Schedule=data['schedule'],
                                                                        Shift=data['shift'],
                                                                        Working_Day=data['working_day']).first()

            job_demand_id = inserted_job_demand.ID_JOB_DEMAND

            job_deman_qualification = Job_Demand_Qualification.Job_Demand_Qualification(
                Id_Qualification=data['qualification'],
                # igualar al id de la  job_demand insertada
                Id_Job_Demand=job_demand_id
            )
            job_demand_category = Job_Demand_Category.Job_Demand_Category(Id_Job_Category=data['job-category'],
                                                                          Id_Job_Demand=job_demand_id
                                                                          )

            job_demand_language = Job_Demand_Language.Job_Demand_Language(Id_Language=data['language'],
                                                                          Id_Job_Demand=job_demand_id
                                                                          )

            db.session.add(job_deman_qualification)
            db.session.add(job_demand_category)
            db.session.add(job_demand_language)

            db.session.commit()
            msg = {"add_offer": "SUCCESS"}
            return Response(json.dumps(msg), status=200)
        except Exception as ex:
            db.session.rollback()
            print("Error:" + ex)
            return internal_server_error(ERROR_500_DEFAULT_MSG)


@app.route("/api_v0/register/company", methods=["POST"])
def api_register_company():
    print("JIJIJAJA")
    try:
        data = request.form
        if data is None or len(data) < 9:
            return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data len()]')
        # USER VALIDATIONS
        if not key_in_request_form('passwd'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <passwd>')
        if not key_in_request_form('email'):
            return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <email>')

        user_id = uuid.uuid4()
        user = User.User(ID_USER=user_id,
                         Passwd=sec.hashed_password(data['passwd']),
                         Email=data['email'],
                         Id_Role=103)
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

        db.session.add(company)
        db.session.commit()
        msg = {'register_company': 'SUCCESS'}
        return Response(json.dumps(msg), status=200)

    except Exception as ex:
        db.session.rollback()
        return internal_server_error(ERROR_500_DEFAULT_MSG)


@app.route("/api_v0/auth", methods=["POST"])
def decode_auth():
    if not_auth_header():
        return bad_request("Not auth")
    role, user = user_privileges()
    if type(role) is Response:
        return role
    msg = {
        'username': user,
        'role': role
    }
    return Response(json.dumps(msg), status=200)


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
    app.run(host='0.0.0.0', port=5034)

# endregion
# ==================================================================================================================== #