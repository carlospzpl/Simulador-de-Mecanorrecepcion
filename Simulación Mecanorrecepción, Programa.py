import numpy as np
import matplotlib.pyplot as plt
import scipy as sp  
from scipy.signal import convolve
print(f"NumPy versión {np.__version__} cargado correctamente.")
print(f"MatPlot versión {plt.matplotlib.__version__} cargado correctamente.")
print(f"SciPy versión {sp.__version__} cargado correctamente.")
print( "Función convolve lista para usar.")

class estimulo:
    def __init__(self):
        self.piel= np.linspace(0, 100, 100) # Este modelo de piel tiene una longitud de 100 mm y 100 receptores.
        self.touch= None
        self.evaluar_presion= None          
    def pinchazo(self):
        while True:
            try:
                presion= float(input("Presión del estímulo (de 0 a 100): "))
                self.evaluar_presion= presion
                if 0 <= presion <= 100:
                    break 
                else:
                    print("Por favor, el número debe estar entre 0 y 100.")
            except ValueError:
                print("Por favor, introduce un número válido (usa punto para decimales).")
        while True:
            try:
                posicion= float(input("Posición del estímulo (de 0 a 100): "))
                self.evaluar_posicion= posicion
                if 0 <= posicion <= 100:
                    break 
                else:
                    print("Por favor, el número debe estar entre 0 y 100: ")
            except ValueError:
                print("Por favor, introduce un número válido (usa punto para decimales).")
        while True:
            try:
                ancho= float(input("Ancho del estímulo (de 0 a 100): "))
                if 0 <= ancho <= 100:
                    break
                else:
                    print("Por favor, el número debe estar entre 0 y 100: ")
            except ValueError:
                print("Por favor, introduce un número válido (usa punto para decimales).")
        if presion < 5:
            presion= 0 # Para eliminar señales innecesarias, como estímulos con una presión insignificante o "ruido", la piel tiene un umbral de disparo de señal.
        if ancho < 5:
            ancho= 5 # La piel tiene un umbral de discriminación táctil de 5mm.
        self.touch= presion*np.exp(-0.5*((self.piel-posicion)/ancho)**2) # El estímulo táctil se representa mediante una función gaussiana.
        print("¡Estímulo generado!") 
        return self.touch
    def graficaest(self):
        x=self.piel
        plt.plot(x, -1*self.touch, label="Estímulo Táctil", color="blue", lw=2)

class red:
    def __init__(self):
        self.inhibicion_lat= np.array([0.9, 1.5, -6, 1.5, 0.9])
        self.resultado_final= None 
        self.historial_pinchazos= [] # Historial con los pinchazos recibidos.
        self.contadorest= 0
    def procesar_señal(self, señal_input):
        self.contadorest= self.contadorest + 1
        if self.contadorest > 1:
            # Por cada repetición, la respuesta baja (habituación). Esto ocurre en la mecanorrecepción, no en la nocicepción (que en el sistema nervioso se procesa en una vía diferente).
            self.factor_habituacion= max(0.1, 1.0 - (self.contadorest - 1) * 0.05) # La sensibilidad disminuye un 5% con cada repetición, sin llegar ser más pequeña que un 10%.
            print("Habituación activada: Respuesta reducida al", self.factor_habituacion*100, "%")
        else:
            self.factor_habituacion= 1.0 # Empieza al 100% de sensibilidad.
        # Procesamiento con el factor de habituación:
        self.resultado_final= convolve(señal_input, self.inhibicion_lat, mode="same") * self.factor_habituacion # En esta línea del código se aplica tanto la inhibición lateral como la haituación.
        # Diccionarios para guardar el historial de señales generadas:
        self.historial_pinchazos.append({
            "contador": self.contadorest,
            "presion":piel.evaluar_presion,
            "posicion":piel.evaluar_posicion,
            "señal": self.resultado_final.copy(),
            "habituacion": self.factor_habituacion,
            })
        return self.factor_habituacion
    def graficared(self, x):
        plt.plot(x, self.resultado_final, label="Señal Procesada (Red)", color="green", lw=2)
    def resetear_sistema(self):
        self.factor_habituacion= 1
        self.historial_pinchazos= []
        self.contadorest= 0
    def mostrar_resumen(self):
        print("RESUMEN DE ACTIVIDAD:")                  
        for d in self.historial_pinchazos:
            if d["presion"]>66:
                tipo_señal= "Sí"
            else:
                tipo_señal= "No"
            print("Pinchazo:", d["contador"], "  Presión:",d["presion"], "  Sensibilidad:", d["habituacion"], "  Nocicepción:", tipo_señal)

