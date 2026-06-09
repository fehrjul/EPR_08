
"""
ecosystem.py

contains all the klasses for the ecosystem.

- LivingBeing
- Plant + subclasses
- Animal + subclasses
- Habitat
"""

__author__ = "8766674, Fehr, 7791598, Schidlauskat"

from random import random
from random import choice




class LivingBeing:
    """
    base and parentclass for all living beings in the ecosystem.

    :param id_number: int, unique ID
    :param species: str, what species the living being has


    >>> lb = LivingBeing(1, "test")
    >>> lb.id
    1
    >>> lb.species
    'test'
    >>> lb.is_alive()
    True
    """

    def __init__(self, id_number: int, species: str):
        self.id = int(id_number)
        self.species = species

        self.age = 0
        self.energy = 0
        self.condition = "alive"
        self.dead_reason = None

    def increment_age(self):
        """
        Increments the age of the living being every round.

        :return: None

        >>> lb = LivingBeing(1, "x")
        >>> lb.increment_age()
        >>> lb.age
        1
        """
        self.age += 1

    def is_alive(self):
        """
        Checks if the living being is alive.

        :return: bool

        >>> lb = LivingBeing(1, "x")
        >>> lb.is_alive()
        True
        """
        return self.condition == "alive"

    def mark_dead(self, reason=None):
        """
        Marks the living being dead.

        :param reason: str oder None
        :return: None

        >>> lb = LivingBeing(1, "x")
        >>> lb.mark_dead("test")
        >>> lb.condition
        'dead'
        """
        self.condition = "dead"
        self.dead_reason = reason

    def act(self, habitat):
        """
        Abstract act method to be able to loop over Living beings.

        :param habitat: Habitat
        :return: None
        """
        raise NotImplementedError


class Plant(LivingBeing):
    """
    abstract parent class of Plants

    :param id_number: int
    :param species: str

    >>> p = Plant(1, "plant")
    >>> p.size
    3
    >>> p.min_size
    3
    >>> p.is_alive()
    True
    """

    def __init__(self, id_number: int, species: str):
        super().__init__(id_number, species)

        self.size = 3
        self.min_size = 3
        self.max_size = 10

    def grow(self, habitat: Habitat):
        """
        Abstract growth mehtod

        :param habitat: Habitat
        :return: None
        """
        raise NotImplementedError

    def try_reproduce(self):
        """
        checks if reproduction is possible.

        :return: bool

        >>> p = Plant(1, "plant")
        >>> p.age = 3
        >>> p.size = 4
        >>> isinstance(p.try_reproduce(), bool)
        True
        """
        if self.age > 2 and self.size >= 4:
            return random() < 0.5
        return False

    def get_eaten(self, amount: int):
        """
        Reduces the size of the plant.

        :param amount: int
        :return: int

        >>> p = Plant(1, "plant")
        >>> p.get_eaten(1)
        1
        >>> p.size
        2
        """
        eaten_amount = min(self.size, amount)
        self.size -= eaten_amount
        return eaten_amount

    def check_death(self):
        """
        Checks if the plant is dead.

        :return: None

        >>> p = Plant(1, "plant")
        >>> p.size = 2
        >>> p.check_death()
        >>> p.condition
        'dead'
        """
        if self.size < self.min_size and self.condition != "dead":
            self.mark_dead("plant_below_min_size")

    def act(self, habitat: Habitat):
        """
        lets the plannt act: grow and log the event in the habitat and also
        check for the death of the plant.

        :param habitat: Habitat
        :return: None
        """
        if not self.is_alive():
            return

        self.grow(habitat)
        habitat.log_event("plant_grow", {
            "id": self.id,
            "species": self.species,
            "size": self.size
        })

        self.check_death()


class SummerPlant(Plant):
    """
    Summerplant class with a specific grow method.

    >>> sp = SummerPlant(1, "summer_plant")
    >>> sp.size
    3
    >>> isinstance(sp, Plant)
    True
    """

    def grow(self, habitat: Habitat):
        """
        Growing is depending on the season and max_size.

        :param habitat: Habitat
        :return: None
        """
        if habitat.season == "summer":
            if habitat.has_space(2):
                self.size = min(self.size + 2, self.max_size)
        elif habitat.season in ("spring", "autumn"):
            if habitat.has_space(1):
                self.size = min(self.size + 1, self.max_size)
        elif habitat.season == "winter":
            self.size += 0


class WinterPlant(Plant):
    """
    Class for the winter plant with specific growth method.

    >>> wp = WinterPlant(1, "winter_plant")
    >>> wp.size
    3
    >>> isinstance(wp, Plant)
    True
    """

    def grow(self, habitat: Habitat):
        """
        Growing is depending on the season and max_size.

        :param habitat: Habitat
        :return: None
        """
        if habitat.season == "winter":
            if habitat.has_space(2):
                self.size = min(self.size + 2, self.max_size)
        else:
            if habitat.has_space(1):
                self.size = min(self.size + 1, self.max_size)


