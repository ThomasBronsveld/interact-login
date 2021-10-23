from config import DB_LOGIN, DB_PASSWORD, DB_SERVER, DB_NAME
import argparse
from cryptography.fernet import Fernet


#gets runtime arguments
parser = argparse.ArgumentParser()
parser.add_argument("-K", "--key", help="encryption key")
args = parser.parse_args()

#unciphers text (credentials) by using key from runtime arguments and returns them as plain text
def decrypt_credentials(text):
  #check if key was given during runtime
  if not args.key:
    return "No key"
  key = args.key
  cipher_suite = Fernet(key)
  unciphered = cipher_suite.decrypt(text)
  plain_text = bytes(unciphered).decode("utf-8")
  return plain_text

#decrypts sql credentials
db_login = decrypt_credentials(DB_LOGIN)
db_pass = decrypt_credentials(DB_PASSWORD)
db_server = decrypt_credentials(DB_SERVER)
db_name = decrypt_credentials(DB_NAME)
db_url = 'mysql://{}:{}@{}/{}'.format(db_login, db_pass, db_server, db_name)
