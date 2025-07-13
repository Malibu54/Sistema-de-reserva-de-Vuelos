import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
from typing import List, Optional
from enum import Enum


class EstadoReserva(Enum):
    """Enum para estados de reserva"""
    ACTIVA = "activa"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"


class ReservaException(Exception):
    """Excepción personalizada para errores de reserva"""
    pass


class Pasajero:
    """Clase que representa un pasajero en el sistema"""
    
    def __init__(self, nombre: str, apellido: str, documento: str):
        self._nombre = self._validar_nombre(nombre)
        self._apellido = self._validar_nombre(apellido)
        self._documento = self._validar_documento(documento)
    
    @property
    def nombre(self) -> str:
        """Getter para nombre"""
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        """Setter para nombre"""
        self._nombre = self._validar_nombre(valor)
    
    @property
    def apellido(self) -> str:
        """Getter para apellido"""
        return self._apellido
    
    @apellido.setter
    def apellido(self, valor: str):
        """Setter para apellido"""
        self._apellido = self._validar_nombre(valor)
    
    @property
    def documento(self) -> str:
        """Getter para documento"""
        return self._documento
    
    @documento.setter
    def documento(self, valor: str):
        """Setter para documento"""
        self._documento = self._validar_documento(valor)
    
    def _validar_nombre(self, nombre: str) -> str:
        """Valida que el nombre/apellido sea válido"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if len(nombre.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre.strip()):
            raise ValueError("El nombre solo puede contener letras y espacios")
        return nombre.strip().title()
    
    def _validar_documento(self, documento: str) -> str:
        """Valida que el documento sea válido"""
        if not documento or not documento.strip():
            raise ValueError("El documento no puede estar vacío")
        documento = documento.strip()
        if not re.match(r'^\d{5,12}$', documento):
            raise ValueError("El documento debe tener entre 5 y 12 dígitos")
        return documento
    
    @property
    def nombre_completo(self) -> str:
        """Devuelve el nombre completo del pasajero"""
        return f"{self._nombre} {self._apellido}"
    
    def __str__(self) -> str:
        return f"{self.nombre_completo} (Doc: {self._documento})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Pasajero):
            return False
        return self._documento == other._documento


class Vuelo:
    """Clase que representa un vuelo en el sistema"""
    
    def __init__(self, numero: str, origen: str, destino: str, fecha: str, capacidad: int):
        self._numero = self._validar_numero_vuelo(numero)
        self._origen = self._validar_ciudad(origen)
        self._destino = self._validar_ciudad(destino)
        self._fecha = self._validar_fecha(fecha)
        self._capacidad_total = self._validar_capacidad(capacidad)
        self._reservas: List['Reserva'] = []
    
    @property
    def numero(self) -> str:
        """Getter para número de vuelo"""
        return self._numero
    
    @property
    def origen(self) -> str:
        """Getter para origen"""
        return self._origen
    
    @property
    def destino(self) -> str:
        """Getter para destino"""
        return self._destino
    
    @property
    def fecha(self) -> str:
        """Getter para fecha"""
        return self._fecha
    
    @property
    def capacidad_total(self) -> int:
        """Getter para capacidad total"""
        return self._capacidad_total
    
    @property
    def capacidad_disponible(self) -> int:
        """Calcula la capacidad disponible"""
        reservas_activas = [r for r in self._reservas if r.estado == EstadoReserva.ACTIVA]
        return self._capacidad_total - len(reservas_activas)
    
    @property
    def reservas(self) -> List['Reserva']:
        """Getter para reservas (copia de la lista)"""
        return self._reservas.copy()
    
    def _validar_numero_vuelo(self, numero: str) -> str:
        """Valida el número de vuelo"""
        if not numero or not numero.strip():
            raise ValueError("El número de vuelo no puede estar vacío")
        numero = numero.strip().upper()
        if not re.match(r'^[A-Z]{1,3}\d{3,4}$', numero):
            raise ValueError("Formato de número de vuelo inválido (ej: V001, AA1234)")
        return numero
    
    def _validar_ciudad(self, ciudad: str) -> str:
        """Valida el nombre de la ciudad"""
        if not ciudad or not ciudad.strip():
            raise ValueError("La ciudad no puede estar vacía")
        if len(ciudad.strip()) < 2:
            raise ValueError("El nombre de la ciudad debe tener al menos 2 caracteres")
        return ciudad.strip().title()
    
    def _validar_fecha(self, fecha: str) -> str:
        """Valida el formato de fecha"""
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return fecha
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")
    
    def _validar_capacidad(self, capacidad: int) -> int:
        """Valida la capacidad del vuelo"""
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("La capacidad debe ser un número entero positivo")
        if capacidad > 1000:
            raise ValueError("La capacidad no puede exceder 1000 pasajeros")
        return capacidad
    
    def agregar_reserva(self, reserva: 'Reserva') -> None:
        """Agrega una reserva al vuelo"""
        if self.capacidad_disponible <= 0:
            raise ReservaException("No hay capacidad disponible en este vuelo")
        
        # Verificar si ya existe una reserva activa para este pasajero
        for r in self._reservas:
            if (r.pasajero == reserva.pasajero and 
                r.estado == EstadoReserva.ACTIVA):
                raise ReservaException("Este pasajero ya tiene una reserva activa en este vuelo")
        
        self._reservas.append(reserva)
    
    def __str__(self) -> str:
        return f"Vuelo {self._numero}: {self._origen} → {self._destino} ({self._fecha})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vuelo):
            return False
        return self._numero == other._numero


class Reserva:
    """Clase que representa una reserva en el sistema"""
    
    def __init__(self, vuelo: Vuelo, pasajero: Pasajero):
        self._vuelo = vuelo
        self._pasajero = pasajero
        self._estado = EstadoReserva.ACTIVA
        self._fecha_reserva = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    @property
    def vuelo(self) -> Vuelo:
        """Getter para vuelo"""
        return self._vuelo
    
    @property
    def pasajero(self) -> Pasajero:
        """Getter para pasajero"""
        return self._pasajero
    
    @property
    def estado(self) -> EstadoReserva:
        """Getter para estado"""
        return self._estado
    
    @property
    def fecha_reserva(self) -> str:
        """Getter para fecha de reserva"""
        return self._fecha_reserva
    
    def cancelar(self) -> None:
        """Cancela la reserva"""
        if self._estado != EstadoReserva.ACTIVA:
            raise ReservaException("Solo se pueden cancelar reservas activas")
        self._estado = EstadoReserva.CANCELADA
    
    def completar(self) -> None:
        """Marca la reserva como completada"""
        if self._estado != EstadoReserva.ACTIVA:
            raise ReservaException("Solo se pueden completar reservas activas")
        self._estado = EstadoReserva.COMPLETADA
    
    def __str__(self) -> str:
        return f"Reserva: {self._pasajero.nombre_completo} - {self._vuelo.numero} ({self._estado.value})"


class GestorReservas:
    """Clase singleton para gestionar todas las reservas del sistema"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._pasajeros: List[Pasajero] = []
            self._vuelos: List[Vuelo] = []
            self._reservas: List[Reserva] = []
            self._inicializar_datos()
            self._initialized = True
    
    def _inicializar_datos(self):
        """Inicializa el sistema con datos de ejemplo"""
        # Pasajeros de ejemplo
        pasajeros_data = [
            ("Juan", "Perez", "12345678"),
            ("Maria", "Gomez", "87654321"),
            ("Carlos", "Lopez", "11223344"),
            ("Ana", "Martinez", "44332211"),
            ("Pedro", "Rodriguez", "55667788"),
            ("Laura", "Gonzalez", "88776655"),
            ("Diego", "Santos", "99887766"),
            ("Isabel", "Fernandez", "66778899"),
            ("Andres", "Rios", "77889900"),
            ("Sofia", "Diaz", "00998877"),
        ]
        
        for nombre, apellido, documento in pasajeros_data:
            try:
                pasajero = Pasajero(nombre, apellido, documento)
                self._pasajeros.append(pasajero)
            except ValueError as e:
                print(f"Error al crear pasajero {nombre} {apellido}: {e}")
        
        # Vuelos de ejemplo
        vuelos_data = [
            ("V001", "Buenos Aires", "Madrid", "2024-03-15", 150),
            ("V002", "Madrid", "Paris", "2024-03-16", 120),
            ("V003", "Paris", "Londres", "2024-03-17", 100),
            ("AA1234", "Buenos Aires", "New York", "2024-03-18", 200),
            ("IB5678", "Madrid", "Barcelona", "2024-03-19", 80),
        ]
        
        for numero, origen, destino, fecha, capacidad in vuelos_data:
            try:
                vuelo = Vuelo(numero, origen, destino, fecha, capacidad)
                self._vuelos.append(vuelo)
            except ValueError as e:
                print(f"Error al crear vuelo {numero}: {e}")
    
    def agregar_pasajero(self, nombre: str, apellido: str, documento: str) -> Pasajero:
        """Agrega un nuevo pasajero al sistema"""
        # Verificar si ya existe un pasajero con ese documento
        for pasajero in self._pasajeros:
            if pasajero.documento == documento:
                raise ReservaException("Ya existe un pasajero con ese documento")
        
        nuevo_pasajero = Pasajero(nombre, apellido, documento)
        self._pasajeros.append(nuevo_pasajero)
        return nuevo_pasajero
    
    def obtener_pasajeros(self) -> List[Pasajero]:
        """Devuelve una copia de la lista de pasajeros"""
        return self._pasajeros.copy()
    
    def obtener_vuelos(self) -> List[Vuelo]:
        """Devuelve una copia de la lista de vuelos"""
        return self._vuelos.copy()
    
    def obtener_reservas(self) -> List[Reserva]:
        """Devuelve una copia de la lista de reservas"""
        return self._reservas.copy()
    
    def buscar_pasajero_por_documento(self, documento: str) -> Optional[Pasajero]:
        """Busca un pasajero por su documento"""
        for pasajero in self._pasajeros:
            if pasajero.documento == documento:
                return pasajero
        return None
    
    def buscar_vuelo_por_numero(self, numero: str) -> Optional[Vuelo]:
        """Busca un vuelo por su número"""
        for vuelo in self._vuelos:
            if vuelo.numero == numero:
                return vuelo
        return None
    
    def crear_reserva(self, numero_vuelo: str, documento_pasajero: str) -> Reserva:
        """Crea una nueva reserva"""
        pasajero = self.buscar_pasajero_por_documento(documento_pasajero)
        if not pasajero:
            raise ReservaException("Pasajero no encontrado")
        
        vuelo = self.buscar_vuelo_por_numero(numero_vuelo)
        if not vuelo:
            raise ReservaException("Vuelo no encontrado")
        
        reserva = Reserva(vuelo, pasajero)
        vuelo.agregar_reserva(reserva)
        self._reservas.append(reserva)
        
        return reserva


