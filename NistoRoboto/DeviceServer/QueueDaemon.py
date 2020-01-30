import threading
import time
import datetime

class QueueDaemon(threading.Thread):
    '''
    '''
    def __init__(self,app,task_queue,history,debug=True):
        app.logger.info('Creating QueueDaemon thread')

        threading.Thread.__init__(self,name='QueueDaemon',daemon=True)

        self.protocol  = None#Protocol(app)

        self.app = app
        self.task_queue = task_queue
        self.history    = history

        self.stop = False
        self.debug = debug
        self.paused = False

    def terminate(self):
        self.app.logger.info('Terminating QueueDaemon thread')
        self.stop = True
        self.task_queue.put(None)

    def run(self):
        while not self.stop:
            package = self.task_queue.get(block=True,timeout=None)
            task = package['task']

            self.app.logger.info(f'Running task {task}')
            package['meta']['started'] = datetime.datetime.now().strftime('%H:%M')

            self.history.append(package)

            # If the task object is None, break the queue-loop
            if task is None: #stop the queue execution
                self.terminate()
                break

            #if debug_mode, pop and wait but don't execute
            if self.debug: 
                time.sleep(3.0)
                package['meta']['ended'] = datetime.datetime.now().strftime('%H:%M')
                continue
            
            # pause queue but notify user of state every minute
            count = 600
            while self.paused: 
                time.sleep(0.1)
                count+=1
                if count>600:
                    self.app.logger.info('Queued is paused. Set paused state to false to continue execution')
                    count = 0

            continue
            getattr(self.protocol,task['name'])(**task)
            package['meta']['ended'] = datetime.datetime.now().strftime('%H:%M')
            time.sleep(0.1)

        self.app.logger.info('QueueDaemon runloop exiting')

    







