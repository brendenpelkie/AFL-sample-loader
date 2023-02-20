import threading
import time
import datetime
import sys
import traceback
import json
import pathlib
from AFL.automation.shared.serialization import is_serialized


class QueueDaemon(threading.Thread):
    '''
    '''

    def __init__(self, app, driver, task_queue, history, debug=False):
        app.logger.info('Creating QueueDaemon thread')

        threading.Thread.__init__(self, name='QueueDaemon', daemon=True)

        self.driver = driver

        self.app = app
        self.task_queue = task_queue
        self.history = history #history local to this server restart
        self.running_task = []

        self.stop = False
        self.debug = debug
        self.paused = False
        self.busy = False  # flag denotes if a task is being processed


        self.history_log_path = pathlib.Path.home() / '.afl' / f'{driver.name}.history'
        try:
            # try to load all previous history if available
            with open(self.history_log_path,'r') as f:
                self.history_log = json.load(f)
        except FileNotFoundError:
            self.history_log = []


    def terminate(self):
        self.app.logger.info('Terminating QueueDaemon thread')
        self.stop = True
        self.task_queue.put(None)
        
    def check_if_paused(self):
        # pause queue but notify user of state every minute
        count = 600
        while self.paused:
            time.sleep(0.1)
            count+=1
            if count>600:
                self.app.logger.info((
                    'Queued is paused. '
                    'Set paused state to false to continue execution'
                ))
                count = 0

    def mask_serialized_objs(self,package):
        masked_package = {'task':{}}
        if 'meta' in package:
            masked_package['meta'] = package['meta']
        if 'uuid' in package:
            masked_package['uuid'] = str(package['uuid'])

        for k,v in package['task'].items():
            if is_serialized(v):
                masked_package['task'][k] = 'serialized_object'
            else:
                masked_package['task'][k] = v
        return masked_package
        

    def run(self):
        self.app.logger.info('Initializing QueueDaemon run-loop')
        while not self.stop:
            self.check_if_paused()

            self.app.logger.debug('Getting item from queue')
            package = self.task_queue.get(block=True, timeout=None)
            self.app.logger.debug('Got item from queue')
            
            # If the task object is None, break the queue-loop
            if package is None:  # stop the queue execution
                self.terminate()
                break

            self.busy = True
            task = package['task']
            self.app.logger.info(f'Running task {task}')
            start_time = datetime.datetime.now()
            masked_package = self.mask_serialized_objs(package)
            #masked_package['meta']['started'] = start_time.strftime('%H:%M:%S')
            masked_package['meta']['started'] = start_time.strftime('%m/%d/%y %H:%M:%S-%f %Z%z')
            self.running_task = [masked_package]
            
            self.check_if_paused()

            # if debug_mode, pop and wait but don't execute
            if self.debug:
                time.sleep(3.0)
                return_val = None
                exit_state = 'Debug Mode!'
            else:

                try:
                    self.driver.pre_execute(**task)
                    return_val = self.driver.execute(**task)
                    self.driver.post_execute(**task)
                    exit_state = 'Success!'
                except Exception as error:
                    return_val = f'Error: {error.__repr__()}\n\n' + traceback.format_exc() + '\n\n'
                    return_val += 'Exception encountered in driver.execute, pausing queue...'
                    exit_state = 'Error!'
                    self.app.logger.error(return_val)
                    self.paused = True

            end_time = datetime.datetime.now()
            run_time = end_time - start_time
            masked_package['meta']['ended'] = end_time.strftime('%m/%d/%y %H:%M:%S-%f %Z%z')
            masked_package['meta']['run_time_seconds'] = run_time.seconds
            masked_package['meta']['run_time_minutes'] = run_time.seconds/60
            masked_package['meta']['exit_state'] = exit_state
            masked_package['meta']['return_val'] = return_val
            masked_package['uuid'] = str(masked_package['uuid'])
            self.running_task = []
            self.history.append(masked_package)#history for this server restart
            self.history_log.append(masked_package)#hopefull **all** history
            with open(self.history_log_path,'w') as f:
                json.dump(self.history_log,f,indent=4)

            self.busy = False
            time.sleep(0.1)

        self.app.logger.info('QueueDaemon runloop exiting')
