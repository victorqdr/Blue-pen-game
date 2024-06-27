import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone = pygame.image.load("recursos/icone.png")
manoel = pygame.image.load("recursos/manoel.png")
fundo = pygame.image.load("recursos/fundo.png")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")
canetaPreta = pygame.image.load("recursos/blackpen.png")

# Carregar e redimensionar a imagem da nuvem
nuvem_imagem = pygame.image.load("recursos/nuvem.png")
nuvem_imagem = pygame.transform.scale(nuvem_imagem, (100, 50))  # Redimensionar a nuvem

pen = pygame.image.load("recursos/pen.png")
tamanho = (800, 600)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Blue pen game")
pygame.display.set_icon(icone)
pensound = pygame.mixer.Sound("recursos/pensound.wav")
explosaoSound = pygame.mixer.Sound("recursos/explosao.wav")
fonte = pygame.font.SysFont("comicsans", 28)
fonteStart = pygame.font.SysFont("comicsans", 55)
fonteMorte = pygame.font.SysFont("arial", 120)
pygame.mixer.music.load("recursos/blueSound.mp3")

branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

def criar_nuvens():
    return [{"x": random.randint(0, 800), "y": random.randint(0, 100), "vel": random.randint(1, 3)} for _ in range(5)]

def mover_nuvens(nuvens):
    for nuvem in nuvens:
        nuvem["x"] += nuvem["vel"]
        if nuvem["x"] > 800:
            nuvem["x"] = -nuvem_imagem.get_width()

def desenhar_nuvens(tela, nuvens):
    for nuvem in nuvens:
        tela.blit(nuvem_imagem, (nuvem["x"], nuvem["y"]))

def jogar(nome):
    pygame.mixer.Sound.play(pensound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    velocidadecaneta = 1
    posicaoYcaneta = -120
    posicaoXcaneta = 200
    larguracaneta = 50
    alturacaneta = 250
    pontos = 0
    larguraPersona = 100
    alturaPersona = 100
    larguaMissel = 50
    alturaMissel = 250
    dificuldade = 10
    nuvens = criar_nuvens()

    # Inicialização do sol
    raio_sol = 30
    crescimento = 1

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        posicaoXPersona += movimentoXPersona            
        posicaoYPersona += movimentoYPersona            

        if posicaoXPersona < 0:
            posicaoXPersona = 10
        elif posicaoXPersona > 550:
            posicaoXPersona = 540

        if posicaoYPersona < 0:
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463

        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        desenhar_nuvens(tela, nuvens)
        mover_nuvens(nuvens)

        # Desenho e animação do sol
        pygame.draw.circle(tela, amarelo, (750, 50), raio_sol)
        raio_sol += crescimento
        if raio_sol >= 35 or raio_sol <= 25:
            crescimento = -crescimento

        tela.blit(manoel, (posicaoXPersona, posicaoYPersona))

        posicaoYMissel += velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos += 1
            velocidadeMissel += 1
            posicaoXMissel = random.randint(0, 800)
            pygame.mixer.Sound.play(pensound)

        tela.blit(pen, (posicaoXMissel, posicaoYMissel))

        texto = fonte.render(nome + "- Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (10, 10))
        # Movimento caneta preta
        posicaoYcaneta += velocidadecaneta 
        if posicaoYcaneta > 600:
            posicaoYcaneta = -120
            pontos += 1
            velocidadecaneta += 1
            posicaoXcaneta = random.randint(0, 800)
            pygame.mixer.Sound.play(pensound)

        tela.blit(canetaPreta, (posicaoXcaneta, posicaoYcaneta))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        pixelsCanetaX = list(range(posicaoXcaneta, posicaoXcaneta + larguracaneta))
        pixelsCanetaY = list(range(posicaoYcaneta, posicaoYcaneta + alturacaneta))

        if (set(pixelsPersonaX).intersection(pixelsMisselX) and set(pixelsPersonaY).intersection(pixelsMisselY)) or \
           (set(pixelsPersonaX).intersection(pixelsCanetaX) and set(pixelsPersonaY).intersection(pixelsCanetaY)):
            dead(nome, pontos)

        pygame.display.update()
        relogio.tick(60)

def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    jogadas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt", "w", encoding="utf-8")
        arquivo.close()

    jogadas[nome] = pontos   
    arquivo = open("historico.txt", "w", encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400, 482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60, 482))
        pygame.display.update()
        relogio.tick(60)

def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass

    nomes = sorted(estrelas, key=estrelas.get, reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330, 482))

        posicaoY = 50
        for key, nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - " + str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300, posicaoY))
            posicaoY += 30

        pygame.display.update()
        relogio.tick(60)

def start():
    nome = simpledialog.askstring("Manoel Gomes", "Nome Completo:")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        buttonRanking = pygame.draw.rect(tela, preto, (35, 50, 200, 50), 0, 30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90, 50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330, 482))

        pygame.display.update()
        relogio.tick(60)

start()
