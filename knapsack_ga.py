#0/1 Knapsack Problem

import random

items = [['laptop', 3, 1500], ['Camera', 1, 800],['smartphone',0.2,500],['Wallet', 0.5, 50],['Sunglasses', 1, 100],
        ['Water Bottle', 0.2, 10],['Book', 1, 20],['Headphones', 0.3, 200],['Jacket', 1.5, 100],['Snack', 1, 50], ['Power Bank', 0.3, 50]]

pop_size = 10 # population size
num_gen = 200 # number of generations
max_weight = 7 # max weight of the knapsack
pc = 0.9 # probability of crossover
pm = 0.2 # probability of mutation

def generate_population(size): # Generate a selection of random solutions with 1 representing that the item is selected, and 0 meaning it hasn't been selected

    population = []
    for _ in range(size):
        genes = [0,1]
        chromosome = []
        for _ in items:
            chromosome.append(random.choice(genes))
        population.append(chromosome)

    return population # The population will look like the following array: e.g  [[0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0], [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0], ...]
                                 # The number of solutions will depend on "pop_size" 

def fitness(chromosome): # This funtion calculates the fitness values, if the total weight is exceeded, the fitness value will be 0, if not retruns total value

    t_weight = 0
    t_value = 0
    for i in range(len(chromosome) - 1):
        if chromosome[i] == 1:
            t_weight += items[i][1]
            t_value += items[i][2]
    if t_weight > max_weight:
        return 0
    else:
        return t_value
    
def list_fitness(population): # Lists the values with the corresponding population

    lst_values = []
    lst_pop = []
     
    for chromosome in population:
        lst_values.append(fitness(chromosome))
        lst_pop.append(chromosome)

    return lst_values, lst_pop

##################### Selection Phase #####################

# In here there are two Selection types (K Tournament and Roulette Wheel), you should only use one at a time

def k_tournament(population):  # This functions runs a selection type named k tournament 

    values = [] #List for the values
    new_pop = [] # New population after K Tournament 
    new_values= [] # New total values after K Tournament

    for chromosome in population:
        values.append(fitness(chromosome)) # calculate the fitness value

    while len(new_pop) < len(population):
        p1 = random.randint(0,len(population)-1) # Takes a random solution from the population
        p2 = random.randint(0,len(population)-1) 

        if values[p1] > values[p2]:
            new_values.append(values[p1])
            new_pop.append(population[p1])
        else:
            new_values.append(values[p2])
            new_pop.append(population[p2])

    return new_pop

def calculate_probability(population):# This function calculates the probabily of selection for Roulette Wheel

    p = [] # list of probabilities of selecting
    w = [] # list of cumulative probabilities

    lst_values, _ = list_fitness(population)
    sum_values = sum(lst_values)

    for value in lst_values:
        p.append(value/sum_values)
    for i in range(0,len(p)-1):
        if i == 0:
            w.append(p[0])
            w.append(w[0] + p[1])
        else:
            w.append(w[i] + p[i+1])

    return w 

def roulette_wheel(population):  # This functions runs a selection type named Roulette Wheel

    new_pop = []
    w = calculate_probability(population)

    while len(new_pop) < len(population): # Using dynamic comparison we select which whether the solution is eligible or not 
        r = random.uniform(0,1)
        for i in range(0, len(w) - 1):
            if r > w[i] and r <= w[i + 1]:
                new_pop.append(population[i]) 
                break

    return new_pop

##################### Crossover Phase #####################

def single_point_crossover(parent1, parent2): # This function runs a type crossover named single point corssover 

    c_point = random.randint(1, len(parent1) - 1) # Generate a random index
    slice1 = parent1[c_point:] # Slice from that index
    slice2 = parent2[c_point:]

    child1 = parent1[:c_point] + slice2 # Swap the selected slices making new offsprings
    child2 = parent2[:c_point] + slice1

    return child1, child2

