from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import PySimpleGUI as sg


def generate_key():
    
    #Genera instancia de clave privada
    private_key = ec.generate_private_key(ec.SECP384R1())
    
    #serializacion de clave publica asociada a la clave privada
    serialized_public=private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,\
    format=serialization.PublicFormat.SubjectPublicKeyInfo)
    
    #Serializacion de la clave privada 
    serialized_private=private_key.private_bytes(encoding=serialization.Encoding.PEM,\
        format=serialization.PrivateFormat.TraditionalOpenSSL,encryption_algorithm=serialization.NoEncryption())

    #Escritura de archivos pem
    with open("Pubic.pem", 'wb') as key:
        key.write(serialized_public)

    with open("Pivate.pem", 'wb') as key:
        key.write(serialized_private)


def menu():
    layout = [[sg.Text('Menu')],         
                    [sg.Button('Generar Clave'),sg.Button('Salir')]]      

    window = sg.Window('Generador de Claves', layout)    
    while 1:
        event,values = window.read()    
        if event == "Salir" or event == sg.WIN_CLOSED:
            break
        if event=="Generar Clave":
            generate_key()
            sg.popup('Archivo de firma creado exitosamente')
            break
    window.close()




menu()