from functions import get_simulation_results, min_p_b, max_p_b
import pickle
import numpy as np
import os


def sumulate_and_save(r_ab, p_a, p_b, Ne, generations, number_of_sim, n_threads, step_to_save=50):
    df = get_simulation_results(r_ab0=r_ab, p_a0=p_a, p_b0=p_b, Ne=Ne, generations=generations, number_of_sim=number_of_sim,
                                n_threads=n_threads, step_to_save=step_to_save)
    df['r_0'] = r_ab
    df['p_a0'] = p_a
    df['p_b0'] = p_b

    df.to_hdf(path_or_buf='results/test.h5', key='test', format='table', append=True, data_columns=True)
    file_name = "results/r_{0}_a_{1}_b_{2}_Ne_{3}_gen_{4}_nsim_{5}.pickle".format(r_ab, p_a, p_b, Ne, generations, number_of_sim,)
    filehandler = open(file_name, "wb")
    pickle.dump(df, filehandler)
    filehandler.close()


def sumilate_and_append_to_hdf(r_ab, p_a, p_b, Ne, generations, number_of_sim, n_threads, step_to_save, path):

    df = get_simulation_results(r_ab0=r_ab, p_a0=p_a, p_b0=p_b, Ne=Ne, generations=generations,
                                number_of_sim=number_of_sim, n_threads=n_threads, step_to_save=step_to_save)
    df['r_0'] = r_ab
    df['p_a0'] = p_a
    df['p_b0'] = p_b
    df.to_hdf(path_or_buf=path, key='result', format='table', append=True, data_columns=True)


def make_hdf5_table(Ne=10**4, generations=10**3, number_of_sim=10, n_threads=2, step_to_save=50, path='results/result.h5'):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

    for r_ab in np.arange(0.75, 1, 0.1):
        for p_a in np.arange(0.05, 1, 0.1):
            for p_b in [min_p_b(p_a=p_a, r=r_ab), p_a, max_p_b(p_a=p_a, r=r_ab)]:
                sumilate_and_append_to_hdf(r_ab=r_ab, p_a=p_a, p_b=p_b, Ne=Ne, generations=generations,
                                           number_of_sim=number_of_sim, n_threads=n_threads, step_to_save=step_to_save,
                                           path=path)

    return 0


if __name__ == "__main__":
    '''sumulate_and_save(r_ab=0.7, p_a=0.3, p_b=0.3, Ne=10**4, generations=1000, number_of_sim=5, n_threads=2,
                      step_to_save=100)
    sumulate_and_save(r_ab=0.0, p_a=0.5, p_b=0.5, Ne=10**4, generations=1000, number_of_sim=5, n_threads=2,
                      step_to_save=100)'''
    make_hdf5_table(Ne=10**4, generations=10**3, number_of_sim=10**3, path='results/results.h5')