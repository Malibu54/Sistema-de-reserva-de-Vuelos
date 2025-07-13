# Sistema de Reserva de Vuelos ✈️

Un sistema completo de gestión de reservas de vuelos desarrollado en Python con interfaz gráfica Tkinter, implementando principios de programación orientada a objetos y mejores prácticas de desarrollo.


## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Clases Principales](#clases-principales)
- [Validaciones](#validaciones)
- [Manejo de Errores](#manejo-de-errores)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Autor](#autor)

## 🚀 Características

### Funcionalidades Principales
- ✅ **Gestión de Pasajeros**: Agregar, validar y administrar información de pasajeros
- ✅ **Gestión de Vuelos**: Sistema completo de vuelos con origen, destino, fecha y capacidad
- ✅ **Sistema de Reservas**: Crear, gestionar y controlar reservas de vuelos
- ✅ **Validación Robusta**: Validación exhaustiva de todos los datos de entrada
- ✅ **Interfaz Gráfica**: Interfaz intuitiva y profesional con Tkinter
- ✅ **Control de Capacidad**: Gestión automática de plazas disponibles
- ✅ **Prevención de Duplicados**: Control de pasajeros y reservas duplicadas
- ✅ **Estadísticas**: Información detallada del sistema y métricas

### Características Técnicas
- 🔒 **Encapsulación**: Atributos privados con propiedades getter/setter
- 🛡️ **Manejo de Excepciones**: Sistema robusto de manejo de errores
- 📊 **Estados de Reserva**: Control de estados (activa, cancelada, completada)
- 🏗️ **Patrón Singleton**: Gestión centralizada del sistema
- 📝 **Documentación**: Docstrings completas en todas las clases
- 🎯 **Type Hints**: Tipado estático para mejor mantenimiento
- ✨ **Principios SOLID**: Código mantenible y extensible

## 📋 Requisitos

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **Memoria RAM**: 256 MB mínimo
- **Espacio en Disco**: 50 MB

### Dependencias
```python
# Librerías estándar de Python (incluidas por defecto)
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
from typing import List, Optional
from enum import Enum
```

**Nota**: No se requieren librerías externas. El proyecto utiliza únicamente módulos estándar de Python.

## 🛠️ Instalación

### Opción 1: Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/sistema-reserva-vuelos.git
cd sistema-reserva-vuelos
```

### Opción 2: Descarga directa
1. Descarga el archivo `sistema_reserva_vuelos.py`
2. Colócalo en tu directorio de trabajo

### Verificar instalación de Python
```bash
python --version
# o
python3 --version
```

## 🚀 Uso

### Ejecución del Programa
```bash
# Opción 1
python sistema_reserva_vuelos.py

# Opción 2 (en sistemas Unix/Linux)
python3 sistema_reserva_vuelos.py

# Opción 3 (ejecución directa)
chmod +x sistema_reserva_vuelos.py
./sistema_reserva_vuelos.py
```

### Guía de Uso

#### 1. Agregar Pasajeros
1. Completa los campos: **Nombre**, **Apellido**, **Documento**
2. Haz clic en **"Agregar Pasajero"**
3. El sistema validará automáticamente los datos

#### 2. Hacer Reservas
1. Selecciona un pasajero de la lista desplegable
2. Selecciona un vuelo disponible
3. Haz clic en **"Hacer Reserva"**
4. El sistema verificará disponibilidad y creará la reserva

#### 3. Consultar Información
- El panel inferior muestra:
  - **Vuelos disponibles** con capacidad actual
  - **Todas las reservas** con sus estados
  - **Estadísticas** del sistema

#### 4. Actualizar Información
- Haz clic en **"Actualizar Información"** para refrescar los datos

## 🏗️ Arquitectura

### Patrón de Diseño
El sistema implementa varios patrones de diseño:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Interfaz      │    │     Gestor      │    │    Modelos      │
│   Gráfica       │◄───┤    Reservas     │◄───┤  (Pasajero,     │
│ (InterfazGrafica│    │  (Singleton)    │    │  Vuelo, Reserva)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Capas del Sistema
1. **Capa de Presentación**: `InterfazGrafica`
2. **Capa de Lógica de Negocio**: `GestorReservas`
3. **Capa de Modelo**: `Pasajero`, `Vuelo`, `Reserva`
4. **Capa de Validación**: Métodos de validación en cada clase

## 📚 Clases Principales

### 👤 Clase `Pasajero`
```python
class Pasajero:
    """Representa un pasajero en el sistema"""
    
    # Atributos privados
    _nombre: str
    _apellido: str
    _documento: str
    
    # Propiedades
    @property
    def nombre_completo(self) -> str
```

**Validaciones**:
- Nombre/Apellido: Solo letras, mínimo 2 caracteres
- Documento: 5-12 dígitos numéricos

### ✈️ Clase `Vuelo`
```python
class Vuelo:
    """Representa un vuelo en el sistema"""
    
    # Atributos privados
    _numero: str
    _origen: str
    _destino: str
    _fecha: str
    _capacidad_total: int
    _reservas: List[Reserva]
    
    # Propiedades calculadas
    @property
    def capacidad_disponible(self) -> int
```

**Validaciones**:
- Número de vuelo: Formato alfanumérico (ej: V001, AA1234)
- Ciudades: Mínimo 2 caracteres
- Fecha: Formato YYYY-MM-DD
- Capacidad: Entero positivo ≤ 1000

### 🎫 Clase `Reserva`
```python
class Reserva:
    """Representa una reserva en el sistema"""
    
    # Estados posibles
    EstadoReserva.ACTIVA
    EstadoReserva.CANCELADA
    EstadoReserva.COMPLETADA
    
    # Métodos de control
    def cancelar(self) -> None
    def completar(self) -> None
```

### 🎮 Clase `GestorReservas` (Singleton)
```python
class GestorReservas:
    """Gestor centralizado del sistema (Singleton)"""
    
    def agregar_pasajero(self, nombre, apellido, documento) -> Pasajero
    def crear_reserva(self, numero_vuelo, documento_pasajero) -> Reserva
    def buscar_pasajero_por_documento(self, documento) -> Optional[Pasajero]
    def buscar_vuelo_por_numero(self, numero) -> Optional[Vuelo]
```

## ✅ Validaciones

### Validaciones de Entrada
| Campo | Validación | Ejemplo Válido | Ejemplo Inválido |
|-------|------------|----------------|------------------|
| Nombre | Solo letras, min 2 chars | "Juan", "María José" | "J", "Juan123" |
| Documento | 5-12 dígitos | "12345678" | "123", "abcd1234" |
| Vuelo | Formato alfanumérico | "V001", "AA1234" | "V", "123456" |
| Fecha | YYYY-MM-DD | "2024-03-15" | "15/03/2024" |
| Capacidad | Entero > 0, ≤ 1000 | 150 | 0, 1001 |

### Validaciones de Negocio
- ✅ **Documentos únicos**: No se permiten pasajeros con el mismo documento
- ✅ **Capacidad de vuelo**: No se pueden hacer reservas si no hay plazas
- ✅ **Reservas duplicadas**: Un pasajero no puede tener reservas activas duplicadas
- ✅ **Estados válidos**: Solo se pueden cancelar/completar reservas activas

## 🛡️ Manejo de Errores

### Excepciones Personalizadas
```python
class ReservaException(Exception):
    """Excepción personalizada para errores de reserva"""
    pass
```

### Tipos de Errores Manejados
1. **Errores de Validación**: Datos inválidos o faltantes
2. **Errores de Negocio**: Violación de reglas (capacidad, duplicados)
3. **Errores de Sistema**: Problemas inesperados

### Manejo en la Interfaz
```python
try:
    # Operación del sistema
    resultado = operacion()
except (ValueError, ReservaException) as e:
    messagebox.showerror("Error", str(e))
except Exception as e:
    messagebox.showerror("Error", f"Error inesperado: {str(e)}")
```

## 📊 Datos de Ejemplo

El sistema incluye datos de ejemplo para facilitar las pruebas:

### Pasajeros Preconfigurados
- Juan Perez (Doc: 12345678)
- Maria Gomez (Doc: 87654321)
- Carlos Lopez (Doc: 11223344)
- Ana Martinez (Doc: 44332211)
- Pedro Rodriguez (Doc: 55667788)
- *... y 5 más*

### Vuelos Preconfigurados
- **V001**: Buenos Aires → Madrid (2024-03-15) - Cap: 150
- **V002**: Madrid → Paris (2024-03-16) - Cap: 120
- **V003**: Paris → Londres (2024-03-17) - Cap: 100
- **AA1234**: Buenos Aires → New York (2024-03-18) - Cap: 200
- **IB5678**: Madrid → Barcelona (2024-03-19) - Cap: 80

## 🖥️ Capturas de Pantalla

### Interfaz Principal

> <p align="center">
  <img src="/assets/screenshot.png" />
</p>


## 🧪 Pruebas

### Casos de Prueba Recomendados

1. **Pruebas de Validación**:
   ```python
   # Documento inválido
   agregar_pasajero("Juan", "Perez", "123")  # Error: muy corto
   
   # Nombre inválido
   agregar_pasajero("J", "Perez", "12345678")  # Error: muy corto
   
   # Documento duplicado
   agregar_pasajero("Maria", "Lopez", "12345678")  # Error: ya existe
   ```

2. **Pruebas de Reserva**:
   ```python
   # Capacidad completa
   # Llenar vuelo y intentar reserva adicional
   
   # Reserva duplicada
   # Mismo pasajero, mismo vuelo, dos veces
   ```

3. **Pruebas de Interfaz**:
   - Campos vacíos
   - Selecciones inválidas
   - Actualización de datos

## 🔧 Personalización

### Modificar Datos de Ejemplo
Edita el método `_inicializar_datos()` en `GestorReservas`:

```python
def _inicializar_datos(self):
    # Agregar tus propios pasajeros
    pasajeros_data = [
        ("Tu", "Nombre", "Tu_Documento"),
        # ... más pasajeros
    ]
    
    # Agregar tus propios vuelos
    vuelos_data = [
        ("TU001", "Tu_Origen", "Tu_Destino", "2024-12-31", 200),
        # ... más vuelos
    ]
```

### Cambiar Validaciones
Modifica los métodos `_validar_*()` en cada clase:

```python
def _validar_documento(self, documento: str) -> str:
    # Personalizar validación según tus necesidades
    if not re.match(r'^\d{8,10}$', documento):  # 8-10 dígitos
        raise ValueError("Documento debe tener 8-10 dígitos")
    return documento
```

### Personalizar Interfaz
Modifica `_crear_widgets()` en `InterfazGrafica`:

```python
def _crear_widgets(self):
    # Cambiar colores, tamaños, disposición
    self.ventana.configure(bg='#f0f0f0')
    # ... más personalizaciones
```

## 📈 Posibles Mejoras

### Funcionalidades Futuras
- 🔄 **Cancelación de reservas**: Permitir cancelar reservas existentes
- 🔍 **Búsqueda avanzada**: Filtros por fecha, origen, destino
- 📊 **Reportes**: Generar reportes en PDF/Excel
- 🗄️ **Persistencia**: Guardar datos en base de datos
- 🌐 **API REST**: Crear API para integración
- 📱 **Responsive**: Interfaz adaptable a diferentes tamaños
- 🔐 **Autenticación**: Sistema de usuarios y roles
- 💳 **Pagos**: Integración con sistemas de pago
- 📧 **Notificaciones**: Envío de confirmaciones por email

### Mejoras Técnicas
- 📋 **Logging**: Sistema de logs detallado
- 🧪 **Testing**: Suite de pruebas unitarias
- 📚 **Documentación**: Documentación automática con Sphinx
- 🐳 **Docker**: Containerización de la aplicación
- 🚀 **CI/CD**: Pipeline de integración continua

## 🤝 Contribución

### Cómo Contribuir
1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

### Pautas de Contribución
- ✅ Sigue el estilo de código existente
- ✅ Agrega docstrings a nuevas funciones
- ✅ Incluye pruebas para nuevas funcionalidades
- ✅ Actualiza la documentación si es necesario
- ✅ Usa commits descriptivos

### Reportar Bugs
1. Verifica que el bug no esté ya reportado
2. Crea un **Issue** con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Capturas de pantalla (si aplica)
   - Información del sistema

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2025 [Ori]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Autor

**[Tu Nombre]**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- LinkedIn: [tu-perfil](https://linkedin.com/in/tu-perfil)
- Email: tu.email@ejemplo.com

## 🙏 Agradecimientos

- Comunidad de Python por las excelentes librerías
- Tkinter por proporcionar una interfaz gráfica nativa
- Todos los contribuidores del proyecto

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐

**Desarrollado con ❤️ en Python**