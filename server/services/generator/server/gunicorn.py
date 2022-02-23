import multiprocessing

bind = "0.0.0.0:6030"
timeout = 300000
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 16