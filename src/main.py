from src import utils
from simulated_annealing import *

CNF_FILES = {
    "1": "../cnf_files/uf20-01.cnf",
    "2": "../cnf_files/uf100-01.cnf",
    "3": "../cnf_files/uf250-01.cnf"
}

## Parameters for simulated annealing
max_evaluations = 1000
min_T = 10E-04
max_T = 1
alfa = 0.995
bits_to_perturbate = 1
energy_threshold = 0

def main():
    print("Select CNF file:")
    print("1 - uf20-01.cnf")
    print("2 - uf100-01.cnf")
    print("3 - uf250-01.cnf")
    cnf_choice = input("Enter choice (1-3): ").strip()

    if cnf_choice not in CNF_FILES:
        print("Invalid CNF file choice.")
        return

    cnf_path = CNF_FILES[cnf_choice]
    clauses, num_clauses, num_vars = utils.read_cnf(cnf_path)
    print(f"\nLoaded: {cnf_path} — vars={num_vars}, clauses={num_clauses}")

    print("\nSelect algorithm:")
    print("1 - SA")
    x = int(input("Enter choice: (1): "))
    if x == 1:
        energy, state = simulated_annealing(clauses, num_vars, max_evaluations, min_T, max_T, alfa, bits_to_perturbate, energy_threshold )
        print(f"\nEnergy: {energy}")

if __name__ == "__main__":
    main()