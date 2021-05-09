import random
from time import time

__author__ = 'Atra'
# Assume no infidelity?
# in other words, once a mother and a father have mated, they are "bound" and can no longer have any other children
# except for with each other

# number of children per couple random between 1-4
NUM_GENERATIONS = 25
YEARS_PER_GENERATION = 20

INITIAL_ANCESTORS = 100000
MAX_AGE = 4  # generations
MAX_BREEDING_AGE = MAX_AGE - 1
MAX_TOTAL_CHILDREN = 5
MIN_CHILDREN_PER_BREED = 0
MAX_CHILDREN_PER_BREED = 2
MARRIAGE_ATTEMPTS_PER_GENERATION = 1


class Person(object):
    age = 0  # generations
    spouse = None
    mother = None
    father = None

    def __init__(self, mother, father, generation):
        self.mother = mother
        self.father = father
        self.generation = generation
        if mother is None and father is None:
            # ancestor
            self.age = random.randint(1, MAX_AGE)

    @property
    def alive(self):
        return self.age <= MAX_AGE


class Couple(object):
    def __init__(self, wife, husband):
        self.wife = wife
        self.husband = husband
        self.children = 0

    def procreate(self):
        """
        :rtype: set
        """
        if self.children >= MAX_TOTAL_CHILDREN:
            return
        if self.wife.age > MAX_BREEDING_AGE:
            return
        num_new_children = random.randint(MIN_CHILDREN_PER_BREED, MAX_CHILDREN_PER_BREED)
        self.children += num_new_children
        return {Person(mother=self.wife, father=self.husband, generation=CURRENT_GENERATION) for _ in range(num_new_children)}


population = set()
ancestors = {Person(mother=None, father=None, generation=0) for i in range(INITIAL_ANCESTORS)}
population.update(ancestors)


married = dict()
singles = set()
singles.update(population)  # everyone is single to begin with

def _find_spouse(person, list_population):
    # list_population = list(population)
    for i in range(MARRIAGE_ATTEMPTS_PER_GENERATION):
        potential_spouse = random.choice(list_population)
        if (potential_spouse is not person) and (potential_spouse.spouse is None):
            break
    else:
        potential_spouse = None

    return potential_spouse


def _remove_dead_people(_the_population):
    dead_humans = set()
    for person in _the_population:
        if not person.alive:
            dead_humans.add(person)
            if person.spouse and person.spouse.alive:  # (if the spouse is dead, the marriage is already deleted)
                del married[person]
                del married[person.spouse]

    _the_population.difference_update(dead_humans)

CURRENT_GENERATION = 0


def next_generation(population):

    new_humans = set()

    recently_married = set()
    list_singles = list(singles)
    for person in singles:
        if person in recently_married:  # O(1)
            continue
        other_person = _find_spouse(person, list_singles)
        if not other_person:
            continue

        newly_wed = Couple(person, other_person)
        person.spouse = other_person
        other_person.spouse = person

        married[person] = newly_wed
        married[other_person] = newly_wed
        recently_married.add(person)
        recently_married.add(other_person)

    singles.difference_update(recently_married)

    for couple in set(married.values()):  # remove duplicates
        kids = couple.procreate()
        if kids:
            new_humans.update(kids)

    population.update(new_humans)
    singles.update(new_humans)

    for person in population:
        person.age += 1
    _remove_dead_people(population)
    singles.intersection_update(population)

def simulate():
    print("Starting. Initial population size: {}".format(len(population)))
    global CURRENT_GENERATION
    for i in range(NUM_GENERATIONS):
        CURRENT_GENERATION = i
        next_generation(population)
        print("Population size, generation {}: {}".format(i+1, len(population)))


def draw_tree():
    pass
    # import tinytree
    # t = tinytree.Tree()
    # t.
    # t.addChild()


def get_all_children(root_node):
    if root_node is None:
        return []
    all_children = get_all_children(root_node.father) + get_all_children(root_node.mother)
    all_children.append(root_node)
    return all_children


if __name__ == '__main__':
    # import cProfile
    # cProfile.run('simulate()')
    t1 = time()
    simulate()
    print("Simulation took {} s.".format(time() - t1))
    latest_generation = {person for person in population if person.generation == CURRENT_GENERATION}
    thesample = random.sample(latest_generation, 2)
    A = thesample[0]
    B = thesample[1]
    all_A_children = get_all_children(A)
    set_A = set(all_A_children)
    print("All A ancestors: {}, after removing duplicates: {}".format(len(all_A_children), len(set_A)))
    all_B_children = get_all_children(B)
    set_B = set(all_B_children)
    print("All B ancestors: {}, after removing duplicates: {}".format(len(all_B_children), len(set_B)))

    common_ancestors = set_A.intersection(set_B)
    print("Number of common ancestors to A and B: {}".format(len(common_ancestors)))
    generations = set()
    for person in common_ancestors:
        generations.add(person.generation)
    print("Generations of common ancestors: {}".format(generations))
