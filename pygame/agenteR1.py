import sys
import numpy as np
from enum import Enum, unique
import pygame
from pygame.locals import *

import time
import scipy.stats
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
    

# Enumeration fo the action
@unique
class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Tile(Enum):
    INACCESSIBLE= -2
    UNKNOWN = -1
    BLANK = 0
    ITEM = 1
    ITEM_SPECIAL = 2
    CORNER = 3
    BORDER_TOP = 4
    BORDER_LATERAL = 5
    AGENT = 6

# class for the agent
class Agent():
    # constructor
    def __init__(self, x = 0, y = 0, agent_type = None, enviroment_size = None):
        # set initial values
        self.x = x
        self.y = y
        self.agent_type = agent_type
        # if type is not reativo_simples
        if self.agent_type != "reativo_simples" and self.agent_type is not None:
            # create enviroment by repeating -1 n*m times, and reshaping it as n x m
            self.enviroment = np.repeat(Tile.UNKNOWN.value, enviroment_size[0]*enviroment_size[1]).reshape(enviroment_size)
            # set borders
            self.enviroment[0, :] = self.enviroment[:, 0] = self.enviroment[:, -1] = self.enviroment[-1, :] = Tile.INACCESSIBLE.value
            # check if the type is baseado_utilidade
            if self.agent_type == "baseado_utilidade":
                # create value of the tile dict
                self.values = {Tile.ITEM.value: 1.0, Tile.ITEM_SPECIAL.value: 4.0, Tile.UNKNOWN.value: 0.2}
        else:
            self.enviroment = None
        #print("[Agente Type] = " + str(self.agent_type) )
        
    # method to read the sensor basesed on the 
    def readSensor(self, enviroment = None):
        # check if an external enviroment wag given
        if enviroment is None:
            # then set enviroment to self envoriment
            enviroment = self.enviroment
        # up sensor
        up = enviroment[self.y+1, self.x]
        # dwon sensor
        down = enviroment[self.y-1, self.x]
        # right sensor
        right = enviroment[self.y , self.x+1]
        # left sensor
        left = enviroment[self.y, self.x-1]
        # return sensors
        return up, right, down, left

    # method to check if the agent succed
    def checkSuccess(self, enviroment):
        # return if there is any item or special item on the enviroment
        return not (np.any(enviroment == Tile.ITEM.value) or np.any(enviroment == Tile.ITEM_SPECIAL.value) )

    # method to update enviroment
    def updateEnviroment(self, sensors):
        # update enviroment at pos of the agent
        self.enviroment[self.y][self.x] = Tile.BLANK.value
        # for each sensor update the enviroment
        self.enviroment[self.y+1][self.x] = sensors[0]
        self.enviroment[self.y][self.x+1] = sensors[1]
        self.enviroment[self.y-1][self.x] = sensors[2]
        self.enviroment[self.y][self.x-1] = sensors[3]
    
    # main agent function
    def __call__(self, enviroment):
        # get sensors
        sensors = self.readSensor(enviroment)
        # check type
        if self.agent_type == "reativo_simples":
            # check the sensors if there is an item in that position
            for action_ in Action:
                # check if the sensor apointed by that action is an item
                if sensors[action_.value] == Tile.ITEM.value or sensors[action_.value] == Tile.ITEM_SPECIAL.value:
                    # set action to action_
                    action = action_ 
                    # break
                    break
            else:
                # use random method
                idx = [Action.DOWN, Action.UP, Action.RIGHT, Action.LEFT]
                # get a random action
                action = idx[np.random.randint(4)]
        
        elif self.agent_type == "baseado_modelo":
            # update self enviroment
            self.updateEnviroment(sensors)
            # check that direction of self.enviroment
            if np.any(self.enviroment[self.y:, self.x] == Tile.ITEM.value) or np.any(self.enviroment[self.y:, self.x] == Tile.ITEM_SPECIAL.value) :
                # set action
                action = Action.UP
            elif np.any(self.enviroment[:self.y, self.x] == Tile.ITEM.value) or np.any(self.enviroment[:self.y, self.x] == Tile.ITEM_SPECIAL.value) :
                # set action
                action = Action.DOWN
            elif np.any(self.enviroment[self.y, :self.x] == Tile.ITEM.value) or np.any(self.enviroment[self.y, :self.x] == Tile.ITEM_SPECIAL.value) :
                # set action
                action = Action.LEFT
            elif np.any(self.enviroment[self.y, self.x:] == Tile.ITEM.value) or np.any(self.enviroment[self.y, self.x:] == Tile.ITEM_SPECIAL.value) :
                # set action
                action = Action.RIGHT
            elif np.any(self.enviroment[self.y:, self.x] == Tile.UNKNOWN.value):
                # set action
                action = Action.UP
            elif np.any(self.enviroment[self.y, self.x:] == Tile.UNKNOWN.value):
                # set action
                action = Action.RIGHT
            elif np.any(self.enviroment[:self.y, self.x] == Tile.UNKNOWN.value):
                # set action
                action = Action.DOWN
            elif np.any(self.enviroment[self.y, :self.x] == Tile.UNKNOWN.value):
                # set action
                action = Action.LEFT
            else:
                # use random method
                idx = [Action.DOWN, Action.UP, Action.RIGHT, Action.LEFT]
                # get a random action
                action = idx[np.random.randint(4)]
               
        elif self.agent_type == "baseado_objetivo":
            # update self enviromentd
            self.updateEnviroment(sensors)
            # get distance:
            distance = self.check_distance(self.x, self.y, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value])
            # get min distance in action
            min_distance = np.min(distance)

            # for action up
            up_distance = np.min(self.check_distance(self.x, self.y+1, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value]) )
            # check if the distance shortned
            if up_distance < min_distance:
                action = Action.UP
                # print action
                # return action
                return action
            # for action up
            left_distance = np.min(self.check_distance(self.x-1, self.y, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value]) )
            # check if the distance shortned
            if left_distance < min_distance:
                action = Action.LEFT
                # print action
                # return action
                return action
            # for action up
            down_distance = np.min(self.check_distance(self.x, self.y-1, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value]) )
            # check if the distance shortned
            if down_distance < min_distance:
                action = Action.DOWN
                # print action
                # return action
                return action
            # for action up
            right_distance = np.min(self.check_distance(self.x+1, self.y, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value]) )
            # check if the distance shortned
            if right_distance < min_distance:
                action = Action.RIGHT
                # print action
                # return action
                return action

             # get distance:
            distance = self.check_distance(self.x, self.y, [Tile.UNKNOWN.value, ])
            # get min distance in action
            min_distance = np.min(distance)


            # for action up
            up_distance = np.min(self.check_distance(self.x, self.y+1, [Tile.UNKNOWN.value, ]) )
            # check if the distance shortned
            if up_distance < min_distance:
                action = Action.UP
                # print action
                # return action
                return action
            # for action up
            left_distance = np.min(self.check_distance(self.x-1, self.y, [Tile.UNKNOWN.value, ]) )
            # check if the distance shortned
            if left_distance < min_distance:
                action = Action.LEFT
                # print action
                # return action
                return action
            # for action up
            down_distance = np.min(self.check_distance(self.x, self.y-1, [Tile.UNKNOWN.value, ]) )
            # check if the distance shortned
            if down_distance < min_distance:
                action = Action.DOWN
                # print action
                # return action
                return action
            # for action up
            right_distance = np.min(self.check_distance(self.x+1, self.y, [Tile.UNKNOWN.value, ]) )
            # check if the distance shortned
            if right_distance < min_distance:
                action = Action.RIGHT
                # print action
                # return action
                return action

            # use random method
            idx = [Action.DOWN, Action.UP, Action.RIGHT, Action.LEFT]
            # get a random action
            action = idx[np.random.randint(4)]
            #print(list(self.en.value))
            
        elif self.agent_type == "baseado_utilidade":
            # update self enviromentd
            self.updateEnviroment(sensors)
            # get distance:
            satisfaction = self.check_satisfaction(self.x, self.y, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value, Tile.UNKNOWN.value])
            # get min satisfaction in action
            min_satisfaction = satisfaction

            # for action up
            up_satisfaction = self.check_satisfaction(self.x, self.y+1, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value, Tile.UNKNOWN.value]) 
            #print(up_satisfaction)
            # check if the satisfaction shortned
            if up_satisfaction > min_satisfaction:
                action = Action.UP
                # print action
                #print(action)
                # return action
                return action
            # for action up
            left_satisfaction = self.check_satisfaction(self.x-1, self.y, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value, Tile.UNKNOWN.value]) 
            #print(left_satisfaction)
            # check if the satisfaction shortned
            if left_satisfaction > min_satisfaction:
                action = Action.LEFT
                # print action
                #print(action)
                # return action
                return action
            # for action up
            down_satisfaction = self.check_satisfaction(self.x, self.y-1, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value, Tile.UNKNOWN.value]) 
            #print(down_satisfaction)
            # check if the satisfaction shortned
            if down_satisfaction > min_satisfaction:
                action = Action.DOWN
                # print action
                #print(action)
                # return action
                return action
            # for action up
            right_satisfaction = self.check_satisfaction(self.x+1, self.y, [Tile.ITEM.value, Tile.ITEM_SPECIAL.value, Tile.UNKNOWN.value]) 
            #print(right_satisfaction)
            # check if the satisfaction shortned
            if right_satisfaction > min_satisfaction:
                action = Action.RIGHT
                # print action
                #print(action)
                # return action
                return action

            # use random method
            idx = [Action.DOWN, Action.UP, Action.RIGHT, Action.LEFT]
            # get a random action
            action = idx[np.random.randint(4)]
            #print(list(self.en.value))
            #print("--Random--")
        
        else:
            # implement the random method
            idx = [Action.DOWN, Action.UP, Action.RIGHT, Action.LEFT]
            # get a random action
            action = idx[np.random.randint(4)]
        
        return action

    # function to calculate the item distance
    def check_distance(self, x, y, paramters):
        # distance matrix
        distance = np.repeat(np.inf, self.enviroment.shape[0]*self.enviroment.shape[1]).reshape(self.enviroment.shape)
        # for i in col
        for i in range(len(self.enviroment)):
            for j in range(len(self.enviroment[i])):
                # check if the tile in that coordinate is an valid one
                if self.enviroment[i, j] in paramters:
                    # then, calculate the distance
                    distance[i, j] = float(i-y)**2 + float(j-x)**2
        # return the distance
        return distance

    # function to calculate satisfaction
    def check_satisfaction(self, x, y, paramters):
        # distance matrix
        satisfaction = np.repeat(0.0, self.enviroment.shape[0]*self.enviroment.shape[1]).reshape(self.enviroment.shape)
        # for i in col
        for i in range(len(self.enviroment)):
            for j in range(len(self.enviroment[i])):
                # item
                item = self.enviroment[i, j]
                # check if the tile in that coordinate is an valid one
                if item in paramters:
                    # then, calculate the distance
                    satisfaction[i, j] = float(self.values[item]**2) / ( ( float(i-y)**2 + float(j-x)**2 ) + 1.0)
        
        # return the distance
        return np.max(satisfaction)