class PoisonPlant(Plant):
    """
    Class for poison plant with specific growth method nad on_eaten poisonous
    function.

    >>> pp = PoisonPlant(1, "poison_plant")
    >>> pp.size
    3
    >>> isinstance(pp, Plant)
    True
    """

    def grow(self, habitat: Habitat):
        """
        Steady Growth only depending on max_size.

        :param habitat: Habitat
        :return: None
        """
        if habitat.has_space(1):
            self.size = min(self.size + 1, self.max_size)

    def on_eaten(self, animal: Animal):
        """
        Poison effect for the plant if eaten.

        :param animal: Animal
        :return: bool

        >>> a = Herbivore(1, "herbivore")
        >>> pp = PoisonPlant(2, "poison_plant")
        >>> isinstance(pp.on_eaten(a), bool)
        True
        """
        if random() < 0.3:
            animal.energy -= 3
            animal.check_death()
            return True
        return False


class Animal(LivingBeing):
    """
    Abstract parent class for animals.

    :param id_number: int
    :param species: str
    :return: None

    >>> a = Animal(1, "animal")
    >>> a.energy
    5
    >>> a.size
    1
    >>> a.max_size
    3
    """

    def __init__(self, id_number: int, species: str):
        super().__init__(id_number, species)

        self.energy = 5
        self.size = 1
        self.max_size = 3

    def consume_energy(self):
        """
        Baseeneryconsumption per round.

        :return: None
        """
        self.energy -= 1

    def try_reproduce(self):
        """
        Checks if reproduce is possible.

        :return: bool
        """
        if self.age > 2 and self.energy >= 6:
            return random() < 0.5
        return False

    def handle_winter(self, habitat: Habitat):
        """
        Checking if the animal has enough energy to do winter sleep. Otherwise
        it dies.

        :param habitat: Habitat
        :return: None
        """
        if habitat.season != "winter":
            return

        if self.energy >= 3:
            self.condition = "sleeping"
        else:
            self.mark_dead("winter_starvation")

    def check_death(self):
        """
        Checks death.

        :return: None
        """
        if self.energy <= 0 and self.condition != "dead":
            self.mark_dead("no_energy_left")

    def grow(self):
        """
        Lets animal grow unless max size is reached.

        :return: None
        """
        if self.size < self.max_size:
            self.size += 1


    def eat(self, habitat: Habitat):
        """
        Abstract eating function.

        :param habitat: Habitat
        :return: None
        """
        raise NotImplementedError

    def act(self, habitat: Habitat):
        """
        Executes the acting for each round for the animal.

        :param habitat: Habitat
        :return: None
        """
        if not self.is_alive():
            return

        if habitat.has_space(1):
            self.grow()

        if self.condition == "sleeping":
            return

        self.consume_energy()
        habitat.log_event("animal_energy_cost", {
            "id": self.id,
            "energy": self.energy
        })

        if self.is_alive():
            self.eat(habitat)

        if self.is_alive():
            self.handle_winter(habitat)

        self.check_death()


class Herbivore(Animal):
    """
    Herbivore class with specific eat function.

    >>> h = Herbivore(1, "herbivore")
    >>> h.energy
    5
    >>> isinstance(h, Animal)
    True
    """

    def eat(self, habitat: Habitat):
        """
        eats plants

        :param habitat: Habitat
        :return: None
        """
        if not habitat.plants:
            habitat.log_event("herbivore_eat_fail", {
                "id": self.id,
                "reason": "no_plants"
            })
            return

        if random() >= 0.7:
            habitat.log_event("herbivore_eat_fail", {
                "id": self.id,
                "reason": "no_food_found"
            })
            return

        plant = choice(habitat.plants)
        if not plant.is_alive():
            return

        eaten = plant.get_eaten(1)
        plant.check_death()

        self.energy += 2

        habitat.log_event("plant_eaten", {
            "plant_id": plant.id,
            "by": self.id,
            "amount": eaten
        })


