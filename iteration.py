import argparse
import utilities as util
import population as pop
import numpy as np


def iterate(n_generations, n_agents, bottleneck, length_models,
            save_path=False, num_trial=None, num_epochs=1):
    # generate all the binary strings of the given length
    # possible_models is a 2d array, where each row is a model
    possible_models = util.generate_list_models(length_models)
    # create first generation
    parent_generation = pop.Population(n_agents, length_models)
    # data is a 3-d numpy array with shape (# gen, # possible models, # agents)
    data = np.empty(shape=(n_generations+1, len(possible_models), n_agents))

    for n in range(n_generations):
        # the new generation is created
        child_generation = pop.Population(n_agents, length_models)
        # the new generation learns from the old one
        child_generation.learn_from_population(parent_generation,
                                               bottleneck,
                                               num_epochs)
        # stores some data to be analyzed later!
        data[n] = util.create_languages_array(parent_generation.agents, possible_models)
        # the new generation becomes the old generation, ready to train the next generation
        parent_generation = child_generation
        print("Done generation {} out of {} \n\n".format(n, n_generations))

    # stores the data from the last trained generation
    data[n_generations] = util.create_languages_array(parent_generation.agents, possible_models)
    if save_path:
        np.save(model_values.save_path, data)

    return data


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # parser.add_argument("--", type=, default=)
    parser.add_argument("--num_trial", type=int, default=0)
    parser.add_argument("--bottleneck", type=int, default=10)
    parser.add_argument("--save_path", type=str, default="")
    parser.add_argument("--n_generations", type=int, default=100)
    parser.add_argument("--n_agents", type=int, default=1)
    parser.add_argument("--length_models", type=int, default=3)
    parser.add_argument("--num_epochs", type=int, default=3)

    model_values = parser.parse_args()
    model_values.save_path += "+".join("{}-{}".format(key, value)
                                       for key, value in sorted(vars(model_values).items())
                                       if key != "save_path")

    iterate(**vars(model_values))
