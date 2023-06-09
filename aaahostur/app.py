import uuid
from base64 import b64encode
from datetime import datetime as dt
from user_agents import parse
import requests
from flask import Flask, request, json, render_template, Response, redirect, url_for, make_response
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

# region testing
# method for testing purposes
@app.route('/prueba')
def prueba():
    return render_template('addoffer.html', prueba='holka')


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

    auth = requests.post("http://localhost:5034/api_v0/auth", cookies=request.cookies)

    user_info = requests.get("http://localhost:5000/api_v0/user/{}".format(user_token), cookies=request.cookies)

    if user_info.status_code == 200:
        json_data = user_info.json()['user']
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
            if role.CanMakeSection:
                context['publisher'] = True
        else:
            context = {}
        # print(context)
        return render_template("profile.html", context=context, payload=payload, profile=True)
    return render_template("profile.html")


def check_company_params() -> str:
    return ""


@app.route("/register/company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        error = "Las contraseñas no coinciden"
        data = request.form
        if data["user-pwd"] == data["user-pwd-2"]:
            error = check_company_params()
            if error != "":
                if navigator_user_agent():
                    return render_template("signincompany.html", error=error)
                return bad_request(error)
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
            print(user_company_data_form)
            # Check if the user has been created
            user_created = requests.post('http://localhost:5000/api_v0/register/company', data=user_company_data_form,
                                         cookies=request.cookies)
            print(user_created)
            # Check if the user has been created
            if user_created.status_code == 200:
                print("OK")
                return redirect(url_for("login"))  # TODO       
            else:
                if 'user_add' in user_created.json():
                    error = user_created.json()["user_add"]
                elif 'message' in user_created.json():
                    error = user_created.json()["message"]
                else:
                    error = 'DEFAULT ERROR MESSAGE'

        return render_template("signincompany.html", error=error)
    elif request.method == "GET":
        return render_template("signincompany.html")
    else:
        return bad_request("{} method not supported".format(request.method))


# TODO
def check_offer_params() -> str:
    return ""


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
            "contact_email": data["offer-contact-email"],
            "contact_name_2": data["offer-contact-name-2"],
            "contact_phone_2": data["offer-contact-phone-2"],
            "contact_email_2": data["offer-contact-email-2"],
            "vacancies": data["job-demand-vacancies"],
            "qualification": data["qualification"],
            "monthly_salary": data["job-demand-monthly-salary"],
            "contract_type": data["job-demand-contract-type"],
            "schedule": data["rb-group-job-demand-schedule"],
            "working_day": data["rb-group-job-demand-working-day"],
            "shift": data["rb-group-job-demand-shift"],
            "holidays": data["job-demand-holidays"],
            "language": data["language"],
            "job-category": data["job-category"],
            "experience": data["job-demand-experience"],
            "vehicle": True if not key_in_request_form('rb-group-car') or data["rb-group-car"] == "y" else False,
            "geographical_mobility": True if not key_in_request_form('rb-group-mov') or data[
                "rb-group-mov"] == "y" else False,
            "others": data["job-demand-others"]
        }
        offer_created = requests.post('http://localhost:5000/api_v0/register/offer', data=offer_job_demand_data_form,
                                      cookies=request.cookies)
        # Check if the user has been created
        if offer_created.status_code == 200:
            print("OK")
            return redirect(url_for("login"))  # TODO redirect to success-offer-page
        else:
            if 'offer_add' in offer_created.json():
                error = offer_created.json()["offer_add"]
            elif 'message' in offer_created.json():
                error = offer_created.json()["message"]
            else:
                error = 'DEFAULT ERROR MESSAGE'
        return render_template("addoffer.html", error=error)
    elif request.method == "GET":
        role, _ = user_privileges()
        if type(role) is Response:
            return role
        # Now we can ask for the requirement set
        if not role.CanMakeOffer:
            return forbidden()
        offer_data_request = requests.get("http://localhost:5000/api_v0/register/offer",
                                          cookies=request.cookies)
        if offer_data_request.status_code == 200:
            return render_template("addoffer.html",
                                   language_list=offer_data_request.json()['offer_add_get']['language_list'],
                                   qualification_list=offer_data_request.json()['offer_add_get']['qualification_list'],
                                   job_category_list=offer_data_request.json()['offer_add_get']['job_category_list'],
                                   shift_list=offer_data_request.json()['offer_add_get']['shift_list'],
                                   schedule_list=offer_data_request.json()['offer_add_get']['schedule_list'],
                                   working_day_list=offer_data_request.json()['offer_add_get']['working_day_list'],
                                   contract_type_list=offer_data_request.json()['offer_add_get']['contract_type_list'])

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
            json_data = company_get_request.json()['user']
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
    # app.config.from_object(conf)
    # # DB Connection (if db exists and not(table models) it will create the tables without data)
    # db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    # HTTP Common errors handlers
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(429, too_many_request)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(504, gateway_timeout)
    # run
    app.run(host='0.0.0.0', port=80)

# endregion
# ==================================================================================================================== #
