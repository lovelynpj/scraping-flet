#!/usr/bin/env python3
"""
Script para verificar las carpetas y archivos creados por el scraper
"""

import os
import json
import glob
from datetime import datetime

def verificar_carpetas():
    """Verifica las carpetas y archivos generados"""
    
    print("📂 Verificando carpetas y archivos...")
    print("=" * 60)
    
    # Obtener el directorio actual
    directorio_actual = os.getcwd()
    print(f"📍 Directorio actual: {directorio_actual}")
    print()
    
    # Buscar todas las carpetas que puedan ser de búsquedas
    carpetas = []
    for item in os.listdir('.'):
        if os.path.isdir(item):
            # Verificar si contiene archivos de resultados
            archivos = os.listdir(item)
            tiene_archivos_resultados = any(
                archivo.endswith(('.json', '.csv', '.txt')) and 
                ('resultados' in archivo.lower() or 'reporte' in archivo.lower())
                for archivo in archivos
            )
            if tiene_archivos_resultados:
                carpetas.append((item, archivos))
    
    if not carpetas:
        print("❌ No se encontraron carpetas con resultados de búsquedas")
        return
    
    print(f"✅ Se encontraron {len(carpetas)} carpetas con resultados:")
    print()
    
    for nombre_carpeta, archivos in carpetas:
        print(f"📁 {nombre_carpeta}")
        print(f"   📄 Archivos ({len(archivos)}):")
        
        for archivo in sorted(archivos):
            ruta_completa = os.path.join(nombre_carpeta, archivo)
            tamaño = os.path.getsize(ruta_completa)
            
            # Determinar tipo de archivo
            if archivo.endswith('.json'):
                tipo = "📊 JSON"
            elif archivo.endswith('.csv'):
                if 'CON_TELEFONO' in archivo:
                    tipo = "📞 CSV con teléfono"
                else:
                    tipo = "📋 CSV"
            elif archivo.endswith('.txt'):
                tipo = "📝 Reporte"
            else:
                tipo = "📄 Archivo"
            
            print(f"      {tipo} - {archivo} ({tamaño} bytes)")
            
            # Si es JSON, mostrar cantidad de resultados
            if archivo.endswith('.json'):
                try:
                    with open(ruta_completa, 'r', encoding='utf-8') as f:
                        datos = json.load(f)
                        if isinstance(datos, list):
                            print(f"         ↳ Contiene {len(datos)} resultados")
                except Exception as e:
                    print(f"         ↳ Error al leer JSON: {str(e)}")
        
        print()
    
    # Buscar archivos sueltos (sin carpeta)
    print("🔍 Buscando archivos sueltos...")
    archivos_sueltos = []
    for archivo in glob.glob("*.json") + glob.glob("*.csv") + glob.glob("*.txt"):
        if any(archivo in archivos for _, archivos in carpetas):
            continue
        archivos_sueltos.append(archivo)
    
    if archivos_sueltos:
        print(f"⚠️  Se encontraron {len(archivos_sueltos)} archivos sueltos:")
        for archivo in archivos_sueltos:
            print(f"   📄 {archivo}")
    else:
        print("✅ No hay archivos sueltos, todo está organizado en carpetas")
    
    print()
    print("=" * 60)
    print("📊 Resumen:")
    total_carpetas = len(carpetas)
    total_archivos = sum(len(archivos) for _, archivos in carpetas)
    print(f"📁 Carpetas de búsqueda: {total_carpetas}")
    print(f"📄 Archivos totales: {total_archivos}")
    print(f"📁 Archivos sueltos: {len(archivos_sueltos)}")

if __name__ == "__main__":
    verificar_carpetas()