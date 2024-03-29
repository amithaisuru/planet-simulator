import math

import pygame

pygame.init()

WIDTH, HEIGHT=800,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("planet simulation")

FONT = pygame.font.SysFont("comicsans", 16)

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
DARK_GREY = (80,78,81)

class Planet:
    AU = 149.6e6 * 1000 #astronomical unit in meters
    G = 6.6743e-11
    SCALE = 200/AU #1AU = 100 pixels
    TIMESTEP = 3600*24 #in seconds (= 1 day)

    def __init__(self,x,y,radius,color,mass) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass  # mass in kg

        self.orbit = [] #stores the points that the planet travels
        self.sun = False
        self.distance_to_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0
    
    def draw(self,win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        drawing_points = []
        if len(self.orbit) > 2:
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                drawing_points.append((x,y))
            pygame.draw.lines(win, self.color, False, drawing_points, 2)

        pygame.draw.circle(win,self.color,(x,y),self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km", 1, WHITE)
            win.blit(distance_text, (x,y))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * self.TIMESTEP
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0,0,30,YELLOW,1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.33 * 10**23)
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000

    planets_list = [sun, earth, mars, mercury, venus]

    
    time =0
    while run:
        clock.tick(60) #maximum frames that can be refreshed in set to 60 frames per second(this loop runs 60 times per sec)

        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets_list:
            planet.update_position(planets_list)
            planet.draw(WIN)
        
        time_text = FONT.render(f"day{time}", 1, WHITE)
        WIN.blit(time_text, (50,50))
        pygame.display.update()
        time += 1
    pygame.quit()

if __name__ == '__main__':
    main()