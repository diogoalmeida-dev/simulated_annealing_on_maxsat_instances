import numpy as np

from src.utils import evaluate_energy

def simulated_annealing(clauses, num_clauses, num_vars, iterations, init_temperature, bits_to_perturbate, alfa):
    temperature = init_temperature
    state = np.random.randint(0,2, size=num_vars) ## 1st random state

    best_energy = evaluate_energy(clauses, state)
    best_state = state.copy()
    energy = best_energy

    for iteration in range(iterations):
        new_state = perturbate(state, bits_to_perturbate) ## perturbar solução atual
        new_energy = evaluate_energy(clauses, new_state)

        if new_energy < energy:
            energy = new_energy
            state = new_state
            if new_energy < best_energy:
                best_energy = new_energy
                best_state = new_state
        else:
            if should_accept_move(energy, new_energy, temperature):
                energy = new_energy
                state = new_state
                continue

        if best_energy == 0:
            print("global optimum found")
            return energy, state

        temperature = lower_temperature(temperature, alfa)

    print("maximum iterations reached")
    return best_energy, best_state

def perturbate(state, bits_to_perturbate):
    new_state = state.copy()

    for _ in range(bits_to_perturbate):  ## make perturbation
        index_to_perturbate = np.random.randint(0, len(state))  ## index of the bit that will be flipped
        new_state[index_to_perturbate] = (state[index_to_perturbate] + 1) % 2  ## flip the bit from 0->1 and 1->0
    return new_state

def should_accept_move(energy, new_energy, temperature):
    probability = np.exp(-(new_energy - energy) / temperature)
    return probability > np.random.random()

def lower_temperature(temperature, alfa):
    if temperature > 10E-3: ## if temp > 0.0001, lower it
        temperature  *= alfa
    return temperature