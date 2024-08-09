import random

def procesar_linea(linea):
    # Eliminar los espacios en blanco al inicio y final de la línea
    linea = linea.strip()
    
    # Dividir la línea en dos partes: antes y después de la coma
    partes = linea.split(',')
    numeros = partes[:-1]
    sufijo = partes[-1]
    
    # Eliminar el sufijo :0:0:0:0: del último elemento (esto depende del formato de tus datos)
    sufijo = sufijo.replace(':0:0:0:0:', '')
    
    del numeros[4]
    del numeros[3]
    del numeros[1]
    
    numeros[1] = float(numeros[1]) / 1000
    numeros[1] = str(numeros[1])
    
    # Convertir numeros[0] a entero para compararlo en las condiciones
    numeros[0] = int(numeros[0])
    
    if numeros[0] == 64:
        numeros[0] = 1
    elif numeros[0] == 192:
        numeros[0] = 2
    elif numeros[0] == 320:
        numeros[0] = 3
    elif numeros[0] == 448:
        numeros[0] = 4
    
    # Convertir numeros[0] a cadena y añadir espacio al principio
    numeros[0] = " " + str(numeros[0])
    
    # Reconstruir la línea
    nueva_linea = ''.join(numeros[1] + numeros[0])
    return nueva_linea
    
def procesar_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    
    lineas_procesadas = [procesar_linea(linea) for linea in lineas]
    
    with open('archivo_procesado.txt', 'w') as archivo:
        archivo.write('\n'.join(lineas_procesadas))

# Ejemplo de uso
procesar_archivo('archivo.txt')
