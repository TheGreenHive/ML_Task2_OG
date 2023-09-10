# This Code is Heavily Inspired By The YouTuber: Cheesy AI
# Code Changed, Optimized And Commented By: NeuralNine (Florian Dedov)
# This code has again been hoisted by the CGS Digital Innovation Department
# giving credit to the above authors for the benfit of our education in ML

import math
import random
import sys
import os

import neat
import pygame

# Constants
# WIDTH = 1600
# HEIGHT = 880

WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 60
CAR_SIZE_Y = 60

BORDER_COLOR = (255, 255, 255, 255)  # Color To Crash on Hit

current_generation = 0  # Generation counter
"""
The Car Class 

Throughout this section, you will need to explore each function
and provide extenive comments in the spaces denoted by the 
triple quotes(block quotes) """ """.
Your comments should describe each function and what it is doing, 
why it is necessary and where it is being used in the rest of the program.

"""


class Car:
    """1. This Function:
        This is the initialization function for the car class and gets called whenever a new car object is created. The first three lines initialise the sprite of the car from the file 'car.png'. This then gets converted to an object that can be displayed in pygame. The next three lines initialise the car position with the starting position, the angle of the car and the speed of the car. A variable is set to whether the car can set its speed. The centre of the car is calculated before initialising an empty array to hold the radars and the radar object that is drawn to the screen. The car is initialised as alive and then the distance driven and the time passed is initialised."""

    def __init__(self):
        # Load Car Sprite and Rotate
        self.sprite = pygame.image.load("car.png").convert()  # Convert Speeds Up A Lot
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite

        # self.position = [690, 740] # Starting Position
        self.position = [830, 920]  # Starting Position
        self.angle = 0
        self.speed = 0

        self.speed_set = False  # Flag For Default Speed Later on

        self.center = [
            self.position[0] + CAR_SIZE_X / 2,
            self.position[1] + CAR_SIZE_Y / 2,
        ]  # Calculate Center

        self.radars = []  # List For Sensors / Radars
        self.drawing_radars = []  # Radars To Be Drawn

        self.alive = True  # Boolean To Check If Car is Crashed

        self.distance = 0  # Distance Driven
        self.time = 0  # Time Passed

    """ 2. This Function:
    This function takes in the self and the screen as an argument and draws the sprite and the radars to the screen.
    
    """

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position)  # Draw Sprite
        self.draw_radar(screen)  # OPTIONAL FOR SENSORS

    """ 3. This Function:
    This function takes the self and the screen as arguments and loops through all the radars in the self.radars array and draws them to the screen.
    
    """

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    """ 4. This Function:
    This function takes in the self and the game_map as an argument. It starts by setting the self.alive to true and then loops through all corners of the object. It then checks if that corner is over the colour of the border and if it is, it set self.alive to false and breaks out of the loop.
    
    """

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            # If Any Corner Touches Border Color -> Crash
            # Assumes Rectangle
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    """ 5. This Function:
    This function takes in the self, a degree value, and a game_map value as arguments. It begins by initializing a length variable to zero. It then creates a vector with the magnitude of the length variable, and the degree of the degree variable. The final point is stored in an x variable and a y variable. A loop is then run, incrementing the length by 1 each time and checking if the vector intersects with the specified colour of the border. If this doesn't happen, the vector has a final length of 300. The distance to that point is then calculated using the pythagorean theorem and the radars, as well as the distance are appended to the self.radars attribute.
    """

    def check_radar(self, degree, game_map):
        length = 0
        x = int(
            self.center[0]
            + math.cos(math.radians(360 - (self.angle + degree))) * length
        )
        y = int(
            self.center[1]
            + math.sin(math.radians(360 - (self.angle + degree))) * length
        )

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(
                self.center[0]
                + math.cos(math.radians(360 - (self.angle + degree))) * length
            )
            y = int(
                self.center[1]
                + math.sin(math.radians(360 - (self.angle + degree))) * length
            )

        # Calculate Distance To Border And Append To Radars List
        dist = int(
            math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))
        )
        self.radars.append([(x, y), dist])

    """ 6. This Function:
    This function takes in the self and the game_map as an argument. It begins by checking if the speed of the self is set, and if it is not, it sets it to 20. This will only happen when the function is called for the first time. The sprite is then rotated to the self.angle value. The car is then moved by the speed value, but if it comes closer than 20px to the edge of the screen, it doesn't let the car. The self.distance value is updated, as well as the self.time. The centre of the car is then recalculated after the car has been moved. All four positions of the corners of the car are then calculated and then updated in the self. Finally, the collisions of the car are checked, the radars are cleared, and their values are recalculated, starting at -90, to 120, with a step size of 45.
    """

    def update(self, game_map):
        # Set The Speed To 20 For The First Time
        # Only When Having 4 Output Nodes With Speed Up and Down
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Get Rotated Sprite And Move Into The Right X-Direction
        # Don't Let The Car Go Closer Than 20px To The Edge
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Increase Distance and Time
        self.distance += self.speed
        self.time += 1

        # Same For Y-Position
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Calculate New Center
        self.center = [
            int(self.position[0]) + CAR_SIZE_X / 2,
            int(self.position[1]) + CAR_SIZE_Y / 2,
        ]

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * CAR_SIZE_X
        left_top = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length,
        ]
        right_top = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length,
        ]
        left_bottom = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length,
        ]
        right_bottom = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length,
        ]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 42):
            self.check_radar(d, game_map)

    """ 7. This Function:
    This function takes the self as an argument. It sets the radars variable to the radars of the self and then sets a return_values variable to an array of 5 zeros. It then iterates over each of the radars and sets the return_values element of that iteration to the radar length / 30 (which is the max length of the radar so it turns it to a value between zero and 1). the return_values array is then returned.
    """

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    """ 8. This Function:
    This function returns whether the self is alive or not. (This is a sign of poorly written code)
    """

    def is_alive(self):
        # Basic Alive Function
        return self.alive

    """ 9. This Function:
    This function returns the reward of the car. It takes the self's total distance driven and divides it by half of the car length. This function will take longer to train than other reward functions, but it will produce a better model in the end. There is a slight issue with this code, which is that it is not calculating the distance around the track, it is calculating the distance driven. This might create a model that zig-zags down the track to maximise its distance rather than driving on the perfect racing line. To fix this issue, each map could include various points so that the distance can be properly calculated.
    """

    def get_reward(self):
        # Calculate Reward (Maybe Change?)
        # return self.distance / 50.0
        return self.distance / (CAR_SIZE_X / 2)

    """ 10. This Function:
    This function takes in the self, an image and an angle value. It uses the pygame library to rotate the inputted image by the inputted angle, calculate the centre of that image, and then return it.
    """

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image


