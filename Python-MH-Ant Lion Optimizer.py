############################################################################

# Created by: Prof. Valdecy Pereira, D.Sc.
# UFF - Universidade Federal Fluminense (Brazil)
# email:  valdecy.pereira@gmail.com
# Course: Metaheuristics
# Lesson: Ant Lion Optimizer

# Citation: 
# PEREIRA, V. (2018). Project: Metaheuristic-Ant_Lion_Optimizer, File: Python-MH-Ant_Lion_Optimizer.py, GitHub repository: <https://github.com/Valdecy/Metaheuristic-Ant_Lion_Optimizer>

############################################################################

# Required Libraries
import numpy  as np
import math
import random
import os

# Function
def target_function():
    return

# Function: Initialize Variables
def initial_population(colony_size = 5, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    population = np.zeros((colony_size, len(min_values) + 1))
    for i in range(0, colony_size):
        for j in range(0, len(min_values)):
             population[i,j] = random.uniform(min_values[j], max_values[j]) 
        population[i,-1] = target_function(population[i,0:population.shape[1]-1])
    return population

# Function: Fitness
def fitness_function(population): 
    fitness = np.zeros((population.shape[0], 2))
    for i in range(0, fitness.shape[0]):
        fitness[i,0] = 1/(1+ population[i,-1] + abs(population[:,-1].min()))
    fit_sum = fitness[:,0].sum()
    fitness[0,1] = fitness[0,0]
    for i in range(1, fitness.shape[0]):
        fitness[i,1] = (fitness[i,0] + fitness[i-1,1])
    for i in range(0, fitness.shape[0]):
        fitness[i,1] = fitness[i,1]/fit_sum
    return fitness

# Function: Selection
def roulette_wheel(fitness): 
    ix = 0
    random = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
    for i in range(0, fitness.shape[0]):
        if (random <= fitness[i, 1]):
          ix = i
          break
    return ix

# Function: Random Walk
def random_walk(iterations):
    x_random_walk = [0]*(iterations + 1)
    x_random_walk[0] = 0
    for k in range(1, len( x_random_walk)):
        rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
        if rand > 0.5:
            rand = 1
        else:
            rand = 0
        x_random_walk[k] = x_random_walk[k-1] + (2*rand - 1)       
    return x_random_walk

# Function: Combine Ants
def combine(population, antlions):
    combination = np.vstack([population, antlions])
    combination = combination[combination[:,-1].argsort()]
    for i in range(0, population.shape[0]):
        for j in range(0, population.shape[1]):
            antlions[i,j]   = combination[i,j]
            population[i,j] = combination[i + population.shape[0],j]
    return population, antlions

# Function: Update Antlion
def update_ants(population, antlions, count, iterations, min_values = [-5,-5], max_values = [5,5], target_function = target_function):
    i_ratio       = 1
    minimum_c_i   = np.zeros((1, population.shape[1]))
    maximum_d_i   = np.zeros((1, population.shape[1]))
    minimum_c_e   = np.zeros((1, population.shape[1]))
    maximum_d_e   = np.zeros((1, population.shape[1]))
    elite_antlion = np.zeros((1, population.shape[1]))
    if  (count > 0.10*iterations):
        w_exploration = 2
        i_ratio = (10**w_exploration)*(count/iterations)  
    elif(count > 0.50*iterations):
        w_exploration = 3
        i_ratio = (10**w_exploration)*(count/iterations)   
    elif(count > 0.75*iterations):
        w_exploration = 4
        i_ratio = (10**w_exploration)*(count/iterations)    
    elif(count > 0.90*iterations):
        w_exploration = 5
        i_ratio = (10**w_exploration)*(count/iterations)   
    elif(count > 0.95*iterations):
        w_exploration = 6
        i_ratio = (10**w_exploration)*(count/iterations)
    for i in range (0, population.shape[0]):
        fitness = fitness_function(antlions)
        ant_lion = roulette_wheel(fitness)
        for j in range (0, population.shape[1] - 1):   
            minimum_c_i[0,j]   = antlions[antlions[:,-1].argsort()][0,j]/i_ratio
            maximum_d_i[0,j]   = antlions[antlions[:,-1].argsort()][-1,j]/i_ratio
            elite_antlion[0,j] = antlions[antlions[:,-1].argsort()][0,j]
            minimum_c_e[0,j]   = antlions[antlions[:,-1].argsort()][0,j]/i_ratio
            maximum_d_e[0,j]   = antlions[antlions[:,-1].argsort()][-1,j]/i_ratio  
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            if (rand < 0.5):
                minimum_c_i[0,j] =   minimum_c_i[0,j] + antlions[ant_lion,j]
                minimum_c_e[0,j] =   minimum_c_e[0,j] + elite_antlion[0,j]
            else:
                minimum_c_i[0,j] = - minimum_c_i[0,j] + antlions[ant_lion,j]
                minimum_c_e[0,j] = - minimum_c_e[0,j] + elite_antlion[0,j]
                
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            if (rand >= 0.5):
                maximum_d_i[0,j] =   maximum_d_i[0,j] + antlions[ant_lion,j]
                maximum_d_e[0,j] =   maximum_d_e[0,j] + elite_antlion[0,j]
            else:
                maximum_d_i[0,j] = - maximum_d_i[0,j] + antlions[ant_lion,j]
                maximum_d_e[0,j] = - maximum_d_e[0,j] + elite_antlion[0,j]   
            x_random_walk = random_walk(iterations)
            e_random_walk = random_walk(iterations)    
            min_x, max_x = min(x_random_walk), max(x_random_walk)
            x_random_walk[count] = (((x_random_walk[count] - min_x)*(maximum_d_i[0,j] - minimum_c_i[0,j]))/(max_x - min_x)) + minimum_c_i[0,j]   
            min_e, max_e = min(e_random_walk), max(e_random_walk)
            e_random_walk[count] = (((e_random_walk[count] - min_e)*(maximum_d_e[0,j] - minimum_c_e[0,j]))/(max_e - min_e)) + minimum_c_e[0,j]    
            population[i,j] = np.clip((x_random_walk[count] + e_random_walk[count])/2, min_values[j], max_values[j])
        population[i,-1] = target_function(population[i,0:population.shape[1]-1])
        return population, antlions

# ALO Function
def ant_lion_optimizer(colony_size = 5, min_values = [-5,-5], max_values = [5,5], iterations = 50, target_function = target_function):    
    count = 0  
    population = initial_population(colony_size = colony_size, min_values = min_values, max_values = max_values, target_function = target_function)
    antlions   = initial_population(colony_size = colony_size, min_values = min_values, max_values = max_values, target_function = target_function) 
    elite = np.copy(antlions[antlions[:,-1].argsort()][0,:]) 
    while (count <= iterations):   
        print("Iteration = ", count, " f(x) = ", elite[-1])   
        population, antlions = update_ants(population, antlions, count = count, iterations = iterations, min_values = min_values, max_values = max_values, target_function = target_function)
        population, antlions = combine(population, antlions)    
        value = np.copy(antlions[antlions[:,-1].argsort()][0,:])
        if(elite[-1] > value[-1]):
            elite = np.copy(value)
        else:
            antlions[antlions[:,-1].argsort()][0,:] = np.copy(elite)   
        count = count + 1      
    print(elite)    
    return elite

######################## Part 1 - Usage ####################################

# Function to be Minimized (Easom). Solution ->  f(x) = -1; xi = 3.14
def easom(variables_values = [0, 0]):
    return -math.cos(variables_values[0])*math.cos(variables_values[1])*math.exp(-(variables_values[0] - math.pi)**2 - (variables_values[1] - math.pi)**2)

alo = ant_lion_optimizer(colony_size = 80, min_values = [-1,-1], max_values = [7,7], iterations = 100, target_function = easom)

# Function to be Minimized (Six Hump Camel Back). Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def six_hump_camel_back(variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

alo = ant_lion_optimizer(colony_size = 80, min_values = [-5,-5], max_values = [5,5], iterations = 500, target_function = six_hump_camel_back)

# Function to be Minimized (Rosenbrocks Valley). Solution ->  f(x) = 0; xi = 1
def rosenbrocks_valley(variables_values = [0,0]):
    func_value = 0
    last_x = variables_values[0]
    for i in range(1, len(variables_values)):
        func_value = func_value + (100 * math.pow((variables_values[i] - math.pow(last_x, 2)), 2)) + math.pow(1 - last_x, 2)
    return func_value

alo = ant_lion_optimizer(colony_size = 100, min_values = [-5,-5], max_values = [5,5], iterations = 2500, target_function = rosenbrocks_valley)
