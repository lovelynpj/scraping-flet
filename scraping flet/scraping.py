import flet as ft
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv
from datetime import datetime
import threading
import os

# 🎨 PALETA DE COLORES VIBRANTES
COLORS = {
    'primary': '#FF6B6B',      # Rojo coral
    'secondary': '#4ECDC4',    # Turquesa
    'success': '#95E1D3',      # Verde menta
    'warning': '#FFE66D',      # Amarillo
    'info': '#6C5CE7',         # Púrpura
    'accent': '#FF85A2',       # Rosa
    'dark': '#1A1A2E',         # Oscuro
    'darker': '#0F0F1E',       # Más oscuro
    'light': '#DFE6E9',        # Claro
    'card': '#16213E',         # Card
}


class GoogleMapsScraperUI:
    """🗺️ Scraper de Google Maps con UI en Flet"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.resultados = []
        self.driver = None
        self.scraping_activo = False
        
        # Configurar página
        self.page.title = "🗺️ Google Maps Scraper Pro"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window_width = 1400
        self.page.window_height = 900
        self.page.window_resizable = True
        self.page.bgcolor = COLORS['darker']
        
        # Referencias a controles
        self.query_input = None
        self.location_input = None
        self.max_results_input = None
        self.wait_time_input = None
        self.headless_switch = None
        self.log_area = None
        self.progress_bar = None
        self.progress_text = None
        self.stats_container = None
        self.btn_iniciar = None
        self.btn_detener = None
        self.resultados_lista = None
        
        self.crear_ui()
    
    def crear_ui(self):
        """🎨 Crea la interfaz principal"""
        
        # Header con gradiente
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MAP, size=50, color=COLORS['secondary']),
                    ft.Column([
                        ft.Text(
                            "GOOGLE MAPS SCRAPER",
                            size=36,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS['secondary'],
                            font_family="Consolas"
                        ),
                        ft.Text(
                            "Extractor Profesional de Datos",
                            size=14,
                            color=COLORS['light'],
                            italic=True
                        ),
                    ], spacing=0),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=30,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLORS['dark'], COLORS['card']]
            ),
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
        )
        
        # Panel de configuración
        config_panel = self._crear_panel_configuracion()
        
        # Panel de control
        control_panel = self._crear_panel_control()
        
        # Panel de progreso
        progress_panel = self._crear_panel_progreso()
        
        # Panel de resultados
        resultados_panel = self._crear_panel_resultados()
        
        # Layout principal
        main_content = ft.Row([
            # Columna izquierda (Config + Control)
            ft.Container(
                content=ft.Column([
                    config_panel,
                    ft.Container(height=20),
                    control_panel,
                ], scroll=ft.ScrollMode.AUTO),
                width=500,
                padding=20,
            ),
            
            # Columna derecha (Progreso + Resultados)
            ft.Container(
                content=ft.Column([
                    progress_panel,
                    ft.Container(height=20),
                    resultados_panel,
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                expand=True,
                padding=20,
            ),
        ], expand=True)
        
        # Agregar todo a la página
        self.page.add(
            ft.Column([
                header,
                main_content,
            ], spacing=0, expand=True)
        )
    
    def _crear_panel_configuracion(self):
        """⚙️ Panel de configuración"""
        
        self.query_input = ft.TextField(
            label="🔍 ¿Qué deseas buscar?",
            hint_text="Ej: escuelas primarias, restaurantes",
            value="escuelas primarias",
            border_color=COLORS['secondary'],
            focused_border_color=COLORS['primary'],
            text_style=ft.TextStyle(size=14),
            color=COLORS['light']
        )
        
        self.location_input = ft.TextField(
            label="📍 ¿Dónde?",
            hint_text="Ej: Buenos Aires, Argentina",
            value="Barrio General Paz, Córdoba, Argentina",
            border_color=COLORS['secondary'],
            focused_border_color=COLORS['primary'],
            text_style=ft.TextStyle(size=14),
            color=COLORS['light']
        )
        
        self.max_results_input = ft.TextField(
            label="📊 Máximo de resultados",
            value="25",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200,
            border_color=COLORS['secondary'],
            focused_border_color=COLORS['primary'],
            color=COLORS['light']
        )
        
        self.wait_time_input = ft.TextField(
            label="⏱️ Tiempo de espera (seg)",
            value="3",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200,
            border_color=COLORS['secondary'],
            focused_border_color=COLORS['primary'],
            color=COLORS['light']
        )
        
        self.headless_switch = ft.Switch(
            label="🕶️ Modo invisible",
            value=False,
            active_color=COLORS['success'],
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SETTINGS, color=COLORS['secondary'], size=30),
                    ft.Text(
                        "CONFIGURACIÓN",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS['secondary']
                    ),
                ]),
                ft.Divider(color=COLORS['secondary'], height=20),
                self.query_input,
                ft.Container(height=10),
                self.location_input,
                ft.Container(height=10),
                ft.Row([
                    self.max_results_input,
                    self.wait_time_input,
                ], spacing=20),
                ft.Container(height=10),
                self.headless_switch,
            ]),
            bgcolor=COLORS['card'],
            padding=25,
            border_radius=15,
            border=ft.border.all(2, COLORS['secondary']),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, COLORS['secondary']),
                offset=ft.Offset(0, 4),
            )
        )
    
    def _crear_panel_control(self):
        """🎮 Panel de control"""
        
        self.btn_iniciar = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.PLAY_ARROW, size=24),
                ft.Text("INICIAR SCRAPING", size=16, weight=ft.FontWeight.BOLD),
            ], tight=True),
            on_click=self._iniciar_scraping,
            style=ft.ButtonStyle(
                bgcolor=COLORS['success'],
                color=COLORS['dark'],
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=220,
            height=60,
        )
        
        self.btn_detener = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.STOP, size=24),
                ft.Text("DETENER", size=16, weight=ft.FontWeight.BOLD),
            ], tight=True),
            on_click=self._detener_scraping,
            style=ft.ButtonStyle(
                bgcolor=COLORS['primary'],
                color=COLORS['light'],
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=220,
            height=60,
            disabled=True,
        )
        
        btn_guardar = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.SAVE, size=24),
                ft.Text("GUARDAR", size=16, weight=ft.FontWeight.BOLD),
            ], tight=True),
            on_click=self._guardar_resultados,
            style=ft.ButtonStyle(
                bgcolor=COLORS['info'],
                color=COLORS['light'],
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            width=220,
            height=60,
        )
        
        btn_limpiar = ft.OutlinedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.CLEAR_ALL, size=24),
                ft.Text("LIMPIAR", size=16, weight=ft.FontWeight.BOLD),
            ], tight=True),
            on_click=self._limpiar_todo,
            style=ft.ButtonStyle(
                color=COLORS['warning'],
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(2, COLORS['warning'])
            ),
            width=220,
            height=60,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CONTROL_CAMERA, color=COLORS['accent'], size=30),
                    ft.Text(
                        "CONTROLES",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS['accent']
                    ),
                ]),
                ft.Divider(color=COLORS['accent'], height=20),
                self.btn_iniciar,
                ft.Container(height=10),
                self.btn_detener,
                ft.Container(height=10),
                btn_guardar,
                ft.Container(height=10),
                btn_limpiar,
            ]),
            bgcolor=COLORS['card'],
            padding=25,
            border_radius=15,
            border=ft.border.all(2, COLORS['accent']),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, COLORS['accent']),
                offset=ft.Offset(0, 4),
            )
        )
    
    def _crear_panel_progreso(self):
        """📊 Panel de progreso"""
        
        self.progress_bar = ft.ProgressBar(
            width=float('inf'),
            color=COLORS['success'],
            bgcolor=COLORS['dark'],
            value=0,
            height=15,
            border_radius=10,
        )
        
        self.progress_text = ft.Text(
            "Esperando inicio...",
            size=14,
            color=COLORS['light'],
            weight=ft.FontWeight.BOLD
        )
        
        self.stats_container = ft.Row([
            self._crear_stat_card("Total", "0", ft.Icons.ANALYTICS, COLORS['info']),
            self._crear_stat_card("Con Tel", "0", ft.Icons.PHONE, COLORS['success']),
            self._crear_stat_card("Sin Tel", "0", ft.Icons.PHONE_DISABLED, COLORS['primary']),
        ], spacing=15, wrap=True)
        
        self.log_area = ft.ListView(
            spacing=5,
            padding=15,
            auto_scroll=True,
            height=250,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SHOW_CHART, color=COLORS['warning'], size=30),
                    ft.Text(
                        "PROGRESO Y ESTADÍSTICAS",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS['warning']
                    ),
                ]),
                ft.Divider(color=COLORS['warning'], height=20),
                self.progress_text,
                ft.Container(height=10),
                self.progress_bar,
                ft.Container(height=20),
                self.stats_container,
                ft.Container(height=20),
                ft.Text("📋 Log de Actividad:", size=16, color=COLORS['light'], weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.Container(
                    content=self.log_area,
                    bgcolor=COLORS['dark'],
                    border_radius=10,
                    border=ft.border.all(1, COLORS['warning']),
                ),
            ]),
            bgcolor=COLORS['card'],
            padding=25,
            border_radius=15,
            border=ft.border.all(2, COLORS['warning']),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, COLORS['warning']),
                offset=ft.Offset(0, 4),
            )
        )
    
    def _crear_stat_card(self, titulo, valor, icono, color):
        """Crea una tarjeta de estadística"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, color=color, size=40),
                ft.Text(titulo, size=14, color=COLORS['light']),
                ft.Text(valor, size=28, weight=ft.FontWeight.BOLD, color=color),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=COLORS['dark'],
            padding=20,
            border_radius=10,
            width=150,
            height=140,
            border=ft.border.all(2, color),
        )
    
    def _crear_panel_resultados(self):
        """📋 Panel de resultados"""
        
        self.resultados_lista = ft.ListView(
            spacing=10,
            padding=15,
            auto_scroll=False,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIST_ALT, color=COLORS['success'], size=30),
                    ft.Text(
                        "RESULTADOS EXTRAÍDOS",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS['success']
                    ),
                ]),
                ft.Divider(color=COLORS['success'], height=20),
                ft.Container(
                    content=self.resultados_lista,
                    bgcolor=COLORS['dark'],
                    border_radius=10,
                    border=ft.border.all(1, COLORS['success']),
                    height=500,
                ),
            ]),
            bgcolor=COLORS['card'],
            padding=25,
            border_radius=15,
            border=ft.border.all(2, COLORS['success']),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, COLORS['success']),
                offset=ft.Offset(0, 4),
            )
        )
    
    def _log(self, mensaje, color=None, icono="•"):
        """Agrega un mensaje al log (seguro para threading)"""
        color = color or COLORS['light']
        
        try:
            log_entry = ft.Container(
                content=ft.Row([
                    ft.Text(icono, size=16, color=color),
                    ft.Text(mensaje, size=12, color=color),
                ], spacing=10),
                padding=5,
            )
            
            # Agregar al log y actualizar UI directamente
            self.log_area.controls.append(log_entry)
            
            # Limitar a 100 mensajes para no sobrecargar
            if len(self.log_area.controls) > 100:
                self.log_area.controls.pop(0)
            
            try:
                self.page.update()
            except Exception as e:
                print(f"Error actualizando UI en _log: {e}")
                
        except Exception as e:
            # Si falla el log en UI, al menos lo imprimimos
            print(f"{icono} {mensaje}")
            print(f"Error en _log: {e}")
    
    def _actualizar_stats(self):
        """Actualiza las estadísticas (seguro para threading)"""
        try:
            total = len(self.resultados)
            con_tel = sum(1 for r in self.resultados if r.get('telefono') != "N/A")
            sin_tel = total - con_tel
            
            # Actualizar estadísticas directamente
            if hasattr(self, 'stats_container') and self.stats_container.controls:
                self.stats_container.controls[0].content.controls[2].value = str(total)
                self.stats_container.controls[1].content.controls[2].value = str(con_tel)
                self.stats_container.controls[2].content.controls[2].value = str(sin_tel)
                self._actualizar_progress_ui()
                
        except Exception as e:
            print(f"Error actualizando stats: {e}")
    
    def _agregar_resultado_ui(self, info, indice):
        """Agrega un resultado a la UI (seguro para threading)"""
        try:
            # Color del borde según tenga teléfono o no
            border_color = COLORS['success'] if info.get('telefono') != "N/A" else COLORS['primary']
            
            resultado_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(
                            ft.Icons.PLACE if info.get('telefono') != "N/A" else ft.Icons.PLACE_OUTLINED,
                            color=border_color,
                            size=24
                        ),
                        ft.Text(
                            f"#{indice}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=border_color
                        ),
                        ft.Text(
                            info.get('nombre', 'N/A'),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS['light'],
                            expand=True,
                        ),
                    ]),
                    ft.Divider(height=5, color=border_color),
                    ft.Row([
                        ft.Icon(ft.Icons.CATEGORY, size=16, color=COLORS['secondary']),
                        ft.Text(info.get('tipo', 'N/A'), size=12, color=COLORS['light']),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, size=16, color=COLORS['secondary']),
                        ft.Text(
                            info.get('direccion', 'N/A'),
                            size=12,
                            color=COLORS['light'],
                            expand=True,
                            no_wrap=False
                        ),
                    ]),
                    ft.Row([
                        ft.Icon(
                            ft.Icons.PHONE if info.get('telefono') != "N/A" else ft.Icons.PHONE_DISABLED,
                            size=16,
                            color=COLORS['success'] if info.get('telefono') != "N/A" else COLORS['primary']
                        ),
                        ft.Text(
                            info.get('telefono', 'N/A'),
                            size=12,
                            color=COLORS['success'] if info.get('telefono') != "N/A" else COLORS['primary'],
                            weight=ft.FontWeight.BOLD
                        ),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.STAR, size=16, color=COLORS['warning']),
                        ft.Text(
                            f"{info.get('rating', 'N/A')} ({info.get('cantidad_reseñas', 'N/A')})",
                            size=12,
                            color=COLORS['warning']
                        ),
                    ]) if info.get('rating') != "N/A" else ft.Container(),
                ], spacing=8),
                bgcolor=COLORS['dark'],
                padding=15,
                border_radius=10,
                border=ft.border.all(2, border_color),
            )
            
            # Agregar resultado directamente
            self.resultados_lista.controls.append(resultado_card)
            self._actualizar_progress_ui()
                
        except Exception as e:
            print(f"Error agregando resultado a UI: {e}")

    def _actualizar_progress_ui(self):
        """Actualiza la UI del progreso de forma segura"""
        try:
            # En Flet, page.update() es seguro desde cualquier hilo
            self.page.update()
        except Exception as e:
            print(f"Error actualizando UI: {e}")
    
    def _iniciar_scraping(self, e):
        """🚀 Inicia el proceso de scraping"""
        if self.scraping_activo:
            return
        
        # Validar inputs
        if not self.query_input.value or not self.location_input.value:
            self._mostrar_alerta("⚠️ Error", "Debes completar la búsqueda y ubicación", COLORS['warning'])
            return
        
        # Cambiar estado de botones
        self.btn_iniciar.disabled = True
        self.btn_detener.disabled = False
        self.scraping_activo = True
        self._actualizar_progress_ui()
        
        # Limpiar resultados anteriores
        self.resultados = []
        self.resultados_lista.controls.clear()
        
        # Ejecutar en thread separado
        thread = threading.Thread(target=self._ejecutar_scraping, daemon=True)
        thread.start()
    
    def _detener_scraping(self, e):
        """🛑 Detiene el scraping"""
        self.scraping_activo = False
        self._log("🛑 Deteniendo scraping...", COLORS['warning'], "⚠️")
        
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
        self.btn_iniciar.disabled = False
        self.btn_detener.disabled = True
        self._actualizar_progress_ui()
    
    def _ejecutar_scraping(self):
        """Ejecuta el scraping (en thread separado)"""
        try:
            # Obtener parámetros
            query = self.query_input.value
            location = self.location_input.value
            max_results = int(self.max_results_input.value or 25)
            wait_time = int(self.wait_time_input.value or 3)
            headless = self.headless_switch.value

            self._log(f"🚀 Iniciando scraping...", COLORS['success'], "▶️")
            self._log(f"🔍 Búsqueda: {query}", COLORS['secondary'])
            self._log(f"📍 Ubicación: {location}", COLORS['secondary'])

            # Configurar navegador
            self.progress_text.value = "⚙️ Configurando navegador..."
            self._actualizar_progress_ui()
            
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            if headless:
                options.add_argument('--headless')
                self._log("🕶️ Modo invisible activado", COLORS['info'])
            
            self.driver = webdriver.Chrome(options=options)
            self._log("✅ Navegador configurado", COLORS['success'], "✓")
            
            # Abrir Google Maps
            self.progress_text.value = "🌍 Abriendo Google Maps..."
            self._actualizar_progress_ui()
            
            search_query = f"{query} {location}"
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            self.driver.get(url)
            time.sleep(wait_time + 2)
            
            self._log("✅ Google Maps cargado", COLORS['success'], "✓")
            
            # Esperar resultados
            self.progress_text.value = "⏳ Esperando resultados..."
            self._actualizar_progress_ui()
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
                )
                self._log("✅ Resultados encontrados", COLORS['success'], "✓")
            except:
                self._log("⚠️ Panel de resultados no encontrado", COLORS['warning'], "⚠️")
            
            # Scroll
            self.progress_text.value = "📜 Cargando más resultados..."
            self._actualizar_progress_ui()
            
            try:
                scrollable_div = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
                for i in range(6):
                    if not self.scraping_activo:
                        break
                    self.driver.execute_script(
                        'arguments[0].scrollTop = arguments[0].scrollHeight',
                        scrollable_div
                    )
                    self.progress_bar.value = (i + 1) / 6
                    self._actualizar_progress_ui()
                    time.sleep(2)
                
                self._log("✅ Scroll completado", COLORS['success'], "✓")
            except Exception as ex:
                self._log(f"⚠️ Error en scroll: {str(ex)}", COLORS['warning'], "⚠️")
            
            # Buscar lugares
            self.progress_text.value = "🔎 Buscando lugares..."
            self._actualizar_progress_ui()
            
            lugares = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
            total_encontrados = len(lugares)
            
            if total_encontrados == 0:
                self._log("❌ No se encontraron resultados", COLORS['primary'], "✗")
                return
            
            self._log(f"✨ Se encontraron {total_encontrados} lugares", COLORS['success'], "★")
            
            # Extraer información
            lugares_a_procesar = min(max_results, total_encontrados)
            self.progress_text.value = f"📊 Extrayendo {lugares_a_procesar} lugares..."
            self._actualizar_progress_ui()
            
            # Lista para almacenar resultados de esta búsqueda específica
            resultados_busqueda_actual = []
            
            for i, lugar in enumerate(lugares[:max_results]):
                if not self.scraping_activo:
                    break
                
                try:
                    # Actualizar progreso
                    progreso = (i + 1) / lugares_a_procesar
                    self.progress_bar.value = progreso
                    self.progress_text.value = f"📊 Extrayendo {i + 1}/{lugares_a_procesar}..."
                    self._actualizar_progress_ui()
                    
                    # Click
                    self.driver.execute_script("arguments[0].click();", lugar)
                    time.sleep(wait_time)
                    
                    # Esperar carga
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))
                        )
                    except:
                        continue
                    
                    # Extraer info
                    info = self._extraer_informacion()
                    self.resultados.append(info)
                    resultados_busqueda_actual.append(info)
                    
                    # Agregar a UI
                    self._agregar_resultado_ui(info, len(self.resultados))
                    self._actualizar_stats()
                    
                    self._log(f"✓ Extraído: {info.get('nombre', 'N/A')}", COLORS['success'], "•")
                    
                except Exception as ex:
                    self._log(f"✗ Error en lugar {i + 1}: {str(ex)}", COLORS['primary'], "✗")
                    continue
            
            # Guardar resultados automáticamente después de cada búsqueda
            if resultados_busqueda_actual:
                self._guardar_resultados_automatico(query, location, resultados_busqueda_actual)
            
            # Finalizar
            self.progress_bar.value = 1.0
            self.progress_text.value = f"✅ ¡Completado! {len(self.resultados)} resultados"
            self._log(f"🎉 Scraping completado: {len(self.resultados)} resultados", COLORS['success'], "★")
            
        except Exception as e:
            try:
                self._log(f"❌ Error crítico: {str(e)}", COLORS['primary'], "✗")
            except:
                print(f"❌ Error crítico: {str(e)}")
        
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    try:
                        self._log("🔒 Navegador cerrado", COLORS['info'], "•")
                    except:
                        print("🔒 Navegador cerrado")
                except:
                    pass
            
            self.scraping_activo = False
            self.btn_iniciar.disabled = False
            self.btn_detener.disabled = True
            
            self._actualizar_progress_ui()
    
    def _extraer_informacion(self):
        """Extrae información del lugar actual"""
        info = {}
        
        try:
            info['nombre'] = self.driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
        except:
            info['nombre'] = "N/A"
        
        try:
            info['tipo'] = self.driver.find_element(By.CSS_SELECTOR, "button[jsaction*='category']").text
        except:
            info['tipo'] = "N/A"
        
        try:
            info['direccion'] = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address']").text
        except:
            info['direccion'] = "N/A"
        
        try:
            tel_elem = self.driver.find_element(By.CSS_SELECTOR, "button[data-item-id*='phone']")
            info['telefono'] = tel_elem.get_attribute('data-item-id').replace('phone:tel:', '')
            if not info['telefono']:
                info['telefono'] = tel_elem.text
        except:
            info['telefono'] = "N/A"
        
        try:
            info['website'] = self.driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']").get_attribute('href')
        except:
            info['website'] = "N/A"
        
        try:
            info['rating'] = self.driver.find_element(By.CSS_SELECTOR, "span.ceNzKf").text
        except:
            info['rating'] = "N/A"
        
        try:
            info['cantidad_reseñas'] = self.driver.find_element(By.CSS_SELECTOR, "span.RDApEe").text
        except:
            info['cantidad_reseñas'] = "N/A"
        
        return info
    
    def _guardar_resultados_automatico(self, query, location, resultados_busqueda=None):
        """💾 Guarda los resultados automáticamente después de cada búsqueda en una carpeta"""
        if not resultados_busqueda and not self.resultados:
            return
        
        # Usar resultados específicos de la búsqueda o todos los resultados
        resultados_a_guardar = resultados_busqueda if resultados_busqueda else self.resultados
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Crear nombre de carpeta con la búsqueda del usuario
        nombre_carpeta = f"{query} en {location}"
        # Limpiar el nombre de la carpeta para que sea válido en el sistema de archivos
        nombre_carpeta = "".join(c for c in nombre_carpeta if c.isalnum() or c in (' ', '_', '-', ',')).rstrip()
        nombre_carpeta = nombre_carpeta.replace("  ", " ").strip()
        
        try:
            # Crear la carpeta si no existe
            if not os.path.exists(nombre_carpeta):
                os.makedirs(nombre_carpeta)
                self._log(f"📁 Carpeta creada: {nombre_carpeta}", COLORS['success'], "✓")
            
            con_telefono = [r for r in resultados_a_guardar if r.get('telefono') != "N/A"]
            
            # JSON - Uno por cada búsqueda
            json_file = os.path.join(nombre_carpeta, f"resultados_{timestamp}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(resultados_a_guardar, f, ensure_ascii=False, indent=2)
            
            # CSV completo
            csv_file = os.path.join(nombre_carpeta, f"resultados_{timestamp}.csv")
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if resultados_a_guardar:
                    writer = csv.DictWriter(f, fieldnames=resultados_a_guardar[0].keys())
                    writer.writeheader()
                    writer.writerows(resultados_a_guardar)
            
            # CSV con teléfono
            if con_telefono:
                csv_tel = os.path.join(nombre_carpeta, f"resultados_CON_TELEFONO_{timestamp}.csv")
                with open(csv_tel, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=con_telefono[0].keys())
                    writer.writeheader()
                    writer.writerows(con_telefono)
            
            # TXT Reporte
            txt_file = os.path.join(nombre_carpeta, f"REPORTE_{timestamp}.txt")
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"🗺️  REPORTE: {query.upper()}\n")
                f.write(f"📍 UBICACIÓN: {location}\n")
                f.write(f"📅 FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Total: {len(resultados_a_guardar)}\n")
                f.write(f"Con teléfono: {len(con_telefono)}\n\n")
                f.write("=" * 80 + "\n")
                f.write("LISTADO COMPLETO\n")
                f.write("=" * 80 + "\n\n")
                
                for i, item in enumerate(resultados_a_guardar, 1):
                    f.write(f"{i}. {item['nombre']}\n")
                    f.write(f"   Tipo: {item['tipo']}\n")
                    f.write(f"   Dirección: {item['direccion']}\n")
                    f.write(f"   Teléfono: {item['telefono']}\n")
                    f.write(f"   Website: {item['website']}\n")
                    f.write(f"   Rating: {item['rating']} ({item['cantidad_reseñas']})\n")
                    f.write("\n" + "-" * 80 + "\n\n")
            
            self._log(f"💾 Guardado automático: {len(resultados_a_guardar)} resultados en '{nombre_carpeta}/'", COLORS['success'], "✓")
            self._log(f"📄 Archivos guardados: JSON, CSV, TXT", COLORS['success'], "✓")
            if con_telefono:
                self._log(f"📞 Archivo con teléfonos: resultados_CON_TELEFONO_{timestamp}.csv", COLORS['success'], "✓")
            
        except Exception as ex:
            self._log(f"❌ Error al guardar automáticamente: {str(ex)}", COLORS['primary'], "✗")

    def _guardar_resultados(self, e):
        """💾 Guarda los resultados manualmente"""
        if not self.resultados:
            self._mostrar_alerta("⚠️ Sin datos", "No hay resultados para guardar", COLORS['warning'])
            return
        
        query = self.query_input.value
        location = self.location_input.value
        self._guardar_resultados_automatico(query, location, self.resultados)
        
        self._mostrar_alerta(
            "✅ Guardado",
            f"Se guardaron {len(self.resultados)} resultados en:\n• JSON\n• CSV\n• TXT",
            COLORS['success']
        )
    
    def _limpiar_todo(self, e):
        """🧹 Limpia todos los resultados"""
        self.resultados = []
        self.resultados_lista.controls.clear()
        self.log_area.controls.clear()
        self.progress_bar.value = 0
        self.progress_text.value = "Esperando inicio..."
        
        # Reset stats
        self.stats_container.controls[0].content.controls[2].value = "0"
        self.stats_container.controls[1].content.controls[2].value = "0"
        self.stats_container.controls[2].content.controls[2].value = "0"
        
        self._log("🧹 Todo limpiado", COLORS['info'], "•")
        self._actualizar_progress_ui()
    
    def _mostrar_alerta(self, titulo, mensaje, color):
        """Muestra un diálogo de alerta"""
        def mostrar_dialogo():
            def cerrar_dialogo(e):
                dialogo.open = False
                self._actualizar_progress_ui()
            
            dialogo = ft.AlertDialog(
                title=ft.Text(titulo, color=color, weight=ft.FontWeight.BOLD),
                content=ft.Text(mensaje, color=COLORS['light']),
                actions=[
                    ft.TextButton("OK", on_click=cerrar_dialogo),
                ],
                bgcolor=COLORS['card'],
            )
            
            self.page.dialog = dialogo
            dialogo.open = True
            self._actualizar_progress_ui()
        
        # Verificar si estamos en el hilo principal
        if threading.current_thread() is threading.main_thread():
            mostrar_dialogo()
        else:
            self.page.invoke(mostrar_dialogo)


def main(page: ft.Page):
    """🚀 Función principal"""
    app = GoogleMapsScraperUI(page)


if __name__ == "__main__":
    ft.app(target=main)