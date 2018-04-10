from functions import get_simulation_results
import pickle




def sumulate_and_save(r_ab, p_a, p_b, Ne, generations, number_of_sim, n_threads, step_to_save = 50):
    df = get_simulation_results(r_ab0=r_ab, p_a0=p_a, p_b0=p_b, Ne=Ne, generations=generations, number_of_sim=number_of_sim,
                                n_threads=n_threads, step_to_save=step_to_save)
    file_name = "r_{0}_a_{1}_b_{2}_Ne_{3}_gen_{4}_nsim_{5}.pickle".format(r_ab, p_a, p_b, Ne, generations, number_of_sim,)

    filehandler = open(file_name, "wb")
    pickle.dump(df, filehandler)
    filehandler.close()


if __name__=="__main__":
    sumulate_and_save(r_ab=0.0, p_a=0.5, p_b=0.5, Ne=10**4, generations=1000, number_of_sim=500, n_threads=4, step_to_save=100)
    #sumulate_and_save(r_ab=0.7, p_a=0.2, p_b=0.2, Ne=10**4, generations=1000, number_of_sim=10000, n_threads=2, step_to_save=100)

