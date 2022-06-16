import pygame
from network import Network

pygame.font.init()

width = 700
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        screen.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.width / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False



def redrawWindow(screen, game, player):
    screen.fill((255, 255, 255))

    if not (game.connected()):
        screen.fill((120, 120, 120))
        font = pygame.font.SysFont("arial", 80)
        text = font.render("Waiting for Player...", 1, (0, 255, 255))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        screen.fill((120, 120, 120))
        font = pygame.font.SysFont("arial", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        screen.blit(text, (80, 200))
        
        text = font.render("Opponent", 1, (0, 255, 255))
        screen.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and player == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and player == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

            if player == 1:
                screen.blit(text2, (100, 350))
                screen.blit(text1, (400, 350))
            else:
                screen.blit(text1, (100, 350))
                screen.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(screen)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)), Button("Paper", 450, 500, (0, 0, 255))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player ", player)
    
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(screen, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            
            font = pygame.font.SysFont("arial", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (100, 255, 100))
            elif (game.winner() == -1):
                text = font.render("Tie Game!", 1, (100, 100, 255))
            else:
                text = font.render("You Lost...", 1, (255, 100, 100))

            screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(screen, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill((120, 120, 120))
        font = pygame.font.SysFont("arial", 60)
        text = font.render("Click to Play!", 1, (0, 255, 255))
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()