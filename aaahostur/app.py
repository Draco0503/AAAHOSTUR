from datetime import datetime as dt, timedelta

from flask import Flask, request, session, json, render_template, Response, redirect
from models import db
from models import Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language, \
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review
from config import config
from security import security

app = Flask(__name__, template_folder='templates')
conf = config['development']
sec = security.Security(conf.SEC_SALT, conf.SECRET_KEY, conf.ALGORITHM)


# metodo de prueba de conexion
@app.route('/prueba')
def index():
    return render_template('t-login.html', prueba='holka')


# -------------------------------ROLE-------------------------------#
@app.route('/api_v0/role-list', methods=['GET'])
def role_list():
    # 1º conseguir header de la peticion
    # 2º si tiene permisos hacer la logica tal cual esta definida
    #    si no tiene permisos return inadequate_Permits()
    list = [role.to_json() for role in Role.Role.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"roles": list}
    return Response(json.dumps(
        msg,
    ), status=200)


# LOGIN
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if request.headers['auth'] is not None:     # and security.validate(request.headers['auth']):
            return redirect('/', code=200)          # todo
        return render_template('t-login.html')
    elif request.method == 'POST':
        if len(request.form) != 2:
            return bad_request()
        else:
            if request.form['user-login'] is not None:
                username = request.form['user-login']
                if username == "":
                    return bad_request()
                else:
                    if request.form['user-passwd']:
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
                                        "exp": dt.now()+timedelta(minutes=30)
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
    # 1º conseguir header de la peticion
    # 2º si tiene permisos hacer la logica tal cual esta definida
    #    si no tiene permisos return inadequate_Permits()
    list = [role.to_json() for role in Role.Role.query.filter_by(ID_ROLE=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"roles": list}
    return Response(json.dumps(
        msg,
    ), status=200)


# -------------------------------MEMBER-------------------------------#


# -------------------------------OFFER-------------------------------#
@app.route('/api_v0/offer-list', methods=['GET'])
def offer_list():
    # comprobar permisos
    list = [offer.to_json() for offer in Offer.Offer.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"offers": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/offer/<id>', methods=['GET'])
def offer_by_id(id: int):
    # comprobar permisos
    list = [offer.to_json() for offer in Offer.Offer.query.filter_by(ID_OFFER=id)]
    if len(list) == 0:
        return not_Found()
    elif len(list) > 1:
        return internal_Server_Error()  # there can't be offers with the same id
    msg = {"offers": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/offer', methods=['POST'])
def offer_add():
    data = request.form
    if data is None or (5 > len(data) > 8):
        return "Fallo"
    if data['company_name'] is None:
        return "Fallo"
    if data['address'] is None:
        return "Fallo"
    if data['contact_name'] is None:
        return "Fallo"
    if data['contact_phone'] is None:
        return "Fallo"
    if data['contact_email'] is None:
        return "Fallo"
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


# -------------------------------JOB_DEMAND-------------------------------#
@app.route('/api_v0/job_demand-list', methods=['GET'])
def job_demand_list():
    # comprobar permisos
    list = [job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demands": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand/<id>', methods=['GET'])
def job_demand_by_id(id: int):
    # comprobar permisos
    list = [job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.filter_by(Id_Offer=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demands": list}  # there can be job_demands with the same id_offer
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND_QUALIFICATION-------------------------------#
@app.route('/api_v0/job_demand_qualification-list', methods=['GET'])
def job_demand_qualification_list():
    # comprobar permisos
    list = [job_demand_qualification.to_json() for job_demand_qualification in
            Job_Demand_Qualification.Job_Demand_Qualification.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demand_qualifications": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_qualification/<id>', methods=['GET'])
def job_demand_qualification_by_id(id: int):
    # comprobar permisos
    list = [job_demand_qualification.to_json() for job_demand_qualification in
            Job_Demand_Qualification.Job_Demand_Qualification.query.filter_by(Id_Job_Demand=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demand_qualifications": list}  # there can be job_demand_qualifications with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND_LANGUAGE-------------------------------#
@app.route('/api_v0/job_demand_language-list', methods=['GET'])
def job_demand_language_list():
    # comprobar permisos
    list = [job_demand_language.to_json() for job_demand_language in
            Job_Demand_Language.Job_Demand_Language.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demand_languages": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_language/<id>', methods=['GET'])
def job_demand_language_by_id(id: int):
    # comprobar permisos
    list = [job_demand_language.to_json() for job_demand_language in
            Job_Demand_Language.Job_Demand_Language.query.filter_by(Id_Job_Demand=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demand_languages": list}  # there can be job_demand_languages with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------JOB_DEMAND_CATEGORY-------------------------------#
@app.route('/api_v0/job_demand_category-list', methods=['GET'])
def job_demand_category_list():
    # comprobar permisos
    list = [job_demand_category.to_json() for job_demand_category in
            Job_Demand_Category.Job_Demand_Category.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demand_categories": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_category/<id>', methods=['GET'])
def job_demand_category_by_id(id: int):
    # comprobar permisos
    list = [job_demand_category.to_json() for job_demand_category in
            Job_Demand_Category.Job_Demand_Category.query.filter_by(Id_Job_Demand=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"job_demand_categories": list}  # there can be job_demand_categories with the same id_job_demand
    return Response(json.dumps(msg), status=200)


# -------------------------------MEMBER_OFFER-------------------------------#
@app.route('/api_v0/member_offer-list', methods=['GET'])
def member_offer_list():
    # comprobar permisos
    list = [member_offer.to_json() for member_offer in Member_Offer.Member_Offer.query.all()]
    if len(list) == 0:
        return not_Found()
    msg = {"member_offers": list}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/member_offer/<id>', methods=['GET'])
def member_offer_by_id(id: int):
    # comprobar permisos
    list = [member_offer.to_json() for member_offer in Member_Offer.Member_Offer.query.filter_by(Id_Member=id)]
    if len(list) == 0:
        return not_Found()
    msg = {"member_offers": list}  # there can be member_offers with the same id_member
    return Response(json.dumps(msg), status=200)


# FUNCIONES PARA LOS ERRORES MAS COMUNES


# Error 404-not found
def not_Found():
    return "<h1>La página a la que intentas acceder no existe</h1>", 404


# Error 403-forbidden
def inadequate_Permits():
    return "<h1>No tienes los permisos necesarios para acceder a este contenido</h1>", 403


# Error 429-Too many request
def too_Many_Request():
    return "<h1>Has enviado demasiadas solicitudes en poco tiempo, Espere un poco</h1>", 429


# Error 500-Internal server error
def internal_Server_Error():
    return "<h1>En mantenimiento</h1>", 500


# Error 504 Gateway Timeout
def gateway_TimeOut():
    return "<h1>Timeout</h1>", 504


def bad_request():
    return "<h1>Bad request</h1>", 400


# inicio del main
if __name__ == '__main__':
    # acceso al diccionario con las credenciales para acceder a la base de datos
    app.config.from_object(conf)
    # Conexion con la base de datos
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # para manegar los errores
    app.register_error_handler(404, not_Found)
    app.register_error_handler(403, inadequate_Permits)
    app.register_error_handler(429, too_Many_Request)
    app.register_error_handler(500, internal_Server_Error)
    app.register_error_handler(504, gateway_TimeOut)
    # run
    app.run(host='0.0.0.0', port=5000)
