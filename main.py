import PySimpleGUI as sg
import os.path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives import serialization 




def generate_key():
    #key generator
    private_key = ec.generate_private_key(
        ec.SECP384R1()
    )
    return private_key


def read(file):
    with open(file, "rb") as f:
        byte = f.read()
    return byte

def write(signature,filename):

    with open(filename+"signature.bin", 'wb') as f:
        f.write(signature)
    return 0


def sign(private_key,data):
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature 


def verify(signature,data,private_key):
    public_key = private_key.public_key()
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        print('Firma verificada con exito')
        return True
    except:
        print('Firma rechazada')
    return False









def interfaz_carga():

    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
        ]
    ]

    window = sg.Window("Cargador de claves", layout)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".txt","bin"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                signature=read(filename)
                sg.popup('Archivo de firma', filename,"cargado")
                window.close()
                return signature
            except:
                pass
    window.close()



def interfaz_firma():

    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
        ]
    ]

    window = sg.Window("Image Viewer", layout)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".gif",".pdf"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                key=generate_key()
                data=read(filename)
                signature=sign(key,data)
                #escribe firma a archivo 
                write(signature,filename)
                sg.popup('Archivo de firma creado con nombre', filename+"signature.txt")
                window.close()
            except:
                pass
    return key
    

def interfaz_verificacion(master):
    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
        ]
    ]

    window = sg.Window("Verificador de firma", layout)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".txt",".bin"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                loaded_sig= read(filename)
                window.close()
            except:
                pass

    window.close()
    file_list_column = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    layout2 = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
        ]
    ]

    window = sg.Window("Verificador de firma 1", layout2)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".pdf"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                verify(loaded_sig,read(filename),master)
                window.close()
            except:
                pass

    window.close()


def menu():
    layout = [[sg.Text('Menu')],         
                    [sg.Button('Generar Clave'),sg.Button('Cargar Clave'), sg.Button('Firmar Documento'),\
                        sg.Button('Verificar Firma')]]      

    window = sg.Window('Window Title', layout)    
    while 1:
        event, values = window.read()    
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event=="Firmar Documento":
            used_k=interfaz_firma()
        if event=="Verificar Firma":
            interfaz_verificacion(used_k)
#        if event=="Generar Clave":
#            key=generate_key()
        if event=="Cargar Clave":
            firma=interfaz_carga()
menu()
        

