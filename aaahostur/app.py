from datetime import datetime as dt, timedelta
from flask import Flask, request, session, json, render_template, Response, redirect, url_for
from models import db
from models import Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language, \
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review
from config import config
from security import security

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
def check_auth() -> bool:
    """True if 'auth' header not found or empty"""
    return 'auth' not in request.headers or request.headers['auth'] is None


def get_privileges_from_token(token: str) -> Role.Role or None:
    """Gets the role from the validated token"""
    payload = sec.decode_jwt(token)
    if payload is None or len(payload) != 4:
        return None
    else:
        return Role.Role.query.filter_by(ID_ROLE=int(payload.get('user-role')))


# endregion
# ==================================================================================================================== #


# region testing
# metodo de prueba de conexion
@app.route('/prueba')
def index():
    return render_template('t-create-language.html', prueba='holka')


# endregion
# ==================================================================================================================== #
# =========================================================  API  ==================================================== #
# region API
# -------------------------------ACADEMIC_PROFILE-------------------------------#
# INSERT
@app.route('/api_v0/academic_profile', methods=['POST'])
def academic_profile_add():
    data = request.form
    # NOT NULL fields
    if data is None or (2 > len(data) > 3):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data len()]')
    if data['school'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <school>]')
    if data['graduation_date'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <graduation_date>]')

    # NULL fields
    promotion = '' if data['promotion'] is None else data['promotion']

    academic_profile = Academic_Profile.Academic_Profile(School=data['school'],
                                                         Graduation_Date=data['graduation_date'],
                                                         Promotion=promotion)
    try:
        # TODO check role
        Academic_Profile.Academic_Profile.query.add(academic_profile)
        Academic_Profile.Academic_Profile.query.commit()
        msg = {'NEW academic_profile ADDED': academic_profile.to_json()}
        status_code = 200

    except Exception as ex:
        Academic_Profile.Academic_Profile.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: academic_profile.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------COMPANY_ACCOUNT-------------------------------#
# TODO not implemented in v.0

