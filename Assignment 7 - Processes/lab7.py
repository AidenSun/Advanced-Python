import queue
import time
import os
import platform
import threading
import multiprocessing as mp

def childInteger(q, e):
    data = q.get()
    while data != 0:
        data += 1
        e.set()
        q.put(data)
        e.wait()
        data = q.get()
        e.clear()
        
def childList(q, e):
    data = q.get()
    while data != []:
        data.append(1)
        e.set() 
        q.put(data)
        e.wait()
        data = q.get()
        e.clear()
        
def processWithQueueInteger(data):
    e = mp.Event()
    q = mp.Queue()
    
    p = mp.Process(target=childInteger, args=(q, e))
    
    p.start()
    
    q.put(1)
    e.wait()
    data = q.get()
    e.set()
    if data != 2:
        raise Exception('Unexpected Data')

    data = 0
    start = time.time()
    
    for i in range(10000):
        data += 1
        q.put(data)
        e.wait()
        data = q.get()
        e.set()
        
    end = time.time()
    q.put(0)
    
    p.join()
    
    if data != 20000:
        raise Exception('Unexpected data')
    
    difference = end - start
    
    print('Data:', data)
    print('Time difference:', difference)
    return 20000/difference

def processWithQueueList(data):
    e = mp.Event()
    q = mp.Queue()
    
    p = mp.Process(target=childList, args=(q, e))
    
    p.start()
    
    q.put([0])
    e.wait()
    data = q.get()
    e.set()
    if data != [0,1]:
        raise Exception('Unexpected Data')

    data = []
    start = time.time()
    
    for i in range(300):
        data.append(0)
        q.put(data)
        e.wait()
        data = q.get()
        e.set()
        
    end = time.time()
    q.put([])
    
    p.join()
    
    if len(data) != 600:
        raise Exception('Unexpected data')
    
    difference = end - start
    
    print('Data:', data)
    print('Time difference:', difference)
    return 600/difference

if __name__ == '__main__':
    test = processWithQueueInteger(0)
    print('Process with Queue (Integer): ', int(test))
    
    print()
    
    test = processWithQueueList([])
    print('Process with Queue (List): ', int(test))
    
    