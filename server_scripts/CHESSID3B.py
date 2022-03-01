import os,sys,subprocess
from pathlib import Path
try:
        import NistoRoboto
except:
        sys.path.append(os.path.abspath(Path(__file__).parent.parent))
        print(f'Could not find NistoRoboto on system path, adding {os.path.abspath(Path(__file__).parent.parent)} to PYTHONPATH')

from NistoRoboto.APIServer.APIServer import APIServer
from NistoRoboto.instrument.CHESSID3B import CHESSID3B

server_port=5000

driver = CHESSID3B()
server = APIServer('CHESSID3B',contact='pab2@nist.gov')
server.add_standard_routes()

server.create_queue(driver)
#server.add_unqueued_routes()
server.init_logging(toaddrs=['tbm@nist.gov','pab@nist.gov'])

#process = subprocess.Popen(['/bin/bash','-c',f'chromium-browser --start-fullscreen http://localhost:{server_port}'])#, shell=True, stdout=subprocess.PIPE)

server.run(host='0.0.0.0', port=server_port, debug=False)#,threaded=False)

#process.wait()

#server._stop()
#server.join()
