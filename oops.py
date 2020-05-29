# Implementing OOPS Concepts

import pygame
import random
from blob import Blob

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

STARTING_BLUE_BLOBS = 10
STARTING_RED_BLOBS = 8
STARTING_GREEN_BLOBS = 8

game_display = pygame.display.set_mode(size=(800, 600))
pygame.display.set_caption("Blob World")
clock = pygame.time.Clock()

class BlueBlob(Blob):
    
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, (0, 0, 255), x_boundary, y_boundary)


class RedBlob(Blob):
    
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, (255, 0, 0), x_boundary, y_boundary)

    def __add__(self, other_blob):
        if other_blob.color == (255, 0, 0):
            self.size -= other_blob.size
            other_blob.size -= self.size
        elif other_blob.color == (0, 255, 0):
            self.size += other_blob.size
            other_blob.size += self.size
        elif other_blob.color == (0, 0, 255):
            pass
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors.')


class GreenBlob(Blob):
    
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, (0, 255, 0), x_boundary, y_boundary)


def draw_enviroment(blobs_list):
    game_display.fill(WHITE)

    for blobs_dict in blobs_list:
        for blob_id in blobs_dict:
            blob = blobs_dict[blob_id]
            pygame.draw.circle(game_display, blob.color, [blob.x, blob.y], blob.size)
            blob.move()
    pygame.display.update()

def main():
    blue_blobs = dict(enumerate([BlueBlob(WIDTH, HEIGHT) for i in range(STARTING_BLUE_BLOBS)]))
    red_blobs = dict(enumerate([RedBlob(WIDTH, HEIGHT) for i in range(STARTING_RED_BLOBS)]))
    green_blobs = dict(enumerate([GreenBlob(WIDTH, HEIGHT) for i in range(STARTING_GREEN_BLOBS)]))
   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
        draw_enviroment([blue_blobs, red_blobs, green_blobs])
        clock.tick(60)

if __name__ == "__main__":
    main()