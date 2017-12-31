import random
import abc
import collections
import enum


class Finder(enum.Enum):
    CONTESTANT = 0
    HOST = 1
    NONE = 2


class MontyHallBase(metaclass=abc.ABCMeta):

    def __init__(self):
        self._nr_doors = 3
        self._opened_door = -1

    @abc.abstractmethod
    def _host_open_door(self):
        pass

    def run(self, swap):
        self._init_round()
        self._choose_door()
        self._host_open_door()
        if swap:
            self._swap_door()
        return self._get_finished_status()

    def _init_round(self):
        self._door_with_car = random.randint(0, self._nr_doors - 1)

    def _swap_door(self):
        door_names = self._make_named_doors()
        self._remove_chosen_door(door_names)
        self._remove_opened_door(door_names)
        self._chosen_door = random.choice(door_names)

    def _choose_door(self):
        self._chosen_door = random.randint(0, self._nr_doors - 1)

    def _get_finished_status(self):
        if self._chosen_door == self._door_with_car:
            return Finder.CONTESTANT
        elif self._opened_door == self._door_with_car:
            return Finder.HOST
        else:
            return Finder.NONE

    def _make_named_doors(self):
        return [i for i in range(self._nr_doors)]

    def _remove_chosen_door(self, doors):
        try:
            doors.remove(self._chosen_door)
        except ValueError:
            pass

    def _remove_opened_door(self, doors):
        try:
            doors.remove(self._opened_door)
        except ValueError:
            pass

    def _remove_door_with_car(self, doors):
        try:
            doors.remove(self._door_with_car)
        except ValueError:
            pass


class MontyHallReal(MontyHallBase):

    def _host_open_door(self):
        door_names = self._make_named_doors()
        self._remove_chosen_door(door_names)
        self._remove_door_with_car(door_names)
        self._opened_door = random.choice(door_names)


class MontyHallRandomOpener(MontyHallBase):

    def _host_open_door(self):
        door_names = self._make_named_doors()
        self._remove_chosen_door(door_names)
        self._opened_door = random.choice(door_names)


MonteCarloResults = collections.namedtuple('MonteCarloResults', ['contestant', 'host', 'none'])


def monte_carlo_simulations(simulations, monty_hall_class, swap):
    monty_hall = monty_hall_class()
    contestant = host = none =0
    for i in range(simulations):
        res = monty_hall.run(swap)
        if res is Finder.CONTESTANT:
            contestant = contestant + 1
        elif res is Finder.HOST:
            host = host + 1
        else:
            none = none + 1
    return MonteCarloResults(contestant=contestant, host=host, none=none)


if __name__ == "__main__":
    number_of_simulations = 10000

    # Information added, swapping should increase winning chance
    real_swap = monte_carlo_simulations(simulations=number_of_simulations,
                                        monty_hall_class=MontyHallReal,
                                        swap=True)
    real_no_swap = monte_carlo_simulations(simulations=number_of_simulations,
                                           monty_hall_class=MontyHallReal,
                                           swap=False)

    # No information added, swapping should do noting
    random_opener_swap = monte_carlo_simulations(simulations=number_of_simulations,
                                                 monty_hall_class=MontyHallRandomOpener,
                                                 swap=True)
    random_opener_no_swap = monte_carlo_simulations(simulations=number_of_simulations,
                                                    monty_hall_class=MontyHallRandomOpener,
                                                    swap=False)

    print("Swap \n{0}\n".format(real_swap))
    print("No swap \n{0}\n".format(real_no_swap))

    print("Random opener with swap \n{0}\n".format(random_opener_swap))
    print("Random opener with no swap \n{0}\n".format(random_opener_no_swap))
