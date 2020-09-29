import os,sys,subprocess
from pathlib import Path

try:
        import NistoRoboto
except:
        sys.path.append(os.path.abspath(Path(__file__).parent.parent))
        print(f'Could not find NistoRoboto on system path, adding {os.path.abspath(Path(__file__).parent.parent)} to PYTHONPATH')

server_port=5000

from NistoRoboto.DeviceServer.DeviceServer import DeviceServer

from NistoRoboto.loading.PushPullSelectorSampleCell import PushPullSelectorSampleCell
from NistoRoboto.loading.NE1kSyringePump import NE1kSyringePump
from NistoRoboto.loading.ViciMultiposSelector import ViciMultiposSelector
from NistoRoboto.loading.Tubing import Tubing

selector = ViciMultiposSelector(
        '/dev/ttyFlowSel',
        baudrate=19200,
        portlabels={
            'catch':1,
            'cell':5,
            'waste':8,
            'rinse':9,
            'air':10,
            }
        )
pump = NE1kSyringePump('/dev/ttySyrPump',14.86,10,baud=19200,pumpid=10) # ID for 10mL = 14.859, for 50 mL 26.43
protocol = PushPullSelectorSampleCell(pump,
                                      selector,
                                      catch_to_sel_vol      =Tubing(1517,112).volume(),
                                      cell_to_sel_vol       =Tubing(1517,170).volume(),
                                      syringe_to_sel_vol    =None,
                                      selector_internal_vol =None,
                                     )
server = DeviceServer('SampleCellServer1')
server.add_standard_routes()
server.create_queue(protocol)
server.run(host='0.0.0.0',port=server_port, debug=False)

# process = subprocess.Popen(['/bin/bash','-c',f'chromium-browser --start-fullscreen http://localhost:{server_port}'])#, shell=True, stdout=subprocess.PIPE)
# 
# server.run_threaded(host='0.0.0.0', port=server_port, debug=False)
# 
# process.wait()
# 
# server._stop()
# server.join()
