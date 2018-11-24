import numpy as np
import random as rnd
import itertools as it


def generate_list_inputs(l):
    # l is the length of the bit strings
    # returns an array with a row for each model
    indices_generator = it.chain.from_iterable(it.combinations(range(l), r) for r in range(len(range(l))+1))
    return np.array([[1 if n in indices_list else 0 for n in range(l)] for indices_list in indices_generator])


def random_quantifiers(number_agents, inputs):
    """
    returns an array, each column is a boolean vector describing which inputs are compatible with agent's quantifier
    the rows correspond to the elements of list_inputs
    """
    return np.random.randint(2, size=(inputs.shape[0], number_agents))


def create_languages_array(agents, possible_inputs, map=False):
    """
    agents as columns, inputs rows
    whether the quantifier applies or not to the input in the agent's language
    """
    languages = np.empty(shape=(possible_inputs.shape[0], len(agents)))
    if map:
        for n, agent in enumerate(agents):
            languages[:, n] = agent.map(possible_inputs).flatten()
    else:
        for n, agent in enumerate(agents):
            # assumes that agent.produce is vectorized
            languages[:, n] = agent.produce(possible_inputs).flatten()
    return languages


def generate_random_input(list_inputs):
    # note that numpy's own np.random.choice assumes 1d array
    # while rnd.random correctly picks a single row
    return rnd.choice(list_inputs)


if __name__ == "__main__":
    import population as pop
    max_model_size = 3
    agent = pop.Agent(max_model_size)
    inputs = generate_list_inputs(max_model_size)
    print(inputs)
    languages = create_languages_array([agent], inputs, map=True)
    # print(check_quantity(inputs, languages))
