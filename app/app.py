from flask import Flask,render_template,redirect,request,url_for,flash
import mysql.connector

#creamos una instacia de la clase flask
app = Flask(__name__)
app.secret_key = '12345678'

#definir ruta
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2024"
)

cursor = db.cursor()

#definir ruta
@app.route('/')
def lista():#item
    cursor= db.cursor()
    cursor.execute('select * FROM personas')
    usuario = cursor.fetchall()
 
    return render_template('index.html',personas=usuario)#esta renderizando el index.html

@app.route('/Registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        Nombres = request.form.get('NOMBRE')
        apellidos = request.form.get('APELLIDO')
        correos = request.form.get('CORREO')
        telefonos = request.form.get('TELEFONO')
        direcciones = request.form.get('DIRECION')
        usuarios = request.form.get('USUARIO')
        contrasenas = request.form.get('CONTRASENA')

        # Verificar si el usuario ya existe en la base de datos
        cursor.execute("SELECT usuarioper FROM personas WHERE usuarioper = %s", (usuarios,))
        existing_user = cursor.fetchone()

        if existing_user is not None:
            flash('El usuario ya está registrado. Por favor, elija otro nombre de usuario.', 'error')
            return redirect(url_for('registrar_usuario'))

        # Insertar datos en la tabla personas
        cursor.execute("INSERT INTO personas(nombreper, apellidoper, emailper, dirper, telper, usuarioper, contraper) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (Nombres, apellidos, correos, direcciones, telefonos, usuarios,contrasenas))
        db.commit()

        return redirect(url_for('registrar_usuario'))

    return render_template('Registrar.html')

   


@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar_usuario(id):
    cursor =db.cursor()
    if request.method  == 'POST':
       nombre = request.form.get('nombreper')
       apellido = request.form.get('apellidoper')
       email = request.form.get('emailper')
       dire = request.form.get('dirper')
       tel = request.form.get('telper')
       usuarios = request.form.get('usuarioper')
       password = request.form.get('passwordper')

        #sentencia para actualizar los datos en la base de datos
       sql = "UPDATE personas SET nombreper=%s, apellidoper=%s, emailper=%s, dirper=%s, telper=%s, usuarioper=%s, contraper=%s WHERE id_perso=%s"
       cursor.execute(sql, (nombre,apellido,email,dire,tel,usuarios,password,id))
       db.commit()
       return redirect(url_for('lista'))#redirecciona a una url
    else:
        cursor=db.cursor()
        #obtener los datos de la persona que se va a editar
        cursor.execute('SELECT * FROM personas WHERE id_perso = %s', (id,))
        data = cursor.fetchall()
    if data:
        return render_template('editar.html',personas=data[0])
    else:
        flash('usuario no encontrado','error')
        return redirect(url_for('lista'))

       
@app.route('/eliminar/<int:id>',methods=['GET','POST'])
def eliminar_usuario(id):
    cursor =db.cursor()
    if request.method =='POST':
       cursor.execute( 'DELETE FROM personas WHERE id_perso =%s',(id,)  ) 
       db.commit()   
       return redirect (url_for('lista'))
    else:
        cursor.execute('SELECT* FROM personas WHERE id_perso =%s',(id,) )
        data = cursor.fetchall()
        if data:
           return render_template('eliminar.html',personas=data)


#para ejecutar instalacion 


#para ejecutar la aplicacion 
if __name__== '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True,port=5005)
    