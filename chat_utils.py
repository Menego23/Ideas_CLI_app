import redis


# Connessione al database Redis tramite il tunnel SSL di stunnel
conn = redis.Redis(
    host='redis-12733.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=12733,
    password='Fz7wqpeYtOfJzuVuHMHDOjLGMCcY5MUV')
# Funzione per la registrazione di un nuovo utente
def registrazione(conn, username, password):
    # Verifica se l'utente esiste già
    if conn.hexists("utenti", username):
        return False

    # Registra l'utente nel database
    conn.hset("utenti", username, password)
    return True

# Funzione per l'accesso di un utente esistente
def accesso(conn, username, password):
    # Verifica se l'utente esiste e la password è corretta
    stored_password = conn.hget("utenti", username)
    if stored_password is None:
        return False
    return stored_password.decode() == password

# Funzione per caricare un nuovo messaggio
def invia_messaggio(conn, mittente, destinatario, messaggio):
    # Genera un ID univoco per il messaggio
    messaggio_id = conn.incr("id_messaggio")

    # Salva il messaggio nel database
    conn.hset("messaggi", messaggio_id, f"{mittente}:{destinatario}:{messaggio}")

# Funzione per scaricare i messaggi di un utente
def scarica_messaggi(conn, destinatario):
    messaggi = []
    for messaggio in conn.hvals("messaggi"):
        mittente, destinatario_messaggio, testo = messaggio.decode().split(":")
        if destinatario_messaggio == destinatario:
            messaggi.append((mittente, testo))
    return messaggi

# Funzione per ottenere la lista di tutti gli utenti registrati
def mostra_utenti(conn):
    utenti = conn.hgetall("utenti")
    if utenti:
        return {username.decode(): password.decode() for username, password in utenti.items()}
    return {}


# Funzione per registrarsi
def esegui_registrazione():
    print("Registrazione")
    username = input("Inserisci username: ")
    password = input("Inserisci password: ")
    if registrazione(conn, username, password):
        print("Registrazione completata.")
    else:
        print("Username già esistente. Riprova.")

# Funzione per effettuare il login
def esegui_login():
    print("Login")
    username = input("Inserisci username: ")
    password = input("Inserisci password: ")
    if accesso(conn, username, password):
        print("Accesso effettuato.")
        return username
    else:
        print("Username o password errati. Riprova.")
        return None

# Funzione per inviare un messaggio
def invia_messaggio_utente(mittente):
    destinatario = input("Inserisci il destinatario: ")
    messaggio = input("Inserisci il messaggio: ")
    invia_messaggio(conn, mittente, destinatario, messaggio)
    print("Messaggio inviato.")

# Funzione per scaricare i messaggi di un utente
def scarica_messaggi_utente(destinatario):
    messaggi = scarica_messaggi(conn, destinatario)
    print("Messaggi ricevuti:")
    for mittente, testo in messaggi:
        print(f"Da: {mittente}\nMessaggio: {testo}\n")

# Funzione per mostrare la lista di tutti gli utenti registrati
def mostra_utenti_registrati():
    utenti = mostra_utenti(conn)
    if utenti:
        print("Utenti registrati:")
        for username, password in utenti.items():
            print(f"Username: {username}, Password: {password}")
    else:
        print("Nessun utente registrato.")
