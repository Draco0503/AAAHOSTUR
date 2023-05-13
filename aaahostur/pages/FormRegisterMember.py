#FORMULARIO DE REGISTRO DE MIEMBRO(TODAS LAS SECCIONES EN UNA PAGINA/CADA SECCION EN OTRA PAGINA)

#Datos Personales
#TEXTBOX*: Nombre
#TEXTBOX*: Apellidos
#TEXTBOX*: DNI/NIE
#RADIOGROUP*: Sexo{
#Hombre, Mujer, Otro
#}
#DATE*: Fecha de nacimiento
#TEXTBOX*: Direccion
#TEXTBOX*: C.P.
#TEXTBOX*: Ciudad
#TEXTBOX*: Provincia
#CHECKBOX: Correo en otra direccion{
    #TEXTBOX*: Dir. efectos notificaciones postales
    #TEXTBOX*: C.P. efectos notificaciones postales
    #TEXTBOX*: Ciudad efectos notificaciones postales
    #TEXTBOX*: Provincia efectos notificaciones postales
#}

#TEXTBOX*: Telefono Móvil
#TEXTBOX: Telefono Fijo
#IMPUT FILE: Foto de perfil
#RADIOGROUP: Vehículo propio{
#No,Si
#}
#RADIOGROUP: Movilidad geografica{
#No,Si
#}
#CHECKBOX: Tiene Discapacidad{
    #TEXTBOX*: Grado
#}



#Datos Estudios
#COMBOBOX*: Titulo
#TEXTBOX*: Escuela
#DATE*: Fecha de finalizacion
#TEXTBOX: Promocion


#Datos Experencia Laboral
#TEXTBOX*: Puesto
#TEXTBOX*: Empresa
#TEXTBOX: Direccion
#DATE*: Fecha de inicio
#DATE: Fecha de fin

#Datos Idiomas
#TEXTBOX*: lENGUAJE
#TEXTBOX*: Nivel
#IMPUT FILE: Certificado

#Datod bancos
#TEXTBOX*: Titular de cuenta
#TEXTBOX*: nª Cuenta
#CHECKBOX* Aceptar Condiciones



