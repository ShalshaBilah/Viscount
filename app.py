from flask import Flask
from markupsafe import escape
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask import jsonify
import base64

from argon2 import PasswordHasher

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


class Base(DeclarativeBase):
    pass

app = Flask(__name__)
db = SQLAlchemy(model_class=Base) 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:salsa@127.0.0.1/myflask"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

app.config["JWT_SECRET_KEY"] = "What is Lorem Ipsum?"  # Setup the Flask-JWT-Extended extension
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)  # Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    password : Mapped [str]

# class ApiKey(db.Model): #User class inherit Model class
#     api_key: Mapped[str] = mapped_column(primary_key=True)

# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id

# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     email = jwt_data["sub"]
#     return User.query.filter_by(email=email).one_or_none()


@jwt.user_lookup_loader
# Ini adalah dekorator yang menunjukkan bahwa fungsi di bawahnya adalah fungsi untuk memuat pengguna (user) berdasarkan data JWT.
def user_lookup_callback(_jwt_header, jwt_data):
# Parameter _jwt_header mungkin berisi informasi tentang header JWT tetapi tidak digunakan dalam fungsi ini. 
#Parameter jwt_data adalah data yang diterima dari JWT, yang kemungkinan berisi informasi tentang subjek token.
    identity = jwt_data["sub"]
    # ni mengambil informasi identitas (subyek) dari data JWT. Dalam JWT, "sub" biasanya berisi identitas unik dari pengguna atau entitas yang tokennya mewakili.
    return User.query.filter_by(id=identity).one_or_none()
    # Fungsi filter_by mengambil entitas dari kelas User yang memiliki atribut id yang sama dengan identity yang ditemukan dari JWT. 
    # Kemudian one_or_none() mengembalikan satu objek pengguna jika ada yang cocok dengan identitas, atau None jika tidak ada yang cocok.

@app.route("/user", methods=['GET','POST','PUT','DELETE'])
def user():
    if request.method == "POST":
    #  Ini memeriksa apakah metode HTTP yang digunakan adalah POST.
        dataDict = request.get_json()
        # Ini mengambil data JSON yang dikirim dengan permintaan POST.
        email = dataDict["email"]
        name = dataDict["name"]
        user = User (
        # Membuat objek User baru dengan atribut email dan name yang diambil dari data JSON.
            email = email,
            name = name,
        )
        db.session.add(user)
        # Ini menambahkan objek user ke dalam sesi database.
        db.session.commit()
        #  Ini melakukan commit perubahan ke database, menyimpan objek user ke dalam tabel user.
        return {
            "message": f"email: {email}, name: {name}"
        }, 200

    elif request.method == "PUT":
        dataDict = request.get_json()
        #  Ini mengambil data JSON yang dikirim dengan permintaan PUT.
        id = dataDict["id"]
        email = dataDict["email"]
        name = dataDict["name"]
        # Mengambil nilai ID, email, dan name dari data JSON

        if not id:
            return {
                "message": "ID required"
            },400
        # Memeriksa apakah ID ada dalam data yang diterima. Jika tidak ada, respons akan mengembalikan pesan "ID required" dengan kode status HTTP 400 (Bad Request)
       
        row = db.session.execute(
            db.select(User)
            .filter_by(id=id) # Order by ID
        ).scalar_one() # Return a list of row

        if "email"  in dataDict:
            row.email = dataDict["email"]

        if "name" in dataDict :
            row.name = dataDict["name"]
        # Mengambil satu baris (record) dari tabel User yang memiliki ID yang sesuai dengan yang diterima dalam data JSON. 
        # Kemudian, atribut email dan name dari baris tersebut diperbarui sesuai dengan nilai yang diterima dalam data JSON. Perubahan tersebut di-commit ke dalam database.
        db.session.commit()
        # Ini melakukan commit perubahan ke database, menyimpan perubahan yang dilakukan pada objek row.
        return{
             "message" : "Successful!"
         },200
    
    elif request.method == "DELETE":
        dataDict = request.get_json()

        id = dataDict["id"]
        # Mengambil nilai ID dari data JSON yang diterima.

        if not id:
            return {
                "message": "ID required"
            },400
       # Memeriksa apakah ID ada dalam data yang diterima. Jika tidak ada, respons akan mengembalikan pesan "ID required" dengan kode status HTTP 400 (Bad Request).
        row = db.session.execute(
            db.select(User)
            .filter_by(id=id) # Order by ID
        ).scalar_one() # Return a list of row
        db.session.delete(row)
        db.session.commit()
        #  Ini mengambil satu baris (record) dari tabel User yang memiliki ID yang sesuai dengan yang diterima dalam data JSON. 
        # Baris tersebut kemudian dihapus dari database menggunakan db.session.delete(row) dan perubahan di-commit ke dalam database.
        return{
             "message" : "Successful!"
         },200

    else: # GET
        rows = db.session.execute(
            db.select(User)
            .order_by(User.id) # Order by ID
        ).scalars() # Return a list
    #  Ini mengambil semua baris (records) dari tabel User dari database, dan setiap baris kemudian diubah menjadi bentuk yang dapat di-serialize menjadi JSON.
        
        users = []
        # Inisialisasi list untuk menyimpan data pengguna.
        for row in rows :
            users.append({
                "id" : row.id,
                "email" : row.email,
                "name" : row.name
            })
        # Looping melalui setiap baris yang diambil dari database, dan menambahkan informasi pengguna ke dalam list users.
        return users,200
    
