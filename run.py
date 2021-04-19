import sys
import csv
import queue
import argparse
import numpy

# global instruciton set
instruction = []


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

# Function Definition for each of the moves. Arguments: State (2d array of values,
# origin and dest are integer values. 0 indicates left and 1 indicates right.)


def oneChicken(state, dest, origin):
    state[origin][0] = (state[origin][0])-1
    state[dest][0] = (state[dest][0])+1
    state[dest][2] = 1
    state[origin][2] = 0


def twoChicken(state, dest, origin):
    state[origin][0] = (state[origin][0])-2
    state[dest][0] = (state[dest][0])+2
    state[dest][2] = 1
    state[origin][2] = 0


def oneWolf(state, dest, origin):
    state[origin][1] = (state[origin][1])-1
    state[dest][1] = (state[dest][1])+1
    state[dest][2] = 1
    state[origin][2] = 0


def twoWolf(state, dest, origin):
    state[origin][1] = (state[origin][1])-2
    state[dest][1] = (state[dest][1])+2
    state[dest][2] = 1
    state[origin][2] = 0


def oneAndOne(state, dest, origin):
    state[origin][0] = (state[origin][0])-1
    state[dest][0] = (state[dest][0])+1
    state[origin][1] = (state[origin][1])-1
    state[dest][1] = (state[dest][1])+1
    state[dest][2] = 1
    state[origin][2] = 0


def check(state):
    if((state[0][0] < state[0][1]) or (state[1][0] < state[1][1])):
        return False
    if(state[0][0] == -1):
        return False
    if(state[0][1] == -1):
        return False
    if(state[1][0] == -1):
        return False
    if(state[1][1] == -1):
        return False
    else:
        return True


def bfs(initial, final):
    if (initial == final):
        return 0

    explored = []
    frontier = []
    frontier.append(initial)
    current = initial
    numNodes = 0

    while(explored):
        # Pop initial 2d array state out of FIFO queue and put into current
        # current = explored.pop(0)
        if(not frontier):
            return numNodes
        # If boat is on the right side
        if(current[0][2] == 0 and current[1][2] == 1):

            # Put one chicken in boat and check if valid

            oneChicken(current, 0, 1)
            if(check(current)):
                frontier.append(current)
                instruction.append("one chicken moved to left")
                if (current == final):
                    return numNodes
            oneChicken(current, 1, 0)

            # Put two chickens in the boat and check if valid

            twoChicken(current, 0, 1)
            if(check(current)):
                frontier.append(current)
                instruction.append("two chicken moved to left")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            twoChicken(current, 1, 0)

            # Put one wolf in boat and check if valid

            oneWolf(current, 0, 1)
            if(check(current)):
                frontier.append(current)
                instruction.append("one wolf moved to left")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            oneWolf(current, 1, 0)

            # Put a chicken and a wolf and check if valid

            oneAndOne(current, 0, 1)
            if(check(current)):
                frontier.append(current)
                instruction.append("one chicken and one wolf moved to left")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            oneAndOne(current, 1, 0)

            # Put two wolves in and check if valid

            twoWolf(current, 0, 1)
            if(check(current)):
                frontier.append(current)
                instruction.append("two wolves moved to left")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            twoWolf(current, 1, 0)
        explored.append(current)

        # Boat is on left side
        if(current[0][2] == 1 and current[1][2] == 0):

            oneChicken(current, 1, 0)
            if(check(current)):
                frontier.append(current)
                instruction.append("one chicken moved to right")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            oneChicken(current, 0, 1)

            twoChicken(current, 1, 0)
            if(check(current)):
                frontier.append(current)
                instruction.append("two chicken moved to right")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            twoChicken(current, 0, 1)

            oneWolf(current, 1, 0)
            if(check(current)):
                frontier.append(current)
                instruction.append("one wolf moved to right")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            oneWolf(current, 0, 1)

            oneAndOne(current, 1, 0)
            if(check(current)):
                frontier.append(current)
                instruction.append("one chicken and one wolf moved to right")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            oneAndOne(current, 0, 1)

            twoWolf(current, 1, 0)
            if(check(current)):
                frontier.append(current)
                instruction.append("two wolves moved to right")
                numNodes = numNodes+1
                if (current == final):
                    return numNodes
            twoWolf(current, 0, 1)
        explored.append(current)


def main():
    width = 3
    height = 2
    values = []
    goals = []

    args = get_args()
    start = args.init.read()
    goal = args.goal.read()
    mode = args.mode
    outFile = args.out

    initial = [[0 for x in range(width)] for y in range(height)]
    final = [[0 for x in range(width)] for y in range(height)]
    f = open(sys.argv[1])
    for row in csv.reader(f):
        values.append(row[0])
        values.append(row[1])
        values.append(row[2])
    f.close()
    initial[0][0] = int(values[0])
    initial[0][1] = int(values[1])
    initial[0][2] = int(values[2])
    initial[1][0] = int(values[3])
    initial[1][1] = int(values[4])
    initial[1][2] = int(values[5])

    f = open(sys.argv[2])
    for row in csv.reader(f):
        goals.append(row[0])
        goals.append(row[1])
        goals.append(row[2])
    f.close()
    final[0][0] = int(goals[0])
    final[0][1] = int(goals[1])
    final[0][2] = int(goals[2])
    final[1][0] = int(goals[3])
    final[1][1] = int(goals[4])
    final[1][2] = int(goals[5])

    bfsNodes = 0
    bfsNodes = bfs(initial, final)
    print(bfsNodes)


if __name__ == "__main__":
    main()
