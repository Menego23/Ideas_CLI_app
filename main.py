import redis
import chat_utils

# Connessione al database Redis tramite il tunnel SSL di stunnel
conn = redis.Redis(
    host='redis-12733.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=12733,
    password='Fz7wqpeYtOfJzuVuHMHDOjLGMCcY5MUV')

# Funzione principale
def main():
    utente_corrente = None
    while True:
        if utente_corrente is None:
            print("\nOpzioni:")
            print("1. Registrati")
            print("2. Accedi")
            print("3. Mostra utenti registrati")
            print("4. Esci")
            scelta = input("Seleziona un'opzione: ")

            if scelta == "1":
                esegui_registrazione()
            elif scelta == "2":
                utente_corrente = esegui_login()
            elif scelta == "3":
                mostra_utenti_registrati()
            elif scelta == "4":
                break
            else:
                print("Opzione non valida. Riprova.")
        else:
            print("\nOpzioni:")
            print("1. Invia messaggio")
            print("2. Scarica messaggi")
            print("3. Logout")
            scelta = input("Seleziona un'opzione: ")

            if scelta == "1":
                invia_messaggio_utente(utente_corrente)
            elif scelta == "2":
                scarica_messaggi_utente(utente_corrente)
            elif scelta == "3":
                utente_corrente = None
            else:
                print("Opzione non valida. Riprova.")

# Avvia il programma
main()