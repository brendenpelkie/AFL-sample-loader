import opentrons.execute
import opentrons
from opentrons.protocol_api.labware import Labware
from NistoRoboto.APIServer.driver.Driver import Driver
from NistoRoboto.shared.utilities import listify
from math import ceil,sqrt
import os,json,pathlib

class OT2_Driver(Driver):
    def __init__(self):
        self.app = None
        self.name = 'OT2_Driver'
        self.protocol = opentrons.execute.get_protocol_api('2.0')
        self.prep_targets = []
        self.modules = {}
        self.min_transfer = 1e6
        self.max_transfer = -1e6

    def reset_prep_targets(self):
        self.prep_targets = []

    def add_prep_targets(self,targets,reset=False):
        if reset:
            self.reset_prep_targets()
        self.prep_targets.extend(targets)

    def get_prep_target(self):
        return self.prep_targets.pop(0)

    def status(self):
        status = []
        if len(self.prep_targets)>0:
                status.append(f'Next prep target: {self.prep_targets[0]}')
                status.append(f'Remaining prep targets: {len(self.prep_targets)}')
        else:
                status.append('No prep targets loaded')
        for k,v in self.protocol.loaded_instruments.items():
            aspirate = v.flow_rate.aspirate
            dispense = v.flow_rate.dispense
            flow_str = f' @ {aspirate}/{dispense} uL/s'
            status.append(str(v)+flow_str)
            status.append(f'Gantry Speed: {v.default_speed} mm/s')
        status.append(f'Min transfer: {self.min_transfer} uL')
        status.append(f'Max transfer: {self.max_transfer} uL')
        for k,v in self.protocol.loaded_labwares.items():
            status.append(str(v))
        return status
    
    def reset_tipracks(self,mount='both'):
        for k,pipette in self.protocol.loaded_instruments.items():
            if (mount.lower()=='both') or (k==mount.lower()):
                pipette.reset_tipracks()
                

    def reset(self):
        self.app.logger.info('Resetting the protocol context')

        raise NotImplementedError('This method doesn\'t work yet. For now, just restart the flask server')

        # opentrons.robot.reset() doesnt work

        # #XXX HACK! asyncio event loop finding borks without this
        # # self.app.logger.debug(opentrons.execute._HWCONTROL)
        # # del opentrons.execute._HWCONTROL
        # # opentrons.execute._HWCONTROL = None
        # self.app.logger.debug(opentrons.execute._HWCONTROL)

        # self.protocol = opentrons.execute.get_protocol_api('2.0')

    def home(self,**kwargs):
        self.app.logger.info('Homing the robot\'s axes')
        self.protocol.home()

    def parse_well(self,loc):
        for i,loc_part in enumerate(list(loc)):
            if loc_part.isalpha():
                break
        slot = loc[:i]
        well = loc[i:]
        return slot,well

    def get_wells(self,locs):
        self.app.logger.debug(f'Converting locations to well objects: {locs}')
        wells = []
        for loc in listify(locs):
            slot,well = self.parse_well(loc)
            labware = self.get_labware(slot)
            wells.append(labware[well])
        self.app.logger.debug(f'Created well objects: {wells}')
        return wells

    def get_labware(self,slot):
        self.app.logger.debug(f'Getting labware from slot \'{slot}\'')
        contents = self.protocol.deck[slot]
        if contents is not None:
            if type(contents) == opentrons.protocols.geometry.module_geometry.ModuleGeometry:
                labware = contents.labware
            else:
                labware = Labware(contents) #need Labware() to convert to public interface
            self.app.logger.debug(f'Found labware \'{labware}\'')
            return labware
        else:
            raise ValueError('Specified slot ({slot}) is empty of labware')


    def load_labware(self,name,slot,module=None,**kwargs):
        '''Load labware (containers,tipracks) into the protocol'''
        
        if self.protocol.deck[slot] is not None:
            try:
                if self.protocol.deck[slot].get_name() == name: #get_name() is part of the LabwareImplementation interface
                        self.app.logger.info(f'Labware \'{name}\' already loaded into slot \'{slot}\'.\n')
                        #do nothing
            except AttributeError:
                if self.protocol.deck[slot].labware.load_name == name:
                        self.app.logger.info(f'Labware \'{name}\' already loaded into module on slot \'{slot}\'/\n')
                        #do nothing
            else:
                raise RuntimeError(f'''Attempted to load labware \'{name}\' into slot \'{slot}\'.
                        Slot is already filled loaded with {self.protocol.deck[slot].get_display_name()}.''')
        else: 
            self.app.logger.debug(f'Loading labware \'{name}\' into slot \'{slot}\' into the protocol context')

        if module is not None:
            self.modules[slot] = self.protocol.load_module(module,slot)
            loadee = self.modules[slot]
        else:
            loadee = self.protocol

        try:
            loadee.load_labware(name,slot)
        except FileNotFoundError:
            CUSTOM_PATH = pathlib.Path(os.environ.get('NISTOROBOTO_CUSTOM_LABWARE'))
            with open(CUSTOM_PATH / name / '1.json') as f:
                labware_def = json.load(f)
            loadee.load_labware_from_definition(labware_def,slot)
            


    def set_temp(self,slot,temp):
        '''Set the temperature of a tempdeck in slot slot'''
        self.modules[slot].set_temperature(temp)
    
    def get_temp(self,slot):
        '''Get the temperature of a tempdeck in slot slot'''
        return (self.modules[slot].target,self.modules[slot].temperature)
    def deactivate_temp(self,slot):
        '''Disablea tempdeck in slot slot'''
        return self.modules[slot].deactivate()


    def load_instrument(self,name,mount,tip_rack_slots,**kwargs):
        '''Load a pipette into the protocol'''

        if mount in self.protocol.loaded_instruments:
            if self.protocol.loaded_instruments[mount].name == name:
                self.app.logger.info(f'Instrument \'{name}\' already loaded into mount \'{mount}\'.\n')
                #do nothing
            else:
                raise RuntimeError(f'''Attempted to load instrument \'{name}\' into mount \'{mount}\'.
                        mount is already loaded with {self.protocol.loaded_instruments[mount]}.''')
        else: 
            self.app.logger.debug(f'Loading pipette \'{name}\' into mount \'{mount}\' with tip_racks in slots {tip_rack_slots}')
            tip_racks = []
            for slot in listify(tip_rack_slots):
                tip_rack = Labware(self.protocol.deck[slot]) #need Labware() to convert from LabwareImplementation to public interface
                if not tip_rack.is_tiprack:
                    raise RuntimeError('Supplied slot doesn\'t contain a tip_rack!')
                tip_racks.append(tip_rack)
            self.protocol.load_instrument(name,mount,tip_racks=tip_racks)
            
        for mount,pipette in self.protocol.loaded_instruments.items():
            self.min_transfer = min(self.min_transfer,pipette.min_volume)
            self.max_transfer = max(self.max_transfer,pipette.max_volume)

    def mix(self,volume, location, repetitions=1,**kwargs):
        self.app.logger.info(f'Mixing {volume}uL {repetitions} times at {location}')

        #get pipette based on volume
        pipette = self.get_pipette(volume)

        #modify source well dispense location
        location_well = self.get_wells(location)[0]

        pipette.mix(repetitions,volume,location_well)

    def transfer(self,source,dest,volume,mix_before=None,mix_after=None,air_gap=0,aspirate_rate=None,dispense_rate=None,blow_out=False,post_aspirate_delay=0.0,post_dispense_delay=0.0,**kwargs):
        '''Transfer fluid from one location to another

        Arguments
        ---------
        source: str 
            Source well to transfer from. Wells should be specified as three
            character strings with the first character being the slot number.

        dest: str 
            Destination well to transfer to. Wells should be specified as
            three character strings with the first character being the slot
            number.

        volume: float
            volume of fluid to transfer

        '''
        self.app.logger.info(f'Transfering {volume}uL from {source} to {dest}')

        if aspirate_rate is not None:
            self.set_aspirate_rate(aspirate_rate)

        if dispense_rate is not None:
            self.set_dispense_rate(dispense_rate)

        #get source well object
        source_wells = self.get_wells(source)
        if len(source_wells)>1:
            raise ValueError('Transfer only accepts one source well at a time!')
        else:
            source_well = source_wells[0]

        #get dest well object
        dest_wells = self.get_wells(dest)
        if len(dest_wells)>1:
            raise ValueError('Transfer only accepts one dest well at a time!')
        else:
            dest_well = dest_wells[0]
            
        
        transfers = self.split_up_transfers(volume)
        for sub_volume in transfers:
            #get pipette based on volume
            pipette = self.get_pipette(sub_volume)
    
            self._transfer(
                    pipette, 
                    sub_volume, 
                    source_well, 
                    dest_well, 
                    mix_before=mix_before, 
                    mix_after=mix_after, 
                    air_gap=air_gap, 
                    blow_out=blow_out, 
                    post_aspirate_delay=post_aspirate_delay, 
                    post_dispense_delay=post_dispense_delay)
        
    def split_up_transfers(self,vol):
        transfers = []
        while True:
            if sum(transfers)<vol:
                transfer = min(self.max_transfer,vol-sum(transfers))
                if transfer<self.min_transfer and (len(transfers)>0) and (transfers[-1]>=(2*(self.min_transfer))):
                    transfers[-1]-=(self.min_transfer-transfer)
                    transfer = self.min_transfer
                
                transfers.append(transfer)
            else:
                break
        return transfers
        
    def _transfer( 
            self,
            pipette,
            volume, 
            source_well, 
            dest_well, 
            mix_before=None, 
            mix_after=None, 
            air_gap=0, 
            blow_out=False,
            post_aspirate_delay=0.0,
            post_dispense_delay=0.0):
                      
        if blow_out:
            raise NotImplemented()        
    
        pipette.pick_up_tip()
        
        #need to mix before final aspirate
        if mix_before is not None:
            nmixes,mix_volume = mix_before
            for _ in range(nmixes):
                pipette.aspirate(mix_volume,location=source_well)
                pipette.dispense(mix_volume,location=source_well)        
        pipette.aspirate(volume+air_gap,location=source_well)
        
        if post_aspirate_delay>0.0:
            pipette.move_to(source_well.top())
            self.protocol.delay(seconds=post_aspirate_delay)
        
        # need to dispense before  mixing
        pipette.dispense(volume+air_gap,location=dest_well)
        if mix_after is not None:
            nmixes,mix_volume = mix_after
            for _ in range(nmixes):
                pipette.aspirate(mix_volume,location=dest_well)
                pipette.dispense(mix_volume,location=dest_well)  
                
        if post_dispense_delay>0.0:
            pipette.move_to(dest_well.top())
            self.protocol.delay(seconds=post_dispense_delay)
    
        pipette.drop_tip(self.protocol.deck[12]['A1'])
        
    
    def set_aspirate_rate(self,rate=150):
        '''Set aspirate rate of both pipettes in uL/s. Default is 150 uL/s'''
        for mount,pipette in self.protocol.loaded_instruments.items():
            pipette.flow_rate.aspirate = rate

    def set_dispense_rate(self,rate=300):
        '''Set dispense rate of both pipettes in uL/s. Default is 300 uL/s'''
        for mount,pipette in self.protocol.loaded_instruments.items():
            pipette.flow_rate.dispense = rate

    def set_gantry_speed(self,speed=400):
        '''Set movement speed of gantry. Default is 400 mm/s'''
        for mount,pipette in self.protocol.loaded_instruments.items():
            pipette.default_speed = speed

    def get_pipette(self,volume,method='min_transfers'):
        self.app.logger.debug(f'Looking for a pipette for volume {volume}')

        pipettes = []
        minVolStr = ''
        for mount,pipette in self.protocol.loaded_instruments.items():
            if volume>=pipette.min_volume:
                pipettes.append({'object':pipette})
    

        for pipette in pipettes:
            max_volume = pipette['object'].max_volume
            ntransfers = ceil(volume/max_volume)
            vol_per_transfer = volume / ntransfers
            
            pipette['ntransfers'] = ntransfers

            # **Peter** personally apologizes for these impressively long lines,
            # which he believes to be correct.  The systematic error is added
            # straight (i.e, not sumsq) while the random is added as sumsq,
            # then the two are combined as sumsq 
            pipette['uncertainty'] = sqrt(
                (ntransfers*self._pipette_uncertainty(max_volume,vol_per_transfer,'random')**2)+
                (ntransfers*self._pipette_uncertainty(max_volume,vol_per_transfer,'systematic'))**2
            )

            # last_transfer_vol_maxmin = volume - max_volume*(ntransfers-1)
            # pipette['total_uncertainty_maxmin'] = sqrt(
            #     (ntransfers-1*_pipette_uncertainty(max_volume,max_volume,'random')**2+ 
            #     _pipette_uncertainty(max_volume,last_transfer_vol_maxmin,'random')**2)+
            #     ((ntransfers-1)*_pipette_uncertainty(max_volume,vol_per_transfer,'systematic')+
            #     _pipette_uncertainty(max_volume,last_transfer_vol_maxmin,'systematic')**2)
            #     )


        self.app.logger.debug(f'Found pipettes with suitable minimum volume and computed uncertainties: {pipettes}')
        if not pipettes:
            raise ValueError('No suitable pipettes found!\n')
        
        if(method == 'uncertainty'):
            pipette = min(pipettes,key=lambda x: x['uncertainty'])
        elif(method == 'min_transfers'):
            min_xfers = min(pipettes,key=lambda x: x['ntransfers'])['ntransfers']
            acceptable_pipettes = filter(lambda x: x['ntransfers']==min_xfers,pipettes)
            pipette = min(acceptable_pipettes,key=lambda x: x['object'].max_volume) 
        else:
            raise ValueError(f'Pipette selection method {method} was not recognized.')
        self.app.logger.debug(f'Chosen pipette: {pipette}')
        return pipette['object']

    def _pipette_uncertainty(self,maxvolume,volume,errortype):
        '''pipet uncertainties from the opentrons gen 1 whitepaper 
        @ https://opentrons.com/publications/OT-2-Pipette-White-Paper-GEN1.pdf
        
        pipette          moving uL      random error uL ±     systematic error uL ±
        P10 single          10                  0.1                 0.2
        P10 single          5                   0.15                0.25
        P10 single          1                   0.05                0.15

        P50 single          50                  0.2                 0.5
        P50 single          25                  0.15                0.375
        P50 single          5                   0.25                0.25

        P300 single         300                 0.9                 1.8
        P300 single         150                 0.6                 1.5
        P300 single         30                  0.45                0.9

        P1000 single        1000                1.5                 7
        P1000 single        500                 1.0                 5
        P1000 single        100                 1.0                 2
        '''
        #dict of uncertainty data where params are  error = a * volume + b
        pipette_uncertainties = [
        {'size':10,  'gen':1,'random_a':0.00491803278688525,  'random_b':0.0737704918032787,'systematic_a':0.00491803278688525,'systematic_b':0.173770491803279},
        {'size':50,  'gen':1,'random_a':-0.000983606557377049,'random_b':0.226229508196721, 'systematic_a':0.0055327868852459, 'systematic_b':0.227459016393443},
        {'size':300, 'gen':1,'random_a':0.00168032786885246,  'random_b':0.381147540983607, 'systematic_a':0.00327868852459016,'systematic_b':0.875409836065574},
        {'size':1000,'gen':1,'random_a':0.000573770491803279, 'random_b':0.860655737704918, 'systematic_a':0.00549180327868852,'systematic_b':1.73770491803279}
        ]

        for pu in pipette_uncertainties:
            if pu['size'] == maxvolume:
                #I think sum squares is the correct way to combine these errors, but not 100%
                if errortype == 'random':
                    return pu['random_a'] * volume + pu['random_b']
                elif errortype == 'systematic':
                    return pu['systematic_a'] * volume + pu['systematic_b']
                else:
                    return None


   