# -------------------------------COMPANY-------------------------------#
# READ ALL
@app.route('/api_v0/company-list', methods=['GET'])
def company_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanSeeApiCompany:
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
    if data['type'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <type>')
    if data['cif'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <cif>]')
    if data['contact_name'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_name>]')
    if data['contact_phone'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_phone>]')
    if data['contact_email'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [academic_profile_add() - data <contact_email>]')

    address = "" if data['address'] is None else data['address']
    cp = "" if data['cp'] is None else data['cp']
    city = "" if data['city'] is None else data['city']
    province = "" if data['province'] is None else data['province']
    description = "" if data['description'] is None else data['description']

    company = Company.Company(Type=data['type'],
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
        # TODO check role
        Company.Company.query.add(company)
        Company.Company.query.commit()
        msg = {'NEW company ADDED': company.to_json()}
        status_code = 200

    except Exception as ex:
        Company.Company.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: company.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------JOB_CATEGORY--------------------------------------#
# READ ALL
@app.route('/api_v0/job_category-list', methods=['GET'])
def job_category_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if data['name'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data <name>')
    if data['description'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_category_add() - data <description>]')

    job_category = Job_Category.Job_Category(Name=data['name'],
                                             Description=data['description'])

    try:
        # TODO check role
        Job_Category.Job_Category.query.add(job_category)
        Job_Category.Job_Category.query.commit()
        msg = {'NEW job_category ADDED': job_category.to_json()}
        status_code = 200

    except Exception as ex:
        Job_Category.Job_Category.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: job_category.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------JOB_DEMAND_CATEGORY-------------------------------#
# READ ALL
@app.route('/api_v0/job_demand_category-list', methods=['GET'])
def job_demand_category_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.filter_by(Id_Offer=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"job_demands": data_list}  # there can be job_demands with the same id_offer
    return Response(json.dumps(msg), status=200)


# INSERT
@app.route('/api_v0/job_demand', methods=['POST'])
def job_demand_add():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanMakeOffer:
        return forbidden()
    data = request.form
    if data is None or (5 > len(data) > 12):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data len()]')
    if data['vacancies'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <vacancies>')
    if data['schedule'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <schedule>')
    if data['working_day'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <working_day>')
    if data['shift'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [job_demand_add() - data <shift>')

    monthly_salary = "" if data['monthly_salary'] is None else data['monthly_salary']
    contract_type = "" if data['contract_type'] is None else data['contract_type']
    holidays = "" if data['holidays'] is None else data['holidays']
    experience = "" if data['experience'] is None else data['experience']
    vehicle = False if data['vehicle'] is None else data['vehicle']
    geographical_mobility = False if data['geographical_mobility'] is None else data['geographical_mobility']
    disability_grade = 0 if data['disability_grade'] is None else data['disability_grade']
    others = "" if data['others'] is None else data['others']

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
                                       Disability_Grade=disability_grade,
                                       Others=others)

    try:
        Job_Demand.Job_Demand.query.add(job_demand)
        Job_Demand.Job_Demand.query.commit()
        msg = {'NEW job_demand ADDED': job_demand.to_json()}
        status_code = 200

    except Exception as ex:
        Job_Demand.Job_Demand.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: job_demand.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------LANGUAGE-------------------------------#
# READ ALL
@app.route('/api_v0/language-list', methods=['GET'])
def language_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if data['name'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [language_add() - data <name>')
    if data['lvl'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [language_add() - data <lvl>')
    if data['certificate'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [language_add() - data <certificate>')

    language = Language.Language(Name=data['name'],
                                 Lvl=data['lvl'],
                                 Certificate=data['certificate'])

    try:
        Language.Language.query.add(language)
        Language.Language.query.commit()
        msg = {'NEW language ADDED': language.to_json()}
        status_code = 200

    except Exception as ex:
        Language.Language.query.rollback()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanSeeApiMember:
        return forbidden()
    data_list = [member.to_json() for member in Member.Member.query.all()]
    if len(data_list) == 0:
        return not_found()
    msg = {"member_list": data_list}
    return Response(json.dumps(msg), status=200)


# READ BY
@app.route('/api_v0/member/<id>', methods=['GET'])
def member_by_id(id: int):
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanSeeApiMember:
        return forbidden()
    data_list = [member.to_json() for member in Member.Member.query.filter_by(ID_MEMBER=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"member_list": data_list}
    return Response(json.dumps(msg), status=200)


# INSERT
@app.route('/api_v0/member', methods=['POST'])
def member_add():
    # TODO check roles
    data = request.form
    if data is None or (18 > len(data) > 21):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data len()]')
    if data['name'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <name>')
    if data['surname'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <surname>')
    if data['dni'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <dni>')
    if data['address'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <address>')
    if data['cp'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <cp>')
    if data['city'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <city>')
    if data['province'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <province>')
    if data['gender'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <gender>')
    if data['mobile'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <mobile>')
    if data['profile_picture'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <profile_picture>')
    if data['birth_date'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <birth_date>')
    if data['join_date'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <join_date>')
    if data['cancelation_date'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [member_add() - data <cancelation_date>')

    pna_address = ""
    pna_cp = ""
    pna_city = ""
    pna_province = ""

    if data['pna_data'] is not None:
        if data['pna_address'] is None:
            return "[ERROR] - member_add() - insert: pna_address"
        if data['pna_cp'] is None:
            return "[ERROR] - member_add() - insert: pna_cp"
        if data['pna_city'] is None:
            return "[ERROR] - member_add() - insert: pna_city"
        if data['pna_province'] is None:
            return "[ERROR] - member_add() - insert: pna_province"
        pna_address = data['pna_address']
        pna_cp = data['pna_cp']
        pna_city = data['pna_city']
        pna_province = data['pna_province']

    land_line = "" if data['land_line'] is None else data["land_line"]
    vehicle = "" if data['vehicle'] is None else data["vehicle"]
    geographical_mobility = "" if data['geographical_mobility'] is None else data["geographical_mobility"]
    disability_grade = "" if data['disability_grade'] is None else data["disability_grade"]

    member = Member.Member(Name=data['name'],
                           Surname=data['surname'],
                           DNI=data['dni'],
                           Address=data['adderss'],
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
                           Profile_Picture=data['profile_picture'],
                           Birth_Date=data['birth_date'],
                           Vehicle=vehicle,
                           Geographical_Mobility=geographical_mobility,
                           Disability_Grade=disability_grade,
                           Join_Date=data['join_date'],
                           Cancelation_Date=data['cancelation_date'])

    try:
        Member.Member.query.add(member)
        Member.Member.query.commit()
        msg = {'NEW member ADDED': member.to_json()}
        status_code = 200

    except Exception as ex:
        Member.Member.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: member.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------OFFER-------------------------------#
# READ ALL
@app.route('/api_v0/offer-list', methods=['GET'])
def offer_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanSeeApiOffer:
        return forbidden()
    data_list = [offer.to_json() for offer in Offer.Offer.query.filter_by(ID_OFFER=id)]
    if len(data_list) == 0:
        return not_found()
    elif len(data_list) > 1:
        return internal_server_error()  # there can't be offers with the same id
    msg = {"offers": data_list}
    return Response(json.dumps(msg), status=200)


# INSERT
@app.route('/api_v0/offer', methods=['POST'])
def offer_add():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanMakeOffer:
        return forbidden()
    data = request.form
    if data is None or (5 > len(data) > 8):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data len()]')
    if data['company_name'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <company_name>')
    if data['address'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <address>')
    if data['contact_name'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_name>')
    if data['contact_phone'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_phone>')
    if data['contact_email'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [offer_add() - data <contact_email>')

    contact_name_2 = "" if data['contact_name_2'] is None else data["contact_name_2"]
    contact_phone_2 = "" if data['contact_phone_2'] is None else data["contact_phone_2"]
    contact_email_2 = "" if data['contact_email_2'] is None else data["contact_email_2"]

    offer = Offer.Offer(Company_Name=data['company_name'],
                        Address=data['address'],
                        Contact_Name=data['contact_name'],
                        Contact_Phone=data['contact_phone'],
                        Contact_Email=data['contact_email'],
                        Contact_Name_2=contact_name_2,
                        Contact_Phone_2=contact_phone_2,
                        Contact_Email_2=contact_email_2)

    try:
        Offer.Offer.query.add(offer)
        Offer.Offer.query.commit()
        msg = {'NEW offer ADDED': offer.to_json()}
        status_code = 200

    except Exception as ex:
        Offer.Offer.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: offer.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------PROFESSIONAL_PROFILE-------------------------------#
# TODO not implemented in v.0


# -------------------------------QUALIFICATION-------------------------------#
# READ ALL
@app.route('/api_v0/qualification-list', methods=['GET'])
def qualification_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if data['name'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data <name>')
    if data['description'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [qualification_add() - data <description>')

    qualification = Qualification.Qualification(Name=data['name'],
                                                Description=data['description'])

    try:
        Qualification.Qualification.query.add(qualification)
        Qualification.Qualification.query.commit()
        msg = {'NEW qualification ADDED': qualification.to_json()}
        status_code = 200

    except Exception as ex:
        Qualification.Qualification.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: qualification.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# -------------------------------REVIEW-------------------------------#
# TODO not implemented in v.0


# -------------------------------ROLE-------------------------------#
# READ ALL
@app.route('/api_v0/role-list', methods=['GET'])
def role_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanMakeSection:
        return forbidden()
    data = request.form
    if data is None or (6 > len(data) > 6):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data len()]')
    if data['category'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <category>')
    if data['description'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <description>')
    if data['publication_date'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <publication_date>')
    if data['schedule'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <schedule>')
    if data['img_resource'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <img_resource>')
    if data['price'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [section_add() - data <price>')

    section = Section.Section(Category=data['category'],
                              Description=data['description'],
                              Publication_Date=data['publication_date'],
                              Schedule=data['schedule'],
                              Img_Resource=data['img_resource'],
                              Price=data['price'])

    try:
        Section.Section.query.add(section)
        Section.Section.query.commit()
        msg = {'NEW section ADDED': section.to_json()}
        status_code = 200

    except Exception as ex:
        Section.Section.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: section.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# UPDATE
@app.route('/api_v0/section_update/<id>', methods=['GET', 'POST'])
def section_update(id):
    section = Section.Section.query.filter_by(ID_SECTION=id)
    if len(section) == 0:
        return not_found()
    try:
        section.Active = True
        Section.Section.query.commit()
        msg = {'section modificada': section.to_json()}
        status = 200
    except:
         Section.Section.query.rollback()
         msg = {ERROR_500_DEFAULT_MSG: section.to_json()}
         status = 500
    return Response(json.dumps(
         msg,
        ), status=200)

# -------------------------------USER-------------------------------#
# READ ALL
@app.route('/api_v0/user-list', methods=['GET'])
def user_list():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
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
@app.route('/api_v0/user/<id>', methods=['GET'])
def user_by_id(id: int):
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanSeeApiUser:
        return forbidden()
    data_list = [user.to_json() for user in User.User.query.filter_by(ID_USER=id)]
    if len(data_list) == 0:
        return not_found()
    msg = {"user": data_list}
    return Response(json.dumps(
        msg,
    ), status=200)


# INSERT
@app.route('/api_v0/user', methods=['POST'])
def user_add():
    if check_auth():
        return redirect(url_for(".login", _method='GET'))
    role = get_privileges_from_token(request.headers['auth'])
    if role is None:
        return bad_request()
    if not role.CanMakeOffer:
        return forbidden()
    data = request.form
    if data is None or (2 > len(data) > 2):
        return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data len()]')
    if data['passwd'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <passwd>')
    if data['email'] is None:
        return bad_request(ERROR_400_DEFAULT_MSG + ' [user_add() - data <email>')

    user = User.User(Passwd=data['passwd'],
                     Email=data['email'])

    try:
        User.User.query.add(user)
        User.User.query.commit()
        msg = {'NEW user ADDED': user.to_json()}
        status_code = 200

    except Exception as ex:
        User.User.query.rollback()
        msg = {ERROR_500_DEFAULT_MSG: user.to_json()}
        status_code = 500

    return Response(json.dumps(msg), status=status_code)


# endregion
# ==================================================================================================================== #
# =======================================================   PAGES   ================================================== #
# region PAGES
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
                    return bad_request("Username cannot be empty")  # Usuario vacio
                else:
                    if request.form['user-passwd'] is not None:
                        passwd = request.form['user-passwd']
                        if passwd == "":
                            return bad_request("Password cannot be empty")
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
        return {}  # empty response


# endregion
# ==================================================================================================================== #
# ==================================== FUNCIONES PARA LOS ERRORES MAS COMUNES ======================================== #
# region RESPONSES DE ERROR
# Error 400-Bad Request
def bad_request(msg: str = ERROR_400_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "message": "{}".format(msg)
    }), status=400)


# Error 403-forbidden
def forbidden(msg: str = ERROR_403_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Forbidden",
        "message": "{}".format(msg)
    }), status=403)


# Error 404-not found
def not_found(msg: str = ERROR_404_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Not found",
        "message": "{}".format(msg)
    }), status=404)


# Error 429-Too many request
def too_many_request(msg: str = ERROR_429_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Too many request",
        "message": "{}".format(msg)
    }), status=429)


# Error 500-Internal server error
def internal_server_error(msg: str = ERROR_500_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "message": "{}".format(msg)
    }), status=500)


# Error 504 Gateway Timeout
def gateway_timeout(msg: str = ERROR_504_DEFAULT_MSG) -> Response:
    return Response(json.dumps({
        "title": "Gateway Timeout",
        "message": "{}".format(msg)
    }), status=504)


# endregion
# ==================================================================================================================== #
# ========================================================= MAIN ===================================================== #
# region MAIN
if __name__ == '__main__':
    # acceso al diccionario con las credenciales para acceder a la base de datos
    app.config.from_object(conf)
    # Conexion con la base de datos
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # para manegar los errores
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(429, too_many_request)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(504, gateway_timeout)
    # run
    app.run(host='0.0.0.0', port=5000)

# endregion
# ==================================================================================================================== #
