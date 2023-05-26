import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()
largura = 640
altura = 480

x_cobra = largura / 2
y_cobra = altura / 2

x_maca = random.randint(40, 600)
y_maca = random.randint(50, 430)

x_bloco_preto = random.randint(40, 600)
y_bloco_preto = random.randint(50, 430)


comprimentoini = 5

xcontrole = 20
ycontrole = 0
pontos = 0

fonte = pygame.font.SysFont("Arial", 40, True, False)

contador_frames = 0
intervalo_frames = 100
velocidade_objeto_preto = 10

pygame.mixer.music.set_volume(0.2)
musicafundo = pygame.mixer.music.load("smw_castle_clear.wav")
pygame.mixer.music.play(-1)
barulhocoli = pygame.mixer.Sound("smw_jump.wav")

fundo_jogo_imagem = pygame.image.load('imagens/fundo_jogo.jpg')
tela_inicial_imagem = pygame.image.load("imagens/tela_inicial_crazy_snake.png")
fundo_lost_imagem = pygame.image.load("imagens/tela_lost_crazy_snake.png")
imagem_cabeca = pygame.image.load("imagens/cabeca_cobra.png")
imagem_cabeca_cima = pygame.image.load("imagens/cabeça_cobra_cima.png")
imagem_cabeca_baixo = pygame.image.load("imagens/cabeça_cobra_baixo.png")
imagem_cabeca_esquerda = pygame.image.load("imagens/cabeça_cobra_esquerda.png")
imagem_cabeca_direita = pygame.image.load("imagens/cabeça_cobra_direita.png")
imagem_bloco_preto = pygame.image.load("imagens/imagem_bloco_preto.png")
imagem_maca = pygame.image.load("imagens/imagem_maça.png")

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Crazy Snake")

def aumentacobra(lista_cobra):
    for xey in lista_cobra:
        pygame.draw.rect(tela, (0, 255, 0), (xey[0], xey[1], 20, 20))

def reiniciar_jogo():
    global pontos, x_cobra, y_cobra, lista_cobra, comprimentoini, x_maca, y_maca, xcontrole, ycontrole
    pontos = 0
    x_cobra = largura / 2
    y_cobra = altura / 2
    lista_cobra = []
    comprimentoini = 5
    x_maca = random.randint(40, 600)
    y_maca = random.randint(50, 430)
    xcontrole = 20
    ycontrole = 0
    pygame.mixer.music.play(-1)
    return pontos, x_cobra, y_cobra, lista_cobra, comprimentoini, x_maca, y_maca, xcontrole, ycontrole

def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_s:
                    pygame.quit()
        tela.blit(fundo_lost_imagem, (0, 0))
        pygame.display.flip()

relogio = pygame.time.Clock()
lista_cobra = []

game_running = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_running = True
                reiniciar_jogo()
            if event.key == pygame.K_UP and ycontrole != 20:  # Evitar que a cobra retroceda em direção oposta
                xcontrole = 0
                ycontrole = -20
            elif event.key == pygame.K_DOWN and ycontrole != -20:
                xcontrole = 0
                ycontrole = 20
            elif event.key == pygame.K_LEFT and xcontrole != 20:
                xcontrole = -20
                ycontrole = 0
            elif event.key == pygame.K_RIGHT and xcontrole != -20:
                xcontrole = 20
                ycontrole = 0

    if not game_running:
        tela.blit(tela_inicial_imagem, (0, 0))
        pygame.display.flip()
        continue

    velocidade = 9 + pontos // 1

    contador_frames += 1
    if contador_frames >= intervalo_frames:
        contador_frames = 0

    x_bloco_preto += velocidade_objeto_preto
    y_bloco_preto += velocidade_objeto_preto

    if x_bloco_preto < 0 or x_bloco_preto > largura - 20:
        velocidade_objeto_preto *= -1
    if y_bloco_preto < 0 or y_bloco_preto > altura - 20:
        velocidade_objeto_preto *= -1

    tela.fill((255, 255, 255))
    tela.blit(fundo_jogo_imagem, (0, 0))
    tela.blit(imagem_bloco_preto, (x_bloco_preto, y_bloco_preto))

    x_cobra = x_cobra + (xcontrole / 10)
    y_cobra = y_cobra + (ycontrole / 10)

    if xcontrole == 0 and ycontrole < 0:
        imagem_cabeca = imagem_cabeca_cima
    elif xcontrole == 0 and ycontrole > 0:
        imagem_cabeca = imagem_cabeca_baixo
    elif xcontrole < 0 and ycontrole == 0:
        imagem_cabeca = imagem_cabeca_esquerda
    elif xcontrole > 0 and ycontrole == 0:
        imagem_cabeca = imagem_cabeca_direita

    if x_cobra < 0 or x_cobra > largura or y_cobra < 0 or y_cobra > altura:
        game_running = False
        if game_over():
            reiniciar_jogo()
            game_running = True
        else:
            pygame.quit()
        continue

    cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 20, 20))
    maca = tela.blit(imagem_maca, (x_maca, y_maca))
    bloco = tela.blit(imagem_bloco_preto, (x_bloco_preto, y_bloco_preto))

    if cobra.colliderect(maca):
        x_maca = random.randint(40, 600)
        y_maca = random.randint(50, 430)
        pontos += 1
        barulhocoli.play()
        comprimentoini += 10

    if cobra.colliderect(bloco):
        game_running = False
        if game_over():
            reiniciar_jogo()
            game_running = True
        else:
            pygame.quit()
        continue

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    lista_cobra.append(lista_cabeca)

    if len(lista_cobra) > comprimentoini:
        del lista_cobra[0]

    aumentacobra(lista_cobra)

    mensagem = f"Pontos: {pontos}"
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))
    tela.blit(texto_formatado, (400, 40))

    pygame.display.update()
    relogio.tick(30)