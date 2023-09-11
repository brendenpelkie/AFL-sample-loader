# import win32com
# import win32com.client
# from win32process import SetProcessWorkingSetSize
# from win32api import GetCurrentProcessId,OpenProcess
# from win32con import PROCESS_ALL_ACCESS
import gc
# import pythoncom
import time
import datetime
from AFL.automation.APIServer.Driver import Driver
# from AFL.automation.instrument.ScatteringInstrument import ScatteringInstrument
# from AFL.automation.instrument.PySpecClient import PySpecClient
import numpy as np # for return types in get data
import h5py #for Nexus file writing
import os
import pathlib
import PIL
import uuid

from scatteringInterpolator import Scattering_generator
import gpflow
import tensorflow as tf
# class DummySAS(ScatteringInstrument,Driver):
class Virtual_SAS_data(Driver):
    defaults = {}
    def __init__(self,overrides=None, dataset=None):
        '''
        Generates smoothly interpolated scattering data via a noiseless GPR from an experiments netcdf file
        '''

        self.app = None
        Driver.__init__(self,name='SAS_Data_generator',defaults=self.gather_defaults(),overrides=overrides)
        # ScatteringInstrument.__init__(self)

        # this class uses the information in dataset, specifically 'SAS_savgol_xlo' and 'SAS_savgol_xhi' to determine the q range
        # it also points to the 'components' attribute of the dataset to get the composition range and dimensions
        # the dataset is stored in the scattering generator object
        self.sg = Scattering_generator(dataset=dataset)
        self.kernel = gpflow.kernels.Matern52(lengthscales=0.1,variance=1.)
        self.optimizer = tf.optimizers.Adam(learning_rate=0.005)
#    @Driver.quickbar(qb={'button_text':'Expose',
#        'params':{
#        'exposure':{'label':'time (s)','type':'float','default':'5'},
#        }})
    def expose(self,name=None,exposure=None,nexp=1,block=True,write_data=True,return_data=True,measure_transmission=True,save_nexus=True):
        ## sample_data is a protected key in the self.data dictionary from Driver.py
        ## composition, which is required to reproduce scattering data, has to be a parameter in the composition dictionary
        if 'sample_composition' not in self.data:
            return ValueError("'sample_composition' is not in self.data")
        
        ## subject to change when data structure is finalized
        if type(self.data['sample_composition']) == dict:
            X = np.array([self.data[component]['values'] for component in list(self.data)])
            components = list(self.data)
        elif type(self.data['sample_composition']) == list:
            X = np.array(self.data['sample_composition'])
        else:
            print('something went wrong on import')
            X = np.array([[1.5,7]])
        ## train the GP model if it has not been already
        if 'model' not in list (self.sg.__dict__):
            return ValueError("generate a model with the 'train_model' method")
        



        ### check that the units and the range of requested composition are within the dimensions of the scattering generator object

        ### predict from the model and add to the self.data dictionary
        self.data['q'] = self.sg.q
        mean, var = self.sg.generate_SAS(coords=X.T)
        self.data['scattering_mu'], self.data['scattering_var'] = mean.squeeze(), var.squeeze()
        self.data['X_*'] = X
        self.data['components'] = components

        data = np.stack((self.sg.q,mean.squeeze(),var.squeeze()),axis=1)


        
        ### write out the data to disk as a csv or h5?
        if write_data:
            self._writedata(data)
        
        if return_data:
            return self.data


    def status(self):
        status = ['Dummy SAS data']
        return status

    def train_model(self, kernel=None, niter=1000, optimizer=None, noiseless=True, tol=1e-6, heteroscedastic=False):
        ### Hyperparameter evaluation and model "training". Can consider augmenting these in a separate call.
        if kernel != None:
            self.kernel = kernel

        if optimizer != None:
            self.kernel = optimizer 
        
        
        self.sg.train_model(
            kernel          =  self.kernel,
            niter           =  niter,
            optimizer       =  self.optimizer,
            noiseless       =  noiseless,
            tol             =  tol,
            heteroscedastic =  heteroscedastic 
        )

    def _writedata(self,data):
        filename = pathlib.Path(self.config['filename'])
        filepath = pathlib.Path(self.config['filepath'])
        print(f'writing data to {filepath/filename}')
        data = np.array(data)
        with h5py.File(filepath/filename, 'w') as f:
            f.create_dataset(str(uuid.uuid1()), data=data)
        
        