# function to create the enviroment matrix
def createEnviroment(size):
    # generate random matrix
    matrix = np.random.randint(3, size = size)
    # change border of the matrix
    # set top and bottom to 4
    matrix[0, :] = matrix[-1, :] = Tile.BORDER_TOP.value
    # set left and right to 5
    matrix[:, 0] = matrix[:, -1] = Tile.BORDER_LATERAL.value
    # set corners to 3
    matrix[0, 0] = matrix[0, -1] = matrix[-1, 0] = matrix[-1, -1] = Tile.CORNER.value
    # return the enviroment matrix
    return matrix

# method to update Enviroment
def updateEnviroment(enviroment, agent, action = None):
    # set the value on the enviroment on that position to 0
    enviroment[agent.y, agent.x] = Tile.BLANK.value
    # check action
    if action == Action.UP and enviroment[agent.y+1, agent.x] < 3:
        agent.y += 1
    elif action == Action.DOWN and enviroment[agent.y-1, agent.x] < 3:
        agent.y -= 1
    elif action == Action.RIGHT and enviroment[agent.y, agent.x+1] < 3:
        agent.x += 1
    elif action == Action.LEFT and enviroment[agent.y, agent.x-1] < 3:
        agent.x -= 1
    # update new agent postion on the enviroment
    enviroment[agent.y, agent.x] = Tile.AGENT.value
    # return enviroment and agent
    return enviroment, agent

