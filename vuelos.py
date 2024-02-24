import tkinter as tk
from tkinter import ttk

class Pasajero:
    def __init__(self, nombre, apellido, documento):
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento

class Vuelo:
    def __init__(self, numero, origen, destino, fecha, capacidad):
        self.numero = numero
        self.origen = origen
        self.destino = destino
        self.fecha = fecha
        self.capacidad = capacidad
        self.reservas = []

class Reserva:
    def __init__(self, vuelo, pasajero):
        self.vuelo = vuelo
        self.pasajero = pasajero

pasajeros = [
    Pasajero("Juan", "Perez", "12345"),
    Pasajero("Maria", "Gomez", "67890"),
    Pasajero("Carlos", "Lopez", "54321"),
    Pasajero("Ana", "Martinez", "98765"),
    Pasajero("Pedro", "Rodriguez", "13579"),
    Pasajero("Laura", "Gonzalez", "24680"),
    Pasajero("Diego", "Santos", "11223"),
    Pasajero("Isabel", "Fernandez", "33445"),
    Pasajero("Andres", "Rios", "55667"),
    Pasajero("Sofia", "Diaz", "77889"),
]

vuelos = [
    Vuelo("V001", "Ciudad A", "Ciudad B", "2024-03-01", 2),
    Vuelo("V002", "Ciudad B", "Ciudad C", "2024-03-02", 3),
    Vuelo("V003", "Ciudad C", "Ciudad D", "2024-03-03", 1),
]

reservas = []

class InterfazGrafica:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Reserva de Vuelos")

        # Entry para agregar nuevos pasajeros
        self.nuevo_pasajero_entry = tk.Entry(self.ventana)
        self.nuevo_pasajero_label = tk.Label(self.ventana, text="Nuevo Pasajero (Nombre Apellido Documento):")
        self.nuevo_pasajero_label.pack()
        self.nuevo_pasajero_entry.pack()

        # Botón para agregar nuevo pasajero
        self.agregar_pasajero_button = tk.Button(self.ventana, text="Agregar Pasajero", command=self.agregar_pasajero)
        self.agregar_pasajero_button.pack()

        # ComboBox para seleccionar pasajero
        self.pasajero_label = tk.Label(self.ventana, text="Seleccionar Pasajero:")
        self.pasajero_combobox = ttk.Combobox(self.ventana, values=[p.nombre for p in pasajeros])
        self.pasajero_label.pack()
        self.pasajero_combobox.pack()

        # ComboBox para seleccionar vuelo
        self.vuelo_label = tk.Label(self.ventana, text="Seleccionar Vuelo:")
        self.vuelo_combobox = ttk.Combobox(self.ventana, values=[v.numero for v in vuelos])
        self.vuelo_label.pack()
        self.vuelo_combobox.pack()

        # Etiqueta para mostrar mensajes
        self.mensaje_label = tk.Label(self.ventana, text="")
        self.mensaje_label.pack()

        # Botón para hacer reservas
        self.reserva_button = tk.Button(self.ventana, text="Hacer Reserva", command=self.hacer_reserva)
        self.reserva_button.pack()

    def agregar_pasajero(self):
        nuevo_pasajero_info = self.nuevo_pasajero_entry.get().split()
        if len(nuevo_pasajero_info) == 3:
            nuevo_pasajero = Pasajero(*nuevo_pasajero_info)
            pasajeros.append(nuevo_pasajero)
            self.pasajero_combobox['values'] = [p.nombre for p in pasajeros]
            self.nuevo_pasajero_entry.delete(0, 'end')  # Limpiar el Entry después de agregar el pasajero
            self.mensaje_label.config(text="Pasajero {} {} agregado con éxito.".format(
                nuevo_pasajero.nombre, nuevo_pasajero.apellido))
        else:
            self.mensaje_label.config(text="Formato incorrecto. Ingrese Nombre, Apellido y Documento.")

    def hacer_reserva(self):
        nombre_pasajero = self.pasajero_combobox.get()
        numero_vuelo = self.vuelo_combobox.get()

        # Buscar el pasajero y el vuelo seleccionados en las listas
        pasajero = next((p for p in pasajeros if p.nombre == nombre_pasajero), None)
        vuelo = next((v for v in vuelos if v.numero == numero_vuelo), None)

        if pasajero and vuelo:
            if vuelo.capacidad > 0:
                reserva = Reserva(vuelo, pasajero)
                vuelo.reservas.append(reserva)
                vuelo.capacidad -= 1
                reservas.append(reserva)
                self.mensaje_label.config(text="Reserva realizada con éxito para {} {} en el vuelo {}.".format(
                    pasajero.nombre, pasajero.apellido, vuelo.numero))
            else:
                self.mensaje_label.config(text="No hay capacidad disponible para este vuelo.")
        else:
            self.mensaje_label.config(text="Pasajero o vuelo no encontrado.")

    def ejecutar(self):
        self.ventana.mainloop()

# Crear una instancia de la interfaz gráfica
interfaz = InterfazGrafica()

# Ejecutar la interfaz gráfica
interfaz.ejecutar()