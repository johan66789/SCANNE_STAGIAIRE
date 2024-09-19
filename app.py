from flask import Flask, request, render_template, jsonify
import datetime
import openpyxl
import os

app = Flask(__name__)

# Chemin du fichier Excel
EXCEL_FILE = 'temp/stagiaires_arrivees.xlsx'

# Route pour afficher le formulaire HTML
@app.route('/')
def Index():
    return render_template('index.html')

# Route pour enregistrer l'arrivée
@app.route('/scan_traine', methods=['POST'])
def Scan_traine():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Enregistrer les informations dans le fichier Excel
    if not os.path.exists(EXCEL_FILE):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Nom", "Prénom", "Date", "Heure"])
        workbook.save(EXCEL_FILE)

    try:
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active

        # Ajouter une nouvelle ligne avec les informations du stagiaire
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        sheet.append([nom, prenom, date_str, time_str])

        # Sauvegarder le fichier Excel
        workbook.save(EXCEL_FILE)
    except PermissionError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Arrivée enregistrée avec succès!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