# method to show the enviroment based on pygame
def showEnviroment_pygame(enviroment, screen, scale_factor):
    # reset to black
    screen.fill((0, 0, 0))
    # initial x and y
    x, y = 0, 0
    # for each row and col
    for col_codes in enviroment:
        for object_code in col_codes:
            # check object code
            if object_code == Tile.BORDER_TOP.value:
                # draw the rectangule of the top 
                pygame.draw.rect(screen, (189, 76, 0), pygame.Rect(x, y, scale_factor, scale_factor))
            elif object_code == Tile.BORDER_LATERAL.value:
                # draw the rectangule of the lateral
                pygame.draw.rect(screen, (0, 76, 255), pygame.Rect(x, y, scale_factor, scale_factor))
            elif object_code == Tile.CORNER.value:
                # draw the rectangule of the corner
                pygame.draw.rect(screen, (189, 76, 255), pygame.Rect(x, y, scale_factor, scale_factor))
            elif object_code == Tile.AGENT.value:
                # points of the losangulo of the agent
                left = (x, y + scale_factor/2 )
                right = (x + scale_factor, y + scale_factor/2)
                top = ( x + scale_factor/2, y)
                bottom = ( x + scale_factor/2, y + scale_factor)
                # draw the losangulo of the agent
                pygame.draw.polygon(screen, (230, 230, 230), (top, right, bottom, left) )
            elif object_code == Tile.ITEM.value:
                # draw the normal circle (smaller)
                pygame.draw.circle(screen, (60, 208, 112), ( int(x + scale_factor/2) , int( y + scale_factor/2) ), int(scale_factor/6 ) )
            elif object_code == Tile.ITEM_SPECIAL.value:
                # draw the special circle (bigger)
                pygame.draw.circle(screen, (255, 157, 171), ( int(x + scale_factor/2) , int( y + scale_factor/2) ), int(scale_factor*0.25 ) )
            
            # increase the x
            x += scale_factor
        # increase y
        y += scale_factor
        # reset x
        x = 0
        
