import math
from numpy.random import choice
import time
import numpy as np
import multiprocessing as mp
import pandas as pd


def get_haplotypes_freq(p_a, p_b, r):
    p_ab = r * math.sqrt(p_a * (1 - p_a) * p_b * (1 - p_b)) + p_a * p_b
    p_aB = p_a - p_ab
    p_Ab = p_b - p_ab
    p_AB = 1 - p_ab - p_aB - p_Ab

    if p_Ab < 0 or p_aB < 0 or p_ab < 0 or p_AB < 0:
        print("Wrong allele frequences for given r", p_a, p_b, r)
        return -1

    return [p_AB, p_Ab, p_aB, p_ab]


def simulate_generation(hapl_freq, Ne):
    elements = [0, 1, 2, 3]
    np.random.seed()
    population = choice(elements,  2*Ne, p=hapl_freq)
    #counts = Counter(population) - works longer
    values, counts = np.unique(population, return_counts=True)
    dictionary = dict(zip(values, counts))
    new_freq = [0, 0, 0, 0]
    for i in elements:
        try:
            new_freq[i] = dictionary[i] / (2 * Ne)
        except KeyError:
            pass

    return new_freq


def hapl_to_r(hapl_freq):
    P, Q, R, S = hapl_freq
    try:
        r = (P * S - Q * R) / math.sqrt((P + Q) * (R + S) * (P + R) * (Q + S))
    except ZeroDivisionError:
        r = float('nan')
    p_a = R + S
    p_b = Q + S
    # p_A = P + Q
    # p_B = P + R
    # r_alt = (P - p_A*p_B)/math.sqrt(p_a*p_A*p_b*p_B)
    return [p_a, p_b, r, P, Q, R, S]


def simulate_generations(hapl_freq, generations, Ne, step=50):
    results = []
    for generation in range(generations):
        hapl_freq = simulate_generation(hapl_freq, Ne)
        generation += 1
        if (generation % step) == 0 or generation == generations:
            results.append([generation] + hapl_to_r(hapl_freq))
    output = pd.DataFrame(np.array(results), columns=['gen', 'p_a', 'p_b', 'r', 'p_AB', 'p_Ab', 'p_aB', 'p_ab'])
    return output


def get_simulation_results(r_ab0, p_a0, p_b0, Ne, generations, number_of_sim, n_threads=2, step_to_save=50):
    result_list = []

    def log_result(result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        result_list.append(result)

    def apply_async_with_callback():
        pool = mp.Pool(n_threads)
        for i in range(number_of_sim):
            pool.apply_async(simulate_generations,
                             args=(get_haplotypes_freq(p_a=p_a0, p_b=p_b0, r=r_ab0), generations, Ne, step_to_save),
                             callback=log_result)
        pool.close()
        pool.join()

    start_time = time.time()
    apply_async_with_callback()
    print("{0} seconds to do {1} simulations".format(time.time() - start_time, number_of_sim))
    output = pd.concat(result_list)
    return output


def max_p_b(p_a, r, precision=5):
    if r == 0:
        return 1
    p_b = p_a / (p_a * (1 - r ** 2) + r ** 2)
    p_b = np.floor(p_b * 10 ** precision) / 10 ** precision
    return p_b


def min_p_b(p_a, r, precision=5):
    if r == 0:
        return 0
    p_b = p_a * r ** 2 / (1 - p_a * (1 - r ** 2))
    p_b = np.ceil(p_b * 10 ** precision) / 10 ** precision
    return p_b
