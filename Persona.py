import random


class Persona:
    male_name = ["seba", "fabri", "freddy", "pol", "diego", "marco", "bruno", "favio", "pedro", "pablo", "jimmy",
                 "juan", "robert"]
    female_name = ["helen", "camila", "luciana", "daniela", "paula", "maria", "abril", "ana", "lilian", "marta",
                   "nicole", "carla", "lizzy"]

    x = int()
    y = int()
    time = int()
    posicion_baile = int()
    # 0 = bailando ; >0 = en cola
    nombre = str()
    pareja = int()

    def __init__(self, a, condicion):
        self.time = random.randint(2, 10)
        self.pareja = a
        if condicion:
            self.nombre = self.male_name[a - 1]
        else:
            self.nombre = self.female_name[a - 1]
        # self.canvas = canvas
        # true va a ser hombre
        if condicion:
            self.x = 20
            self.y = 70 * a
        else:
            self.x = 550
            self.y = 70 * a

    def bailando(self, a, condicion):
        self.posicion_baile = a
        self.x = 0
        self.y = 0
        if condicion:
            self.x = 250
            self.y = 70 * a
        else:
            self.x = 350
            self.y = 70 * a

    def reacomodar(self, b, condicion):
        self.posicion_baile = 0
        self.x = 0
        self.y = 0
        if condicion:
            self.x = 20
            self.y = 70 * b
        else:
            self.x = 550
            self.y = 70 * b

    def restarTiempo(self):
        self.time -= 1

    def reiniciartiempo(self):
        self.time = random.randint(2, 10)