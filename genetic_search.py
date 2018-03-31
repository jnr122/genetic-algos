import random
import math
import sys
import time

# Jonah Rubin
# A genetic word search

AB = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz, "

TARGET = input("Enter a word/ phrase: ") #"test"
POP_SIZE = 200
MUTATION_RATE = 1
GENERATIONS = 100000
FITNESS_POW = 2

count = 0
start = time.time()


def main():
    global count


    mutation_level = math.ceil((MUTATION_RATE / 100 * len(TARGET)))
    string_size = len(TARGET)

    population_list = populate(string_size)

    fitter_population = get_fitter_pop(population_list)

    for i in range(GENERATIONS):
        mutated_population = mutate(fitter_population, mutation_level)
        fitter_population = get_fitter_pop(mutated_population)
        count += 1
        if i % 100 == 0:
            print(fitter_population[0])
    print(fitter_population)

# Creates a list of strings of the target's length
#
# @param population_count the number of strings to add
# @param string_size the size of the target string
# @return population the newly populated list
def populate(string_size):
    pop_list = []
    for i in range (POP_SIZE):
        pop_list.append(rand_string(string_size))

    return pop_list

# Generates a random string for the first population
#
# @param size the length of the string to create
# @return element the new string
def rand_string(size):
    element = ""
    for i in range(size):
        element += AB[random.randrange(len(AB))]

    return element

# Populate with spliced strings
#
# @param pop list the list manipulate
# @return fittest_list the best combinations of elemnts
def get_fitter_pop(pop_list):
    fitter_list = []
    fittest_list = []
    for i in pop_list:
        fitness = get_fitness(i)
        for j in range(fitness):
            fitter_list.append(i)

    if len(fitter_list) == 0:
        sys.exit("No matches, try random repopulation")
    for i in range(POP_SIZE):
        father = fitter_list[random.randrange(len(fitter_list))]
        mother = fitter_list[random.randrange(len(fitter_list))]

        #child = splice(father, mother)
        child = reproduce(father, mother)

        fittest_list.append(child)

    return fittest_list

# Check the accuracy of a string
#
# @param element the string
# @return fitness the accuracy of the string (squared)
def get_fitness(element):
    if element == TARGET:
        correct(element)
    match = 0
    for i in range(len(TARGET)):
        if element[i] == TARGET[i]:
            match += 1
    fitness = int((match / len(TARGET) * 100) / 4)
    return fitness ** FITNESS_POW


# Combine by cutting together the first half of the father and second half of the mother
#
# @param father the first element to combine
# @param mother the second element to combine
# @return child a combination of both
def splice(father, mother):
    child = ""
    for i in range(len(TARGET)):
        if i % 2 == 0:
            child += father[i]
        else:
            child += mother[i]
    return child

# Combine by cutting together a random portion of the father and filling it in with
# the second portion of the mother
#
# @param father the first element to combine
# @param mother the second element to combine
# @return child a combination of both
def reproduce(father, mother):
    split_at = random.randrange(len(TARGET))
    #length = int(len(TARGET)/2)
    child = father[:split_at] + mother[split_at:]
    return child

# Modify a string manually to avoid stagnation
#
# @param population the list of elements
# @param mutation_level the rate at which to modify
# @return mutated_population a now modified set of elements
def mutate(population, mutation_level):
    mutated_population = []
    for i in population:
        list = toList(i)
        for j in range(mutation_level):
            list[random.randrange(len(list))] = AB[random.randrange(len(AB))]
        string = toString(list)
        mutated_population.append(string)
    return (mutated_population)

# Convert to list so operations can be performed in place
#
# @param string the element to be converted
# @return list the new list
def toList(string):
    list = []
    for i in range(len(string)):
        list.append(string[i])
    return (list)

# Convert back to string
#
# @param list the list
# @return string the modified string
def toString(list):
    string = ""
    for i in list:
        string += i
    return (string)

# Calculate theoretical time of random guesses
#
# @return calculation
def random_time():
    start_rand = time.time()
    rand = rand_string(len(TARGET))
    end_rand = time.time()
    return end_rand - start_rand


# Display data to user
#
# @param target_match the correct answer
def correct(target_match):
    global count
    end = time.time()
    count += POP_SIZE
    genetic_time =  end - start
    random_count = int((len(AB) ** len(TARGET)))

    random_seconds = random_time() * random_count


    minutes, random_seconds = divmod(random_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    years = (int(weeks/52))

    # print("days", days)
    # print("hours", hours)
    # print("weeks", weeks)
    # print("minutes", minutes)


    print()
    print("Target: " + TARGET)
    print("Final attempt: " + target_match)
    print()
    print("         Genetic Algorithm       |  Random Generation")
    print("         ----------------------------------------------" )
    print("Tries:   ", str(count).ljust(25), random_count)


    if years > 0:
        print("Time:    ", format(genetic_time, '.5f'), "seconds".ljust(17), years, "years")
    elif weeks > 0:
        print("Time:    ", format(genetic_time, '.5f'), "seconds".ljust(17), weeks, "weeks")
    elif days > 0:
        print("Time:    ", format(genetic_time, '.5f'), "seconds".ljust(17), days, "days")
    elif hours > 0:
        print("Time:    ", format(genetic_time, '.5f'), "seconds".ljust(17), hours, "hours")
    elif minutes > 0:
        print("Time:    ", format(genetic_time, '.5f'), "seconds".ljust(17), minutes, "minutes")
    else:
        print("Time:    ", format(genetic_time, '.5f'), "seconds".ljust(17), random_seconds, "seconds")

    sys.exit()

main()