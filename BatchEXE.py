import concurrent.futures
import multiprocessing
from rqalpha import run

tasks = []
for short_period in range(3, 10, 3):
    for long_period in range(30, 90, 10):
        config = {
            "extra": {
                "context_vars": {
                    "SHORTPERIOD": short_period,
                    "LONGPERIOD": long_period,
                },
                "log_level": "error",
            },
            "base": {
                "matching_type": "current_bar",
                "start_date": "2015-01-01",
                "end_date": "2016-01-01",
                "benchmark": "000001.XSHE",
                "frequency": "1d",
                "strategy_file": "C:/ProgramData/Anaconda3/Lib/site-packages/rqalpha/examples/golden_cross.py",
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
                    "output_file": "E:/tmp/result/out-{short_period}-{long_period}.pkl".format(
                        short_period=short_period,
                        long_period=long_period,
                    )
                },
            },
        }

        tasks.append(config)

for task in tasks:
    run(task)

def run_bt(config):
    run(config)

with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    for task in tasks:
        executor.submit(run_bt, task)


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