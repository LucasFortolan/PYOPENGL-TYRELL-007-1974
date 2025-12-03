import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# --- Variáveis Globais ---
rot_x = 20.0
rot_y = -45.0
zoom = -15.0
mouse_pressed = False
tex_goodyear = None
tex_elf = None  # Nova variável para a textura ELF

# Estados
estado_animacao = 0
posicao_carro_z = 0.0
posicao_carro_x = 0.0
velocidade = 0.0
angulo_roda = 0.0
angulo_direcao = 0.0

# --- Cores ---
AZUL_ELF = [0.0, 0.15, 0.65]
PRETO_PNEU = [0.12, 0.12, 0.12]
PRATA_METAL = [0.75, 0.75, 0.75]
CINZA_MOTOR = [0.3, 0.3, 0.3]
BRANCO = [1.0, 1.0, 1.0]
AMARELO_NEON = [0.9, 0.9, 0.1]
VIDRO = [0.4, 0.8, 0.9, 0.6]
CINZA_PISTA = [0.2, 0.2, 0.2]
VERDE_GRAMA = [0.1, 0.4, 0.1]
VERMELHO_ZEBRA = [0.8, 0.1, 0.1]

# =========================================================================
#  GERENCIAMENTO DE TEXTURA
# =========================================================================


def gerar_textura_texto(texto, cor_texto, cor_fundo):
    font = pygame.font.SysFont('Arial', 64, bold=True)
    surface = font.render(texto, True, cor_texto, cor_fundo)
    text_data = pygame.image.tostring(surface, "RGBA", 1)
    width = surface.get_width()
    height = surface.get_height()
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    return tex_id


