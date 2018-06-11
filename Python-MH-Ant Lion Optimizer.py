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
import pandas as pd
import numpy  as np
import math
import random
import os

# Function: Initialize Variables
def initial_population(colony_size = 5, min_values = [-5,-5], max_values = [5,5]):
    population = pd.DataFrame(np.zeros((colony_size, len(min_values))))
    population['Fitness'] = 0.0
    for i in range(0, colony_size):
        for j in range(0, len(min_values)):
             population.iloc[i,j] = random.uniform(min_values[j], max_values[j])
        population.iloc[i,-1] = target_function(population.iloc[i,0:population.shape[1]-1])
    return population

# Function: Fitness
def fitness_function(population): 
    fitness = pd.DataFrame(np.zeros((population.shape[0], 1)))
    fitness['Probability'] = 0.0
    for i in range(0, fitness.shape[0]):
        fitness.iloc[i,0] = 1/(1+ population.iloc[i,-1] + abs(population.iloc[:,-1].min()))
    fit_sum = fitness.iloc[:,0].sum()
    fitness.iloc[0,1] = fitness.iloc[0,0]
    for i in range(1, fitness.shape[0]):
        fitness.iloc[i,1] = (fitness.iloc[i,0] + fitness.iloc[i-1,1])
    for i in range(0, fitness.shape[0]):
        fitness.iloc[i,1] = fitness.iloc[i,1]/fit_sum
    return fitness

# Function: Selection
def roulette_wheel(fitness): 
    ix = 0
    rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
    for i in range(0, fitness.shape[0]):
        if (rand <= fitness.iloc[i, 1]):
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

def combine(population, antlions):
    combination = pd.concat([population, antlions])
    combination = combination.sort_values('Fitness')
    for i in range(0, population.shape[0]):
        for j in range(0, population.shape[1]):
            antlions.iloc[i,j]   = combination.iloc[i,j]
            population.iloc[i,j] = combination.iloc[i + population.shape[0],j]
    return population, antlions

# Function: Update Antlion
def update_ants(population, antlions, count, iterations, min_values = [-5,-5], max_values = [5,5]):

    i_ratio = 1
    minimum_c_i = pd.DataFrame(np.zeros((1, population.shape[1])))
    maximum_d_i = pd.DataFrame(np.zeros((1, population.shape[1])))
    minimum_c_e = pd.DataFrame(np.zeros((1, population.shape[1])))
    maximum_d_e = pd.DataFrame(np.zeros((1, population.shape[1])))

    elite_antlion = pd.DataFrame(np.zeros((1, population.shape[1])))
    
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
            
            minimum_c_i.iloc[0,j] = antlions.iloc[antlions['Fitness'].idxmin(),:][j]/i_ratio
            maximum_d_i.iloc[0,j] = antlions.iloc[antlions['Fitness'].idxmax(),:][j]/i_ratio
            elite_antlion.iloc[0,j] = antlions.iloc[antlions['Fitness'].idxmin(),j]
            minimum_c_e.iloc[0,j] = antlions.iloc[antlions['Fitness'].idxmin(),:][j]/i_ratio
            maximum_d_e.iloc[0,j] = antlions.iloc[antlions['Fitness'].idxmax(),:][j]/i_ratio
            
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            if (rand < 0.5):
                minimum_c_i.iloc[0,j] =   minimum_c_i.iloc[0,j] + antlions.iloc[ant_lion,j]
                minimum_c_e.iloc[0,j] =   minimum_c_e.iloc[0,j] + elite_antlion.iloc[0,j]
            else:
                minimum_c_i.iloc[0,j] = - minimum_c_i.iloc[0,j] + antlions.iloc[ant_lion,j]
                minimum_c_e.iloc[0,j] = - minimum_c_e.iloc[0,j] + elite_antlion.iloc[0,j]
                
            rand = int.from_bytes(os.urandom(8), byteorder = "big") / ((1 << 64) - 1)
            if (rand >= 0.5):
                maximum_d_i.iloc[0,j] =   maximum_d_i.iloc[0,j] + antlions.iloc[ant_lion,j]
                maximum_d_e.iloc[0,j] =   maximum_d_e.iloc[0,j] + elite_antlion.iloc[0,j]
            else:
                maximum_d_i.iloc[0,j] = - maximum_d_i.iloc[0,j] + antlions.iloc[ant_lion,j]
                maximum_d_e.iloc[0,j] = - maximum_d_e.iloc[0,j] + elite_antlion.iloc[0,j]
            
            x_random_walk = random_walk(iterations)
            e_random_walk = random_walk(iterations)
            
            min_x, max_x = min(x_random_walk), max(x_random_walk)
            x_random_walk[count] = (((x_random_walk[count] - min_x)*(maximum_d_i.iloc[0,j] - minimum_c_i.iloc[0,j]))/(max_x - min_x)) + minimum_c_i.iloc[0,j]
            
            min_e, max_e = min(e_random_walk), max(e_random_walk)
            e_random_walk[count] = (((e_random_walk[count] - min_e)*(maximum_d_e.iloc[0,j] - minimum_c_e.iloc[0,j]))/(max_e - min_e)) + minimum_c_e.iloc[0,j] 
            
            population.iloc[i,j] = (x_random_walk[count] + e_random_walk[count])/2
            if (population.iloc[i,j] > max_values[j]):
                population.iloc[i,j] =  max_values[j]
            elif(population.iloc[i,j] < min_values[j]):
                population.iloc[i,j] = min_values[j]
          
        population.iloc[i,-1] = target_function(population.iloc[i,0:population.shape[1]-1])
        
        #if(population.iloc[i,-1] < antlions.iloc[ant_lion,-1]):
            #for j in range(0, population.shape[1]):
                #antlions.iloc[ant_lion,j] = population.iloc[i,j]
                  
        return population, antlions