@app.post('/signup')
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    # re_password = request.form.get("re_password")
    
    # created_at= datetime.now()
    # updated_at= datetime.now()
    
    # Memeriksa apakah password sama dengan re_password
    # if password != re_password:
    #     return {
    #         "message" : "Password tidak sama!"
    #     }, 400
    
    # Memeriksa apakah email terisi
    if not email:
        return {
            "message" : "Email harus diisi"
        }, 400
        
    # Mengecek apakah email sudah terdaftar sebelumnya
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {
            "error" : True,
            "message": "Email sudah terdaftar. Silakan gunakan email lain."
        }, 400
        
    # Menghash password menggunakan Argon2
    hashed_password = PasswordHasher().hash(password)
    
    # Encode password menggunakan Base64
    # encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    
    # Membuat objek User dengan menggunakan properti yang sesuai
    # Pastikan properti ini sesuai dengan definisi model
    new_user = User(
        email=email,
        name=name,
        password=hashed_password,  
        # created_at=created_at,
        # updated_at=updated_at
    )
    db.session.add(new_user)
    db.session.commit()
    
    # res = {
    #     "id": new_user.id,
    #     "name" : name,
    #     "email" : email,
    # }
    return {
        # "data" : res,
        "message" : "Sukses melakukan registrasi",
        "error": False
        },201

@app.post("/signin")
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one()

    if not user or not PasswordHasher().verify(user.password, password):
    # Jika email atau password tidak sesuai atau pengguna tidak ditemukan, maka akan dikembalikan pesan "Wrong password or email" dengan kode status HTTP 400 (Bad Request).
        return {
        "message" : "Wrong password or email" 
    },400
    
    # if not user:
    #     return {
    #         "message": "Email dan kata sandi diperlukan!"
    #     }, 400
    
    # try:
    #     PasswordHasher().verify(user.password, password)
    # except:
    #     return jsonify (
    #         {
    #             "message" : "Email or password is incorrect"
    #         }
    #     ),400
    
    # Autentikasi berhasil, generate token akses JWT
    access_token = create_access_token(identity=user.id)
    
    return {
        "token_access": access_token
        },200

# @app.post("/signup")
# def signup():
#     dataDict = request.get_json()
#     # Ini mengambil data JSON yang dikirim dengan permintaan POST.

#     name = dataDict["name"]
#     email = dataDict["email"]
#     password = dataDict["password"]
#     re_password = dataDict["re_password"]
#     #  Ini mengambil nilai name, email, password, dan re_password dari data JSON yang diterima.

#     if password != re_password:
#         return {
#             "message" : "Password is not the same"
#         },400
#     # Ini memeriksa apakah password dan re_password sama. Jika tidak, respons akan mengembalikan pesan "Password is not the same" dengan kode status HTTP 400 (Bad Request).
#     # Memeriksa apakah email terisi
#     if not email:
#         return {
#             "message" : "Email harus diisi"
#         }, 400
    
#     # Menghash password menggunakan Argon2
#     hashed_password = PasswordHasher().hash(password)
#     #  Ini menghash password menggunakan algoritma Argon2 untuk keamanan. Password yang dihash akan disimpan dalam database.

#  #begin: createa new user
#       # Membuat objek User dengan menggunakan properti yang sesuai
#     new_user = User(
#         email=email,
#         name=name,
#         password=hashed_password,  # Pastikan properti ini sesuai dengan definisi model
#     )
#     #  Ini membuat objek User baru dengan atribut email, name, dan password yang dihash.
#     db.session.add(new_user)
#     #  Ini menambahkan objek new_user ke dalam sesi database.
#     db.session.commit()
#     # Ini melakukan commit perubahan ke database, menyimpan objek new_user ke dalam tabel user.