""" This Function:
This function starts by taking in a genomes parameter and a config parameter. The function initializes a nets array and cars array to empty arrays. It then initializes the pygame display to the width and height constants. The function then initializes all agents in the genomes array, and appends an empty car object to the cars array. The clock variable is initialized to the current pygame time and the fonts and maps are loaded. The current_generation variable is loaded as a global variable and is incremented by one. A counter variable is initialized to zero to serve as a primitive time limit variable. The code then begins to loop. The loop starts by checking if pygame has called a quit event, and if this has happend, the code exits with a 0 return code. The code then loops through all of the cars and runs their neurla network with their inputs. The highest value output neuron is then calculated and based on this, the car speeds up, slows down, turns left, or turns right. A still_alive variable is initialized with a value of 0. All of the cars are then looped over, and if they are alive, their total fitness gets updated and the still_alive variable is incremented by one. The code then checks if there are zero cars still alive or if the counter variable is greater than 30 * 40 (which will happen after about 20 seconds) and if they are true, the loop is broken. The info about the current generation and the number still alive is displayed on the screen, and clock is ticked at 60fps.
"""


def run_simulation(genomes, config):
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load("map3.png").convert()  # Convert Speeds Up A Lot

    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10  # Left
            elif choice == 1:
                car.angle -= 10  # Right
            elif choice == 2:
                if car.speed - 2 >= 12:
                    car.speed -= 2  # Slow Down
            else:
                car.speed += 2  # Speed Up

        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40:  # Stop After About 20 Seconds
            break

        # Draw Map And All Cars That Are Alive
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        # Display Info
        text = generation_font.render(
            "Generation: " + str(current_generation), True, (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS


""" 1. This Section:
    This section starts by checking if the program is running directly from the kernels request. It then loads the config.txt and uses the neat library to load the hyperparametres of the model into a variable called config. It then creates a population variable that is a neat.Population object that takes in the hyperparameters from the config variable. A reporter is added to the variable which will print out to the standard output. A statistics reporter is also added to the population variable. The population variable is then for 1000 generations.
"""
if __name__ == "__main__":
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)
