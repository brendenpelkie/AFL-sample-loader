from labjack import ljm

from AFL.automation.loading.Sensor import Sensor
import time

class LabJackSensor(Sensor):
    def __init__(self,devicetype="ANY",connection="ANY",deviceident="ANY",port_to_read="AIN0",polling_rate=200):
        '''
    	Initialize a LabJack connection
    	
    	Params:
    	
    	devicetype (str): series/type of LJ to connect to "T4" "T7" etc.
    	connection (str): "ANY", "USB", "TCP", "ETHERNET", or "WIFI"
    	deviceident (str): serial number OR IP OR device name OR "ANY"
    	port_to_read (str): LabJack port for device
        '''
        self.device_handle = ljm.openS(devicetype, connection, deviceident)
        self.port_to_read = port_to_read
        self.intervalHandle = 0
        ljm.startInterval(self.intervalHandle, polling_rate)
        ljm.eWriteName(self.device_handle,"DIO6",1)#set physical FIO6 / logical DIO6 to TTL-hi
    
    def __del__(self):
    	ljm.close(self.device_handle)
    	
    def calibrate(self):
        ljm.eWriteName(self.device_handle,"DIO6",0)
        time.sleep(0.2)
        ljm.eWriteName(self.device_handle,"DIO6",1)
        
    def read(self):
        numSkippedIntervals = ljm.waitForNextInterval(self.intervalHandle)
        result = ljm.eReadName(self.device_handle, self.port_to_read)
        return result
    
    def __str__(self):
        info = ljm.getHandleInfo(self.device_handle)
        return f"LabJack with Device type: %{info[0]}, Connection type: {info[1]}, Serial number: {info[2]}, IP address: {ljm.numberToIP(info[3])}, Port: {info[4]}, Max bytes per MB: {info[5]}"
        
