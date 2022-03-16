import PySimpleGUI as sg
import os.path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives import serialization 




def privateKeyLoader(filename) -> ec.EllipticCurvePrivateKey:
    with open(filename, "rb") as f:
        pk = f.read()
    try:
        key = serialization.load_pem_private_key(data=pk,password=None)
        print('Clave cargada con exito')
        if isinstance(key, ec.EllipticCurvePrivateKey):    
            return key
    except:
        print('El archivo proporcionado no es una clave privada')



def publicKeyLoader(filename) -> ec.EllipticCurvePublicKey:
    with open(filename, "rb") as f:
        pk = f.read()
    try:
        key = serialization.load_pem_public_key(pk)
        print('Clave cargada con exito')
        if isinstance(key, ec.EllipticCurvePublicKey):    
            return key
    except:
        print('El archivo proporcionado no es una clave publica')
        raise




def read(file):
    with open(file, "rb") as f:
        byte = f.read()
    return byte

def write(signature,filename):
    try:
        with open(filename+"signature.bin", 'wb') as f:
            f.write(signature)
    except:
        raise


def sign(private_key,data):
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature 


def verify(signature,data,public_key):
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        sg.popup('Firma verificada con exito')
        return True
    except:
        sg.popup('Firma rechazada')
    return False










def interfaz_firma():
######Se carga la clave privada del firmante
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
                and f.lower().endswith((".pem"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                try:
                    key=privateKeyLoader(filename)
                    window.close()
                except:
                    sg.popup('El archivo proporcionado no es un archivo de clave privada')
                    continue
            except:
                pass




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

    window = sg.Window("Firma de archivo", layout2)

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
                data=read(filename)
                signature=sign(key,data)
                #escribe firma a archivo 
                try:
                    write(signature,filename)
                    sg.popup('Archivo de firma creado con nombre', filename+"signature.bin")
                    window.close()
                except:
                    continue
            except:
                pass











def interfaz_verificacion():
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

    publicKeyLoaderLayout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
        ]
    ]

    window = sg.Window("Carga de clave publica", publicKeyLoaderLayout)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Salir" or event == sg.WIN_CLOSED:
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
                and f.lower().endswith((".pem"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                try: 
                    loaded_public_key= publicKeyLoader(filename)
                except:
                    sg.popup('El archivo cargado no es una clave publica')
                    continue
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

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
        ]
    ]

    window = sg.Window("Carga de archivo de firma", layout)

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
                and f.lower().endswith((".bin"))
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

    window = sg.Window("Carga de documento firmado", layout2)

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
                verify(loaded_sig,read(filename),loaded_public_key)
                window.close()
            except:
                pass

    window.close()


def menu():
    layout = [[sg.Text('Menu')],         
                    [sg.Button('Firmar Documento'),sg.Button('Verificar Firma')]]      

    window = sg.Window('Window Title', layout)    
    while 1:
        event, values = window.read()    
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event=="Firmar Documento":
            interfaz_firma()
        if event=="Verificar Firma":
            interfaz_verificacion()

menu()
        

