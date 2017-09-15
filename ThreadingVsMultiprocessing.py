import sched, time, threading, multiprocessing

stopThread = False
threadCounts = []
processCounts = []

s = sched.scheduler(time.time, time.sleep)

def thread_handle(args):
    global threadCounts
    print ('In Thread - %d\n' % args),
    counter = 0
    while not stopThread:
        counter += 1

    threadCounts.append(counter)


threads = []    
def process_thread():
    global theads
    print ('Processing Thread ......')

    for i in range(5):
        t = threading.Thread(target=thread_handle, args=[i])
        t.start()
        threads.append(t)

def process_handle(args):
    global processCounts
    print ('In Process - %d' % args)
    counter = 0;
    while not stopThread:
        counter += 1

    processCounts.append(counter)

processes = []
def process_process():
    global processes
    print ('Processing Process ......')

    for i in range(5):
        p = multiprocessing.Process(target=process_handle, args=[i])
        p.start()
        processes.append(p)
        
    print(processes)
    
        
def stop_process():
    global stopThread
    global threadCounts
    global thread

    stopThread = True

    for t in threads:
        t.join()

def count_p_process():
    global processCounts
    global processes
    
    for p in processes:
        p.join()
        
    print ('Process Counts -', sum(processCounts))

s.enter(0, 1, process_thread, ())
s.enter(0, 1, process_process, ())
s.enter(5, 2, stop_process, ())
s.enter(5, 3, count_p_process, ())
s.run()

        
