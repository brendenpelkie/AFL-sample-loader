import threading
import time
import datetime
import sys
import traceback

class QueueDaemon(threading.Thread):
    '''
    '''
    def __init__(self,app,driver,task_queue,history,debug=True):
        app.logger.info('Creating QueueDaemon thread')

        threading.Thread.__init__(self,name='QueueDaemon',daemon=True)

        self.driver  = driver

        self.app = app
        self.task_queue = task_queue
        self.history    = history
        self.running_task = []

        self.stop = False
        self.debug = debug
        self.paused = False
        self.busy = False #flag denotes if a task is being processed

    def terminate(self):
        self.app.logger.info('Terminating QueueDaemon thread')
        self.stop = True
        self.task_queue.put(None)

    def run(self):
        self.app.logger.info('Initializing QueueDaemon run-loop')
        while not self.stop:
            self.app.logger.debug('Getting item from queue')
            package = self.task_queue.get(block=True,timeout=None)
            self.app.logger.debug('Got item from queue')

            # If the task object is None, break the queue-loop
            if package is None: #stop the queue execution
                self.terminate()
                break

            self.busy=True
            task = package['task']
            self.app.logger.info(f'Running task {task}')
            package['meta']['started'] = datetime.datetime.now().strftime('%H:%M:%S')
            self.running_task = [package]

            # pause queue but notify user of state every minute
            count = 600
            while self.paused: 
                time.sleep(0.1)
                count+=1
                if count>600:
                    self.app.logger.info('Queued is paused. Set paused state to false to continue execution')
                    count = 0

            #if debug_mode, pop and wait but don't execute
            if self.debug: 
                time.sleep(3.0)
            else:
                try:
                    self.driver.execute(**task)
                except Exception as error:
                    output_str  = f'Error: {error.__repr__()}\n\n'+traceback.format_exc()+'\n\n'
                    output_str += 'Exception encountered in driver, pausing queue...'
                    self.app.logger.error(output_str)
                    self.paused=True

            package['meta']['ended'] = datetime.datetime.now().strftime('%H:%M:%S')
            self.running_task = []
            self.history.append(package)
            self.busy = False
            time.sleep(0.1)

        self.app.logger.info('QueueDaemon runloop exiting')

    






