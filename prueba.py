import tkinter as tk
import random
from tkinter import *
from PIL import Image, ImageTk

from Persona import Persona

# Esto funciona como un recoradatorio de en que posicion de la pista se encuentra o si esta vacia
male_reacomodar = []
female_reacomodar = []

# Lista de quienes van a llegar cada n segundos
male_arrive = []
female_arrive = []

# El maximo de personas que se encuentra al comienzo
max_personas = 5

# El tiempo que toma cambiar la cantidad de parejas bailando
tiempo_espera = 5000


# Se crea la lista de persona que van a estar en la cola, la condicion determina si es male o female
def crear_lista(condicion, a):
    lista = []

    for x in range(max_personas):
        ls = Persona(x + 1, condicion)
        lista.append(ls)

    if condicion:
        for x in range(a):
            male_reacomodar.append(None)
        for x in range(max_personas, 13):
            male = Persona(x + 1, condicion)
            male_arrive .append(male)
    else:
        for x in range(a):
            female_reacomodar.append(None)

        for x in range(max_personas, 13):
            female = Persona(x + 1, condicion)
            female_arrive .append(female)

    return lista


class SampleApp(tk.Tk):
    # La cantidad de personas que van a estar bailando
    personas_bailando = max_personas

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Las Personas en la cola
        self.male = crear_lista(True, self.personas_bailando)
        self.female = crear_lista(False, self.personas_bailando)
        # Las Personas en la pista
        self.dancing_male = []
        self.dancing_female = []
        # Se invierte la imagen para parecer que estan bailando
        self.dance_sequence = True

        self.wm_title("Salon de Baile")

        self.canvas = Canvas(self, height=614, width=620)

        self.canvas.configure(borderwidth=0, highlightthickness=0)

        self.button = Button(self.canvas,
                             text="Bailar",
                             command=lambda: [self.click()],
                             font=("Comic Sans", 30),
                             fg="#00FF00",
                             bg="black",
                             activeforeground="#00FF00",
                             activebackground="black")

        self.button.place(x=250, y=250)

        # Se crea las imagenes de las parejas
        self.img = (Image.open("dancefloor.jpg"))
        self.img2 = (Image.open("dancingmale.png"))
        self.img3 = (Image.open("dancingfemale.png"))

        # Se ajusta su tamaño
        self.resized_floor = self.img.resize((650, 614), Image.LANCZOS)
        self.resized_image = self.img2.resize((50, 50), Image.LANCZOS)
        self.resized_image2 = self.img3.resize((50, 50), Image.LANCZOS)


        # Se invierte la imagen para dar la sensacion de movimiento
        self.pil_image_flip = self.resized_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.pil_image_flip2 = self.resized_image2.transpose(Image.FLIP_LEFT_RIGHT)

        # Se guarda la pista de baile
        self.dance_floor = ImageTk.PhotoImage(self.resized_floor)

        # Se guarda las imagenes inviertas en un formato valido para tkinter
        self.flip_mdance = ImageTk.PhotoImage(self.pil_image_flip)
        self.flip_fdance = ImageTk.PhotoImage(self.pil_image_flip2)
        self.mdance = ImageTk.PhotoImage(self.resized_image)
        self.fdance = ImageTk.PhotoImage(self.resized_image2)



        self.dibujar(self.canvas)

    def dibujar(self, canvas):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=NW, image=self.dance_floor)
        canvas.create_text(30, 20, text="Cola", fill="black", font='Helvetica 18 bold')
        canvas.create_text(570, 20, text="Cola", fill="black", font='Helvetica 18 bold')
        canvas.create_text(320, 20, text="Sala de Baile", fill="black", font='Helvetica 18 bold')
        for x in self.male:
            canvas.create_text(x.x + 20, x.y - 10, text=(str(x.nombre) + " | " + str(x.pareja)), fill="black",
                               font='Helvetica 12 bold')
            self.canvas.create_image(x.x + 20, x.y+25, image=self.mdance)

        for x in self.female:
            canvas.create_text(x.x + 20, x.y - 10, text=(str(x.nombre) + " | " + str(x.pareja)), fill="black",
                               font='Helvetica 12 bold')
            self.canvas.create_image(x.x + 20, x.y + 25, image=self.flip_fdance)
            canvas.pack()
        for x in self.dancing_male:
            canvas.create_text(x.x + 20, x.y - 10, text=(str(x.nombre) + " | " + str(x.pareja)), fill="black",
                               font='Helvetica 12 bold')
            if self.dance_sequence:
                self.canvas.create_image(x.x + 20, x.y + 25, image=self.mdance)
            else:
                self.canvas.create_image(x.x + 20, x.y + 25, image=self.flip_mdance)
            canvas.pack()
        for x in self.dancing_female:
            canvas.create_text(x.x + 20, x.y - 10, text=(str(x.nombre) + " | " + str(x.pareja)), fill="black",
                               font='Helvetica 12 bold')
            if not self.dance_sequence:
                self.canvas.create_image(x.x + 20, x.y + 25, image=self.fdance)
            else:
                self.canvas.create_image(x.x + 20, x.y + 25, image=self.flip_fdance)
            canvas.pack()
        self.dance_sequence = not self.dance_sequence

    def click(self):
        self.button.place_forget()
        print("bailemos")
        self.bailar()
        self.after(tiempo_espera, lambda: self.aleatorio())
        self.after(7000, lambda: self.llegan())

    def llegan(self):
        self.male.append(male_arrive[0])
        self.female.append(female_arrive[0])

        del male_arrive[0]
        del female_arrive[0]

        if len(male_arrive) > 0:
            self.after(7000, lambda: self.llegan())

    def aleatorio(self):
        r = random.randint(1, 8)
        self.personas_bailando = r
        self.after(tiempo_espera, lambda: self.aleatorio())


    def bailar(self):
        total = self.personas_bailando

        print(total)
        # Se reacomoda la pista de baile si es que cambia el total de parejas bailando
        self.reacomodar(total)

        # Si la pista tiene menos de personas_bailando, se agrega una de la cola
        self.agregar_pista(total)

        # Se acomoda la posicion de la persona segun su posicion en la pista(reacomodar)
        self.acomodar_pistaycola()

        # Se vuelve a dibujar el panel
        self.dibujar(self.canvas)

        # Se resta un segundo a los que estan bailando y en caso de 0 se saca de la pista
        self.cola()

    def reacomodar(self, total):
        if len(male_reacomodar) < total:
            for x in range(len(male_reacomodar), total):
                male_reacomodar.append(None)
            # Si es que hay mas personas en la pista que el numero total se quita los ultimos de la pista
        if len(male_reacomodar) > total:
            for x in range(len(male_reacomodar), total, -1):
                for j in range(len(self.dancing_male)):
                    if self.dancing_male[j].posicion_baile == x:
                        for i in range(len(male_reacomodar)):
                            if male_reacomodar[i] is not None:
                                if self.dancing_male[j].nombre == male_reacomodar[i].nombre:
                                    del male_reacomodar[i]
                                    break
                        self.male.append(self.dancing_male[j])
                        del self.dancing_male[j]
                        break
            # Se reacomoda la pista de baile si es que cambia el total de parejas bailando
        if len(female_reacomodar) < total:
            for x in range(len(female_reacomodar), total):
                female_reacomodar.append(None)
            # Si es que hay mas personas en la pista que el numero total se quita los ultimos de la pista
        if len(female_reacomodar) > total:
            for x in range(len(female_reacomodar), total, -1):
                for j in range(len(self.dancing_female)):
                    if self.dancing_female[j].posicion_baile == x:
                        for i in range(len(female_reacomodar)):
                            if female_reacomodar[i] is not None:
                                if self.dancing_female[j].nombre == female_reacomodar[i].nombre:
                                    del female_reacomodar[i]
                                    break
                        self.female.append(self.dancing_female[j])
                        del self.dancing_female[j]
                        break

    def agregar_pista(self, total):
        for_male = self.male
        for_female = self.female
        contador = 0
        eliminar = 0

        # Se reacomoda la pista de baile si es que cambia el total de parejas bailando
        self.reacomodar(total)

        # Si la pista tiene menos de personas_bailando, se agrega una de la cola
        for x in for_male:
            if len(self.dancing_male) < total:
                for j in range(len(male_reacomodar)):
                    if male_reacomodar[j] is None:
                        male_reacomodar[j] = x
                        break
                self.dancing_male.append(x)
                eliminar += 1
            contador += 1

        # Se elimina la primera persona de la cola n veces
        for x in range(eliminar):
            del self.male[0]
        eliminar = 0
        contador = 0
        for x in for_female:
            if len(self.dancing_female) < total:
                for j in range(len(female_reacomodar)):
                    if female_reacomodar[j] is None:
                        female_reacomodar[j] = x
                        break
                self.dancing_female.append(x)
                # Se agrega la cantidad de personas que se va a eliminar de la cola
                eliminar += 1
            contador += 1

        for x in range(eliminar):
            del self.female[0]

    def acomodar_pistaycola(self):
        # Se acomoda la posicion de la persona segun su posicion en la pista(reacomodar)
        for x in range(len(self.dancing_male)):
            for j in range(len(male_reacomodar)):
                if male_reacomodar[j] is not None:
                    if male_reacomodar[j].nombre == self.dancing_male[x].nombre:
                        self.dancing_male[x].bailando(j + 1, True)

        # Se acomoda la posicion de la persona segun su posicion en la pista(reacomodar)
        for x in range(len(self.dancing_female)):
            for j in range(len(female_reacomodar)):
                if female_reacomodar[j] is not None:
                    if female_reacomodar[j].nombre == self.dancing_female[x].nombre:
                        self.dancing_female[x].bailando(j + 1, False)

        # Se acomoda la posicion de la persona segun su posicion en la cola
        for x in range(len(self.male)):
            self.male[x].reacomodar(x + 1, True)

        for x in range(len(self.female)):
            self.female[x].reacomodar(x + 1, False)

    def cola(self):
        eliminar = []

        # Se resta el tiempo de baile
        for x in range(len(self.dancing_male)):
            # Si el tiempo == 0 se quita de la pista y se agrega a la cola
            if self.dancing_male[x].time <= 0:
                for j in range(len(male_reacomodar)):
                    if male_reacomodar[j] is not None:
                        if male_reacomodar[j].nombre == self.dancing_male[x].nombre:
                            male_reacomodar[j] = None
                            break
                self.dancing_male[x].reiniciartiempo()
                self.male.append(self.dancing_male[x])
                eliminar.append(self.dancing_male[x].nombre)
            else:
                self.dancing_male[x].restarTiempo()

        # Se elimina de la pista
        for x in range(len(eliminar)):
            for j in range(len(self.dancing_male)):
                if self.dancing_male[j].nombre == eliminar[x]:
                    del self.dancing_male[j]
                    break

        eliminar = []
        # Se resta el tiempo de baile
        for x in range(len(self.dancing_female)):
            # Si el tiempo == 0 se quita de la pista y se agrega a la cola
            if self.dancing_female[x].time <= 0:
                for j in range(len(female_reacomodar)):
                    if female_reacomodar[j] is not None:
                        if female_reacomodar[j].nombre == self.dancing_female[x].nombre:
                            female_reacomodar[j] = None
                            break
                self.dancing_female[x].reiniciartiempo()
                self.female.append(self.dancing_female[x])
                eliminar.append(self.dancing_female[x].nombre)
            else:
                self.dancing_female[x].restarTiempo()

        # Se elimina de la pista
        for x in range(len(eliminar)):
            for j in range(len(self.dancing_female)):
                if self.dancing_female[j].nombre == eliminar[x]:
                    del self.dancing_female[j]
                    break

        # Se llama a bailar() despues de un segundo
        self.after(1000, lambda: self.bailar())


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
