from enum import Enum, auto
import pandas as pd
from random import randint
from copy import deepcopy


class Thing(Enum):
    FARMER = auto()
    GOOSE = auto()
    GRAIN = auto()
    FOX = auto()


class Direction(Enum):
    LEFT2RIGHT = 0
    RIGHT2LEFT = 1


class State:
    def __init__(self, side0=None, side1=None, prv=None):
        if side1 is None:
            side1 = []
        if side0 is None:
            side0 = [Thing.FARMER, Thing.GOOSE, Thing.GRAIN, Thing.FOX]
        self.side0 = side0
        self.side1 = side1
        self.prv = prv

    def is_valid(self):
        if Thing.FOX in self.side0 and Thing.GOOSE in self.side0 and Thing.FARMER not in self.side0:
            return False
        if Thing.FOX in self.side1 and Thing.GOOSE in self.side1 and Thing.FARMER not in self.side1:
            return False
        if Thing.GOOSE in self.side0 and Thing.GRAIN in self.side0 and Thing.FARMER not in self.side0:
            return False
        if Thing.GOOSE in self.side1 and Thing.GRAIN in self.side1 and Thing.FARMER not in self.side1:
            return False
        return True

    def __repr__(self):
        return pd.DataFrame(data=[[item.name for item in self.side0],
                                  [item.name for item in self.side1]],
                            index=["left", "right"]).to_string(header=False)

    def is_solved(self):
        if len(self.side0) == 0:
            return True
        return False

    def get_side(self, index):
        if index == 0:
            return self.side0
        else:
            return self.side1

    def find_farmer(self):
        if Thing.FARMER in self.side0:
            return 0
        else:
            return 1


def use_boat(_state, direction, thing):
    if direction == Direction.RIGHT2LEFT:
        _state.side1.remove(Thing.FARMER)
        _state.side1.remove(thing)
        _state.side0.append(Thing.FARMER)
        _state.side0.append(thing)
    elif direction == Direction.LEFT2RIGHT:
        _state.side0.remove(Thing.FARMER)
        _state.side0.remove(thing)
        _state.side1.append(Thing.FARMER)
        _state.side1.append(thing)


def move_farmer(_state):
    if Thing.FARMER in _state.side0:
        _state.side0.remove(Thing.FARMER)
        _state.side1.append(Thing.FARMER)
    else:
        _state.side1.remove(Thing.FARMER)
        _state.side0.append(Thing.FARMER)


def get_thing(_state, _location):
    return _state.get_side(_location)[randint(0, len(_state.get_side(_location)) - 1)]


def solve(_state, even=True):
    if _state.is_solved():
        return _state
    else:
        temp = deepcopy(_state)
        temp.prv = _state
        f_location = temp.find_farmer()
        if f_location == 0:
            direction = Direction.LEFT2RIGHT
        else:
            direction = Direction.RIGHT2LEFT
        if not even:
            temp_state = deepcopy(temp)
            move_farmer(temp_state)
            if not temp_state.is_valid():
                thing = get_thing(temp, f_location)
                while thing == Thing.FARMER:
                    thing = get_thing(temp, f_location)
                use_boat(temp, f_location, thing)
            else:
                move_farmer(temp)
        else:
            thing = get_thing(temp, f_location)
            temp_state = deepcopy(temp)
            while thing == Thing.FARMER:
                thing = get_thing(temp, f_location)
            use_boat(temp_state, direction, thing)
            while not temp_state.is_valid() or thing == thing.FARMER:
                temp_state = deepcopy(temp)
                thing = get_thing(temp, f_location)
                if thing == Thing.FARMER:
                    continue
                use_boat(temp_state, direction, thing)
            use_boat(temp, direction, thing)
        return solve(temp, not even)


if __name__ == "__main__":
    initial_state = State()
    final = solve(initial_state)
    while final is not None:
        print(final, "\n")
        final = final.prv
