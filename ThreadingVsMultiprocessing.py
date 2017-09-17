import sched, time, threading, multiprocessing

stopThread = False
threadCounts = []
processCounts = []

s = sched.scheduler(time.time, time.sleep)

#%% Handle Thread
def thread_handle(args):
    '''
    Used global stopThread variable to stop all threads at the same time
    '''
    global threadCounts
    print ('In Thread - %d\n' % args, end='')
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

def stop_thread():
    global stopThread
    stopThread = True


#%% Handle Process
def process_handle(args, processCounts):
    '''
    As process has separate memory space stopProcess variable is not share 
    among all the processes. Therefore, a single schedular cannot be used to 
    stop all processes at the same time.
    '''
    global stopProcess
    
    stopProcess = False
    
    print ('In Process - %d' % args)
            
            
    s = sched.scheduler(time.time, time.sleep)
    
    def stop_process():
        global stopProcess
        stopProcess = True
    
    s.enter(5, 2, stop_process, ())
    threading.Thread(target=lambda : s.run()).start()
    
    counter = 0;
    while not stopProcess:
        counter += 1
    
    processCounts.append(counter)

processes = []
def process_process():
    global processes
    global processCounts
    
    print ('\nProcessing Process ......')
    
    processCounts = multiprocessing.Manager().list()

    for i in range(5):
        p = multiprocessing.Process(target=process_handle, args=(i, processCounts))
        p.start()
        processes.append(p)

#%% End Calculations      
def stop():
    global threadCounts
    global threads
    global processCounts
    global processes
    
    for t in threads:
        t.join()
        
    
    for p in processes:
        p.join()
    
    totalThreadCounts = sum(threadCounts)
    totalProcessCounts = sum(processCounts)
    
    print ('\nThread Counts -', totalThreadCounts )
    print ('\nProcess Counts -', totalProcessCounts, end='\n\n')
    
    if totalThreadCounts > totalProcessCounts:
        print ('Thread is faster')
    elif totalThreadCounts < totalProcessCounts:
        print ('Process is faster')
    else:
        print ('Its a Draw')

#%% Schedule Program
s.enter(0, 1, process_thread, ())
s.enter(5, 1, stop_thread, ())
s.enter(6, 2, process_process, ())
s.enter(6, 1, stop, ())
s.run()

        
