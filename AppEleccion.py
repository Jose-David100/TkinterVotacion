from tkinter import ttk, messagebox
from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import pygame

app = Tk()
app.configure(bg='gray')
app.title("Centro de votacion")
app.geometry('800x600')
app.resizable(width=0, height=0)

# CREAR BASE DE DATOS
conexion = sqlite3.connect('votacion.db')

# CURSOR DE LA BASE DE DATOS ( ACCIONADOR )
cursor_db = conexion.cursor()

# CREAR TABLA DE CANDIDATOS SI NO EXISTE
cursor_db.execute("""
    CREATE TABLE if not exists candidatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        votaciones INTEGER NOT NULL
    );
""")

# CREAR TABLA DE VOTANTES SI NO EXISTE
cursor_db.execute("""
    CREATE TABLE if not exists votantes (
        cedula INTEGER NOT NULL PRIMARY KEY
    );
""")



# CREAR CANDIDATO MADURO (ID = 1) Y GUAIDO (ID = 2) SI NO ESTA CREADO
cursor_db.execute("""
    INSERT OR IGNORE INTO candidatos (id, votaciones) VALUES (?, ?)
""", (1,0))
cursor_db.execute("""
    INSERT OR IGNORE INTO candidatos (id, votaciones) VALUES (?, ?)
""", (2,0))


def clicked():
    text = form.get()
    form.delete(0, END)

    if text.isdigit() and len(text) == 8:
        # CONSULTA DE LA BASE DE DATOS PARA OBTENER A CEDULA SI EXISTE
        buscar_cedula = cursor_db.execute("""
            SELECT cedula FROM votantes WHERE cedula = ?
        """,(text,))
        cedula = buscar_cedula.fetchone()
        if cedula == None:
            cursor_db.execute("""
            INSERT INTO votantes (cedula) VALUES (?)
            """, (text,))

            # CONSULTA DE LA BASE DE DATOS PARA OBTENER A MADURO
            cursor_db.execute("""
                SELECT votaciones FROM candidatos WHERE id = 1
            """)
            # SI EXITE MADURO
            if cursor_db:
                votaciones_tupla = cursor_db.fetchone()
                votaciones = votaciones_tupla[0]
                votaciones += 1

                # ACTUALIZAR Y SUMAR VOTACIONES DE MADURO
                cursor_db.execute("""
                    UPDATE candidatos SET votaciones = ? WHERE id = ?;
                """, (votaciones, 1))
                conexion.commit()
                messagebox.showinfo('Notificacion', 'Voto exitoso')

            else:
                messagebox.showinfo('Notificacion', 'Ha ocurriod un error')
        else:
            messagebox.showerror('Notificacion', 'Ya has votado anteriormente')
    else:
        messagebox.showerror('Notificacion', 'Verifica que el dato ingresado sea numerico y tenga 8 digitos')


    