class Carnivore(Animal):
    """
    Carnivore class with specific eat function.

    >>> c = Carnivore(1, "carnivore")
    >>> c.energy
    5
    >>> isinstance(c, Animal)
    True
    """

    def eat(self, habitat: Habitat):
        """
        Jagt andere Tiere.

        :param habitat: Habitat
        :return: None
        """
        prey_candidates = [animal for animal in habitat.animals if
                           animal.is_alive() and animal.id != self.id and
                           animal.species in (
                               "herbivore", "omnivore")]

        if not prey_candidates:
            habitat.log_event("carnivore_hunt_fail", {
                "id": self.id,
                "reason": "no_prey"
            })
            return

        if habitat.season == "autumn":
            success_chance = 0.3
        else:
            success_chance = 0.6

        if random() >= success_chance:
            habitat.log_event("carnivore_hunt_fail", {
                "id": self.id,
                "reason": "hunt_failed"
            })
            return

        prey = choice(prey_candidates)
        prey.mark_dead("eaten_by_carnivore")

        self.energy += 3

        habitat.log_event("animal_eaten", {
            "predator_id": self.id,
            "prey_id": prey.id,
            "prey_species": prey.species
        })


class Omnivore(Animal):
    """
    Omnivore class with specific eat function.

    >>> o = Omnivore(1, "omnivore")
    >>> o.energy
    5
    >>> isinstance(o, Animal)
    True
    """

    def eat(self, habitat: Habitat):
        """
        Frisst Pflanzen oder Tiere.

        :param habitat: Habitat
        :return: None
        """
        plant_options = [plant for plant in habitat.plants if plant.is_alive()]
        animal_options = [animal for animal in habitat.animals if
                          animal.is_alive() and animal.id != self.id]
        food_options = plant_options + animal_options

        if random() >= 0.6:
            habitat.log_event("omnivore_eating_fail", {
                "id": self.id,
                "reason": "no_food_found"
            })
            return

        if not food_options:
            habitat.log_event("omnivore_eating_fail", {
                "id": self.id,
                "reason": "no_food"
            })
            return

        food = choice(food_options)

        if isinstance(food, Plant):
            if isinstance(food, PoisonPlant):
                poisonous = food.on_eaten(self)
                habitat.log_event("poison_plant_eaten", {
                    "plant_id": food.id,
                    "by": self.id,
                    "poisonous": poisonous
                })
                if poisonous:
                    return

            eaten = food.get_eaten(1)
            food.check_death()
            self.energy += 2

            habitat.log_event("plant_eaten", {
                "plant_id": food.id,
                "by": self.id,
                "amount": eaten
            })
            return

        food.mark_dead("eaten_by_omnivore")
        self.energy += 3

        habitat.log_event("animal_eaten", {
            "predator_id": self.id,
            "prey_id": food.id,
            "prey_species": food.species
        })


class Habitat:
    """
    Central Habitat class with all the functions for the habitat logic.

    :param space: int

    >>> h = Habitat(10)
    >>> h.season
    'spring'
    >>> h.new_id()
    1
    >>> h.new_id()
    2
    """

    seasons = {
        "spring": "summer",
        "summer": "autumn",
        "autumn": "winter",
        "winter": "spring"
    }

    def __init__(self, space: int):
        self.space = int(space)
        self.season = "spring"

        self.plants = []
        self.animals = []

        self.next_id = 1
        self.event_log = []

    def new_id(self):
        """
        Gives new ID

        :return: int
        """
        current_id = self.next_id
        self.next_id += 1
        return current_id

    def log_event(self, event_type: str, information: dict):
        """
        Logs an Event

        :param event_type: str
        :param information: dict
        :return: None
        """
        self.event_log.append({
            "type": event_type,
            "information": information
        })

    def clear_events(self):
        """
        Deletes Event Logs

        :return: None
        """
        self.event_log = []

    def add_plant(self, plant: Plant):
        """
        Adds plant to habitat.plants

        :param plant: Plant
        :return: None
        """
        self.plants.append(plant)

    def add_animal(self, animal: Animal):
        """
        Adds animal to habitat.animals

        :param animal: Animal
        :return: None
        """
        self.animals.append(animal)

    def change_season(self):
        """
        Changes season

        :param: None
        :return: None
        """
        self.season = self.seasons[self.season]
        self.log_event("season_change", {"season": self.season})

    def has_space(self, required_space: int) -> bool:
        """
        Checks available space

        :param required_space: int oder float
        :return: bool
        """
        used_space = 0
        for plant in self.plants:
            used_space += plant.size
        return used_space + required_space <= self.space

    def cleanup(self):
        """
        Removes dead entities.

        :param: None
        :return: None
        """
        alive_plants = []
        for plant in self.plants:
            if plant.condition == "dead":
                self.log_event("remove_plant", {
                    "id": plant.id,
                    "reason": plant.dead_reason
                })
            else:
                alive_plants.append(plant)
        self.plants = alive_plants

        alive_animals = []
        for animal in self.animals:
            if animal.condition == "dead":
                self.log_event("remove_animal", {
                    "id": animal.id,
                    "reason": animal.dead_reason
                })
            else:
                alive_animals.append(animal)
        self.animals = alive_animals



# python -m doctest -v ecosystem.py
# python -m doctest -v round.py
# python -m doctest -v main.py
