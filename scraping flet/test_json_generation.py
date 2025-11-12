#!/usr/bin/env python3
"""
Script de prueba para verificar la generación de archivos JSON por búsqueda
"""

import json
import os
import glob
from datetime import datetime

def test_json_generation():
    """Prueba la generación de archivos JSON"""
    
    print("🔍 Verificando archivos JSON existentes...")
    
    # Buscar todos los archivos JSON en el directorio actual
    archivos_json = glob.glob("*.json")
    
    if not archivos_json:
        print("❌ No se encontraron archivos JSON")
        return False
    
    print(f"📁 Se encontraron {len(archivos_json)} archivos JSON:")
    
    for archivo in archivos_json:
        try:
            # Obtener información del archivo
            tamano = os.path.getsize(archivo)
            fecha_mod = datetime.fromtimestamp(os.path.getmtime(archivo))
            
            # Leer y validar el contenido JSON
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = json.load(f)
            
            # Verificar que el JSON tenga la estructura esperada
            if isinstance(contenido, list):
                num_resultados = len(contenido)
                print(f"  📄 {archivo} - {num_resultados} resultados - {tamano} bytes - {fecha_mod.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Mostrar ejemplo del primer resultado si existe
                if contenido:
                    primer_resultado = contenido[0]
                    print(f"     📋 Primer resultado: {primer_resultado.get('nombre', 'Sin nombre')}")
                    print(f"     📞 Teléfono: {primer_resultado.get('telefono', 'N/A')}")
                    print(f"     📍 Dirección: {primer_resultado.get('direccion', 'N/A')}")
            else:
                print(f"  ⚠️ {archivo} - Formato inesperado (no es una lista)")
                
        except json.JSONDecodeError:
            print(f"  ❌ {archivo} - Error al leer JSON")
        except Exception as e:
            print(f"  ❌ {archivo} - Error: {str(e)}")
    
    # Verificar que haya archivos con resultados
    archivos_con_resultados = []
    for archivo in archivos_json:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = json.load(f)
            if isinstance(contenido, list) and len(contenido) > 0:
                archivos_con_resultados.append(archivo)
        except:
            pass
    
    print(f"\n✅ Resumen:")
    print(f"   📊 Total de archivos JSON: {len(archivos_json)}")
    print(f"   📋 Archivos con resultados: {len(archivos_con_resultados)}")
    
    if len(archivos_con_resultados) > 1:
        print(f"   🎉 ¡Éxito! Se están generando múltiples archivos JSON por búsqueda")
    elif len(archivos_con_resultados) == 1:
        print(f"   ℹ️ Solo se encontró un archivo con resultados")
    else:
        print(f"   ❌ No se encontraron archivos con resultados válidos")
    
    return len(archivos_con_resultados) > 0

if __name__ == "__main__":
    print("🧪 Iniciando prueba de generación de JSON...")
    print("=" * 50)
    
    exito = test_json_generation()
    
    print("=" * 50)
    if exito:
        print("✅ Prueba completada exitosamente")
    else:
        print("❌ Prueba fallida")
    
    input("\nPresiona Enter para salir...")