from flask import Flask, request, session, json, render_template, Response
from models import db
from models import Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language, \
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review
from config import config

app = Flask(__name__, template_folder='templates')


# metodo de prueba de conexion
@app.route('/prueba')
def index():
    return render_template('t-login.html', keyValue='holka')


# --------------------ROLE----------------------#
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


# TODO: Falta cifrar la cabezera de la peticion
# def authorize_admin(req: request) -> bool:
#     return req.headers['auth'] is not None and req.headers['auth'] == 'ADMIN'
#
#
# def authorize_member(req: request) -> bool:
#     return req.headers['auth'] is not None and req.headers['auth'] == 'MEMBER'


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


# --------------------MEMBER--------------------#


# --------------------OFFER---------------------#
@app.route('/api_v0/offer-list', methods=['GET'])
def offer_list():
    msg = {"ofertas": [offer.to_json() for offer in Offer.Offer.query.all()]}
    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/offer/<id>', methods=['GET'])
def offer_by_id(id: int):
    # COMPROBACIONES DE SEGURIDAD ...
    list = [offer.to_json() for offer in Offer.Offer.query.filter_by(ID_OFFER=id)]
    if len(list) == 0:
        return not_Found()
    elif len(list) > 1:
        return internal_Server_Error()
    msg = {"ofertas": list}
    return Response(json.dumps(msg), status=200)


# --------------------JOB DEMAND----------------#
@app.route('/api_v0/job_demand-list', methods=['GET'])
def job_demand_list(id_off):
    if (id_off != None) and (id_off != ''):
        msg = {'demanda_de_empleo': [
            job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.filter_by(Id_Offer=id_off).all()]}
    else:
        msg = {'demanda_de_empleo': [
            job_demand.to_json() for job_demand in Job_Demand.Job_Demand.query.all()]}

    return Response(json.dumps(msg), status=200)


# -------------INTERMEDIATE TABLES--------------#
@app.route('/api_v0/member_offer-list', methods=['GET'])
def member_offer_list(id_mem):
    if (id_mem != None) and (id_mem != ''):
        msg = {'miembro_oferta': [
            member_offer.to_json() for member_offer in
            Member_Offer.Member_Offer.query.filter_by(Id_Member=id_mem).all()]}
    else:
        msg = {'miembro_oferta': [
            member_offer.to_json() for member_offer in Member_Offer.Member_Offer.query.all()]}

    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_language-list', methods=['GET'])
def job_demand_language_list(id_jd):
    if (id_jd != None) and (id_jd != ''):
        msg = {'demanda_de_empleo_idioma': [
            job_demand_language.to_json() for job_demand_language in
            Job_Demand_Language.Job_Demand_Language.query.filter_by(Id_Job_Demand=id_jd).all()]}
    else:
        msg = {'demanda_de_empleo_idioma': [
            job_demand_language.to_json() for job_demand_language in
            Job_Demand_Language.Job_Demand_Language.query.all()]}

    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_qualification-list', methods=['GET'])
def job_demand_qualification_list(id_jd):
    if (id_jd != None) and (id_jd != ''):
        msg = {'demanda_de_empleo_cualificacion': [
            job_demand_qualification.to_json() for job_demand_qualification in
            Job_Demand_Qualification.Job_Demand_Qualification.query.filter_by(Id_Job_Demand=id_jd).all()]}
    else:
        msg = {'demanda_de_empleo_cualificacion': [
            job_demand_qualification.to_json() for job_demand_qualification in
            Job_Demand_Qualification.Job_Demand_Qualification.query.all()]}

    return Response(json.dumps(msg), status=200)


@app.route('/api_v0/job_demand_category-list', methods=['GET'])
def job_demand_category_list(id_jd):
    if (id_jd != None) and (id_jd != ''):
        msg = {'demanda_de_empleo_categoria': [
            job_demand_category.to_json() for job_demand_category in
            Job_Demand_Category.Job_Demand_Category.query.filter_by(Id_Job_Demand=id_jd).all()]}
    else:
        msg = {'demanda_de_empleo_categoria': [
            job_demand_category.to_json() for job_demand_category in
            Job_Demand_Category.Job_Demand_Category.query.all()]}

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


# inicio del main
if __name__ == '__main__':
    # acceso al diccionario con las credenciales para acceder a la base de datos
    app.config.from_object(config['development'])
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
