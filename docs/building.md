# Build guide

This is a build guide for the Pozzo lab fork of the NIST AFL system. This is how we built it and may not be the way the original NIST designers have built it. In case of conflict, go with the NIST version

## Parts list

- Frame parts:
    - extrusion parts
    - some brackets
    - Piece of acrylic to cut a panel out of

Electronics:
- Raspberry Pi
- Relay plate
- power distribution block
- 24 V power supply. Note ours is kinda sketchy - go with something NRTL listed if you want people to sign off on it
- Labjack. Note you can probably get away with using something else (read cheaper) here, like just using the RPi potentially
- Power entry module
- Bubble sensor
- Various wiring and M12 connectors for panel connections

Pneumatic components:
- 2x static regulators
- digital regulators
- 5/2 valve
- solenoid valves
- 1/4" tubing
- brukert release valve for arm
- PRV valves


Fluidic components:
- Box of 1/4-28 fittings
- 1/8" OD and 1/16" OD PTFE tubing
- check valves
- Pressure plus bottles and caps
- panel pass through fittings

Custom fabricated components:
- Catch and piston

Printed parts:
- Catch mount base thing
- Compute control module thing
- PEM housing
- Various frame brackets
- rinse bottle holders
- 5/2 valve holder


## Build guide:

### Build the frame
The frame is assembled from the extrusion pieces and the corner braces. Assemble it so it is 24" "tall" x 22" "wide" by 4 1/4" "deep". Don't put any brackets on the bottom.

![frame](frame.JPEG)


### Wire solenoid valves

We suggest wiring the solenoid valves with a quick-connect connector of your choice to make the rest of assembly and travel easier. Connect the male plug end of your quick connector to the supplied solenoid wiring if the valve came with wires. For the 5/2 valve for the clamp arm, you will need to add wires by removing the screws on the wire caps, removing the caps, and adding wires to the terminals. For the Burkert whisper valve for the piston vent, you will need to either wire your own lead using the specified connectors or buy a cable along with the valve. The Burkert valve mounts to the Jubilee-mounted catch assembly, so make sure the wire for this is long enough to reach. For this valve, pay attention to wiring polarity. Also wire yourself a ~48" connector 'extension' for each valve. Terminate one end of this extension with the female socket of your quick connector and leave the other end unterminated. Use red and black wire for this. All the wire pairs should be a single cable, so either use dual-conductor wire or place both strands in some sort of sheathing like the one suggested in the BOM. At this point, it is a good idea to label every valve. 

| Label | AFL internal name |Valve type | Relay plate number | 
| --- | ---| --- | 
| Sample Hold | 'postsample' Mini solenoid cylinder | 1|
| Vent | 'piston-vent' | Burkert whisper | 2 |
| Sample push | 'blow' | Mini solenoid cylinder | 3 |
| Rinse 2 | 'rinse2' | Mini solenoid cylinder | 4 |
| Rinse 1 | 'rinse1' | Mini solenoid cylinder | 5|
| Arm up | 'arm-up' | 5/2 valve A | 6 |
| Arm down | 'arm-down' | 5/2 valve B | 7 | 


![valve wiring](valvewire.JPEG)

![wire extension](wireextension.JPEG)

### Wire the compute control box

This is a rats nest. This box contains the raspberry pi that controls everything, the PiPlates relayplate that actuates the pneumatics, and power wiring. It is easiest to route all the wires into the box where they need to go, but keep the power distribution block and relay plate loose (don't screw them down yet). Make sure everything will still fit/wires reach/etc once it goes in the box. 


1. Connect a red wire to one of the 'A' terminals on the end of the power distribution block, and a black wire to one of the 'B' blocks. These will be the +24v and ground from your power supply.

2. For each of the 7 solenoid valves you need to: 
    1. Connect an 'A' terminal from the power distribution block to the relay terminal.
    2. connect the red wire from your valve extension wire from above to the other terminal of the relay.
    3. Connect the black wire from the valve extension to the corresponding 'B' terminal on the power distribution block.

![wiring the box](controlboxwiring.png)

3. Now screw everything down to the box using M3 (? maybe 2.5?) screws.

4. Mount the raspberry pi to the standoffs on the lid.

5. Use the raspberry pi female-female ribbon cable to connect the pi to the relay plate, minding the orientation as shown here. 

![pi relay connect](pi_relayplate_connect.JPEG)

### Mount connectors to valves

Mount the connectos to the valves as described in the main pneumatic connections figure. Use teflon tape to prevent leaks on NPT connectors.

### Physically mount everything to the frame



Mounte everything to the frame using the 3D printed mounts and brackets. The specific arrangement isn't critical as long as everything clears. Pay attention to which side your panel is going to be on if you are using one - make sure to put the 90* elbow connectors on that side. 


### Make electronic connections

Wire everything up as described in electronic connections

### Make pneumatic and fluidic connections

### Assemble front panel

### Assemble catch assembly

1. Drill and tap M5 holes in Jubilee deck on slot 1 for catch, using the catch block as a template. If you are using the original lab automation deck template, you will also need to remove some material from the back edge. The modified AFL automation deck template does not have this material. 

2. Connect the 1/4" OD x NPT ? push to connect fittings to the clamp. 

3. Mount the clamp to the catch base using the 5/32 x 3" screws. Use washers and assembly lube.

4. Loosely mount the piston to the catch arm by assembling the hardware stack as shown in the picture. The 1/4-20 screw threads into the top of the piston, washers are used to space the piston down from the arm, and a washer and 2 nuts are used on top of the arm to tighten down the assembly. Leave this loose as the number of washers between the arm and the piston may need adjusting. 

5. Mount a sufficiently long amount of 1/16" OD tubing to reach your flow cell to the bottom of the catch, using a 1/4-28 fitting. Be extremely careful not to cross-thread the soft HDPE threads. 

6. Connect a short piece of tubing between the piston and the normally closed port of the whisper valve, using 1/4-28 fittings.

7. Mount the piston arm to the clamp, aligning it so that it is lined up with the catch when closing.

8. Fine tune the washer stack for the piston so that the piston just clears the rim of the catch when the clamp swings over it. 


- Wire up all your valves using quick-connectors of your choice. This will make assembly and travel easier
- Mount the power components: PSU, PEM. Wire this up. Don't kill yourself here.
- Wire up the solenoid valves. This box will be a mess
- Mount appropriate fittings onto the solenoid valves
- Mount the solenoid valves to the frame
- Make your front panel, if using (not strictly necessary). This is done by measure and manually with a table saw and a drill press
- make all the tubing connections
- Wire up the labjack with regulator out and bubble sensor in things
- Assemble the catch arm
    - If using Jubilee, punch some holes in Jubilee deck to screw this down

- Connection diagram in powerpoint showing how everything fits together
- Some pictures of assembled things



## Provision Pi

- Set up networking
- Install labjack control software
- Set up a venv for afl server
- Clone and install this repo

## Connect everything

## Bring up the control server

- launch with Flask
- Connect through GUI: 
    - have some screenshots on how to do this

- Connect over HTTP:
    - Include a notebook and example requests to log in 

## Rinse cell

## Load a sample

## Using with science-jubilee
- See the tool guide on science-jubilee web page



## Troubleshooting and tweaking:
- Getting the arm and catch positioned right
- Tuning the load stop parameters
    - Make sure resistance is reasonable for your system, tweak with jumper
    - will need to adjust load detection to work with your system

- 
