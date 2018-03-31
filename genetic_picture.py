from PIL import Image
import random

# Jonah Rubin
# Genetic Image Evolver


POP_SIZE = 100
GENERATIONS = 200000000
MUTATION_RATE = .00025

def main():
    #name = input("Select the picture file ")
    name = "tree_lake.jpg"
    target = open_image(name)
    population = populate(target)

    fitter_pop, fitness_list = get_fitter_pop(population, target)
    print(min(fitness_list))
    for i in range(GENERATIONS):
        fitter_pop, fitness_list = get_fitter_pop(fitter_pop, target)
        minFit = fitness_list.index(min(fitness_list))
        print(fitness_list[minFit])

        if i % 100 == 0:
            fitter_pop[minFit].save(str(min(fitness_list)) + ".jpg", "JPEG")
            #fitter_pop[minFit].show()

# Open given file
#
# @param name the name of the image file
# @return target the image file that will be the target
def open_image(name):
    target = Image.open(name)
    #target.show()
    #target_pix_values = list(target.getdata())
    #print(target_pix_values)
    return target

# Fills the first list random elements
#
# @param target the target image
# @return population the populated list
def populate(target):
    population = []
    for i in range(POP_SIZE):
        individual = create_copy(target.size)
        population.append(individual)
    return(population)

# Creates random copies for the initial population
#
# @param size the size of the target element
# @return copy a random copy of the target size
def create_copy(size):
    copy = Image.new("RGB", size, color=0)
    copy_pix = copy.load()

    for row in range(size[0]):
        for column in range(size[1]):
            copy_pix[row, column] = (random.randrange(256), random.randrange(256), random.randrange(256))

    return(copy)

# Creates a new list of elements with better fitness scores
#
# @param population the initial list
# @param target the target image
# @return fitter_pop the list of fitter images
# @return fitness_list a parallel list of each image's fitness
def get_fitter_pop(population, target):
    count = 0
    fitness_list = []
    fitter_pop = []

    for individual in population:
        fitness = get_fitness(individual, target)
        fitness_list.append(fitness)

    max_fitness = max(fitness_list)
    min_fitness = min(fitness_list)

    while(len(fitter_pop) <= POP_SIZE):
        father = accept_reject(max_fitness, min_fitness, population, fitness_list)
        mother = accept_reject(max_fitness, min_fitness, population, fitness_list)
        child = pair(father, mother, target)
        fitter_pop.append(child)

    print(fitness_list)

    return(fitter_pop, fitness_list)

# Combine mother and father 'DNA' to create a child element
#
# @param father the chosen father element
# @param mother the chosen mother element
# @param target the target image
# @return child the spliced mother/ father
def pair(father, mother, target):

    child = Image.new("RGB", target.size)
    child_dna = []

    father_dna = tuple(father.getdata())
    mother_dna = tuple(mother.getdata())

    split = int(len(father_dna)/2)
    for i in range(split):
        child_dna.append(father_dna[i])
    for i in range(split, len(father_dna)):
        child_dna.append(mother_dna[i])

    child_dna = mutate(child_dna)

    child.putdata(child_dna)
    return (child)

# Randomly modify the element to avoid stagnation
#
# @param dna the information stored in the child element
# @return dna the modified information
def mutate(dna):
    size = len(dna)

    for i in range(int(MUTATION_RATE * size)):
        randomInd = random.randrange(size)
        randomTup = random.randrange(2)
        randomPix = random.randrange(256)

        dna[randomInd] = list(dna[randomInd])
        dna[randomInd][randomTup] = randomPix
        dna[randomInd] = tuple(dna[randomInd])

    return(dna)

# Use rejection sampling to pick elements 'randomly' in porportion to their fitness scores
#
# @param max the max of the fitness lest
# @param min the min of the fitness list
# @param pop the population list
# @param fitnesses the parallel fitness list
# @return pop[n] the selected element
def accept_reject(max, min, pop, fitnesses):
    while True:
        randNum = random.randrange(min, max + 1)
        randIndex = random.randrange(len(fitnesses))
        if fitnesses[randIndex] <= randNum:
            return pop[randIndex]

# Compare the copy to the target and assess its fitness
#
# @param copy the attempted recreation
# @param target the goal
# @return fitness the fitness score
def get_fitness(copy, target):
    target_pix = target.load()
    copy_pix = copy.load()
    fitness = 0
    for length in range(target.size[0]):
        for height in range(target.size[1]):
            target_tuple = target_pix[length, height]
            copy_tuple = copy_pix[length, height]

            delta_r = abs(target_tuple[0] - copy_tuple[0])
            delta_g = abs(target_tuple[1] - copy_tuple[1])
            delta_b = abs(target_tuple[2] - copy_tuple[2])

            pixel_fitness = delta_r ** 2 + delta_g ** 2 + delta_b ** 2
            fitness += pixel_fitness

    return(fitness)


main()
