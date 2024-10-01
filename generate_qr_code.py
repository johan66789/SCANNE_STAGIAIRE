import qrcode

# Adresse IP locale de l'ordinateur exécutant le serveur Flask
url = "http://172.24.1.189:5000/"
# url = "http://192.168.100.60:5000/"
# url = "https://cloud.docteurpc.ci/"

# Générer le code QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Créer une image du code QR
img = qr.make_image(fill='black', back_color='green')

# Sauvegarder l'image du code QR
img.save("entry_qr_code_bara.png")
