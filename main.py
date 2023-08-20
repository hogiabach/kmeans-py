import pygame
import math
from random import randint
from sklearn.cluster import KMeans


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 700

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("kmeans visualization")
running = True

# FPS
clock = pygame.time.Clock()

K = 0

points = []
clusters = []
labels = []

BACKGROUND = (214, 214, 214)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_PANEL = (249, 255, 230)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

def font_create_text(string, color, size=40):
    font = pygame.font.SysFont("sans", size)
    return font.render(string, True, color)


# Font
text_plus = font_create_text("+", WHITE)
text_minus = font_create_text("-", WHITE)
text_run = font_create_text("Run", WHITE)
text_random = font_create_text("Random", WHITE)
text_algorithm = font_create_text("Algorithm", WHITE)
text_reset = font_create_text("Reset", WHITE)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill(BACKGROUND)

     # Panel
    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    if 55 <= mouse_x <= 745 and 55 <= mouse_y <= 545: 
        text_position = font_create_text(f"({mouse_x - 55}, {mouse_y - 55})", BLACK, 20)
        screen.blit(text_position, (mouse_x, mouse_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Click point in panel
            if 55 <= mouse_x <= 745 and 55 <= mouse_y <= 545:
                labels = [] 
                point = [mouse_x - 55, mouse_y - 55]
                points.append(point)

            #K+ button
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if (K < 9):
                    K += 1
            
            # K- button
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if (K > 0): 
                    K -= 1

            # Run button
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                labels = []
                if not len(clusters):
                    continue
                # Change color points
                for p in points:
                    distances_to_cluster = []
                    for c in clusters:
                        distance_two_points = distance(p, c)
                        distances_to_cluster.append(distance_two_points)
                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance)
                    labels.append(label)
                # Update clusters
                for i in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j, d in enumerate(points):
                        if labels[j] == i:
                            sum_x += d[0]
                            sum_y += d[1]
                            count += 1
                    if count != 0:
                        new_cluster_x = sum_x / count
                        new_cluster_y = sum_y / count 
                        clusters[i] = [new_cluster_x, new_cluster_y]

            # Random button
            if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                if (len(clusters)):
                    clusters = []
                if (K != 0):
                    for i in range(K):
                        random_points = [randint(0, 690), randint(0, 490)]
                        clusters.append(random_points)
            
            # Reset button
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                points = []
                clusters = []
                labels = []

            # Algorithm button
            if 850 < mouse_x < 1030 and 450 < mouse_y < 500:
                if K != 0 and len(points):
                    kmeans = KMeans(n_clusters=K).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_

    # Draw Button
    pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
    pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
    pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
    pygame.draw.rect(screen, BLACK, (850, 250, 150, 50))
    pygame.draw.rect(screen, BLACK, (850, 550, 150, 50))
    pygame.draw.rect(screen, BLACK, (850, 450, 180, 50))

    for i, d in enumerate(points):
        pygame.draw.circle(screen, BLACK, (d[0] + 55, d[1] + 55), 4)
        pygame.draw.circle(screen, WHITE if not len(labels) else COLORS[labels[i]], (d[0] + 55, d[1] + 55), 3) 
    for i, d in enumerate(clusters):
        pygame.draw.circle(screen, COLORS[i], (d[0] + 55, d[1] + 55), 5)

    text_K = font_create_text(f"K = {str(K)}", BLACK)


    screen.blit(text_K, (1050, 50))

    screen.blit(text_plus, (864, 52))
    screen.blit(text_minus, (968, 49))
    screen.blit(text_run, (890, 152))
    screen.blit(text_random, (850, 250))
    screen.blit(text_reset, (873, 552))
    screen.blit(text_algorithm, (855, 452))


    error = 0
    if len(clusters) and len(labels):
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]])
    text_error = font_create_text(f"Error = {str(int(error))}", BLACK)
    screen.blit(text_error, (850, 350))

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)


pygame.quit()