#!/usr/bin/env python3
"""
Script de prueba para verificar la creación de carpetas con nombres de búsqueda
"""

import os
import shutil
import time

def test_folder_creation():
    """Prueba la creación de carpetas con nombres de búsqueda"""
    
    print("🧪 Probando creación de carpetas...")
    print("=" * 50)
    
    # Ejemplos de búsquedas
    pruebas = [
        ("shoppings en cordoba", "Cordoba, Argentina"),
        ("escuelas primarias", "Buenos Aires, Argentina"),
        ("restaurantes veganos", "Palermo, Buenos Aires"),
        ("hospitales públicos", "Rosario, Santa Fe"),
    ]
    
    for query, location in pruebas:
        # Crear nombre de carpeta (mismo formato que el programa)
        nombre_carpeta = f"{query} en {location}"
        # Limpiar el nombre de la carpeta para que sea válido
        nombre_carpeta = "".join(c for c in nombre_carpeta if c.isalnum() or c in (' ', '_', '-', ',')).rstrip()
        nombre_carpeta = nombre_carpeta.replace("  ", " ").strip()
        
        print(f"📝 Búsqueda: {query}")
        print(f"📍 Ubicación: {location}")
        print(f"📁 Carpeta resultante: '{nombre_carpeta}'")
        
        # Crear la carpeta
        try:
            if not os.path.exists(nombre_carpeta):
                os.makedirs(nombre_carpeta)
                print(f"✅ Carpeta creada exitosamente")
                
                # Crear archivos de ejemplo dentro de la carpeta
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                archivos_ejemplo = [
                    f"resultados_{timestamp}.json",
                    f"resultados_{timestamp}.csv",
                    f"resultados_CON_TELEFONO_{timestamp}.csv",
                    f"REPORTE_{timestamp}.txt"
                ]
                
                for archivo in archivos_ejemplo:
                    ruta_archivo = os.path.join(nombre_carpeta, archivo)
                    with open(ruta_archivo, 'w', encoding='utf-8') as f:
                        f.write(f"Archivo de ejemplo: {archivo}\n")
                        f.write(f"Búsqueda: {query}\n")
                        f.write(f"Ubicación: {location}\n")
                
                print(f"📄 Archivos de ejemplo creados: {len(archivos_ejemplo)}")
                
            else:
                print(f"ℹ️ La carpeta ya existe")
            
            print()
            
        except Exception as e:
            print(f"❌ Error al crear carpeta: {str(e)}")
            print()
    
    print("=" * 50)
    print("📊 Resumen de carpetas creadas:")
    
    # Listar todas las carpetas creadas
    carpetas_encontradas = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and any(prueba[0] in item for prueba in pruebas):
            archivos = os.listdir(item)
            carpetas_encontradas.append((item, len(archivos)))
    
    if carpetas_encontradas:
        for carpeta, num_archivos in carpetas_encontradas:
            print(f"📁 {carpeta} - {num_archivos} archivos")
    else:
        print("❌ No se encontraron carpetas creadas")
    
    print()
    print("✅ Prueba completada")
    
    # Preguntar si limpiar las carpetas de prueba
    respuesta = input("¿Deseas limpiar las carpetas de prueba? (s/n): ").lower().strip()
    if respuesta == 's':
        for query, location in pruebas:
            nombre_carpeta = f"{query} en {location}"
            nombre_carpeta = "".join(c for c in nombre_carpeta if c.isalnum() or c in (' ', '_', '-', ',')).rstrip()
            nombre_carpeta = nombre_carpeta.replace("  ", " ").strip()
            
            if os.path.exists(nombre_carpeta):
                try:
                    shutil.rmtree(nombre_carpeta)
                    print(f"🗑️ Carpeta eliminada: {nombre_carpeta}")
                except Exception as e:
                    print(f"❌ Error al eliminar {nombre_carpeta}: {str(e)}")

if __name__ == "__main__":
    test_folder_creation()