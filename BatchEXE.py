import concurrent.futures
import multiprocessing
from rqalpha import run
import csv
tasks = []
csvfile = open('E:/wendou/tick.csv','r')
tick = csv.reader(csvfile)

for inst in tick:
    config = {
            "extra": {
                "context_vars": {
                    "s1": inst[0],
                },
                "log_level": "verbose",
            },
            "base": {
                "matching_type": "current_bar",
                "start_date": "2017-01-01",
                "end_date": "2018-02-06",
                "benchmark": "000001.XSHE",
                "frequency": "1d",
                "strategy_file": "C:/ProgramData/Anaconda3/Lib/site-packages/rqalpha/examples/FBB.py",
        "accounts": {
            "stock": 100000
        }
            },
            "mod": {
                "sys_progress": {
                    "enabled": True,
                    "show": True,
                },
                "sys_analyser": {
                    "enabled": True,
                    "output_file": "E:/tmp/result/FBB-out-{tick}.pkl".format(tick=inst[0])
                },
            },
        }

    tasks.append(config)

for task in tasks:
    run(task)

def run_bt(config):
    run(config)
csvfile.close
###################################
# below is the result analyze code
import glob
import pandas as pd


results = []

for name in glob.glob("E:/tmp/result/*.pkl"):
    result_dict = pd.read_pickle(name)
    summary = result_dict["summary"]
    results.append({
        "name": name,
        "annualized_returns": summary["annualized_returns"],
        "sharpe": summary["sharpe"],
        "max_drawdown": summary["max_drawdown"],
    })

results_df = pd.DataFrame(results)

print("-" * 50)
print("Sort by sharpe")
print(results_df.sort_values("sharpe", ascending=False)[:10])

print("-" * 50)
print("Sort by annualized_returns")
print(results_df.sort_values("annualized_returns", ascending=False)[:10])