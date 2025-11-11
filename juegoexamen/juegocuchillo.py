import pygame
import sys
import math
import random
import os

pygame.init()

ANCHO, ALTO = 480, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Cuchillos")
reloj = pygame.time.Clock()
FUENTE = pygame.font.SysFont(None, 40)


ruta_sonido_cuchillo = "juegoexamen/sounds/sonidocuchillo.mp3"
if os.path.exists(ruta_sonido_cuchillo):
    sonido_cuchillo = pygame.mixer.Sound(ruta_sonido_cuchillo)
    sonido_cuchillo.set_volume(0.7)
else:
    sonido_cuchillo = None
    print("No se encontró el sonido del cuchillo:", ruta_sonido_cuchillo)


# --- IMAGEN CUCHILLO ---
ruta_cuchillo = "juegoexamen/imgs/cuchillo1.webp"
if os.path.exists(ruta_cuchillo):
    imagen_cuchillo = pygame.image.load(ruta_cuchillo).convert_alpha()
    imagen_cuchillo = pygame.transform.scale(imagen_cuchillo, (40, 100))
else:
    imagen_cuchillo = None
    print("No se encontró la imagen del cuchillo:", ruta_cuchillo)


# --- MÚSICA DEL JUEGO ---
ruta_musica = "juegoexamen/sounds/musica.mp3"
musica_muted = False
if os.path.exists(ruta_musica):
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
else:
    print("No se encontró la música:", ruta_musica)


# --- CONFIGURACIÓN PRINCIPAL ---
ANCHO, ALTO = 480, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Cuchillos")
reloj = pygame.time.Clock()
FUENTE = pygame.font.SysFont(None, 40)

# --- COLORES ---
BLANCO = (255, 255, 255)
GRIS = (60, 60, 60)
MARRON = (150, 100, 50)
ROJO = (255, 70, 70)
VERDE = (0, 200, 0)
NEGRO = (0, 0, 0)