def desenhar_texto_na_tela(x, y, lista_textos):
    font = pygame.font.SysFont('arial', 18, bold=True)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    pos_y = 600 - y
    for texto in lista_textos:
        text_surface = font.render(texto, True, (255, 255, 0, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        w, h = text_surface.get_width(), text_surface.get_height()
        glRasterPos2i(x, pos_y - h)
        glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        pos_y -= 25
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# =========================================================================
#  PRIMITIVAS GEOMÉTRICAS
# =========================================================================


def desenhar_caixa(sx, sy, sz):
    glPushMatrix()
    glScalef(sx, sy, sz)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glNormal3f(0, 0, -1)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glNormal3f(-1, 0, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glNormal3f(1, 0, 0)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glNormal3f(0, -1, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()
    glPopMatrix()


def desenhar_circulo(raio, r, g, b):
    segmentos = 20
    glColor3f(r, g, b)
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    for i in range(segmentos + 1):
        theta = 2.0 * math.pi * i / segmentos
        glVertex3f(raio * math.cos(theta), raio * math.sin(theta), 0)
    glEnd()


def desenhar_cilindro(raio, comprimento, r, g, b):
    segmentos = 20
    glColor3f(r, g, b)
    glBegin(GL_QUAD_STRIP)
    for i in range(segmentos + 1):
        theta = 2.0 * math.pi * i / segmentos
        x = raio * math.cos(theta)
        y = raio * math.sin(theta)
        glNormal3f(x, y, 0.0)
        glVertex3f(x, y, comprimento/2)
        glVertex3f(x, y, -comprimento/2)
    glEnd()
    glPushMatrix()
    glTranslatef(0, 0, comprimento/2)
    desenhar_circulo(raio, r, g, b)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, -comprimento/2)
    glRotatef(180, 1, 0, 0)
    desenhar_circulo(raio, r, g, b)
    glPopMatrix()


def desenhar_haste(p1, p2):
    glLineWidth(3)
    glColor3fv(PRATA_METAL)
    glBegin(GL_LINES)
    glVertex3fv(p1)
    glVertex3fv(p2)
    glEnd()
    glLineWidth(1)

# =========================================================================
#  CARRO
# =========================================================================


def desenhar_roda(raio, largura, lado_direito, angulo_giro):
    glPushMatrix()
    glRotatef(90, 0, 1, 0)
    glRotatef(angulo_giro, 0, 0, 1)
    desenhar_cilindro(
        raio, largura, PRETO_PNEU[0], PRETO_PNEU[1], PRETO_PNEU[2])
    desenhar_cilindro(raio * 0.65, largura + 0.02,
                      PRATA_METAL[0], PRATA_METAL[1], PRATA_METAL[2])
    glColor3f(0.1, 0.1, 0.1)
    for ang in range(0, 360, 60):
        glPushMatrix()
        glRotatef(ang, 0, 0, 1)
        glTranslatef(0, raio * 0.4, 0)
        desenhar_caixa(0.08, raio * 0.45, largura + 0.03)
        glPopMatrix()
    desenhar_cilindro(raio * 0.20, largura + 0.04, 0.1, 0.1, 0.1)
    cor = [0, 0, 0.8] if lado_direito else [0.8, 0, 0]
    desenhar_cilindro(raio * 0.10, largura + 0.1, cor[0], cor[1], cor[2])
    glPopMatrix()


def desenhar_bico():
    glPushMatrix()
    glTranslatef(0.0, -0.1, 2.2)
    glColor3fv(AZUL_ELF)
    glBegin(GL_QUADS)
    glNormal3f(0, 0.5, 0.5)
    glVertex3f(-0.45, 0.25, -0.6)
    glVertex3f(0.45, 0.25, -0.6)
    glVertex3f(0.35, 0.05, 0.8)
    glVertex3f(-0.35, 0.05, 0.8)
    glNormal3f(0, -1, 0)
    glVertex3f(-0.45, -0.25, -0.6)
    glVertex3f(0.45, -0.25, -0.6)
    glVertex3f(0.35, -0.05, 0.8)
    glVertex3f(-0.35, -0.05, 0.8)
    glNormal3f(-1, 0, 0)
    glVertex3f(-0.45, -0.25, -0.6)
    glVertex3f(-0.45, 0.25, -0.6)
    glVertex3f(-0.35, 0.05, 0.8)
    glVertex3f(-0.35, -0.05, 0.8)
    glNormal3f(1, 0, 0)
    glVertex3f(0.45, -0.25, -0.6)
    glVertex3f(0.45, 0.25, -0.6)
    glVertex3f(0.35, 0.05, 0.8)
    glVertex3f(0.35, -0.05, 0.8)
    glEnd()

    # --- NOVO: LOGO GOODYEAR NA FRENTE DO BICO ---
    if tex_goodyear:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_goodyear)
        glColor3f(1, 1, 1)
        glPushMatrix()
        glTranslatef(0, 0.26, -0.2)
        glRotatef(90, 1, 0, 0)  # Em cima do bico
        glScalef(0.8, 0.2, 1.0)  # Ajusta tamanho
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-0.5, -0.5, 0)
        glTexCoord2f(1, 0)
        glVertex3f(0.5, -0.5, 0)
        glTexCoord2f(1, 1)
        glVertex3f(0.5, 0.5, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-0.5, 0.5, 0)
        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    glPushMatrix()
    glTranslatef(0, 0.16, 0.0)
    glRotatef(-15, 1, 0, 0)
    glScalef(1, 0.1, 1)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    desenhar_circulo(0.25, 1, 1, 1)
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()


def desenhar_tyrrell_full(angulo_pneus, direcao_rodas):
    # Corpo
    glColor3fv(AZUL_ELF)
    glPushMatrix()
    glTranslatef(0, 0, 0.5)
    desenhar_caixa(0.9, 0.6, 2.5)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.7, -0.2)
    desenhar_caixa(0.5, 0.8, 0.5)
    glTranslatef(0, 0.2, 0.26)
    glColor3f(0.1, 0.1, 0.1)
    desenhar_caixa(0.3, 0.3, 0.05)
    glPopMatrix()

    # Sidepods com Logo ELF (TROCA REALIZADA)
    for x_lado in [-0.7, 0.7]:
        glPushMatrix()
        glTranslatef(x_lado, -0.15, 0.0)
        glColor3fv(AZUL_ELF)
        desenhar_caixa(0.45, 0.45, 1.8)
        glColor3f(0.1, 0.1, 0.1)
        glPushMatrix()
        glTranslatef(0, 0, 0.91)
        for i in range(5):
            glPushMatrix()
            glTranslatef(0, -0.15 + (i*0.07), 0)
            desenhar_caixa(0.4, 0.02, 0.02)
            glPopMatrix()
        glPopMatrix()

        # LOGO ELF (Agora na lateral, substituindo Goodyear)
        if tex_elf:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, tex_elf)
            glColor3f(1, 1, 1)
            offset = 0.23 if x_lado > 0 else -0.23
            glPushMatrix()
            glTranslatef(offset, 0, 0)
            glRotatef(90 if x_lado > 0 else -90, 0, 1, 0)
            # Desenha o quad da textura (elf é mais curto, ajuste de escala)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex3f(-0.5, -0.25, 0)
            glTexCoord2f(1, 0)
            glVertex3f(0.5, -0.25, 0)
            glTexCoord2f(1, 1)
            glVertex3f(0.5, 0.25, 0)
            glTexCoord2f(0, 1)
            glVertex3f(-0.5, 0.25, 0)
            glEnd()
            glPopMatrix()
            glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    # Partes do carro
    glColor3fv(PRETO_PNEU)
    glPushMatrix()
    glTranslatef(0, 0.31, 0.4)
    desenhar_caixa(0.6, 0.05, 0.7)
    glPopMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4fv(VIDRO)
    glPushMatrix()
    glTranslatef(0, 0.45, 0.8)
    desenhar_caixa(0.65, 0.25, 0.05)
    glPopMatrix()
    glDisable(GL_BLEND)
    desenhar_bico()
    glColor3fv(AZUL_ELF)
    glPushMatrix()
    glTranslatef(0, -0.35, 3.2)
    desenhar_caixa(2.8, 0.05, 0.7)
    glColor3fv(AMARELO_NEON)
    for l in [-1.4, 1.4]:
        glPushMatrix()
        glTranslatef(l, 0.15, 0)
        desenhar_caixa(0.05, 0.35, 0.7)
        glPopMatrix()
    glPopMatrix()
    glColor3fv(AZUL_ELF)
    glPushMatrix()
    glTranslatef(0, 0.9, -2.4)
    desenhar_caixa(2.4, 0.05, 0.9)
    glColor3fv(PRATA_METAL)
    glPushMatrix()
    glTranslatef(0, -0.4, 0.1)
    desenhar_caixa(0.1, 0.8, 0.4)
    glPopMatrix()
    glColor3fv(AZUL_ELF)
    for l in [-1.2, 1.2]:
        glPushMatrix()
        glTranslatef(l, -0.1, 0)
        desenhar_caixa(0.05, 0.6, 1.0)
        glPopMatrix()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.0, 0.1, -1.2)
    glColor3fv(CINZA_MOTOR)
    desenhar_caixa(0.5, 0.5, 0.9)
    glPopMatrix()

    # Rodas
    posicoes = [(-1.5, -0.05, -1.5, 0.75, 1.2, False), (1.5, -0.05, -1.5, 0.75, 1.2,
                                                        True), (-1.5, -0.3, 2.4, 0.50, 0.7, False), (1.5, -0.3, 2.4, 0.50, 0.7, True)]
    for i, (px, py, pz, r, w, right) in enumerate(posicoes):
        glPushMatrix()
        glTranslatef(px, py, pz)
        if i >= 2:
            glRotatef(direcao_rodas, 0, 1, 0)
        desenhar_roda(r, w, right, angulo_pneus)
        glPopMatrix()
        lado = 1 if px > 0 else -1
        p_chassi = [0.5 * lado, 0, pz - (0.4 if pz > 0 else -0.3)]
        desenhar_haste([p_chassi[0], 0.1, p_chassi[2]], [px, 0.1, pz])
        desenhar_haste([p_chassi[0], -0.1, p_chassi[2]], [px, -0.1, pz])