def clicked2():

    text = form.get()
    form.delete(0, END)

    if text.isdigit() and len(text) == 8:
        # CONSULTA DE LA BASE DE DATOS PARA OBTENER A CEDULA SI EXISTE
        buscar_cedula = cursor_db.execute("""
            SELECT cedula FROM votantes WHERE cedula = ?
        """,(text,))
        cedula = buscar_cedula.fetchone()
        if cedula == None:
            cursor_db.execute("""
            INSERT INTO votantes (cedula) VALUES (?)
            """, (text,))

            # CONSULTA DE LA BASE DE DATOS PARA OBTENER A GUAIDO
            cursor_db.execute("""
                SELECT votaciones FROM candidatos WHERE id = 2
            """)

            # SI EXITE GUAIDO
            if cursor_db:
                votaciones_tupla = cursor_db.fetchone()
                votaciones = votaciones_tupla[0]
                #VOTAR A GUAIDO SI TIENE MENOS DE 10 VOTACIONES
                if votaciones < 10:
                    votaciones += 1
                    # ACTUALIZAR Y SUMAR VOTACIONES DE GUAIDO
                    cursor_db.execute("""
                        UPDATE candidatos SET votaciones = ? WHERE id = ?;
                    """, (votaciones, 2))
                    conexion.commit()
                    messagebox.showinfo('Notificacion', 'Voto exitoso')

                # VOTAR A MADURO YA QUE GUAIDO TIENE MAS DE 9 VOTACIONES
                else:
                    # CONSULTA DE LA BASE DE DATOS PARA OBTENER A MADURO
                    cursor_db.execute("""
                        SELECT votaciones FROM candidatos WHERE id = 1
                    """)
                    votaciones_tupla = cursor_db.fetchone()
                    votaciones = votaciones_tupla[0]
                    votaciones += 1
                    # ACTUALIZAR Y SUMAR VOTACIONES DE MADURO
                    cursor_db.execute("""
                        UPDATE candidatos SET votaciones = ? WHERE id = ?;
                    """, (votaciones, 1))
                    conexion.commit()
                    messagebox.showinfo('Notificacion', 'Voto exitoso')

            else:
                messagebox.showinfo('Notificacion', 'Ha ocurrido un error')
        else:
            messagebox.showerror('Notificacion', 'Ya has votado anteriormente')
    else:
        messagebox.showerror('Notificacion', 'Verifica que el dato ingresado sea numerico y tenga 8 digitos')


# OBTENER RESULTADOS DE VOTACION Y REPRODUCIR MUSICA
def result():
    pygame.mixer.init()
    pygame.mixer.music.load("himno.mp3")
    pygame.mixer.music.play()
    # CONSULTA DE LA BASE DE DATOS PARA OBTENER LOS RESULTADOS
    cursor_db.execute("""
        SELECT * FROM candidatos
    """)
    lista = cursor_db.fetchall()
    tupla1, tupla2 = lista[0], lista[1]
    resultado1, resultado2 = tupla1[1], tupla2[1]
    mensaje = messagebox.showinfo('Notificacion', 'Resultados: \n \n' +'Maduro : ' + str(resultado1) +  ' Votantes \n' + 'Guaido: ' + str(resultado2)  +' Votantes')
    if mensaje == 'ok':
        pygame.mixer.music.stop()
#MADURO
url = "IMG_4755.JPG"
img = ImageTk.PhotoImage(Image.open(url))
panel = Label(app, image = img)
panel.place(x=110, y=140)
lbl2 = Label(app, text="Nicolas Maduro", font=("Arial Bold", 25), bg='gray').place(x=120, y=90)

#GUAIDO
url2 = "IMG_4756.JPG"
img2 = ImageTk.PhotoImage(Image.open(url2))
panel2 = Label(app, image = img2)
panel2.place(x=500, y=140)
lbl3 = Label(app, text="Juan Guaido", font=("Arial Bold", 25), bg='gray').place(x=530, y=90)

# TITULO
tit1 = Label(app, text="Consejo", font=("Arial Bold", 25), fg="Yellow", bg='gray').place(x=200,y=10)
tit2 = Label(app, text="Nacional", font=("Arial Bold", 25), fg="blue", bg='gray').place(x=320,y=10)
tit3 = Label(app, text="Electoral", font=("Arial Bold", 25), fg="red", bg='gray').place(x=440,y=10)

# BOTONES
btn = Button(app, text="Seleecionar", command=clicked).place(x=170, y=500)
btn2 = Button(app, text="Seleecionar", command=clicked2).place(x=600, y=500)

# BOTON (VER RESULTADOS)
btn3 = Button(app, text="Ver resultados", command=result).place(x=390, y=500)

# INPUT CEDULA
label_form = Label(app, text="Insertar Cedula:", font=("Arial Bold", 10), bg='gray').place(x=390, y=242)
form = Entry(app, width=14)
form.focus()
form.place(x=390, y=270)


app.mainloop()