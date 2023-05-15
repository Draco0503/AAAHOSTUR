from flask import Flask, request, session, jsonify, render_template
from models import db
from models import Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language,\
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review
from config import config


app = Flask(__name__, template_folder='templates')


# metodo de prueba de conexion
@app.route('/prueba')
def index():
  return render_template('t-login.html', keyValue = 'holka')



@app.route('/newSection', methods=['Post'])
def create_section():
  try:
    Category = request.json['category']
    Description = request.json['description']
    Publication_Date = request.json['publication_date']
    Schedule = request.json['schedule']
    Img_Resource = request.json['Img_Resource']
    Price = request.json['Price']

    new_Section = Section(Category, Description, Publication_Date, Schedule, Img_Resource, Price)
    db.session.add(new_Section)
    db.session.commit()
    return jsonify({'mensaje':"Usuario Registrado"})
  except Exception as ex:
    return jsonify({'mensaje':"Error al registrar...."})
  

@app.route('/viewSection', methods=['GET'])
def get_all_section():
  all_section = Section.query.all()
  return jsonify(all_section)

@app.route('/section/<id>', methods=['GET'])
def get_section(id):
  section = Section.query.get(id)
  return jsonify(section)

@app.route('/viewRoles', methods=['GET'])
def get_all_roles():
  all_roles = Role.query.all()
  return jsonify(all_roles) 

# FUNCIONES PARA LOS ERRORES MAS COMUNES

# Error 404-not found
def not_Found(err):
    return "<h1>La página a la que intentas acceder no existe</h1>", 404


# Error 403-forbidden
def inadequate_Permits(err):
    return "<h1>No tienes los permisos necesarios para acceder a este contenido</h1>", 403


# Error 429-Too many request
def too_Many_Request(err):
    return "<h1>Has enviado demasiadas solicitudes en poco tiempo, Espere un poco</h1>", 429


# Error 500-Internal server error
def internal_Server_Error(err):
    return "<h1>En mantenimiento</h1>", 500


# Error 504 Gateway Timeout
def bad_Request(err):
    return "<h1>ns que poner aqui jijijajaja</h1>", 504


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
    app.register_error_handler(504, bad_Request)
    # run
    app.run(host='0.0.0.0', port=5000)