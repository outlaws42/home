from cryptography.fernet import Fernet
from helpers.file import Location as loc
from helpers.io import IO as io

class Encryption():

  def gen_key(fname: str,):
    home = loc.home_dir()
    key = Fernet.generate_key()
    with open(f'{home}/{fname}', 'wb')as fkey:
      fkey.write(key)

  def encrypt(
    key: str, 
    fname: str, 
    e_fname: str, 
    fdest='relative', 
    ):
    """
    key = key file used to encrypt file,
    fname = file to encrypt,
    e_fname = name of the encrypted file,
    fdest = file destination relative too,
    Takes a input file and encrypts output file
    requires tmod open_file and save_file functions
    requires from cryptography.fernet import Fernet
    """
    keyf = Fernet(key)
    e_file = io.open_file(
      fname = fname,
      fdest = fdest,
      mode = "rb"
      )
    encrypted_file = keyf.encrypt(e_file)
    io.save_file(
      fname = e_fname,
      content = encrypted_file,
      fdest = fdest,
      mode = "wb"
    )

  def decrypt(
    key: str, 
    fname: str, 
    e_fname: str,
    fdest: str = 'relative'
    ):
    """
    key = key file used to encrypt file,
    fname = file to encrypt,
    e_fname = name of the encrypted file,
    fdest = file destination relative too,
    Takes a encrypted input file and dencrypts output file
    requires the io open_file and save_file functions
    requires from cryptography.fernet import Fernet
    """
    keyf = Fernet(key)
    encrypted = io.open_file(
      fname = e_fname,
      fdest = fdest, 
      mode ="rb") 
    decrypt_file = keyf.decrypt(encrypted)
    io.save_file(
      fname = fname,
      content = decrypt_file,
      fdest = fdest,
      mode = "wb")

  def decrypt_login(
    key: str, 
    e_fname: str,
    fdest: str = 'relative'
    ):
    keyf = Fernet(key)
    encrypted = io.open_file(
      fname = e_fname,
      fdest = fdest,
      mode = "rb"
      )
    decrypt_file = keyf.decrypt(encrypted)
    usr = decrypt_file.decode().split(':')
    return [usr[0],usr[1]]