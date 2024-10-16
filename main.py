"""
Jogo: Fuga Espacial
Descrição: Um grupo de diplomatas escapam de uma fortaleza estelar a bordo de uma nave danificada.
A nave precisa se desviar das ameaças e sobreviver até atingir a zona de segurança diplomática.
"""

import pygame
import time
import random


class Background:
    """
    Esta classe define o Plano de Fundo do jogo
    """

    image = None
    margin_left = None
    margin_right = None

    def __init__(self):

        # Atribui imagem pára o background
        background_fig = pygame.image.load("Images/background.png")
        background_fig.convert()
        background_fig = pygame.transform.scale(background_fig, (800, 602))
        self.image = background_fig

        margin_left_fig = pygame.image.load("Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602))
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 602))
        self.margin_right = margin_right_fig

    def update(self, dt):
        pass

    # Imagem do background na tela
    def draw(self, screen):
        screen.blit(self.image, (0, 0))

        # 60 depois da primeira margem
        screen.blit(self.margin_left, (0, 0))

        # 60 antes da segunda margem
        screen.blit(self.margin_right, (740, 0))

    # Define posições do plano de fundo para criar o movimento
    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):
        for i in range(0, 2):
            screen.blit(self.image, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_left, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_right, (movR_x, movR_y - i * scr_height))


class Game:
    screen = None
    screen_size = None
    width = 800
    height = 680
    run = True
    background = None
    player = None
    hazard = []
    render_text_bateulateral = None
    render_text_perdeu = None

    # movimento do Player
    DIREITA = pygame.K_RIGHT
    ESQUERDA = pygame.K_LEFT
    mudar_x = 0.0

    def __init__(self, size, fullscreen):
        """
        Função que inicializa o pygame, define a resolução da tela,         caption e desabilita o mouse.
        """

        pygame.init()

        # tamanho da tela
        self.screen = pygame.display.set_mode((self.width, self.height))

        # define o tamanho da tela do jogo
        self.screen_size = self.screen.get_size()

        # desabilitar o mouse
        pygame.mouse.set_visible(0)

        # definir caption da janela do jogo
        pygame.display.set_caption("Fuga Espacial")

        # Define as fontes
        my_font = pygame.font.Font("Fonts/Fonte4.ttf", 100)

        # Mensagens para o jogador
        self.render_text_bateulateral = my_font.render(
            "VOCÊ BATEU!", 0, (255, 255, 255)
        )
        self.render_text_perdeu = my_font.render("GAME OVER!", 0, (255, 0, 0))

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """

        # Trata a saída do jogo
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.run = False

            # Se clicar em qualquer tecla, entra no if
            if event.type == pygame.KEYDOWN:

                # Se clicar na seta esquerda, anda 3 para a esquerda no eixo x
                if event.key == self.ESQUERDA:
                    self.mudar_x = -3

                # Se clicar na seta da direita, anda 3 para a direita no eixo x
                if event.key == self.DIREITA:
                    self.mudar_x = 3

                # Se soltar qualquer tecla, não faz nada
                if event.type == pygame.KEYUP:
                    if event.key == self.ESQUERDA or event.key == self.DIREITA:
                        self.mudar_x = 0

    # handle_events()

    def elements_update(self, dt):
        # Atualiza elementos
        self.background.update(dt)

    def elements_draw(self):
        # Desenhar elementos
        self.background.draw(self.screen)

    def loop(self):
        """
        Laço principal
        """

        # variáveis para moviemnto de Plano de Fundo/Background
        velocidade_background = 10
        velocidade_hazard = 10

        hzrd = 0
        h_x = random.randrange(125, 660)
        h_y = -500

        # Info Hazard
        h_widh = 1900
        h_height = 110

        # movimento da margem esquerda
        movL_x = 0
        movL_y = 0

        # movimento da margem direita
        movR_x = 740
        movR_y = 0

        # Criar o plano de fundo
        self.background = Background()

        # Posição do player
        x = (self.width - 56) / 2
        y = self.height - 125

        # Criar o Player
        self.player = Player(x, y)

        # Inicializa o relogio e o dt que vai limitar o valor de FPS (frames por segundo) do jogo
        clock = pygame.time.Clock()
        dt = 16

        # Inicio do loop principal do programa
        while self.run:
            clock.tick(1000 / dt)

            # Handle Input events
            self.handle_events()

            # Atualiza o background buffer
            self.elements_draw()

            # Atualiza a tela
            pygame.display.update()
            clock.tick(2000)

            # adiciona movimento ao background
            self.background.move(
                self.screen, self.height, movL_x, movL_y, movR_x, movR_y
            )
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            # se a imagem ultrapassar a extremidade da tela, move de volta
            if movL_y > 600 and movR_y > 600:
                movL_y -= 600
                movR_y -= 600

            # Movimentação do Player
            # Altera a coordenada x da nave de acordo com as mudanças no event_handle() apra ele se mover
            x = x + self.mudar_x

            # Desenhar Player
            self.player.draw(self.screen, x, y)

            # Restrições do movimento do Player
            # Se o Player bate na lateral não é Game Over
            if x > 760 - 92 or x < 40 + 5:
                self.screen.blit(self.render_text_bateulateral, (80, 200))

                # Atualizar a tela
                pygame.display.update()

                time.sleep(3)
                self.loop()
                self.run = False

                pygame.display.update()

            # Criar os Hazards
            self.hazard.append(Hazard("Images/satelite.png", h_x, h_y))
            self.hazard.append(Hazard("Images/nave.png", h_x, h_y))
            self.hazard.append(Hazard("Images/cometaVermelho.png", h_x, h_y))
            self.hazard.append(Hazard("Images/meteoros.png", h_x, h_y))
            self.hazard.append(Hazard("Images/buracoNegro.png", h_x, h_y))

            # Adicionando movimento ao hazard
            h_y = h_y + velocidade_hazard / 4
            self.hazard[hzrd].draw(self.screen, h_x, h_y)
            h_y = h_y + velocidade_hazard

            # Definindo onde o hazard vai aparecer, recomeçando a posição do obstaculo e da faixa
            if h_y > self.height:
                h_y = 0 - h_height
                h_x = random.randrange(125, 650 - h_height)
                hzrd = random.randint(0, 4)
            # Atualiza a tela
            pygame.display.update()

        # while self.run

    # loop()


class Player:
    """
    Esta classe define Jogador
    """

    image = None
    x = None
    y = None

    def __init__(self, x, y):
        player_fig = pygame.image.load("Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90, 90))
        self.image = player_fig
        self.x = x
        self.y = y

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))


class Hazard:
    """
    Esta classe define Ameaça ao Jogador
    """

    image = None
    x = None
    y = None

    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))


# Inicia o jogo: Cria o objeto game e chama o loop básico
game = Game("resolution", "fullscreen")
game.loop()