def crossover(population): # This function used single point crossover to return new offsprings

    new_cpop= [] # New population after crossover
    while len(new_cpop) < len(population):
        r = random.uniform(0,0.99) # Generate a random number to compare with the Propability

        parent1 = random.choice(population)
        parent2 = random.choice(population)

        if r<=pc:
            child1, child2 = single_point_crossover(parent1, parent2)
        else:
            child1, child2 = parent1,parent2
        new_cpop.append(child1)
        new_cpop.append(child2)

    return new_cpop

##################### Mutation Phase #####################

def local_mutation(population): # This function runs a mutation type named Local mutation

    for chromosome in population:
        r = random.uniform(0,0.99) # Generate a random number to compare with the Propability
        if r <= pm:
            r_index = random.randint(0, len(chromosome)-1) # random index in the chromosome
            if chromosome[r_index] == 1:
                chromosome[r_index] = 0
            else:
                chromosome[r_index] = 1

    return population

def global_mutation(population): # This function runs a mutation type named global mutation (The only difference is the probalilty)

    gene_size = len(population[0])
    pm = 1/gene_size
    for chromosome in population:
        r = random.uniform(0,0.99)
        if r <= pm:
            r_index = random.randint(0, len(chromosome) - 1)
            if chromosome[r_index] == 1:
                chromosome[r_index] = 0
            else:
                chromosome[r_index] = 1

    return population 
 
##################### Survivor Phase #####################

def elitist(old_pop, off_pop): # This function runs a survivor type named Elitism (Takes the best solutions from both original population and offsprings)

    old_values, lst_old_pop = list_fitness(old_pop) # old population values 
    print(f"The old population values:\n {old_values}")

    off_values, lst_off_pop = list_fitness(off_pop) # off springs values 

    c_values = old_values + off_values
    c_pop = lst_old_pop + lst_off_pop

    zipped_list = zip(c_values, c_pop) # [(v, [1 0 1 ... 1]),(v, [0 1 1 ... 0]), ...]
    
    s_zipped_list = sorted(zipped_list, key=lambda x: x[0], reverse = True ) #Time complexity (O(n log n))
    elit_zipped_list = s_zipped_list[:len(s_zipped_list)//2]
    
    s_values = [value[0] for value in elit_zipped_list] #This uses list comprehension 
    s_pop = [chromosome[1] for chromosome in elit_zipped_list] 

    return s_pop

def non_elits(off_pop): # This function runs a survivor type named non Elitism (Takes the best solutions only from the offsprings)

    off_values, lst_off_pop = list_fitness(off_pop)
    print(f"List of off values:\n{off_values}")

    zipped_list = zip(off_values, lst_off_pop)
    s_zipped_list = sorted(zipped_list, key=lambda x:x[0], reverse = True)
    s_values = [value[0] for value in s_zipped_list]
    s_pop = [chromosome[1] for chromosome in s_zipped_list]
    print(f"This is the sorted elit values:\n{s_values}")

    return s_pop

def returnSol(pop): # This function returns the final solutions and the items you are allowed to take

    sol_items = []
    off_pop = pop[0]

    for gene in range(len(off_pop) -1):
        if off_pop[gene] == 1:
            sol_items.append(items[gene])
    print(sol_items)

##################### Final Loop #####################

def run_bga(): 

# Use whatever selection and survivor function you wish, you only need to uncomment them

    t = 1
    gen_pop = generate_population(pop_size)
    while t <= num_gen:
        print(f"################# Generation: {t} #################")
        off_pop = k_tournament(gen_pop) #O(n) 
        #off_pop = roulette_wheel(gen_pop) #O(n^2)
        c_pop = crossover(off_pop) # O(n) 
        m_pop = global_mutation(c_pop) # O(n)
        #m_pop = local_mutation(c_pop) # O(n)
        gen_pop = elitist(gen_pop, m_pop) # O(n log n)
        # gen_pop = non_elits(m_pop) #O(n log n)
        returnSol(gen_pop)
        t+=1

run_bga()





