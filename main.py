"""
main.py

Main user interface for the ecosystem simulation.

includes ask_number, setup_simulation and main function.

"""

__author__ = "8766674, Fehr, 7791598, Schidlauskat"

from ecosystem import (
    Habitat,
    SummerPlant,
    WinterPlant,
    PoisonPlant,
    Herbivore,
    Carnivore,
    Omnivore
)

from round import run_simulation


def ask_number(text: str) -> int:
    """
    Ask the user for a non-negative integer.

    Repeats until a valid input is given.

    :param text: str, question shown to the user
    :return: int, non-negative integer

    >>> isinstance(ask_number, object)
    True
    """
    while True:
        try:
            value: int = int(input(text))
            if value >= 0:
                return value
            print("Please enter a number greater than or equal to 0.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def setup_simulation() -> tuple[Habitat, int]:
    """
    Create the habitat and initial population based on user input.

    This function handles only the setup, not the simulation itself.

    :return: tuple (Habitat, int) where int is the number of rounds

    >>> isinstance(setup_simulation, object)
    True
    """
    print("\nWelcome to the ecosystem simulation.")
    print("You will now define the initial state of the ecosystem.\n")

    space: int = ask_number("How large should the habitat be (available space)? ")
    rounds: int = ask_number("How many rounds should be simulated? ")

    habitat: Habitat = Habitat(space)

    # Plants
    print("\n--- Plants ---")
    summer_plants: int = ask_number("Number of summer plants: ")
    winter_plants: int = ask_number("Number of winter plants: ")
    poison_plants: int = ask_number("Number of poison plants: ")

    for _ in range(summer_plants):
        habitat.add_plant(SummerPlant(habitat.new_id(), "summer_plant"))

    for _ in range(winter_plants):
        habitat.add_plant(WinterPlant(habitat.new_id(), "winter_plant"))

    for _ in range(poison_plants):
        habitat.add_plant(PoisonPlant(habitat.new_id(), "poison_plant"))

    # Animals
    print("\n--- Animals ---")
    herbivores: int = ask_number("Number of herbivores: ")
    carnivores: int = ask_number("Number of carnivores: ")
    omnivores: int = ask_number("Number of omnivores: ")

    for _ in range(herbivores):
        habitat.add_animal(Herbivore(habitat.new_id(), "herbivore"))

    for _ in range(carnivores):
        habitat.add_animal(Carnivore(habitat.new_id(), "carnivore"))

    for _ in range(omnivores):
        habitat.add_animal(Omnivore(habitat.new_id(), "omnivore"))

    print("\nInitial setup completed.")
    print(f"Plants: {len(habitat.plants)} | Animals: {len(habitat.animals)}")
    print("Starting simulation...\n")

    return habitat, rounds


def main() -> None:
    """
    Main function of the program.

    Handles setup and starts the simulation.

    :return: None

    >>> main.__name__
    'main'
    """
    habitat, rounds = setup_simulation()

    # Simulation logic
    run_simulation(habitat, rounds)

    print("\nSimulation finished.")
    print("Final state:")
    print(f"Plants remaining: {len(habitat.plants)}")
    print(f"Animals remaining: {len(habitat.animals)}")


if __name__ == "__main__":
    main()
