import numpy as np

from src.utils import evaluate_energy

def simulated_annealing(clauses, num_vars, max_evaluations, min_temperature, max_temperature, alfa, bits_to_perturbate, energy_threshold):
    """
    :param clauses: Clauses are variations of the variables {x1, x2, ..., xn} with "and" and "or" operators.
    (Array of clauses, clauses[0] = (8 -12 19) -> x8 ^x12 x19)
    :param num_vars: Number of variables in clauses across all instance (int value)
    :param max_evaluations: Max objective function evaluations (evaluate_energy) (int value)
    :param min_temperature: Minimum temperature threshold (int value)
    :param max_temperature: The starting temperature (+ temperature + exploring) (int value)
    :param alfa: Temperature coefficient (float value)
    :param bits_to_perturbate: the number of bits to perturb (int value)
    :param energy_threshold: Energy threshold, 0 being a global optima (int value)
    :return: Returns the best energy value found (int value), 0 being a global optima
     and the state in which the energy was found (array of 0's and 1's corresponding variable values)
    """
    temperature = max_temperature ## set the initial temperature as given in params
    state = np.random.randint(0,2, size=num_vars) ## initialise first random state

    energy = evaluate_energy(clauses, state) ## discover the initial state energy
    best_energy = energy                     ## update best state values
    best_state = state.copy()

    evaluations = 1 ## objective function evaluations (evaluate_energy)

    while (evaluations < max_evaluations    ## while we don't reach max evaluations
        and best_energy > energy_threshold  ## or find the global optima
        and temperature > min_temperature): ## or temperature is too low, do:

        new_state = perturbate(state, bits_to_perturbate) ## perturbate current state
        new_energy = evaluate_energy(clauses, new_state)

        if new_energy < energy: ## if the new state's energy is lower (better) than current, instantly swap them.
            energy = new_energy
            state = new_state
        else:                   ## if new state energy is worse than current:
            if should_accept_move(energy, new_energy, temperature): ## calculate the probability of accepting them and find out
                energy = new_energy                                 ## if we should accept it based on random probabilities
                state = new_state

        if new_energy < best_energy:    ## update global best
            best_energy = new_energy
            best_state = new_state.copy()

        temperature *= alfa ## lower temperature multiplying it by alfa value and increment evaluations
        evaluations += 1

    return best_energy, best_state

def perturbate(state, bits_to_perturbate):
    """
    Flips n bits of the given state, n = bits_to_perturbate

    :param state: current state to perturbate (array of bits)
    :param bits_to_perturbate: the number of bits to perturb (int value)
    :return: returns the state with the random perturbated bits
    """
    new_state = state.copy()

    for _ in range(bits_to_perturbate):  ## make perturbation
        index_to_perturbate = np.random.randint(0, len(state))  ## index of the bit that will be flipped
        new_state[index_to_perturbate] = (new_state[index_to_perturbate] + 1) % 2  ## flip the bit from 0->1 and 1->0
    return new_state

def should_accept_move(energy, new_energy, temperature):
    """
    This function determines if the energy is accepted or not.

    probability (P) = exp(-(ΔE)/T)

    ΔE = new_energy - energy. How bad the new solution is correlates directly with how big ΔE is.
    Temperature controls how forgiving we are to bad states, when T is high (on the first few evals), the algorithm will often take worse states
    this avoids local optima and allows the algorithm to roam the search space.

    This is the Boltzmann factor, we use it to determine how many times we will go "uphill" (new state with bigger energy)
    to escape local optima, without this step this would simply be greedy hillclimbing (if better accept, if worse reject).


    After finding out the probability of accepting this worse state, we generate a random value, if the probability is bigger than
    the random value, we accept the worse state.
    np.random.random() -> random float value between 0 and 1

    :param energy: current state energy
    :param new_energy: new state energy
    :param temperature: current temperature
    :return: true if we should accept move, false otherwise
    """
    probability = np.exp(-(new_energy - energy) / temperature)
    return probability > np.random.random()