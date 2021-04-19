# boat riddle
# @author: John C. Zontos
# email: zontosj@oregonstate.edu

import argparse
import csv
import copy

explored = []
frontier = []
expanded_count = 0


class State:
    def __init__(self, left, right, parent=None):
        self.left_chickens = left[0]
        self.left_wolves = left[1]
        self.right_chickens = right[0]
        self.right_wolves = right[1]
        # boat position: 0 for left 1 for right
        self.boat = 0 if left[2] else 1

    def __str__(self):
        left_boat = 0 if self.boat else 1
        right_boat = 1 if self.boat else 0
        str = f'\nchickens: {self.left_chickens}, {self.right_chickens}\
        \nwolves:   {self.left_wolves}, {self.right_wolves}\
        \nboat:     {left_boat}, {right_boat}'
        # + self.parent.__str__()
        return str

    def __eq__(self, other):
        if(self.left_chickens == other.left_chickens and
           self.left_wolves == other.left_wolves and
           self.right_chickens == other.right_chickens and
           self.right_wolves == other.right_wolves and
           self.boat == other.boat):
            return True
        return False

# helper function for the action funcitons bellow
# takes # of chickens and number of wolves to be moved
#  returns a new state

# !! maybe add check before returning state
#           otherwise we have to check that the state is valid later.
#           maybe before adding it to the frontier

    def move(self, chickens, wolves):
        # !! may need a deepcopy
        temp = copy.copy(self)
        # boat is on the left going right
        if(self.boat == 0):
            # move chickens
            temp.left_chickens -= chickens
            temp.right_chickens += chickens
            # move wolves
            temp.left_wolves -= wolves
            temp.right_wolves += wolves
            # move Boat
            temp.boat = 1
        elif (self.boat == 1):
            # move chickens
            temp.right_chickens -= chickens
            temp.left_chickens += chickens
            # move wolves
            temp.right_wolves -= wolves
            temp.left_wolves += wolves
            # move Boat
            temp.boat = 0
        else:
            print("boat is lost...")
        return temp

    def check_move(self, chickens, wolves):
        temp = self.move(chickens, wolves)
        if(temp in explored):
            return False
        if(temp.left_chickens < 0 or
           temp.left_wolves < 0 or
           temp.right_chickens < 0 or
           temp.right_wolves < 0):
            return False
        if(temp.left_wolves > temp.left_chickens and temp.left_chickens):
            return False
        if(temp.right_wolves > temp.right_chickens and temp.right_chickens):
            return False

        return True


class Node:
    def __init__(self, state, cost=0, parent=None):
        self.state = state
        self.cost = cost
        self.parent = parent

    def __str__(self):
        str = f'{self.parent.__str__()}\
        \n{self.state.__str__()}'
        return str

    def __eq__(self, other):
        return self.state == other.state

    def get_state(self):
        return self.state

    def get_cost(self):
        return self.cost

    def check_action(self, c, w):
        if(self.state.check_move(c, w)):
            temp = self.gen_child(c, w)
            if(temp in frontier):
                return False
            return True
        return False

    def gen_child(self, c, w):
        # !! may need a deepcopy
        temp = copy.copy(self)
        temp.state = self.state.move(c, w)
        temp.cost += 1
        temp.parent = self
        return temp

    def one_chicken(self):
        return self.gen_child(1, 0)

    def two_chickens(self):
        return self.gen_child(2, 0)

    def one_wolf(self):
        return self.gen_child(0, 1)

    def one_both(self):
        return self.gen_child(1, 1)

    def two_wolves(self):
        return self.gen_child(0, 2)


def increment():
    global expanded_count
    expanded_count = expanded_count+1


def mode_type(s):
    if s not in {"bfs", "dfs", "iddfs", "astar"}:
        raise argparse.ArgumentTypeError("Invalid mode! check -h")
    return s


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "init",
        type=argparse.FileType("r"),
        help="initial state file",
    )

    parser.add_argument(
        "goal",
        type=argparse.FileType("r"),
        help="goal state file",
    )

    parser.add_argument(
        "mode",
        type=mode_type,
        help="The mode argument is either: bfs, dfs, iddfs, astar",
    )

    parser.add_argument(
        "out",
        type=argparse.FileType("w"),
        help="output file",
    )

    return parser.parse_args()


