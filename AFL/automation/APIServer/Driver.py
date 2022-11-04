from AFL.automation.shared.utilities import listify
from AFL.automation.shared.PersistentConfig import PersistentConfig
from AFL.automation.shared import serialization
from math import ceil,sqrt
import inspect 
import pathlib

def makeRegistrar():
    functions = []
    decorator_kwargs = {}
    function_info = {}
    def registrarfactory(**kwargs):
        #print(f'Set up registrar-factory with registry {registry}...')
        def registrar(func):#,render_hint=None):  #kwarg = kwargs):
            functions.append(func.__name__)
            decorator_kwargs[func.__name__]=kwargs

            argspec = inspect.getfullargspec(func)
            if argspec.defaults is None:
                fargs = argspec.args
                fkwargs = []
            else:
                fargs = argspec.args[:-len(argspec.defaults)]
                fkwargs = [(i,j) for i,j in zip(argspec.args[-len(argspec.defaults):],argspec.defaults)]
            if fargs[0] == 'self':
                del fargs[0]
            function_info[func.__name__] = {'args':fargs,'kwargs':fkwargs,'doc':func.__doc__}
            if 'qb' in kwargs:
                function_info[func.__name__]['qb'] = kwargs['qb']
            return func  # normally a decorator returns a wrapped function, 
                         # but here we return func unmodified, after registering it
        return registrar
    registrarfactory.functions = functions
    registrarfactory.decorator_kwargs = decorator_kwargs
    registrarfactory.function_info = function_info
    return registrarfactory


class Driver:
    unqueued = makeRegistrar()
    queued = makeRegistrar()
    quickbar = makeRegistrar()
    def __init__(self,name,defaults=None,overrides=None):
        self.app = None
        if name is None:
            self.name = 'Driver'
        else:
            self.name = name
        
        self.path = pathlib.Path.home() / '.nistoroboto' 
        self.path.mkdir(exist_ok=True,parents=True)
        self.filepath = self.path / (name + '.config.json')
            
        self.config = PersistentConfig(
            path=self.filepath,
            defaults= defaults,
            overrides= overrides,
            )

    @classmethod
    def gather_defaults(cls):
        '''Gather all inherited static class-level dictionaries called default.'''

        defaults = {}
        for parent in cls.__mro__:
            if hasattr(parent,'defaults'):
                defaults.update(parent.defaults)
        return defaults
    
    def set_config(self,**kwargs):
        if ('driver' in kwargs) and (kwargs['driver'] is not None):
            driver_name = kwargs['driver']
            del kwargs['driver']

            try:
                driver_obj = getattr(self,driver_name)
            except AttributeError:
                raise ValueError(f'Driver \'{driver_name}\' not found in protocol \'{self.name}\'')

            driver_obj.config.update(kwargs)
        else:
            self.config.update(kwargs)

    def get_config(self,name,print_console=False):
        if ('driver' in kwargs) and (kwargs['driver'] is not None):
            driver_name = kwargs['driver']
            del kwargs['driver']

            try:
                driver_obj = getattr(self,driver_name)
            except AttributeError:
                raise ValueError(f'Driver \'{driver_name}\' not found in protocol \'{self.name}\'')

            value = driver_obj.config[name]
        else:
            value = self.config[name]

        if print_console:
            print(f'{name:30s} = {value}')

        return value

    def get_configs(self,driver=None,print_console=False):
        if driver is not None:
            try:
                driver_obj = getattr(self,driver_name)
            except AttributeError:
                raise ValueError(f'Driver \'{driver_name}\' not found in protocol \'{self.name}\'')
            config=driver_obj.config
        else:
            config = self.config

        if print_console:
            for name,value in config:
                print(f'{name:30s} = {value}')
        return config.config
        
    def status(self):
        status = []
        return status

    def pre_execute(self,**kwargs):
        '''Executed before each call to execute

           All of the kwargs passed to execute are also pass to this method. It
           is expected that this method be overridden by subclasses.
        '''
        pass

    def post_execute(self,**kwargs):
        '''Executed after each call to execute

           All of the kwargs passed to execute are also pass to this method. It
           is expected that this method be overridden by subclasses.
        '''
        pass

    def execute(self,**kwargs):
        task_name = kwargs.get('task_name',None)
        if task_name is None:
            raise ValueError('No name field in task. Don\'t know what to execute...')
        del kwargs['task_name']

        if 'device' in kwargs:
            device_name = kwargs['device']
            del kwargs['device']
            try:
                device_obj = getattr(self,device_name)
            except AttributeError:
                raise ValueError(f'Device \'{device_name}\' not found in protocol \'{self.name}\'')

            self.app.logger.info(f'Sending task \'{task_name}\' to device \'{device_name}\'!')
            return_val = getattr(device_obj,task_name)(**kwargs)
        else:
            return_val = getattr(self,task_name)(**kwargs)
        return return_val
    
    def set_object(self,serialized=True,**kw):
        for name,value in kw.items():
            self.app.logger.info(f'Sending object \'{name}\'')
            if serialized:
                value = serialization.deserialize(value)
            setattr(self,name,value)
    
    def get_object(self,name,serialize=True):
        value = getattr(self,name)
        self.app.logger.info(f'Getting object \'{name}\'')
        if serialize:
            value = serialization.serialize(value)
        return value


   
