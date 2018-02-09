from rqalpha import run
import csv
import time

tasks = []
csvfile = open('E:/wendou/tick.csv', 'r')
tick = csv.reader(csvfile)

for inst in tick:
    config = {
        "extra": {
            "context_vars": {
                "s1": inst[0],
            },
            "log_level": "error",
        },
        "base": {
            "matching_type": "current_bar",
            "start_date": "2017-01-01",
            "end_date": "2018-02-06",
            "benchmark": "000001.XSHE",
            "frequency": "1d",
            "strategy_file": "C:/Users/think/PycharmProjects/wendou/FBB.py",
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
    time.sleep(2)

csvfile.close