# --- PARÁMETROS DEL JUEGO ---
CENTRO = (ANCHO // 2, ALTO // 3)
RADIO_TRONCO = 80
LARGO_CUCHILLO = 60
VELOCIDAD_CUCHILLO = 12
CUCHILLOS_INICIALES = 7
ARCHIVO_PUNTAJES = "puntajes.txt"


# --- IMÁGENES ---
ruta_crash = "juegoexamen/imgs/crashmenu.png"
if os.path.exists(ruta_crash):
    imagen_crash = pygame.image.load(ruta_crash).convert_alpha()
    imagen_crash = pygame.transform.scale(imagen_crash, (200, 250))
else:
    imagen_crash = None

imagen_pantallajuego = "juegoexamen/imgs/fondojuego.jpg"
if os.path.exists(imagen_pantallajuego):
    imagen_pantalla = pygame.image.load(imagen_pantallajuego).convert()
    imagen_pantalla = pygame.transform.scale(imagen_pantalla, (ANCHO, ALTO))
else:
    imagen_pantalla = None

ruta_game_over = "juegoexamen/imgs/gameover.webp"
if os.path.exists(ruta_game_over):
    imagen_game_over = pygame.image.load(ruta_game_over).convert_alpha()
    imagen_game_over = pygame.transform.scale(imagen_game_over, (400, 280))
else:
    imagen_game_over = None


#-----IMAGENES PASANDO DE NIVEL------

imagenes_niveles = []
rutas_niveles = [
    "juegoexamen/imgs/fondonivel1.webp",
    "juegoexamen/imgs/fondonivel2.jpg",
    "juegoexamen/imgs/fondonivel3.jpg",
    "juegoexamen/imgs/fondonivel4.jpg",
    "juegoexamen/imgs/fondonivel5.webp"
]

for ruta in rutas_niveles:
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert()
        img = pygame.transform.scale(img, (ANCHO, ALTO))
        imagenes_niveles.append(img)
    else:
        print("No se encontró la imagen:", ruta)



# --- PERSONALIZACIÓN DE CUCHILLOS ---
cuchillos_disponibles = [
    "juegoexamen/imgs/cuchillo2.png",
    "juegoexamen/imgs/cuchillo3.png",
    "juegoexamen/imgs/cuchillo1.webp"
]

indice_cuchillo = 0  # el cuchillo seleccionado

#-----FUNCION PARA ELEGIR CUCHILLO-----
def menu_personalizar():
    global indice_cuchillo, imagen_cuchillo

    en_menu = True
    while en_menu:
        pantalla.fill((40, 40, 40))
        mostrar_texto("ELEGIR CUCHILLO", 60, BLANCO, (ANCHO // 2, 100))

        # Mostrar el cuchillo actual
        try:
            img = pygame.image.load(cuchillos_disponibles[indice_cuchillo]).convert_alpha()
            img = pygame.transform.scale(img, (80, 160))
            pantalla.blit(img, (ANCHO // 2 - 40, 240))
        except:
            mostrar_texto("(Falta imagen)", 30, BLANCO, (ANCHO // 2, 250))

        mostrar_texto("para cambiar cuchillo precionar flecha derecha", 30, BLANCO, (ANCHO // 2, 450))
        mostrar_texto("ESPACIO - volver", 30, BLANCO, (ANCHO // 2, 520))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    indice_cuchillo = (indice_cuchillo - 1) % len(cuchillos_disponibles)
                elif evento.key == pygame.K_RIGHT:
                    indice_cuchillo = (indice_cuchillo + 1) % len(cuchillos_disponibles)
                elif evento.key == pygame.K_SPACE:
                    # Cargar el cuchillo seleccionado para el juego
                    imagen_cuchillo = pygame.image.load(cuchillos_disponibles[indice_cuchillo]).convert_alpha()
                    imagen_cuchillo = pygame.transform.scale(imagen_cuchillo, (40, 100))
                    en_menu = False

#-----FUNCION PARA MOSTRAR UN TEXTO-----
def mostrar_texto(texto, tamano, color, centro):
    fuente = pygame.font.SysFont(None, tamano)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=centro)
    pantalla.blit(superficie, rect)

#-----FUNCION PARA DIBUJAR EL TROCO-------
def dibujar_tronco(angulo):
    pygame.draw.circle(pantalla, MARRON, CENTRO, RADIO_TRONCO)
    extremo = (
        CENTRO[0] + RADIO_TRONCO * math.cos(math.radians(angulo)),
        CENTRO[1] + RADIO_TRONCO * math.sin(math.radians(angulo)),
    )
    pygame.draw.line(pantalla, NEGRO, CENTRO, extremo, 4)

#  --- FUNCIÓN ACTUALIZADA PARA DIBUJAR EL CUCHILLO CON IMAGEN ---
def dibujar_cuchillo(x, y):
    if imagen_cuchillo:
        rect_cuchillo = imagen_cuchillo.get_rect(center=(x, y))
        pantalla.blit(imagen_cuchillo, rect_cuchillo)
    else:
        pygame.draw.rect(pantalla, BLANCO, (x - 2, y, 4, LARGO_CUCHILLO))

def dibujar_cuchillos_clavados(angulos, rotacion):
    for ang_rel in angulos:
        angulo = (ang_rel + rotacion) % 360
        x = CENTRO[0] + (RADIO_TRONCO - 10) * math.cos(math.radians(angulo))
        y = CENTRO[1] + (RADIO_TRONCO - 10) * math.sin(math.radians(angulo))
        if imagen_cuchillo:
            imagen_rotada = pygame.transform.rotate(imagen_cuchillo, -angulo + 90)
            rect = imagen_rotada.get_rect(center=(x, y))
            pantalla.blit(imagen_rotada, rect)
        else:
            extremo = (
                x + LARGO_CUCHILLO * math.cos(math.radians(angulo)),
                y + LARGO_CUCHILLO * math.sin(math.radians(angulo)),
            )
            pygame.draw.line(pantalla, BLANCO, (x, y), extremo, 3)

# --- ANIMACIÓN DE ROTURA DEL TRONCO ---
def animacion_rotura_tronco():
    trozos = []
    for i in range(6):
        angulo = random.uniform(0, 360)
        velocidad = random.uniform(3, 6)
        dx = math.cos(math.radians(angulo)) * velocidad
        dy = math.sin(math.radians(angulo)) * velocidad
        trozos.append([CENTRO[0], CENTRO[1], dx, dy, random.randint(10, 25)])

    for _ in range(40):
        pantalla.fill(GRIS)
        for trozo in trozos:
            trozo[0] += trozo[2]
            trozo[1] += trozo[3]
            pygame.draw.circle(pantalla, MARRON, (int(trozo[0]), int(trozo[1])), trozo[4])
        pygame.display.flip()
        reloj.tick(60)


def mostrar_transicion_nivel(nivel):
    if nivel - 1 < len(imagenes_niveles):
        imagen = imagenes_niveles[nivel - 1]
        pantalla.blit(imagen, (0, 0))
    else:
        pantalla.fill(GRIS)
        mostrar_texto(f"NIVEL {nivel}", 70, BLANCO, (ANCHO // 2, ALTO // 2))
        

    mostrar_texto(f"Nivel {nivel}", 60, BLANCO, (ANCHO // 2, ALTO - 100))
    mostrar_texto("Presiona ESPACIO para continuar", 30, BLANCO, (ANCHO // 2, ALTO - 50))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False



# --- SISTEMA DE PUNTAJES ---
def guardar_puntaje(nombre, puntaje):
    with open(ARCHIVO_PUNTAJES, "a", encoding="utf-8") as f:
        f.write(f"{nombre},{puntaje}\n")

#-----CARGAR LOS PUNTAJES----
def cargar_puntajes():
    if not os.path.exists(ARCHIVO_PUNTAJES):
        return []
    with open(ARCHIVO_PUNTAJES, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    puntajes = []
    for linea in lineas:
        try:
            nombre, puntos = linea.strip().split(",")
            puntajes.append((nombre, int(puntos)))
        except:
            pass
    puntajes.sort(key=lambda x: x[1], reverse=True)
    return puntajes[:5]

def mostrar_puntajes():
    puntajes = cargar_puntajes()
    pantalla.fill(GRIS)
    mostrar_texto("MEJORES PUNTAJES", 50, BLANCO, (ANCHO // 2, 100))
    y = 180
    if puntajes:
        for nombre, puntos in puntajes:
            mostrar_texto(f"{nombre} - {puntos}", 35, VERDE, (ANCHO // 2, y))
            y += 50
    else:
        mostrar_texto("No hay puntajes aún", 35, BLANCO, (ANCHO // 2, ALTO // 2))
    mostrar_texto("Presiona ESPACIO para volver", 25, BLANCO, (ANCHO // 2, ALTO - 60))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False

# --- PANTALLAS ---
def pantalla_inicio():
    global musica_muted
    en_menu = True
    while en_menu:
        pantalla.fill(GRIS)
        mostrar_texto("JUEGO DE CUCHILLOS", 60, BLANCO, (ANCHO // 2, ALTO // 4))

        if imagen_crash:
            rect_crash = imagen_crash.get_rect(center=(ANCHO // 2, ALTO // 2.2))
            pantalla.blit(imagen_crash, rect_crash.topleft)

        # --- Botón JUGAR ---
        boton_jugar = pygame.Rect(0, 0, 200, 70)
        boton_jugar.center = (ANCHO // 2, ALTO // 1.5)
        pygame.draw.rect(pantalla, VERDE, boton_jugar, border_radius=20)
        mostrar_texto("JUGAR", 40, NEGRO, boton_jugar.center)

        # --- Botón PUNTAJES ---
        boton_puntajes = pygame.Rect(0, 0, 200, 50)
        boton_puntajes.center = (ANCHO // 2, ALTO // 1.3)
        pygame.draw.rect(pantalla, BLANCO, boton_puntajes, border_radius=20)
        mostrar_texto("PUNTAJES", 35, NEGRO, boton_puntajes.center)

        # --- Botón PERSONALIZAR (nuevo) ---
        boton_personalizar = pygame.Rect(0, 0, 200, 50)
        boton_personalizar.center = (ANCHO // 2, ALTO // 1.15)
        pygame.draw.rect(pantalla, (180, 180, 255), boton_personalizar, border_radius=20)
        mostrar_texto("PERSONALIZAR", 35, NEGRO, boton_personalizar.center)

        # --- Texto inferior ---
        estado_musica = "ON" if not musica_muted else "OFF"
        mostrar_texto(f"Música: {estado_musica} (tecla M)", 25, BLANCO, (ANCHO // 2, ALTO - 30))
        

        pygame.display.flip()

        # --- Manejo de eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    en_menu = False
                elif boton_puntajes.collidepoint(evento.pos):
                    mostrar_puntajes()
                elif boton_personalizar.collidepoint(evento.pos):
                    menu_personalizar()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:
                    if musica_muted:
                        pygame.mixer.music.set_volume(0.4)
                        musica_muted = False
                    else:
                        pygame.mixer.music.set_volume(0)
                        musica_muted = True

def ingresar_nombre(puntaje):
    nombre = ""
    escribiendo = True
    while escribiendo:
        pantalla.fill(GRIS)
        if imagen_game_over:
            rect_game_over = imagen_game_over.get_rect(center=(ANCHO // 2, ALTO // 4))
            pantalla.blit(imagen_game_over, rect_game_over)
        else:
            mostrar_texto("¡Perdiste!", 60, ROJO, (ANCHO // 2, ALTO // 4))
        
        mostrar_texto(f"Tu puntaje: {puntaje}", 40, BLANCO, (ANCHO // 2, ALTO // 2 + 40))
        mostrar_texto("Ingresa tu nombre:", 35, BLANCO, (ANCHO // 2, ALTO // 2 + 90))
        mostrar_texto(nombre + "|", 40, VERDE, (ANCHO // 2, ALTO // 2 + 140))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip() != "":
                    guardar_puntaje(nombre.strip(), puntaje)
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 12 and evento.unicode.isprintable():
                        nombre += evento.unicode

# --- JUEGO PRINCIPAL ---
def juego_principal():
    nivel = 1
    jugando = True
    puntaje_total = 0

    while jugando:
        mostrar_transicion_nivel(nivel)
        rotacion_tronco = 0
        base_velocidad = 120 + (nivel - 1) * 40  # cada nivel sube un poco más
        velocidad_tronco = random.choice([base_velocidad, -base_velocidad])
        cuchillo_lanzado = False
        y_cuchillo = ALTO - 120
        angulos_clavados = []
        puntaje = 0
        cuchillos_restantes = CUCHILLOS_INICIALES + nivel - 1
        dt = 0

        nivel_en_curso = True
        while nivel_en_curso:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and not cuchillo_lanzado and cuchillos_restantes > 0:
                        cuchillo_lanzado = True
                        cuchillos_restantes -= 1
                        if sonido_cuchillo:
                            sonido_cuchillo.play()

            if imagen_pantalla:
                pantalla.blit(imagen_pantalla, (0, 0))
            else:
                pantalla.fill(GRIS)

            rotacion_tronco = (rotacion_tronco + velocidad_tronco * dt) % 360

            if cuchillo_lanzado:
                y_cuchillo -= VELOCIDAD_CUCHILLO
                if y_cuchillo <= CENTRO[1] + RADIO_TRONCO:
                    ang = 90
                    colision = False
                    for ang_rel in angulos_clavados:
                        ang_clav = (ang_rel + rotacion_tronco) % 360
                        if abs(ang_clav - ang) < 15:
                            colision = True
                            break
                    if colision:
                        mostrar_texto("¡PERDISTE!", 50, ROJO, (ANCHO // 2, ALTO // 2))
                        pygame.display.flip()
                        pygame.time.delay(1200)
                        ingresar_nombre(puntaje_total + puntaje)
                        return
                    else:
                        ang_rel = (ang - rotacion_tronco) % 360
                        angulos_clavados.append(ang_rel)
                        cuchillo_lanzado = False
                        y_cuchillo = ALTO - 120
                        puntaje += 1

                        if puntaje >= CUCHILLOS_INICIALES + nivel - 1:
                            mostrar_texto("¡GANASTE!", 50, VERDE, (ANCHO // 2, ALTO // 2))
                            pygame.display.flip()
                            pygame.time.delay(500)
                            animacion_rotura_tronco()
                            pygame.time.delay(300)
                            nivel_en_curso = False
                            puntaje_total += puntaje

            dibujar_tronco(rotacion_tronco)
            dibujar_cuchillos_clavados(angulos_clavados, rotacion_tronco)
            dibujar_cuchillo(CENTRO[0], y_cuchillo)

            mostrar_texto(f"Nivel: {nivel}", 30, BLANCO, (70, 40))
            mostrar_texto(f"jugar con tecla ESPACIO", 30, BLANCO, (150, 70))
            mostrar_texto(f"Cuchillos: {cuchillos_restantes}", 30, BLANCO, (ANCHO - 120, 30))
            mostrar_texto(f"Puntaje: {puntaje_total + puntaje}", 30, BLANCO, (ANCHO // 2, 30))

            pygame.display.flip()
            dt = reloj.tick(60) / 1000

        nivel += 1

# --- EJECUCIÓN ---
if __name__ == "__main__":
    while True:
            pantalla_inicio()
            juego_principal()
