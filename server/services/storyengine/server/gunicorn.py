import multiprocessing

bind = "0.0.0.0:6010"
workers = 16
timeout = 300
# workers = multiprocessing.cpu_count() * 2 + 1