def bfs(init, goal):
    if (init == goal):
        return init

    node = Node(init)
    frontier.append(node)
    while(True):
        if(len(frontier) <= 0):
            print("failure!")
            return None
        node = frontier.pop(0)
        increment()
        if(node.get_state() == goal):
            print("found goal")
            return node
        explored.append(node.get_state())
        if(node.check_action(1, 0)):
            child = node.one_chicken()
            frontier.append(child)
        if(node.check_action(2, 0)):
            child = node.two_chickens()
            frontier.append(child)
        if(node.check_action(0, 1)):
            child = node.one_wolf()
            frontier.append(child)
        if(node.check_action(1, 1)):
            child = node.one_both()
            frontier.append(child)
        if(node.check_action(0, 2)):
            child = node.two_wolves()
            frontier.append(child)


def dfs(init, goal):
    if (init == goal):
        return init

    node = Node(init)
    frontier.append(node)
    while(True):
        if(len(frontier) <= 0):
            print("failure!")
            return None
        node = frontier.pop()
        increment()
        if(node.get_state() == goal):
            print("found goal")
            return node
        explored.append(node.get_state())
        if(node.check_action(1, 0)):
            child = node.one_chicken()
            frontier.append(child)
        if(node.check_action(2, 0)):
            child = node.two_chickens()
            frontier.append(child)
        if(node.check_action(0, 1)):
            child = node.one_wolf()
            frontier.append(child)
        if(node.check_action(1, 1)):
            child = node.one_both()
            frontier.append(child)
        if(node.check_action(0, 2)):
            child = node.two_wolves()
            frontier.append(child)


def rddfs(node, goal, limit):
    increment()
    explored.append(node.get_state())
    if (node.get_state() == goal):
        print("found goal")
        return node
    elif (limit <= 0):
        return None
    else:
        if(node.check_action(1, 0)):
            child = node.one_chicken()
            if((result := rddfs(child, goal, limit-1)) is not None):
                return result
        if(node.check_action(2, 0)):
            child = node.two_chickens()
            if((result := rddfs(child, goal, limit-1)) is not None):
                return result
        if(node.check_action(0, 1)):
            child = node.one_wolf()
            if((result := rddfs(child, goal, limit-1)) is not None):
                return result
        if(node.check_action(1, 1)):
            child = node.one_both()
            if((result := rddfs(child, goal, limit-1)) is not None):
                return result
        if(node.check_action(0, 2)):
            child = node.two_wolves()
            if((result := rddfs(child, goal, limit-1)) is not None):
                return result
        return None


def ddfs(init, goal, limit):
    return rddfs(Node(init), goal, limit)


def iddfs(init, goal):
    lim = 0
    while(True):
        frontier.clear()
        explored.clear()
        lim += 1
        temp = ddfs(init, goal, lim)
        if(temp):
            return temp


def astar():
    return None


def parse_state(f):
    temp = []
    for line in csv.reader(f):
        temp.append(int(line[0]))
        temp.append(int(line[1]))
        temp.append(int(line[2]))
    return State(temp[0:3], temp[3:6])


def main():
    # parse args
    args = get_args()
    init = parse_state(args.init)
    goal = parse_state(args.goal)
    mode = args.mode
    outFile = args.out

    # print(Node(init, 0))
    print(init)

    print(goal)

# "bfs", "dfs", "iddfs", "astar"
    if(mode == "bfs"):
        temp = bfs(init, goal)
    if(mode == "dfs"):
        temp = dfs(init, goal)
    if(mode == "iddfs"):
        temp = iddfs(init, goal)
    if(mode == "astar"):
        temp = astar(init, goal)

    # print(temp)
    print(f'cost: {temp.get_cost()}')

    print(f'nodes expanded: {expanded_count}')


if __name__ == "__main__":
    main()
