import json
from opentrons import robot, labware, instruments

CALIBRATION_CROSS_COORDS = [380.87, 9.0, 0.0]
CALIBRATION_CROSS_SLOT = '3'
TEST_LABWARE_SLOT = CALIBRATION_CROSS_SLOT
TIPRACK_SLOT = '5'

RATE = 0.25  # % of default speeds
SLOWER_RATE = 0.1


def uniq(l):
    res = []
    for i in l:
        if i not in res:
            res.append(i)
    return res


def set_speed(rate):
    robot.head_speed(x=(600 * rate), y=(400 * rate),
                      z=(125 * rate), a=(125 * rate))


def run_custom_protocol(pipette_name, mount, tiprack_load_name, labware_def):
    tiprack = labware.load(tiprack_load_name, TIPRACK_SLOT)
    pipette = getattr(instruments, pipette_name)(mount, tip_racks=[tiprack])
    test_labware = robot.add_container_by_definition(
        labware_def,
        TEST_LABWARE_SLOT,
        label=labware_def.get('metadata', {}).get(
            'displayName', 'test labware')
    )

    num_cols = len(labware_def.get('ordering', [[]]))
    num_rows = len(labware_def.get('ordering', [[]])[0])
    well_locs = uniq([
        'A1',
        '{}{}'.format(chr(ord('A') + num_rows - 1), str(num_cols))])

    pipette.pick_up_tip()
    set_speed(RATE)

    pipette.move_to((robot.deck, CALIBRATION_CROSS_COORDS))
    robot.pause(
        f"Confirm {mount} pipette is at slot {CALIBRATION_CROSS_SLOT} calibration cross")

    pipette.retract()
    robot.pause(f"Place your labware in Slot {TEST_LABWARE_SLOT}")

    for well_loc in well_locs:
        well = test_labware.wells(well_loc)
        all_4_edges = [
            [well.from_center(x=-1, y=0, z=1), 'left'],
            [well.from_center(x=1, y=0, z=1), 'right'],
            [well.from_center(x=0, y=-1, z=1), 'front'],
            [well.from_center(x=0, y=1, z=1), 'back']
        ]

        set_speed(RATE)
        pipette.move_to(well.top())
        robot.pause("Moved to the top of the well")

        for edge_pos, edge_name in all_4_edges:
            set_speed(SLOWER_RATE)
            pipette.move_to((well, edge_pos))
            robot.pause(f'Moved to {edge_name} edge')

        set_speed(RATE)
        pipette.move_to(well.bottom())
        robot.pause("Moved to the bottom of the well")

        # need to interact with labware for it to show on deck map
        pipette.blow_out(well)


    set_speed(1.0)
    pipette.return_tip()


LABWARE_DEF = """{"ordering":[["A1","B1"],["A2","B2"],["A3","B3"]],"brand":{"brand":"NIST","brandId":["gvh2"]},"metadata":{"displayName":"NIST 6 x 20 mL vial holder","displayCategory":"wellPlate","displayVolumeUnits":"µL","tags":[]},"dimensions":{"xDimension":127.75,"yDimension":85.5,"zDimension":62.6},"wells":{"A1":{"depth":56.5,"totalLiquidVolume":20000,"shape":"circular","diameter":28.95,"x":23,"y":62.5,"z":6.1},"B1":{"depth":56.5,"totalLiquidVolume":20000,"shape":"circular","diameter":28.95,"x":23,"y":22.37,"z":6.1},"A2":{"depth":56.5,"totalLiquidVolume":20000,"shape":"circular","diameter":28.95,"x":63.13,"y":62.5,"z":6.1},"B2":{"depth":56.5,"totalLiquidVolume":20000,"shape":"circular","diameter":28.95,"x":63.13,"y":22.37,"z":6.1},"A3":{"depth":56.5,"totalLiquidVolume":20000,"shape":"circular","diameter":28.95,"x":103.26,"y":62.5,"z":6.1},"B3":{"depth":56.5,"totalLiquidVolume":20000,"shape":"circular","diameter":28.95,"x":103.26,"y":22.37,"z":6.1}},"groups":[{"metadata":{"displayName":"NIST 6 x 20 mL vial holder","displayCategory":"wellPlate","wellBottomShape":"flat"},"brand":{"brand":"NIST","brandId":["gvh2"]},"wells":["A1","B1","A2","B2","A3","B3"]}],"parameters":{"format":"irregular","quirks":[],"isTiprack":false,"isMagneticModuleCompatible":false,"loadName":"nist_6_20ml_vials"},"namespace":"custom_beta","version":1,"schemaVersion":2,"cornerOffsetFromSlot":{"x":0,"y":0,"z":0}}"""

PIPETTE_MOUNT = 'right'
PIPETTE_NAME = 'P1000_Single'
TIPRACK_LOADNAME = 'opentrons_96_tiprack_1000ul'

run_custom_protocol(PIPETTE_NAME, PIPETTE_MOUNT,
                    TIPRACK_LOADNAME, json.loads(LABWARE_DEF))
