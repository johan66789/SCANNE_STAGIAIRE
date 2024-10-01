from flask import Flask, request, render_template, jsonify, redirect, url_for, send_from_directory
import datetime
import openpyxl
import os
import base64
import pymysql.cursors

app = Flask(__name__)

# Chemin du fichier Excel
EXCEL_FILE = 'temp/stagiaires_arrivees.xlsx'

# Dossier pour les images de signature
SIGNATURES_FOLDER = 'temp/signatures'

# Créer le dossier pour les signatures s'il n'existe pas
if not os.path.exists(SIGNATURES_FOLDER):
    os.makedirs(SIGNATURES_FOLDER)

# Configuration de la base de données
app.config['MYSQL_HOST'] = 'localhost'  # Remplacez par votre hôte
app.config['MYSQL_USER'] = 'root'  # Remplacez par votre utilisateur
app.config['MYSQL_PASSWORD'] = ''  # Remplacez par votre mot de passe
app.config['MYSQL_DB'] = 'scanner_db'  # Remplacez par le nom de votre base de données
app.config['SIGNATURES_FOLDER'] = SIGNATURES_FOLDER

# Fonction pour obtenir la connexion MySQL
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor  # Pour récupérer les résultats sous forme de dictionnaires
    )

# Route pour afficher le formulaire HTML
@app.route('/')
def Index():
    return render_template('index.html')

# Route pour enregistrer l'arrivée
@app.route('/scan_trainee', methods=['POST'])
def Scan_traine():
    nom = request.form['nom']
    prenom = request.form['prenom']
    signature = request.form['signature']  # Récupérer la signature

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Enregistrer la signature en tant qu'image
    signature_filename = f"{nom}_{prenom}_{date_str}.png"  # Nom du fichier
    signature_path = os.path.join(SIGNATURES_FOLDER, signature_filename)

    if signature.startswith('data:image/png;base64,'):
        # Enlever le préfixe pour récupérer le code base64 pur
        signature_data = signature.split(',')[1]
        with open(signature_path, 'wb') as img_file:
            img_file.write(base64.b64decode(signature_data))

    # Insertion dans la base de données
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO trainee (nom, prenoms, signature, heure, date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nom, prenom, signature_filename, time_str, date_str))
        connection.commit()
    finally:
        connection.close()

    return render_template('scan_trainee.html', nom=nom)

# Route pour afficher le tableau des utilisateurs
@app.route('/users.html')
def board_user():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM trainee"
            cursor.execute(sql)
            users = cursor.fetchall()
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {e}")
        users = []  # Assurez-vous de toujours avoir une valeur pour users
    finally:
        connection.close()
    
    return render_template("users.html", users=users)


# Route pour servir les fichiers de signature
@app.route('/temp/signatures/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['SIGNATURES_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