#     return {
#         "message" : "Registration Succesfull"
#     }, 201

# @app.post("/signin")
# def signin():
#     base64Str = request.headers.get('Authorization')
#     # Ini mengambil nilai header Authorization dari permintaan HTTP.
#     base64Str = base64Str[6:] # hapus "Basic" string

#     # BEGIN Base64 Decoding
#     base64Bytes = base64Str.encode('ascii')
#     # Ini mengubah string Base64 menjadi byte
#     messageBytes = base64.b64decode(base64Bytes)
#     #  Ini mendekode byte Base64 menjadi byte pesan yang asli.
#     pair = messageBytes.decode('ascii')
#     # Ini mengubah byte pesan menjadi string ASCII. String ini berisi pasangan email dan password yang dipisahkan oleh titik dua (':').

#     # END Base64 Decoding
#     email, password = pair.split(":") 
#     # Ini memisahkan email dan password dari string ASCII berdasarkan titik dua (':').

#     user = db.session.execute (
#         db.select(User)
#         .filter_by(email=email)
#     ).scalar_one()
#     # Ini mengambil satu baris (record) dari tabel User yang memiliki email yang sesuai dengan yang diterima dari permintaan. Kemudian dilakukan verifikasi password menggunakan PasswordHasher().verify()

#     if not user or not PasswordHasher().verify(user.password, password):
#     # Jika email atau password tidak sesuai atau pengguna tidak ditemukan, maka akan dikembalikan pesan "Wrong password or email" dengan kode status HTTP 400 (Bad Request).
#         return {
#         "message" : "Wrong password or email" 
#     },400

#     #Start Generate JWT Token
#     access_token = create_access_token(identity=user.id)
#     # Jika email dan password sesuai, maka akan di-generate JWT token menggunakan create_access_token(identity=user.id). JWT token ini kemudian dikembalikan sebagai respons dengan kode status HTTP 200 (OK).
#     #End Generate JWT Token
#     return {
#         "token_access" : access_token,
#     },200

# @app.post("/login")
# def login():
#     data = request.json
#     #  Ini mengambil data JSON yang dikirim dengan permintaan POST.
#     email = data.get('email')
#     password = data.get('password')
#     #  Ini mengambil nilai email dan password dari data JSON yang diterima.
    
#     if not email or not password:
#         return {
#             "message": "Email dan kata sandi diperlukan!"
#         }, 400
#     # ni memeriksa apakah email atau password tidak terisi. Jika salah satu atau keduanya kosong, respons akan mengembalikan pesan "Email dan kata sandi diperlukan!" dengan kode status HTTP 400 (Bad Request).
#     user = db.session.execute(
#         db.select(User)
#         .filter_by(email=email)
#     ).scalar_one() 
#     # Ini mencari pengguna dalam database berdasarkan email yang diberikan. Kemudian dilakukan verifikasi password menggunakan PasswordHasher().verify().
    
#     if not user or not PasswordHasher().verify(user.password, password):
#         return {
#             "message": "Email atau kata sandi salah!"
#         }, 400
#     # Jika pengguna tidak ditemukan atau password tidak sesuai, respons akan mengembalikan pesan "Email atau kata sandi salah!" dengan kode status HTTP 400 (Bad Request).
    
#     # Autentikasi berhasil, generate token akses JWT
#     access_token = create_access_token(identity=user.id)
#     # Jika email dan password sesuai, JWT token di-generate menggunakan create_access_token(identity=user.id).
    
#     return {
#         "token_access": access_token
#     }, 200
    
    
    
@app.get("/myprofile")
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    
    return {
        "id" : current_user.id,
        "email" : current_user.email,
        "name" : current_user.name,
        
    }

@app.get("/who")
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
    )



# @app.route("/")
# def index():
#     return {
#         'message' : 'Hello'
#     },200

# @app.route("/hello")
# def hello_world():
#     return {
#         'message' : 'Hello, World!'
#     },200

# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return {
#         "message" : f"Hello, {username}!"
#     }

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return {
#         "message" : f"This is my ID, {post_id}!"
#     },200

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return {
#         "message" : f"We are in, {subpath}!"
#     }

# @app.post('/upload')
# def upload_file():
#         f = request.files['image']
#         f.save('image.jpg')
#         return {
#              "message" : "Succesfull"
#  }
