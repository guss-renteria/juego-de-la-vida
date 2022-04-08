import pygame
import numpy as np
import time

# iniciar juego
pygame.init()

width, height = 800, 800
screen = pygame.display.set_caption('juego de la vida')
screen = pygame.display.set_mode((width, height))

# colors
c_bg = 28, 28, 28
c_line = 255, 255, 255

# numero de celdas
num_cx, num_cy = 25, 25

# tamaño de celdas
dim_cw = width / num_cx
dim_ch = height / num_cy

# cargar celdas
game_state = np.zeros((num_cx, num_cy))

#
in_game = True
pause = False

while in_game:
    # nuevos estados para cambiar en el bucle
    new_game_state = np.copy(game_state)

    # limpiar pantalla
    screen.fill(c_bg)
    # pausa entre iteración
    time.sleep(0.1)
    
    # eventos
    ev = pygame.event.get()
    for event in ev:
        # ev. salir
        if event.type == pygame.QUIT:
            in_game = False

        # ev. pause
        elif event.type == pygame.KEYDOWN:
            pause = not pause

        # ev. click
        mouse_click = pygame.mouse.get_pressed()
        if sum(mouse_click) > 0:
            pos_x, pos_y = pygame.mouse.get_pos()
            cel_x, cel_y = int(np.floor(pos_x / dim_cw)), int(np.floor(pos_y / dim_ch))
            new_game_state[cel_x, cel_y] = not mouse_click[2]

    for y in range(0, num_cx):
        for x in range(0, num_cy):
            if not pause:
                # calcula el número de vecinos cercanos.
                n_neigh = game_state[(x-1) % num_cx, (y-1) % num_cy] + \
                          game_state[x     % num_cx, (y-1) % num_cy] + \
                          game_state[(x+1) % num_cx, (y-1) % num_cy] + \
                          game_state[(x-1) % num_cx, y     % num_cy] + \
                          game_state[(x+1) % num_cx, y     % num_cy] + \
                          game_state[(x-1) % num_cx, (y+1) % num_cy] + \
                          game_state[x     % num_cx, (y+1) % num_cy] + \
                          game_state[(x+1) % num_cx, (y+1) % num_cy]
                
                # regla 1: una célula muerta con exactamente 3 vecinas vivas, "revive".
                if game_state[x, y] == 0 and n_neigh == 3:
                    new_game_state[x, y] = 1

                # regla 2: una célula viva con menos de 2 o más de 3 vecinas vivas, "muere".
                elif game_state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_game_state[x, y] = 0

            # crea el polígono de cada celda a dibujar.
            poly = [(x     * dim_cw, y     * dim_ch),
                    ((x+1) * dim_cw, y     * dim_ch),
                    ((x+1) * dim_cw, (y+1) * dim_ch),
                    (x     * dim_cw, (y+1) * dim_ch)]

            # dibujar la célula según su estado
            if new_game_state[x, y] == 0:
                pygame.draw.polygon(screen, c_line, poly, 1)
            else:
                pygame.draw.polygon(screen, c_line, poly, 0)

    # actualizar estado
    game_state = np.copy(new_game_state)

    pygame.display.flip()

print('[+] se ha salido con exito.')
