import os
import random

import numpy as np
import pandas as pd
from src import utils

from simulated_annealing import simulated_annealing

CNF_FILES = {
    "1": "../cnf_files/uf20-01.cnf",
    "2": "../cnf_files/uf100-01.cnf",
    "3": "../cnf_files/uf250-01.cnf",
}

INDEPENDENT_RUNS = 30                 ## number of independent runs
RESULTS_FILE = "../results/sa_results.xlsx"

## Simulated Annealing Parameters (adjust as you wish)
MAX_EVALUATIONS = 1_000_000  ## maximum amount of times evaluate_energy will be called
MIN_TEMPERATURE = 10E-7      ## how low can the temperature go after being cooled
MAX_TEMPERATURE = 1.0        ## the starting temperature
ALFA = 0.9999930923          ## cooling to achieve max of 1 million evaluations
BITS_TO_PERTURBATE = 1       ## number of bits to flip
ENERGY_THRESHOLD = 0         ## lowest possible amount of energy (clauses unsatisfied)

def main():
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)

    results = []

    for instance_id, cnf_path in CNF_FILES.items():
        print(f"\nLoaded {cnf_path}")
        clauses, num_clauses, num_vars = utils.read_cnf(cnf_path)
        num_clauses = len(clauses)

        for run in range(INDEPENDENT_RUNS):
            seed = run  # seeds 0..29
            random.seed(seed)
            np.random.seed(seed)

            print(f"File {instance_id}, run {run}, seed {seed}")

            best_energy, best_state = simulated_annealing(
                clauses=clauses,
                num_vars=num_vars,
                max_evaluations=MAX_EVALUATIONS,
                min_temperature=MIN_TEMPERATURE,
                max_temperature=MAX_TEMPERATURE,
                alfa=ALFA,
                bits_to_perturbate=BITS_TO_PERTURBATE,
                energy_threshold=ENERGY_THRESHOLD,
            )

            # energy = number of clauses not satisfied
            best_fitness = num_clauses - best_energy  # number of clauses satisfied

            results.append(
                {
                    "instance_id": instance_id,
                    "cnf_file": cnf_path,
                    "run": run,
                    "seed": seed,
                    "num_vars": num_vars,
                    "num_clauses": num_clauses,
                    "best_energy_unsatisfied": best_energy,
                    "best_fitness_satisfied": best_fitness,
                }
            )

    df = pd.DataFrame(results)
    df.to_excel(RESULTS_FILE, index=False)
    print(f"\nSaved results to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
