from NistoRoboto.loading.FlowSelector import FlowSelector
from NistoRoboto.loading.SerialDevice import SerialDevice
from NistoRoboto.loading.ViciMultiPosSelector import ViciMultiPosSelector
import serial

class DoubleViciMultiposSelector(FlowSelector):
    def __init__(self,port1,port2,baudrate=9600,portlabels=None):
        '''
        connect to valve and query the number of positions

        parameters:
            port - string describing the serial port the actuator is connected to
            baud - baudrate to use
            portlabels - dict for smart port naming, of the form {'sample':3,'instrument':4,'rinse':5,'waste':6}
        '''

        self.app = None
        self.name = 'DoubleViciMultiPosSelector'

        portlabels1 = {k:v[0] for k,v in portlabels.items()}
        self.selector1 = ViciMultiPosSelector(port1,baudrate,portlabels)

        portlabels2 = {k:v[1] for k,v in portlabels.items()}
        self.selector2 = ViciMultiPosSelector(port2,baudrate,portlabels)

        self.portlabels = portlabels

        portnum = self.getPort()
        port = self.getPort(as_str=True)
        self.portString = f'{port}/{portnum}'

    def selectPort(self,port,direction=None):
        '''
            moves the selector to portnum

            if direction is set to either "CW" or "CCW" it moves the actuator in that direction.  
            if unset or other value, will move via most efficient route.

        '''
        if self.app is not None:
            self.app.logger.debug(f'Setting port to {port}')

        if type(port) is str:
            portnum1,portnum2 = self.portlabels[port]
        else:
            portnum1,portnum2 = int(port[0]),int(port[1])

        self.selector1.selectPort(portnum1,direction=direction)
        self.selector2.selectPort(portnum2,direction=direction)

        self.portString = f'{port}/{portnum1}/{portnum2}'

    def getPort(self,as_str=False):
        '''
            query the current selected position
        '''

        portnum1 = self.selector1.getPort(as_str=as_str)
        portnum2 = self.selector1.getPort(as_str=as_str)

        return portnum1,portnum2
                