def desenhar_pista_infinita(z_carro):
    passo = 4.0
    z_ancora = math.floor(z_carro / passo) * passo
    glPushMatrix()
    glTranslatef(0, -0.8, z_carro)
    glColor3fv(CINZA_PISTA)
    glPushMatrix()
    glScalef(12.0, 0.01, 400.0)
    desenhar_caixa(1, 1, 1)
    glPopMatrix()
    glColor3fv(VERDE_GRAMA)
    glPushMatrix()
    glTranslatef(-16.0, -0.1, 0)
    glScalef(20.0, 0.01, 400.0)
    desenhar_caixa(1, 1, 1)
    glPopMatrix()
    glColor3fv(VERDE_GRAMA)
    glPushMatrix()
    glTranslatef(16.0, -0.1, 0)
    glScalef(20.0, 0.01, 400.0)
    desenhar_caixa(1, 1, 1)
    glPopMatrix()
    glPopMatrix()
    for i in range(-10, 60):
        z_atual = z_ancora - (i * passo)
        idx = int(z_atual / passo)
        glColor3fv(BRANCO if idx % 2 == 0 else VERMELHO_ZEBRA)
        glPushMatrix()
        glTranslatef(-6.0, 0.05, z_atual)
        glScalef(0.5, 0.05, 2.0)
        desenhar_caixa(1, 1, 1)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(6.0, 0.05, z_atual)
        glScalef(0.5, 0.05, 2.0)
        desenhar_caixa(1, 1, 1)
        glPopMatrix()
        if idx % 4 == 0:
            glColor3fv(BRANCO)
            glPushMatrix()
            glTranslatef(-8.0, 0.5, z_atual)
            glScalef(0.2, 1.0, 3.8)
            desenhar_caixa(1, 1, 1)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(8.0, 0.5, z_atual)
            glScalef(0.2, 1.0, 3.8)
            desenhar_caixa(1, 1, 1)
            glPopMatrix()


