import pygame
import sys

if __name__ == '__main__':
    pygame.init()

    width, height = 400, 300
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Простое окно с кнопкой")

    font = pygame.font.Font(None, 36)

    button_rect = pygame.Rect(150, 130, 100, 40)
    button_text = font.render("Выход", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 128, 0), button_rect)
        screen.blit(button_text, (button_rect.x, button_rect.y))

        pygame.display.flip()

    pygame.quit()
