Fork of NIST Autonomous Formulation Laboratory - Automation Software for sample loader implementation

This package contains the core laboratory automation software used in the NIST AFL platform.

Its core is the 'DeviceServer' API, a simple way of exposing functionality in simple Python classes to the outside world via HTTP servers.  It includes robust item queueing support, output rendering, and hooks to allow for 'smart' generation of user interfaces automatically.

Specific deviceserver instances are provided for a variety of hardware used in the AFL platform: syringe pumps, valves, multiposition flow selectors, UV-Vis spectrometers, x-ray and neutron scattering instruments/beamlines.  There are further deviceserver classes that integrate these base devices to perform higher-level functions, e.g. "loading".  These classes aim to specify instructions for running a particular protocol in a hardware-agnostic way.



Getting a new pi configured to run the AFL:

1. Turn on the SPI interface of the raspberry pi
2. Install the labjack software (separate from the labjack python package). Should be Linux AArch64 version from [their downloads page](https://support.labjack.com/docs/ljm-software-installer-downloads-t4-t7-t8-digit#LJMSoftwareInstallerDownloads-T4,T7,T8,Digit-Linuxx64LJMSoftwareInstallerDownloads)
3. Clone this repo onto the pi
4. Install requirements into your venv from r



## To queue something via API:

1. Get a token with


`curl --header "Content-Type: application/json" --request POST --data '{"username":"bgpelkie", "password":"domo_arigato"}' localhost:5000/login`

2. save token as env $jwt

3. Push to queue: 

`curl --header "Content-Type: application/json" --header "Authorization: Bearer $jwt"  --request POST --data '{"task":"loadSample", "sampleVolume":"0.5"}' localhost:5000/enqueue`