class nocicepcion:
    def __init__(self):
        self.umbral_dolor= 66.0 # A partir de esta presión se generará una señal nociceptiva (es decir, que le provocará dolor a la piel).
        self.registro_alertas= [] # Historial de señales nociceptivas.
        self.estado_alerta= False
        self.contador_alertas= 0
    def evaluar_daño(self, presion_input):
        if presion_input > self.umbral_dolor:
            self.estado_alerta = True
            mensaje = f"¡ALERTA! Nociceptores activados. Presión de {presion_input} es peligrosa."
            print(mensaje)
            self.registro_alertas.append(mensaje) # Se añade al historial.
            self.contador_alertas= self.contador_alertas + 1
        else:
            self.estado_alerta= False
            print("Presión dentro del rango seguro (Mecanorrecepción pura).")
    def graficar_alerta(self): # Gráfica para la nocicepción:
        if self.estado_alerta:
            plt.axhspan(-1*self.umbral_dolor, -500, color="red", alpha=0.1, label="Zona de Dolor") # Sombreado de dolor.
            plt.scatter(piel.evaluar_posicion, -1*piel.evaluar_presion, color="red", s=30, zorder=5, label="Señal Nociceptiva") # Señal nociceptiva en el punto donde se ha aplicado el estímulo.      

# Instancias:
piel= estimulo()
red_neuronal= red()
sistema_dolor= nocicepcion()

# Generación del estímulo:
presion_usuario= piel.pinchazo()

# Procesamiento del estímulo por la red neuronal (inhibición lateral y habituación):
red_neuronal.procesar_señal(piel.touch)

# Procesamiento de dolor:
sistema_dolor.evaluar_daño(piel.evaluar_presion) 

# Gráfica:
plt.figure(figsize=(10, 6))
piel.graficaest() # Línea azul (estímulo).
red_neuronal.graficared(piel.piel) # Línea verde (señal generada por la red neuronal).
sistema_dolor.graficar_alerta() # Datos de la nocicepción (si aplica).
plt.axhline(-sistema_dolor.umbral_dolor, color="orange", linestyle="--", label="Umbral Nociceptivo")
plt.title(f"Estímulo nº {red_neuronal.contadorest}. Sensibilidad: {red_neuronal.factor_habituacion*100:.0f}%.")
plt.ylim(-225, 10)
plt.legend()
plt.show()

while True:
    print("1. Generar nuevo estímulo (pinchazo).")
    print("2. Resetear habituación.")
    print("3. Ver historial de datos.")
    print("4. Salir.")
    
    opcion= input("Selecciona una opción: ")

    if opcion== "1":
        # Generación del estímulo:
        presion_leida = piel.pinchazo()
            
        # Procesamiento del estímulo por la red neuronal (inhibición lateral y habituación):
        h_actual = red_neuronal.procesar_señal(piel.touch)
            
        # Procesamiento del dolor:
        sistema_dolor.evaluar_daño(piel.evaluar_presion)
            
        # Gráfica:
        plt.figure(figsize=(10, 5))
        piel.graficaest() # Línea azul (estímulo).
        red_neuronal.graficared(piel.piel) # Línea verde (señal generada por la red neuronal).
        if piel.evaluar_presion> sistema_dolor.umbral_dolor: # Representación de la nocicepción (si hay):
            plt.axhspan(-1*sistema_dolor.umbral_dolor, -500, color="red", alpha=0.1, label="Zona Nociceptiva") # Sombreado de dolor.
            plt.scatter(piel.evaluar_posicion, -1*piel.evaluar_presion, color="red", s=30, zorder=5, label="Señal Nociceptiva") # Señal nociceptiva en el punto donde se ha aplicado el estímulo.
        plt.title(f"Estímulo nº {red_neuronal.contadorest}. Sensibilidad: {red_neuronal.factor_habituacion*100:.0f}%.")
        plt.axhline(-sistema_dolor.umbral_dolor, color="orange", linestyle="--", label="Umbral Nociceptivo")
        plt.ylim(-225, 10)
        plt.legend()
        plt.show()

    elif opcion== "2":  
        red_neuronal.resetear_sistema()

    elif opcion== "3":
        red_neuronal.mostrar_resumen()
        print("Total de señales generadas:",red_neuronal.contadorest, "  Total de señales nociceptivas:", sistema_dolor.contador_alertas)
        plt.figure(figsize=(10, 5))
        plt.axhline(-1*sistema_dolor.umbral_dolor, color="orange", linestyle="--", label="Umbral Nociceptivo")
        for dato in red_neuronal.historial_pinchazos:
            linea,=plt.plot(piel.piel, dato["señal"], label=f"Estímulo {dato["contador"]}") # Representación de las señales generadas por la red (no el estímulo).
            color_asignado = linea.get_color()
            plt.scatter(dato["posicion"], -1 * dato["presion"], color=color_asignado, s=30) # Representación del estímulo mediante un punto (así se puede evaluar si hubo nocicepción o no).   
        plt.title("Comparativa de todas las señales registradas.")
        plt.ylim(-225, 10)
        plt.legend()
        plt.show()

    elif opcion== "4":
        print("Cerrando el programa.")
        break

    else:
        print("Por favor, introduce una opción válida.")