import multiprocessing

bind = "0.0.0.0:8000"
workers = 1 # multiprocessing.cpu_count() * 2 + 1

timeout = 3 * 60  # 3 minutes