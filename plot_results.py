#!python3

""" 
A main program for analyzing experiment results.
The result file should be generated first by experiment.py.

Author: Erel Segal-Halevi
Since:  2020-2021
"""

import pandas
import matplotlib.pyplot as plt
import numpy as np


figsize=(5, 7)
dpi=80
facecolor='w'
edgecolor='k'

styles = ["b-","g-","r-", "b--","g--","r--", "b:","g:","r:"]

def plot_results(results_csv_file:str, n:int=4):
    figure_title = f"n={n}" 
    output_file = results_csv_file.replace(".csv",f"-{n}.png")
    results = pandas.read_csv(results_csv_file)
    results = results.query(f"num_of_agents=={n}")
    plt.style.use('grayscale')  # reference: https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
    plt.rc('legend', fontsize=12, loc="lower right")
    _, axis = plt.subplots(1,1) 
    L_values = sorted(results["L"].unique())
    D_values = sorted(results["D"].unique())

    for index,(L,D) in enumerate(zip(reversed(L_values),reversed(D_values))):
        results.query(f"L=={L}").groupby("num_of_items")["greedy_approximation_to_MMS"].mean().plot(
            legend=True,
            style=styles[index % len(styles)],
            label=f"L={L}, D={D}",
            ax=axis)

    max_num_of_items = results["num_of_items"].max()
    print("n={n}, max_num_of_items=",max_num_of_items)
    garg_taki_approximation = int((3/4+1/(12*n))*100)
    axis.plot(range(max_num_of_items), max_num_of_items*[garg_taki_approximation], "k-")
    axis.set_title(figure_title, fontsize=20)

    axis.set_xlabel("Num of items",fontsize=16)
    axis.set_ylabel(f"Ratio of L-out-of-D MMS to Total-Value/{n} (%)",fontsize=15)
    axis.set_yticks(np.arange(0,100,step=10))
    axis.tick_params(labelsize=16)

    plt.savefig(output_file)


def plot_results_for_JAIR_paper():
    nums_of_agents = [4,20]
    for n in nums_of_agents:
        plot_results("results/unif-1-1000-double.csv", n=n)
        plot_results("results/unif-1000-2000-double.csv", n=n)
        plot_results("results/geom-1000-double.csv", n=n)


if __name__ == "__main__":
    plot_results_for_JAIR_paper()