# method to show the enviroment  on low graphics
def showEnviroment_low(enviroment):
    # check if envoriment is None
    if enviroment is None:
        return
    #list of sprites
    sprites = ['@', '.', '*', '+', '-', '|', 'A', 'X', '?']
    # for each row
    for row in enviroment:
        # for element in the row
        for element in row:
            # print the sprite
            print(sprites[element], end = ' ')
        # print endline
        print('')

# main function
def main(size = None, agent_type = "random"):
    # check if size is None
    if size is None:
        # if so, set it to defaut (36)
        size = 36
    # game time_block
    time_block = 60
    # set enviroment size
    enviroment_size = (size, size)
    #scale factor
    scale_factor = 15
    # create enviroment
    enviroment = createEnviroment(enviroment_size)
    # create Agent
    agent = Agent(1, 1, agent_type = agent_type, enviroment_size=enviroment_size)
    # update enviroment
    enviroment, agent = updateEnviroment(enviroment, agent)

    # create screen
    screen = pygame.display.set_mode( ( enviroment_size[0]*scale_factor, enviroment_size[1]*scale_factor) ) 
    # game clock
    clock = pygame.time.Clock()
    # boolean value if the game is done
    done = False
    # boolean if the automation is true
    automate = True

    # while the agent didnt succeed
    while not done:
        # show enviroment
        showEnviroment_pygame(enviroment, screen, scale_factor)
        
        # get button pressed
        pressed = pygame.key.get_pressed()
        
        # flip the display
        pygame.display.flip()
        # for each event
        for event in pygame.event.get():
            # check if the event is quit
            if event.type == pygame.QUIT:
                # if so, done = True
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_DOWN and not automate:
                    # get agent action
                    action = agent(enviroment)
                    # update enviroment
                    enviroment, agent = updateEnviroment(enviroment, agent, action)
                elif event.key == K_UP:
                    # chage automate
                    automate = not automate
                    
        # check if the success was achieved
        if agent.checkSuccess(enviroment):
            # set done to true
            done = True
            
        # check if the game is on automate
        if automate:
            # get agent action
            action = agent(enviroment) 
            # update enviroment
            enviroment, agent = updateEnviroment(enviroment, agent, action)
            
        # will block execution until 1/60 seconds have passed 
        # since the previous time clock.tick was called. 
        clock.tick(time_block)
        
