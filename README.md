# 0/1 Knapsack problem with genetic algorithm🧬:
The 0/1 Knapsack problem is a classic optimization problem in computer science and mathematics. It involves selecting a subset of items from a given set, each with its own value and weight, to maximize the total value while keeping the total weight within a given capacity constraint. The name "0/1" refers to the fact that items can either be included completely (weight of 1) or excluded entirely (weight of 0) from the knapsack.

# Implementation:
## Generating Population:
To implement the 0/1 Knapsack Problem using a Binary GA, we define the chromosome representation. Each chromosome represents a potential solution and is encoded as a binary string of the same length as the number of items in the problem with the value of '1' at a particular index means that the corresponding item is included in the knapsack, while '0' denotes exclusion. 

The GA starts by initializing a population of random chromosomes. The fitness of each chromosome is evaluated by calculating its total value while respecting the weight constraint. Chromosomes with higher fitness values are more likely to be selected for reproduction.

## Selection Phase With Crossover:
The next step is the selection process, where parents are chosen for mating based on their fitness. Popular selection methods include roulette wheel selection and tournament selection. The selected parents undergo crossover (In our case we used Single Point Crossover), where a random point is chosen along the chromosomes, and the binary strings are exchanged between parents to create offspring.

## Mutation Phase:
Mutation is then applied to introduce diversity in the population. Randomly selected bits in the chromosomes are flipped from '0' to '1' or vice versa. This helps explore new regions of the search space.

## Survivor Phase:
Finally the Survivor stage determines which individuals will be carried over to the next generation, we pass only the best solutions to the next generation.

## Final Loop:
All the phases run in a loop defined in the function `run_bga()`, It will run depending on the number of generations (Currently 200), while showing the best solution at each generation..

## Some Final Notes:
In the code I used different types of Selection, Crossover, Mutation and Survivor, whenever you want to test different methods, you can just uncomment one at a time the function you wish to use to compare the results and see which solution fits the best. 

I couldn't go over how some functions completely work, because it will take a lot of documentation and some of them use formulas, so I recommend you to do some research on Binary Genetic Algorithm methods in order to fully understand the code.
