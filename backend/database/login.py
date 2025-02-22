import hashlib
from difflib import get_close_matches
import database_layout_tables as db
map_dict: dict = db.get_dict()
cursor = db.conn.cursor()

# Funktion, um das Passwort zu hashen
def hash_password(password: str) -> str:
    # Verwende SHA-256 Hashing
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Funktion, um das Passwort zu überprüfen
def verify_password(stored_hash: str, provided_password: str) -> bool:
    # Hashen des angegebenen Passworts und vergleichen mit dem gespeicherten Hash
    return stored_hash == hash_password(provided_password)

while True:
    # Benutzernamen- und Passworteingabe des Nutzers
    username_input = input("Geben Sie Ihren Benutzernamen ein, wenn Sie eine verifizierte, Karten hochladende und natürliche Person sind: ")
    password_input_hashed = hash_password(input("Geben Sie Ihr Passwort ein: "))

    def login(username_input):
        if username_input in db.users:
            original_password = cursor.execute('''
        SELECT password FROM users WHERE username = ?
        ''', (username_input,))
        return cursor.fetchall()
    
    # Passwortüberprüfung falls Benutzername korrekt
    if login != []:
        is_correct = verify_password(password_input_hashed, login[0])
        truth = {is_correct}
        is_incorrect = verify_password(password_input_hashed, login[0])
        ly = {is_incorrect}
        if truth is True:
            break
        elif ly is True:
            print(f"Passwort ist inkorrekt.")
    else: 
        print(f"Dieser Benutzername existiert mitnichten. Wiederholen Sie Ihre Eingabe daher bitte mit einem korrekten Benutzernamen.")
