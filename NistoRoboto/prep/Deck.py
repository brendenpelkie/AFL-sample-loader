import numpy as np
from NistoRoboto.prep.Mixture import Mixture
from NistoRoboto.prep.PipetteAction import PipetteAction

get_pipette='''
def get_pipette(volume,loaded_pipettes):
    found_pipettes = []
    minVol = ''
    for pipette in loaded_pipettes:
        minVol += f'{pipette.min_volume}>{volume}\\n'
        if volume>pipette.min_volume:
            found_pipettes.append(pipette)

    if not found_pipettes:
        raise ValueError('No suitable pipettes found!\\n'+ minVol)
    else:
        return min(found_pipettes,key=lambda x: x.max_volume)
'''

metadata = '''
metadata = {
    'protocolName': 'Alignment',
    'author': 'NistoRoboto',
    'description': 'Script for aligning and testing',
    'apiLevel': '2.0'
}
'''


class Deck:
    def __init__(self):
        self.stocks        = []
        self.targets       = []
        self.stock_location = {}
        self.target_location = {}
        
        self.components        = set()
        self.components_stock  = set()
        self.components_target = set()
        
        self.protocol = []

        self.tip_racks    = {}
        self.containers    = {}
        self.pipettes      = {}

        self.client = None

    def init_remote_connection(self,url):
        from NistoRoboto.server.Client import Client
        self.client = Client(url)
        self.client.login('NistoRobotoDeck')

    def send_protocol(self,debug_mode=False):
        if not self.protocol:
            raise ValueError('No protocol to send. Did you call make_protocol()?')

        if self.client is None:
            raise ValueError('Need to call \'init_remote_connection\' before sending protocol')

        if not self.client.logged_in():
            # just re-login
            self.client.login('NistoRobotoDeck')

        self.client.set_queue_mode(debug_mode=debug_mode)#unlock the queue

        for slot,tip_rack in self.tip_racks.items():
            self.client.load_labware(tip_rack,slot)

        for slot,container in self.containers.items():
            self.client.load_labware(container,slot)

        for mount,(pipette,tip_rack_slots) in self.pipettes.items():
            self.client.load_instrument(pipette,mount,tip_rack_slots)

        self.client.home()# must home robot before sending commands
        for task in self.protocol:
            kw = task.get_kwargs()
            self.client.transfer(**kw)

    def add_pipette(self,name,mount,tipracks):
        if not (mount in ['left','right']):
            raise ValueError('Pipette mount point can only be "left" or "right"')

        tiprack_list = []
        for slot,rack_name in tipracks:
            self.tip_racks[slot] = rack_name
            tiprack_list.append(slot)

        self.pipettes[mount] = name,tiprack_list

    def add_container(self,name,slot):
        self.containers[slot] = name

    def add_stock(self,stock,location):
        stock = stock.copy()
        self.stocks.append(stock)
        self.stock_location[stock] = location
        
        for name,component in stock:
            self.components.add(name)
            self.components_stock.add(name)
            
    def add_target(self,target,location):
        target = target.copy()
        self.targets.append(target)
        self.target_location[target] = location
        
        for name,component in target:
            self.components.add(name)
            self.components_target.add(name)
            
    def make_protocol(self):
        for target in self.targets:
            
            # build matrix and vector representing mass balance
            mass_fraction_matrix = []
            target_component_masses = []
            for name in self.components:
                row = []
                for stock in self.stocks:
                    if name in stock.components:
                        if stock[name]._has_mass:
                            row.append(stock.mass_fraction[name])
                        else:
                            raise ValueError('Need masses specified for mass balance')
                    else:
                        row.append(0)
                mass_fraction_matrix.append(row)
                
                if name in target.components:
                    if target[name]._has_mass:
                        target_component_masses.append(target[name].mass)
                    else:
                        raise ValueError('Need masses specified for mass balance')
                else:
                    target_component_masses.append(0)

            #solve mass balance 
            mass_transfers,residuals,rank,singularity = np.linalg.lstsq(mass_fraction_matrix,target_component_masses,rcond=-1)
            
            #apply mass balance
            target_check = Mixture()
            for stock,mass in zip(self.stocks,mass_transfers):
                if mass>0:
                    removed = stock.remove_mass(mass)
                    target_check = target_check + removed
                    
                    action = PipetteAction(
                                source = self.stock_location[stock],
                                dest = self.target_location[target],
                                volume = removed.volume*1000 #assume ml for now
                                
                    )
                    self.protocol.append(action)
                    
            if not (target == target_check):
                raise RuntimeError('Mass transfer calculation failed...')

    def make_script(self,filename):
        with open(filename,'w') as f:
            f.write('from opentrons import protocol_api\n')
            f.write('\n')
            f.write('\n')
            #f.write('metadata={\'apiLevel\':\'2.0\'}\n')
            f.write(metadata)
            f.write('\n')
            f.write('\n')
            f.write(get_pipette)
            f.write('\n')
            f.write('\n')
            f.write('def run(protocol):\n')

            
            f.write(' '*4+ 'deck={}\n')
            f.write('\n')
            for slot,tiprack in self.tip_racks.items():
                f.write(' '*4+ f'tiprack_{slot} = protocol.load_labware(\'{tiprack}\',\'{slot}\')\n')
                f.write(' '*4+ f'deck[{slot}] = tiprack_{slot}\n')
            f.write('\n')

            for slot,container in self.containers.items():
                f.write(' '*4 + f'container_{slot} = protocol.load_labware(\'{container}\',\'{slot}\')\n')
                f.write(' '*4+ f'deck[{slot}] = container_{slot}\n')
            f.write('\n')

            f.write(' '*4 + 'pipettes = []\n')
            for mount,(pipette,tip_rack_slots) in self.pipettes.items():
                
                f.write(' '*4 + f'tip_racks = []\n')
                f.write(' '*4 + f'for slot in {tip_rack_slots}:\n')
                f.write(' '*8 + f'tip_racks.append(protocol.deck[slot])\n')
                f.write(' '*4 + f'pipette_{mount} = protocol.load_instrument(\'{pipette}\',\'{mount}\',tip_racks=tip_racks)\n')
                f.write(' '*4 + f'pipettes.append(pipette_{mount})\n')
                f.write(' '*4 + '\n')
            f.write('\n')

            if not self.protocol:
                return

            for action in self.protocol:
                f.write(' '*4 + f'pipette = get_pipette({action.volume},pipettes)\n')
                f.write(' '*4 + f'well_source = container_{action.source[0]}[\'{action.source[1:]}\']\n')
                f.write(' '*4 + f'well_dest = container_{action.dest[0]}[\'{action.dest[1:]}\']\n')
                f.write(' '*4 + f'pipette.transfer({action.volume},well_source,well_dest)\n')
                f.write('\n')