class InterfazGrafica:
    """Interfaz gráfica para el sistema de reserva de vuelos"""
    
    def __init__(self):
        self.gestor = GestorReservas()
        self._crear_ventana()
        self._crear_widgets()
        self._actualizar_comboboxes()
    
    def _crear_ventana(self):
        """Crea la ventana principal"""
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Reserva de Vuelos - Versión Mejorada")
        self.ventana.geometry("600x500")
        self.ventana.resizable(True, True)
        
        # Configurar el estilo
        style = ttk.Style()
        style.theme_use('clam')
    
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Sección para agregar pasajeros
        ttk.Label(main_frame, text="Agregar Nuevo Pasajero", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        ttk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.nombre_entry = ttk.Entry(main_frame, width=30)
        self.nombre_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Apellido:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.apellido_entry = ttk.Entry(main_frame, width=30)
        self.apellido_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Documento:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.documento_entry = ttk.Entry(main_frame, width=30)
        self.documento_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(main_frame, text="Agregar Pasajero", 
                  command=self._agregar_pasajero).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Sección para hacer reservas
        ttk.Label(main_frame, text="Hacer Reserva", font=('Arial', 12, 'bold')).grid(
            row=6, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        ttk.Label(main_frame, text="Seleccionar Pasajero:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.pasajero_combobox = ttk.Combobox(main_frame, state="readonly", width=40)
        self.pasajero_combobox.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Seleccionar Vuelo:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.vuelo_combobox = ttk.Combobox(main_frame, state="readonly", width=40)
        self.vuelo_combobox.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Button(main_frame, text="Hacer Reserva", 
                  command=self._hacer_reserva).grid(row=9, column=0, columnspan=2, pady=10)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Área de información
        ttk.Label(main_frame, text="Información del Sistema", font=('Arial', 12, 'bold')).grid(
            row=11, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Text widget para mostrar información
        self.info_text = tk.Text(main_frame, height=10, width=60, wrap=tk.WORD)
        self.info_text.grid(row=12, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para el text widget
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        scrollbar.grid(row=12, column=2, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        # Botón para actualizar información
        ttk.Button(main_frame, text="Actualizar Información", 
                  command=self._actualizar_informacion).grid(row=13, column=0, columnspan=2, pady=10)
        
        # Configurar el grid para que se expanda
        main_frame.rowconfigure(12, weight=1)
        
        # Mostrar información inicial
        self._actualizar_informacion()
    
    def _actualizar_comboboxes(self):
        """Actualiza los valores de los comboboxes"""
        # Actualizar pasajeros
        pasajeros = self.gestor.obtener_pasajeros()
        pasajeros_display = [f"{p.nombre_completo} ({p.documento})" for p in pasajeros]
        self.pasajero_combobox['values'] = pasajeros_display
        
        # Actualizar vuelos
        vuelos = self.gestor.obtener_vuelos()
        vuelos_display = [f"{v.numero} - {v.origen} → {v.destino} ({v.fecha}) - Disponibles: {v.capacidad_disponible}" 
                         for v in vuelos]
        self.vuelo_combobox['values'] = vuelos_display
    
    def _agregar_pasajero(self):
        """Agrega un nuevo pasajero al sistema"""
        try:
            nombre = self.nombre_entry.get().strip()
            apellido = self.apellido_entry.get().strip()
            documento = self.documento_entry.get().strip()
            
            if not nombre or not apellido or not documento:
                raise ValueError("Todos los campos son obligatorios")
            
            nuevo_pasajero = self.gestor.agregar_pasajero(nombre, apellido, documento)
            
            # Limpiar campos
            self.nombre_entry.delete(0, tk.END)
            self.apellido_entry.delete(0, tk.END)
            self.documento_entry.delete(0, tk.END)
            
            # Actualizar comboboxes
            self._actualizar_comboboxes()
            self._actualizar_informacion()
            
            messagebox.showinfo("Éxito", f"Pasajero {nuevo_pasajero.nombre_completo} agregado exitosamente")
            
        except (ValueError, ReservaException) as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def _hacer_reserva(self):
        """Realiza una nueva reserva"""
        try:
            pasajero_seleccionado = self.pasajero_combobox.get()
            vuelo_seleccionado = self.vuelo_combobox.get()
            
            if not pasajero_seleccionado or not vuelo_seleccionado:
                raise ValueError("Debe seleccionar un pasajero y un vuelo")
            
            # Extraer documento del pasajero seleccionado
            documento = pasajero_seleccionado.split('(')[1].split(')')[0]
            
            # Extraer número de vuelo
            numero_vuelo = vuelo_seleccionado.split(' - ')[0]
            
            reserva = self.gestor.crear_reserva(numero_vuelo, documento)
            
            # Actualizar comboboxes e información
            self._actualizar_comboboxes()
            self._actualizar_informacion()
            
            messagebox.showinfo("Éxito", 
                              f"Reserva realizada exitosamente:\n{reserva}")
            
        except (ValueError, ReservaException) as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def _actualizar_informacion(self):
        """Actualiza la información mostrada en el text widget"""
        self.info_text.delete(1.0, tk.END)
        
        # Información de vuelos
        vuelos = self.gestor.obtener_vuelos()
        self.info_text.insert(tk.END, "=== VUELOS DISPONIBLES ===\n\n")
        
        for vuelo in vuelos:
            self.info_text.insert(tk.END, f"{vuelo}\n")
            self.info_text.insert(tk.END, f"  Capacidad: {vuelo.capacidad_disponible}/{vuelo.capacidad_total}\n")
            
            reservas_activas = [r for r in vuelo.reservas if r.estado == EstadoReserva.ACTIVA]
            if reservas_activas:
                self.info_text.insert(tk.END, "  Pasajeros:\n")
                for reserva in reservas_activas:
                    self.info_text.insert(tk.END, f"    - {reserva.pasajero.nombre_completo}\n")
            self.info_text.insert(tk.END, "\n")
        
        # Información de reservas
        reservas = self.gestor.obtener_reservas()
        self.info_text.insert(tk.END, "=== TODAS LAS RESERVAS ===\n\n")
        
        for reserva in reservas:
            self.info_text.insert(tk.END, f"{reserva}\n")
            self.info_text.insert(tk.END, f"  Fecha: {reserva.fecha_reserva}\n\n")
        
        # Estadísticas
        total_reservas = len(reservas)
        reservas_activas = len([r for r in reservas if r.estado == EstadoReserva.ACTIVA])
        
        self.info_text.insert(tk.END, "=== ESTADÍSTICAS ===\n\n")
        self.info_text.insert(tk.END, f"Total de pasajeros: {len(self.gestor.obtener_pasajeros())}\n")
        self.info_text.insert(tk.END, f"Total de vuelos: {len(vuelos)}\n")
        self.info_text.insert(tk.END, f"Total de reservas: {total_reservas}\n")
        self.info_text.insert(tk.END, f"Reservas activas: {reservas_activas}\n")
    
    def ejecutar(self):
        """Ejecuta la interfaz gráfica"""
        self.ventana.mainloop()


# Función principal
def main():
    """Función principal del programa"""
    try:
        app = InterfazGrafica()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    main()