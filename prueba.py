import tkinter as tk
from tkinter import *

from Persona import Persona

male_name = ["seba", "fabri", "freddy", "pol", "diego"]
female_name = ["helen", "camila", "luciana", "daniela", "paula"]
class Cons:
    contador = 0


def crearLista(condicion):
    lista = []

    for x in range(5):
        l = Persona(x + 1, condicion)
        lista.append(l)

    return lista


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #self.container = tk.Frame(self, height=400, width=600)
        #self.container.pack(side="top", fill="both", expand=True)
        self.male = crearLista(True)
        self.female = crearLista(False)
        self.dancing_male = []
        self.dancing_female = []
        self.wm_title("Salon de Baile")
        self.button = Button(self,
                        text="Bailar",
                        command=lambda:[self.click()],
                        font=("Comic Sans", 30),
                        fg="#00FF00",
                        bg="black",
                        activeforeground="#00FF00",
                        activebackground="black")

        self.button.pack(fill="none", expand=True)
        self.canvas = Canvas(self, height=600, width=620)
        self.dibujar(self.canvas)

    def dibujar(self,canvas):
        self.canvas.delete("all")
        for x in self.male:
            canvas.create_text(x.x+20, x.y - 10, text=(str(x.cola) + " | " + str(x.time)), fill="black", font=('Helvetica 12 bold'))
            canvas.create_rectangle(x.x, x.y, (x.x + 30), (x.y+30), fill="red")

        for x in self.female:
            canvas.create_text(x.x+20, x.y - 10, text=(str(x.cola) + " | " + str(x.time)), fill="black", font=('Helvetica 12 bold'))
            canvas.create_rectangle(x.x, x.y, (x.x + 30), (x.y+30), fill="blue")
            canvas.pack()
        for x in self.dancing_male:
            canvas.create_text(x.x+20, x.y - 10, text=(str(x.cola) + " | " + str(x.time)), fill="black", font=('Helvetica 12 bold'))
            canvas.create_rectangle(x.x, x.y, (x.x + 30), (x.y+30), fill="red")
            canvas.pack()
        for x in self.dancing_female:
            canvas.create_text(x.x+20, x.y - 10, text=(str(x.cola) + " | " + str(x.time)), fill="black", font=('Helvetica 12 bold'))
            canvas.create_rectangle(x.x, x.y, (x.x + 30), (x.y+30), fill="blue")
            canvas.pack()

    def click(self):
        self.button.pack_forget()
        print("bailemos")
        self.bailar()

    #experimentando
    def bailar(self):
        for_male = self.male
        for_female = self.female
        contador = 0
        eliminar = 0
        #Si la pista tiene menos de 3 personas, se agrega una de la cola
        for x in for_male:
            if len(self.dancing_male) < 3:
                self.dancing_male.append(x)
                eliminar += 1
            contador += 1
        #Se elimina el primer item de la cola n veces
        for x in range(eliminar):
            del self.male[0]
        eliminar = 0
        contador = 0
        for x in for_female:
            if len(self.dancing_female) < 3:
                self.dancing_female.append(x)
                eliminar += 1
            contador += 1

        for x in range(eliminar):
            del self.female[0]


        for x in range(len(self.dancing_male)):
            self.dancing_male[x].bailando(x + 1, True)
        
        for x in range(len(self.dancing_female)):
            self.dancing_female[x].bailando(x+1, False)
        #print(Cons.contador)
        Cons.contador += 1
        self.dibujar(self.canvas)
        self.cola()
        #self.after(1000,lambda: self.bailar())

    def cola(self):
        eliminar = []
        #Se resta el tiempo de baile
        for x in range(len(self.dancing_male)):

            if self.dancing_male[x].time <= 0:
                self.dancing_male[x].reiniciartiempo()
                self.male.append(self.dancing_male[x])
                eliminar.append(self.dancing_male[x].cola)
            else:
                self.dancing_male[x].restarTiempo()

        for x in range(len(eliminar)):
            for j in range(len(self.dancing_male)):
                if self.dancing_male[j].cola == eliminar[x]:
                    del self.dancing_male[j]
                    break

        eliminar = []
        for x in range(len(self.dancing_female)):
            if self.dancing_female[x].time <= 0:
                self.dancing_female[x].reiniciartiempo()
                self.female.append(self.dancing_female[x])
                eliminar.append(self.dancing_female[x].cola)
            else:
                self.dancing_female[x].restarTiempo()

        for x in range(len(eliminar)):
            for j in range(len(self.dancing_female)):
                if self.dancing_female[j].cola == eliminar[x]:
                    del self.dancing_female[j]
                    break
        
        #se reacomoda la cola
        for x in range(len(self.male)):
            self.male[x].reacomodar(x+1,True)

        for x in range(len(self.female)):
            self.female[x].reacomodar(x + 1, False)

        self.dibujar(self.canvas)
        self.after(1000, lambda: self.bailar())


if __name__== "__main__":
    app = SampleApp()
    app.mainloop()
