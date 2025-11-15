from src import utils
from simulated_annealing import *

CNF_FILES = {
    "1": "../cnf_files/uf20-01.cnf",
    "2": "../cnf_files/uf100-01.cnf",
    "3": "../cnf_files/uf250-01.cnf"
}

iterations = 100000

## for SA
init_temperature = 1
bits_to_perturbate = 1

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
        energy, state = simulated_annealing(clauses, num_clauses, num_vars, iterations, init_temperature, bits_to_perturbate, 0.99)
        print(f"\nEnergy: {energy}")

if __name__ == "__main__":
    main()