# ALO Function
def ant_lion_optimizer(colony_size = 5, min_values = [-5,-5], max_values = [5,5], iterations = 50):    
    count = 0
    
    population = initial_population(colony_size = colony_size, min_values = min_values, max_values = max_values)
    antlions   = initial_population(colony_size = colony_size, min_values = min_values, max_values = max_values)
    
    elite = antlions.iloc[antlions['Fitness'].idxmin(),:].copy(deep = True)
    
    while (count <= iterations):
        
        print("Iteration = ", count, " f(x) = ", elite[-1])
        
        population, antlions = update_ants(population, antlions, count = count, iterations = iterations, min_values = min_values, max_values = max_values)
        population, antlions = combine(population, antlions)
        
        if(antlions.iloc[antlions['Fitness'].idxmin(),:][-1] < elite[-1]):
            elite = antlions.iloc[antlions['Fitness'].idxmin(),:].copy(deep = True)
        else:
            for j in range(0, antlions.shape[1]):
                antlions.iloc[antlions['Fitness'].idxmin(),j] = elite[j]
        
        count = count + 1 
        
    print(elite)    
    return elite

######################## Part 1 - Usage ####################################

# Function to be Minimized. Solution ->  f(x1, x2) = -1.0316; x1 = 0.0898, x2 = -0.7126 or x1 = -0.0898, x2 = 0.7126
def target_function (variables_values = [0, 0]):
    func_value = 4*variables_values[0]**2 - 2.1*variables_values[0]**4 + (1/3)*variables_values[0]**6 + variables_values[0]*variables_values[1] - 4*variables_values[1]**2 + 4*variables_values[1]**4
    return func_value

alo = ant_lion_optimizer(colony_size = 30, min_values = [-5,-5], max_values = [5,5], iterations = 250)

# Function to be Minimized (Rosenbrocks Valley). Solution ->  f(x) = 0; xi = 1
def target_function(variables_values = [0, 0]):
    func_value = 0
    last_x = variables_values[0]
    for i in range(1, len(variables_values)):
        func_value = func_value + (100 * math.pow((variables_values[i] - math.pow(last_x, 2)), 2)) + math.pow(1 - last_x, 2)
    return func_value

alo = ant_lion_optimizer(colony_size = 50, min_values = [-5,-5,-5,-5], max_values = [5,5,5,5], iterations = 5000)