def desenhar_largada():
    glColor3f(1, 1, 1)
    glPushMatrix()
    glTranslatef(0, -0.79, 0)
    glScalef(10.0, 0.01, 1.0)
    desenhar_caixa(1, 1, 1)
    glPopMatrix()


def main():
    global rot_x, rot_y, zoom, mouse_pressed, posicao_carro_z, posicao_carro_x, velocidade, angulo_roda, angulo_direcao, estado_animacao, tex_goodyear, tex_elf

    pygame.init()
    pygame.font.init()
    viewport = (800, 600)
    screen = pygame.display.set_mode(viewport, DOUBLEBUF | OPENGL | RESIZABLE)
    pygame.display.set_caption("Tyrrell-007 - Final")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 10.0, 10.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])

    # GERAÇÃO DAS DUAS TEXTURAS
    tex_goodyear = gerar_textura_texto(
        "GOODYEAR", (255, 255, 0), (0, 38, 166))  # Amarelo fundo Azul
    tex_elf = gerar_textura_texto(
        "elf", (255, 255, 255), (0, 38, 166))  # Branco fundo Azul

    clock = pygame.time.Clock()
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (viewport[0]/viewport[1]), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEWHEEL:
                zoom += event.y * 1.0
            if event.type == MOUSEBUTTONDOWN:
                mouse_pressed = True if event.button == 1 else False
            if event.type == MOUSEBUTTONUP:
                mouse_pressed = False
            if event.type == VIDEORESIZE:
                viewport = (event.w, event.h)
                glViewport(0, 0, event.w, event.h)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(45, (event.w/event.h), 0.1, 200.0)
                glMatrixMode(GL_MODELVIEW)

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    estado_animacao = 1 if estado_animacao == 0 else 0
                if event.key == K_r:
                    estado_animacao = 0
                    posicao_carro_z = 0.0
                    posicao_carro_x = 0.0
                    velocidade = 0.0
                    angulo_roda = 0.0
                    angulo_direcao = 0.0

        if mouse_pressed:
            rx, ry = pygame.mouse.get_rel()
            rot_y += rx * 0.5
            rot_x += ry * 0.5
        else:
            pygame.mouse.get_rel()

        keys = pygame.key.get_pressed()
        angulo_direcao = 0
        if estado_animacao == 1:
            if keys[K_LEFT] and posicao_carro_x > -5.0:
                posicao_carro_x -= 0.1
                angulo_direcao = 25
            if keys[K_RIGHT] and posicao_carro_x < 5.0:
                posicao_carro_x += 0.1
                angulo_direcao = -25
            if velocidade < 1.8:
                velocidade += 0.02
            posicao_carro_z -= velocidade
            angulo_roda += velocidade * 15
        else:
            if velocidade > 0:
                velocidade -= 0.05
                posicao_carro_z -= velocidade
                angulo_roda += velocidade * 15
            else:
                velocidade = 0

        glClearColor(0.5, 0.7, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, -1.0, zoom)
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)
        glTranslatef(0, 0, -posicao_carro_z)

        desenhar_pista_infinita(posicao_carro_z)
        desenhar_largada()
        glPushMatrix()
        glTranslatef(posicao_carro_x, 0, posicao_carro_z)
        glRotatef(180, 0, 1, 0)
        desenhar_tyrrell_full(angulo_roda, angulo_direcao)
        glPopMatrix()

        status = "PARADO (Espaco)" if estado_animacao == 0 else "CORRENDO (Espaco)"
        desenhar_texto_na_tela(10, 10, [
                               "Tyrrell 007 de 1974", f"Status: {status}", "Setas (Direção): <- Esquerda, -> Direita | R: Reset", "Mouse: Cam | Scroll: Zoom"])

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