if __name__ == "__main__":
    # boolean if the parameters are valid
    valid = True
    # boolean if profile is setted
    profile = False
    # number of times
    profile_times = 10
    # plot
    plot = False
    # size
    size = 36
    # save
    save = False
    # tyoe
    agent_type = "random"
    # check sys argv
    for element in sys.argv[1:]:
        # check if size is in element
        if "--size=" in element:
            idx = element.find("--size=") + len("--size=")
            # try to convert size
            try:
                size = int(element[idx:])
            except Exception as err:
                print("[ERROR] Invalid Value for Size")
                valid = False
        # check if size is in element
        if "--type=" in element:
            idx = element.find("--type=") + len("--type=")
            # try to convert size
            agent_type = element[idx:]
            if agent_type not in ["random", "reativo_simples", "baseado_modelo", "baseado_objetivo", "baseado_utilidade"]:
                print("[ERROR] Invalid Value for Type")
                valid = False
        # profile
        if "--profile" in element:
            profile = True
        # check if profile
        if "--profile=" in element:
            idx = element.find("--profile=") + len("--profile=")
            # try to convert size
            try:
                profile_times = int(element[idx:])
            except:
                print("[ERROR] Invalid Value for Profile")
                valid = False
            else:
                profile = True
        # check if plot settings is on
        if "--plot" in element and profile:
            plot = True
        # check if plot settings is on
        if "--save" in element and profile:
            save = True
        
    # check if valid
    if valid:
        # init pygame
        pygame.init()
        # check if profile
        if not profile:
            # call test function with paramters
            main(size, agent_type)
        else:
            # array
            array = []
            # for each time
            for i in range(profile_times):
                # initial time
                initial_time = time.time()
                # call function
                main(size, agent_type)
                # final time
                final_time = time.time()
                # time
                delta_time = final_time-initial_time
                # print time
                print(str(i) + ": Time = " + str(delta_time) + "s")
                # append delta time to the array
                array.append(delta_time)
            # convert to numpy
            array = np.array(array)
            # get standar derivation and mean
            std = np.std(array)
            mean = np.mean(array)
                
            # check if plot
            if plot or save:
                # runs array
                runs = np.arange(len(array))
                # create figurs
                fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize=(10, 8))
                # plot array
                ax[0].plot(runs, array, linestyle='--', marker='.')
                # plt title
                ax[0].grid(True)
                ax[0].set_title("Time of the Runs")
                ax[0].set_ylabel("Time")
                # range
                range_ = size
                # get normal distribution
                x = np.linspace(mean-range_, mean+range_, 300)
                # ticks
                x_ticks = np.linspace(mean-range_, mean+range_, 11)
                # plot normal distribution
                y = scipy.stats.norm.pdf(x, mean, std)
                # plot plt
                ax[1].grid(True)
                ax[1].plot(x, y, color = "red")
                ax[1].set_title("Normal Distribution ")
                ax[1].set_xlabel("X")
                ax[1].set_ylabel("Y")
                ax[1].set_xticks(x_ticks)
                #ax[1].xaxis.set_major_locator(MultipleLocator(mean))
                
                # show plot
                if save:
                    # save it
                    fig.savefig("results/size_" + str(size) + "-" + str(profile_times) + "_samples-" + agent_type + ".png")
                if plot:
                    # show plot
                    plt.show()
                
            else:
                # print array
                print("Array:")
                print(array)

            print("================")
            print("Standard Derivation: " + str( std ) )
            print("Mean: " + str( mean ) + "s")