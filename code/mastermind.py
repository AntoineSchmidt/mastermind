import os
import sys

import numpy as np

from tqdm import tqdm


def codes(length, count):
    a = np.ones((count ** length, length), dtype=np.uint8)

    for i in range(1, len(a)):
        a[i] = a[i - 1]

        for x in range(length)[::-1]:
            a[i, x] += 1

            if a[i, x] > count:
                a[i, x] = 1
            else:
                break

    return a


def evaluate(test, hidden):
    comparison = (test == hidden)
    b = np.sum(comparison)

    # solved
    if b == len(test):
        return b, 0

    comparison = np.invert(comparison)

    test = list(np.array(test)[comparison])
    hidden = list(np.array(hidden)[comparison])

    test = sorted(test)
    hidden = sorted(hidden)

    w = 0
    index = len(hidden) - 1
    for i in test[::-1]:
        while index >= 0:
            if hidden[index] > i:
                index -= 1
            elif i == hidden[index]:
                w += 1
                index -= 1
                break
            else:
                break

    return b, w


def evaluate_codes(a):
    e = np.zeros((len(a), len(a), 2), dtype=np.uint8)

    np.fill_diagonal(e[:, :, 0], a.shape[1])

    for x in tqdm(range(len(a))):
        for y in range(x + 1, len(a)):
            e[x, y] = evaluate(a[x], a[y])

    # mirror half matrix
    e = np.maximum(e, np.transpose(e, axes=(1, 0, 2)))

    return e


# min-max code selection optimization, Knuth (modified)
def best_code(e_cantor, a_valid, a_selected):
    i_valid = np.array(list(a_valid))
    i_selected = np.array(list(a_selected))

    # first code selection, 1122
    #if len(i_selected) == len(e_cantor):
    #    return 7

    # last possible code
    if len(i_valid) == 1:
        return i_valid[0]

    elimination = np.zeros((len(i_selected), 2), dtype=np.uint)

    cantor = e_cantor[i_selected][:, i_valid]
    for i in range(len(elimination)):
        counts = np.unique(cantor[i], return_counts=True)[1]
        elimination[i] = np.sort(counts)[-1], len(counts)

    best_elimination = (elimination[:, 0] == np.min(elimination[:, 0]))
    # subselect by max unique answer count, improves elimination when not getting the worst answer
    best_answercount = (elimination[:, 1] == np.max(elimination[best_elimination, 1]))
    best = np.bitwise_and(best_elimination, best_answercount)

    best = i_selected[best]
    best_valid = set(best).intersection(a_valid)

    # priorize codes which are valid
    if len(best_valid) > 0:
        return np.random.choice(list(best_valid))

    return np.random.choice(best)


def cantor_pairing(e):
    e_cantor = e[:, :, 0] ** 2 + 3 * e[:, :, 0] + 2 * e[:, :, 0] * e[:, :, 1] + e[:, :, 1] + e[:, :, 1] ** 2
    return e_cantor // 2


if __name__ == "__main__":
    np.random.seed(123)

    length, count = int(sys.argv[1]), int(sys.argv[2])
    name = "{}-{}.npz".format(length, count)

    # create codes and evaluation matrix
    if os.path.exists(name):
        data = np.load(name)
        a = data['a']
        e = data['e']
    else:
        a = codes(length, count)
        e = evaluate_codes(a)
        e = cantor_pairing(e)
        np.savez(name, a=a, e=e)

    trial_count = []

    # game
    while True:
        a_valid = set(np.arange(len(a)))
        a_selected = set(np.arange(len(a)))

        #hidden = a[np.random.randint(len(a))]
        #hidden = a[len(trial_count) % len(a)]
        hidden = np.random.randint(count, size=(length,)) + 1
        #hidden = None
        print(hidden)

        trial_count.append(0)

        # trial
        while True:
            selected = best_code(e, a_valid, a_selected)
            selected_code = a[selected]

            if hidden is not None:
                response = evaluate(selected_code, hidden)
            else:
                # user input
                print(selected_code, len(a_valid))
                response = (int(input('Blacks: ')), int(input('Whites: ')))

            print(selected_code, response, len(a_valid))

            trial_count[-1] += 1

            #solved
            if response[0] == length:
                break

            # remove tested code
            if selected in a_valid:
                a_valid.remove(selected)
            a_selected.remove(selected)

            # response to cantor
            response_cantor = np.zeros((1, 1, 2))
            response_cantor[0, 0] = response
            response = cantor_pairing(response_cantor)[0, 0]

            # remove invalid codes
            for i in list(a_valid):
                if e[selected, i] != response:
                    a_valid.remove(i)

            # evaluation input error
            if len(a_valid) == 0:
                print("No possible solution")
                trial_count = trial_count[:-1]
                break

        if trial_count:
            print(">>", np.max(trial_count), np.average(trial_count)) # Knuth: 5 4.478
        print()