# Build guide

This is a build guide for the Pozzo lab fork of the NIST AFL system. This is how we built it and may not be the way the original NIST designers have built it. In case of conflict, go with the NIST version

- [Build guide](#build-guide)
  - [Parts list](#parts-list)
    - [Resin printed components](#resin-printed-components)
    - [PLA etc. printed components](#pla-etc-printed-components)
    - [Custom fabricated components](#custom-fabricated-components)
    - [Purchased components](#purchased-components)
  - [Build guide:](#build-guide-1)
    - [Build the frame](#build-the-frame)
    - [Wire solenoid valves](#wire-solenoid-valves)
    - [Wire the compute control box](#wire-the-compute-control-box)
    - [Mount connectors to valves](#mount-connectors-to-valves)
    - [Physically mount everything to the frame](#physically-mount-everything-to-the-frame)
    - [Make electronic connections](#make-electronic-connections)
    - [Make pneumatic and fluidic connections](#make-pneumatic-and-fluidic-connections)
    - [Assemble front panel](#assemble-front-panel)
    - [Assemble catch assembly](#assemble-catch-assembly)
    - [Assemble to flow cell components](#assemble-to-flow-cell-components)
      - [Prepare the flow cell](#prepare-the-flow-cell)
      - [Install AFL flow cell components on instrument:](#install-afl-flow-cell-components-on-instrument)
    - [Provision Pi](#provision-pi)
  - [Comissioning](#comissioning)
    - [Test valve function](#test-valve-function)
    - [Connect and prepare:](#connect-and-prepare)
    - [Final software configurations](#final-software-configurations)
    - [Connect a Jubilee and move it to a safe position](#connect-a-jubilee-and-move-it-to-a-safe-position)
    - [Bring up the app](#bring-up-the-app)
    - [Connect with the web app GUI:](#connect-with-the-web-app-gui)
    - [Connect with Science-Jubilee](#connect-with-science-jubilee)
      - [Connect with HTTP](#connect-with-http)
    - [Basic use](#basic-use)
      - [Prepare the cell](#prepare-the-cell)
      - [Load a sample](#load-a-sample)
      - [Rinse the cell](#rinse-the-cell)
    - [Troubleshooting](#troubleshooting)
      - [Queue pausing](#queue-pausing)
      - [Solenoid valves aren't switching when they are supposed to](#solenoid-valves-arent-switching-when-they-are-supposed-to)
      - [Sample stopping problems](#sample-stopping-problems)
      - [Samples and rinse solution leak out of the catch](#samples-and-rinse-solution-leak-out-of-the-catch)
    - [Registering the AFL server as a systemd service](#registering-the-afl-server-as-a-systemd-service)
  - [Additional resources](#additional-resources)


## Parts list

### Resin printed components

We suggest printing these parts out of an engineering SLA resin, such as Formlabs tough 2000, due to their load bearing nature.

| Part name | Assembly | Link |
| --- | --- | --- |
| Catch holder | Catch | https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-101-(LoaderV2)/002-(CatchCarrierAssy)/AFL-101-002-01-0D%20CatchlessCatchHolder-Braced-For1inCatch-Sidebar-Lowered.stl |
| Piston arm/ elevator arm | Catch | https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-101-(LoaderV2)/002-(CatchCarrierAssy)/AFL-101-002-01-2B%20Elevator%20arm%20r2.stl |

### PLA etc. printed components
Brackets, mounts, etc. that aren't struturally critical

| Part name | Assembly | Link | Print notes |
| --- | --- | --- | --- |
| Rinse bottle holder | Frame | https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-102-(TravelAFL)/002-(ExternalComponents)/AFL-102-002-01-0B%20Bottle%20Holder%20for%20RoadBot%20Rail-r2.stl| 2 needed |
| 5/2 valve holder | Frame | https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-102-(TravelAFL)/004-(PneumaticModule)/AFL-102-004-01-0D%20RoadBot%20Pneumatic%20Module%20-%20with%20Jack%20-%20r4.stl | Original design uses this for more components, we just use it to hold the 5/2 valve. Could replace with something smaller for this purpose |
| Catch holder nut | catch | https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-101-(LoaderV2)/002-(CatchCarrierAssy)/AFL-101-002-01-3B%20CatchHolderNut.stl | |
| Compute control module | Frame |https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/ComputeControlModule%20v6.stl | |
| Compute control module lid  | Frame |https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/module_lid%20v2.stl | |
| Digital regulator mount | Frame |https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/DigitalRegulator_mount_base%20v4.stl | |
| Digital regulator clamp | Frame | https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/DigitalRegulator_mount_clamp%20v2.stl | |
| Digital regulator rail mount | Frame | https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/DigitalRegulator_mount_railmount%20v2.stl | Need 2 |
| Labjack rail mount | Frame | https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/LabjackT4_railmount%20v2.stl | Need 2|
| Power entry module housing | Frame | https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/PEM_housing%20v3.stl | |
| Power entry module housing lid | Frame |https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/PSU_socket_holder_cover%20v3.stl | | 
| Power supply rail mount | Frame | https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/PSU_rail_mount%20v3.stl| Need 2 |
| Regulator rail mount for static regulator | Frame |https://github.com/brendenpelkie/AFL-sample-loader/blob/main/fabrication_files/stl/Regulator_mount%20v3.stl | Need 2, intended to work with manufacturer mounting bracket |


### Custom fabricated components

| Part | Link | Notes |
| --- | ---- | --- |
| X-ray piston | https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-101-(LoaderV2)/001-(CatchAssy)/Catches/piston%20for%20xray.stp and https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-101-(LoaderV2)/001-(CatchAssy)/Piston-Xray-Drawing.pdf | We did not actually have these made so can't directly advise on procurement. Machine out of HDPE. Can be procured from sendcutsend etc, expensive for small quantities |
| X-ray catch |https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-101-(LoaderV2)/001-(CatchAssy)/Catches/catch%20for%20xray.stp and  https://github.com/pbeaucage/AFL-hardware/blob/main/CAD-NewOrgScheme/AFL-101-(LoaderV2)/001-(CatchAssy)/Catch-Xray-Drawing.pdf | |

### Purchased components

| ﻿Component name | Vendor | Vendor part number | Link | Unit Price (Apr 2025) | Quantity | Extended price | Notes |
|---|---|---|---|---|---|---|---|
| **Catch assembly** |  |  |  |  |  |  |  |
| Air-powered hold-down fixture clamp | McMaster-Carr | 50185A34 | https://www.mcmaster.com/50185A34/ | 518 | 1 | 518 |  |
| 5-way air directional control valve | McMaster-Carr | 6425k18 | https://www.mcmaster.com/6425K18/ | 233 | 1 | 233 |  |
| 1/8" OD tubing | McMaster-Carr | 5548K45 | https://www.mcmaster.com/5548K966/ | 25 | 1 | 25 | 25 ft likely sufficient for internal connections and a short run from air supply. Get more if you need to make a long connection to your air supply |
| screws to bolt clamp to base - 5/16-24 x 3inch socket head cap screw | McMaster-Carr | 91251A370 | https://www.mcmaster.com/91251A370/ | 11.48 | 1 | 11.48 | You need 3, come in packs of 5 from McMaster |
| 5/16 nylock nuts | McMaster-Carr | 91831A125 | https://www.mcmaster.com/91831A125/ | 8.42 | 1 | 8.42 | You need 3, comes in packs of 50 from Mcmaster |
| 5/16 washers | McMaster-Carr | 92141A030 | https://www.mcmaster.com/92141A030/ | 7.53 | 1 | 7.53 | You need 3 |
| M5x10 button head screw | From assortment pack - see below |  |  |  |  | 0 |  |
| 1/4-20 x 3" socket head cap screw | McMaster-Carr | 92196A823 | https://www.mcmaster.com/92196A823/ | 17.57 | 1 | 17.57 | You need 1, they come in a 10 pack. Used to mount piston to catch arm. 2" of 1.5" even is probably better here |
| 1/4-20 nuts (no nylock just basic nuts) | McMaster-Carr | 92673A113 | https://www.mcmaster.com/92673A113/ | 2.49 | 1 | 2.49 |  |
| 1/4-20 washers | McMaster-Carr | 92141A029 | https://www.mcmaster.com/92141A029/ | 5.5 | 1 | 5.5 |  |
| Screws to mount catch to base - 6/32 x 2" socket cap screws | McMaster-Carr | 92196A169 | https://www.mcmaster.com/92196A169/ | 4.96 | 1 | 4.96 | You need 2 - mount catch and nut to catch base |
| 6/32 nuts (nylock) | McMaster-Carr | 91831A007 | https://www.mcmaster.com/91831A007/ | 5.83 | 1 | 5.83 | You need 2   |
| **General pneumatic supplies and fittings** |  |  |  |  |  |  |  |
| Relieving adjustable regulator | McMaster-Carr | 8812K52 | https://www.mcmaster.com/8812K52/ | 31 | 2 | 62 |  |
| Mounting brackets for regulators | McMaster-Carr | 8812K62 | https://www.mcmaster.com/8812K62/ | 4 | 2 | 8 |  |
| 1/4" NPT x 1/4" tube push connector | McMaster-Carr | 5779K109 | https://www.mcmaster.com/5779K109/ | 5.83 | 5 | 29.15 |  |
| 1/4" NPT x 1/8" tube push connector | McMaster-Carr | 5779K243 | https://www.mcmaster.com/5779K243/ | 8.2 | 2 | 16.4 |  |
| 1/4" push to connect tee  | McMaster-Carr | 5779K34 | https://www.mcmaster.com/5779K34/ | 7.43 | 1 | 7.43 |  |
| 1/4" NPT x 1/4" Tube elbow push to connect connector | McMaster-Carr | 5779K152 | https://www.mcmaster.com/5779K152/ | 4.7 | 3 | 14.1 |  |
| **Fluid dispensing system** |  |  |  |  |  |  |  |
| Digital regulator | McMaster | 8083T1 | https://www.mcmaster.com/8083T1/ | 810 | 1 | 810 |  |
| Cable for regulator | Digikey | 10-04466 | https://www.digikey.com/en/products/detail/tensility-international-corp/10-04466/21777514 | 19 | 1 | 19 |  |
| Solenoid valve  | McMaster | 5001T36 | https://www.mcmaster.com/5001T36/ | 85 | 4 | 340 |  |
| System vent solenoid whisper valve | Burkert | part 6724 - article 280888 |  | 202 | 1 | 202 | Appears to have been discontinued - any small solenoid with 1/4-28 fittings should work here |
| Check valves | Masterflex | MFLX01355-24 | https://www.avantorsciences.com/us/en/product/NA5132420/masterflex-inert-in-line-check-valves-peek-avantor | 73.5 | 5 | 367.5 |  |
| 5PSI PRV | Idex | U-455 | https://www.idex-hs.com/store/product-detail/pressure_relief_valve_assembly_5_psi/u-455?search=true | 212.29 | 1 | 212.29 | This is suggested but we chose to operate without it in place. |
| 20PSI PRV | Idex | P-791 | https://www.idex-hs.com/store/product-detail/bpr_assembly_20_psi/p-791 | 152 | 1 | 152 |  |
| 1000mL pressure rated bottles | Duran | Pressure plus 1000mL GL45 |  | 40 | 2 | 80 |  |
| GL45 3-port caps | Cole-Parmer | EW-12018-01 | https://www.coleparmer.com/i/cole-parmer-vaplock-solvent-delivery-cap-with-304-ss-port-thread-inserts-three-1-4-28-gl45-1-ea/1201801 | 66 | 2 | 132 |  |
| Bubble detector | Digikey | 365-1490-ND | https://www.digikey.com/en/products/detail/tt-electronics-optek-technology/OCB350L062Z/1942310?s=N4IgTCBcDaIEIHkCCAlAIgAgMJIDIEk4Vt8UsBVfAFQwQAU4BmAVgAZdWA2CAXQF8gA | 26 | 2 | 52 | 1 needed, strongly suggest having a spare |
| 1/16" OD tubing | McMaster | 5239K23 | https://www.mcmaster.com/5239K23/ | 36 | 1 | 36 | 25ft may be enough - check tubing length needed to reach instrument |
| 1/8" OD tubing | McMaster | 5548K966 | https://www.mcmaster.com/5548K966-5548K401/ | 25 | 1 | 25 | 25ft should be enough. Check material compatability for your system |
| 1/4-28 F to 10-32 M adapter | Idex | 1582 | https://www.idex-hs.com/store/product-detail/english_thread_adapter_10_32_male_x_1_4_28_female/1582 | 74.52 | 1 | 74.52 |  |
| 1/4-28 fittings | Idex | 1451 | https://www.idex-hs.com/store/product-detail/flangeless_fittings_kit/1451?search=true | 357 | 1 | 357 | Suggested to just buy the kit |
| 1/8" push to connect to 10-32 fittings | McMaster | 5779k241 | https://www.mcmaster.com/5779K241/ | 4.35 | 8 | 34.8 |  |
| 1/8" push to connect tee fittings | McMaster | 5779K31 | https://www.mcmaster.com/5779K31/ | 7.58 | 3 | 22.74 |  |
| Connector crimp for burkert valve | Digikey | SPH-002T-P0.5S | https://www.digikey.com/en/products/detail/jst-sales-america-inc/SPH-002T-P0-5S/527359?s=N4IgTCBcDaICwFYEFoCMqwHY3IHIBEQBdAXyA | 4.09 | 1 | 4.09 | You need 2, it looks like you are buying 100 now.  |
| Connector housing for burkert valve | Digikey | PHR-2 | https://www.digikey.com/en/products/detail/jst-sales-america-inc/PHR-2/608607 | 0.1 | 2 | 0.2 |  |
| **Control electronics** |  |  |  |  |  |  |  |
| Raspberry Pi 4 8GB | PiShop |  | https://www.pishop.us/product/raspberry-pi-4-model-b-8gb/ | 75 | 1 | 75 |  |
| PiPlates Relayplate | PiPlates | RELAYPlate | https://pi-plates.com/relayr1/ | 42 | 1 | 42 |  |
| Labjack T4 | Labjack | T4 | https://labjack.com/products/labjack-t4 | 280 | 1 | 280 | Used to read voltage of sensor and set voltage for digital regulator. Should be possible to do this with a raspberry pi and save some $$ |
| Labjack DAQ TIC | Labjack | LJTick-DAC | https://labjack.com/products/ljtick-dac | 95 | 1 | 95 |  |
| 24V power supply | Meanwell | LRS-350-24 | https://www.amazon.com/MEAN-WELL-LRS-350-24-350-4W-Switchable/dp/B013ETVO12/?_encoding=UTF8&pd_rd_w=czC45&content-id=amzn1.sym.d0ebfbb2-6761-494f-8e2f-95743b37c35c%3Aamzn1.symc.50e00d6c-ec8b-42ef-bb15-298531ab4497&pf_rd_p=d0ebfbb2-6761-494f-8e2f-95743b37c35c&pf_rd_r=P3NGMT1FE76ZJF4F5DE3&pd_rd_wg=Lk0QN&pd_rd_r=15057e39-23bc-4c85-9e15-0580f2191d70&ref_=pd_gw_ci_mcx_mr_hp_atf_m | 30 | 1 | 30 |  |
| 22g wire - single strand | Generic |  | https://www.amazon.com/TUOFENG-Hookup-Wires-6-Different-Colored/dp/B07TX6BX47?crid=1KSZ1FWIIGHIJ&dib=eyJ2IjoiMSJ9.WSg2cJvoMznQ1mF6NKXgDjgxahf8h3f91Jh03RD4XNwBZKF9PamtRq8n660GOvLT7RiqfZP0I97wmYF5tKv7EggqDlK4WR3KXrD2ElPyw-DLkFNcT6cXIggNRQfMchc3H86Xq-85_g4iV5ChHaG6jULzsCHBqcD7_vpAyocV_EFmM-_fNTIdxLxnJdTSipcYpk_Q6B5AGioFLfdmC4G123MV9XRSKwXi_EXIxU1zH4YfjPIm9Q3DgG-xMBw2Rpd8q3K6aelP2tPsLOWgrjHnrs9awBJa5BIx0kpYlRMK9jw.iVjGW5KIguuyh2-91oruCqZ1TtyjhcX83hOMJ0EZohM&dib_tag=se&keywords=22g%2Bhookup%2Bwire&qid=1713377808&s=industrial&sprefix=22g%2Bhookup%2Bwir%2Cindustrial%2C179&sr=1-1&th=1 | 15 | 1 | 15 |  |
| 22g wire dual conductor |  |  | https://www.amazon.com/AOTORUA-Electrical-Oxygen-Parallel-Extension/dp/B088RC5ZT3?crid=JCC2KSNPTAQL&dib=eyJ2IjoiMSJ9.uU_5gBszooQmZauIS4C55LX-OxqjEiDrdTclo5uDa_SDvQWYI7KIJzNWZ8kWs2xM4wMuNwfh8w58OW1FO_WQMVSgjA9fWe3rTzNvqsfxfnCakHmi9LEH6a8_-oUhKCGhNQKLHacw5KfgxMvHgEnhrAoCwtQxGYoOo3nrkxIsdeAmvig5YvGFk1Q82HVx4ptFo-2lJ_r-KliQd7bpcVYD8Q.Zf1ZWTcd8FoSbHQpOFayQj2HCIO6PLldRA_H6oumQwk&dib_tag=se&keywords=aotorua+hookup+wire&qid=1713311987&s=industrial&sprefix=aotorua+hookup+wir%2Cindustrial%2C121&sr=1-3 | 15 | 1 | 15 |  |
| 1/8" flexible braided cable sleeve | Alextech |  | https://www.amazon.com/100ft-Expandable-Braided-Sleeving-Sleeve/dp/B074GN12PY?crid=11KZ0EUHWKX6O&dib=eyJ2IjoiMSJ9.ZJkuDZRpSa8p_gUxguZ_K7I_Tldf3XPNQ7eZNKYuwkVFmxKfysOjXxTGpB28jqAeu6SJKZT3L6LK_iYsPFaRYqN5WG36POLmvoAc0SWWHMehwXC1mYAC9cYZxFKRF8A-BTt8DUFPR2cyNNhlIjLBHfpwIzx1crwA3jZdCEGYehArByidZunv-RttXiJQYGD1pe3718rDuz5RF3bVYJkLNML8rz8jem2mg48LN_CY-OY.f_pS8ld9DWrLZHVgCKjktoI_9yKG_MGJTjH48VmqmrE&dib_tag=se&keywords=expandable%2Bbraided%2Bsleeving%2B1%2F4&qid=1747976103&sprefix=expandable%2Bbraided%2B%2Caps%2C739&sr=8-4&th=1 | 1 | 13 | 13 | Optional but suggested  |
| quick connectors - receptacle housing | Digikey (JST) | SMP-02V-BC | https://www.digikey.com/en/products/detail/jst-sales-america-inc/SMP-02V-BC/1835574?s=N4IgTCBcDaICwFYEFowE4x2QOQCIgF0BfIA | 20 | 0.1 | 2 |  |
| quick connectors - receptacle crimp | Digikey( JST) | SHF-001T-0.8BS | https://www.digikey.com/en/products/detail/jst-sales-america-inc/SHF-001T-0-8BS/527351?s=N4IgTCBcDaICwFYEFoCMqyrcgcgERAF0BfIA | 40 | 0.1 | 4 |  |
| quick connectors - socket housing | Digikey | SMR-02V-B | https://www.digikey.com/en/products/detail/jst-sales-america-inc/SMR-02V-B/764265?s=N4IgTCBcDaICwFYEFowE4wDZkDkAiIAugL5A | 20 | 0.1 | 2 |  |
| quick connectors  - socket crimp | Digikey | SYM-001T-P0.6(N) | https://www.digikey.com/en/products/detail/jst-sales-america-inc/SYM-001T-P0-6-N/1465026?s=N4IgTCBcDaICwFYEFoCMBOADOtyByAIiALoC%2BQA | 40 | 0.1 | 4 |  |
| power distribution block | Amazon |  | https://www.amazon.com/OONO-Position-Terminal-Distribution-Module/dp/B08TBXQ7H6?crid=2QQKIBI34BWN6&dib=eyJ2IjoiMSJ9.TyW4XcJK91XHfZ1hB2XxVG8RNOK-Sd9ASYgPFD863yOaq-eywlgzPZhj7DfqN-g6VAqMwy5-iH_e3kvR0liyMvur4Eg8qpzOu3foD8ny7KL_gT8LXTveHKuKFhthvg-mGv_R32rXwcrPvB7-GLyv2ae4bcCTHDSoS6ITQfKjHIshRiosOqWA3mjqkjRNxUSL2G4LQ2fRWSDqKF5_JTXPDdDH3MVjwgw3lS1wRwzyeWOcPfjNxWz1ChmgRsUu7wb7Uvjp_RUALPJic0vX1k-ZGVO9wyj9y2dMwm827llu1eY.rsQEDjTTnnNYaUHDYR-rr_W7qrggb2B89jOENzXNZsk&dib_tag=se&keywords=power%2Bdistribution%2Bblock&qid=1747976788&s=industrial&sprefix=power%2Bdistr%2Cindustrial%2C189&sr=1-5&th=1 | 1 | 1 | 1 |  |
| 22g ring connectors | Digikey | 190700040 | https://www.digikey.com/en/products/detail/molex/0190700040/279074?s=N4IgTCBcDaIOoFkCMAOMB2AzAWgHIBEQBdAXyA | 15 | 0.2 | 3 |  |
| Butt splices |  | A09010-ND | https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/321198/255782?s=N4IgTCBcDaIIIAYCcCCMCC0A5AIiAugL5A | 20 | 0.33 | 6.6 | Nice to have on hand, or substitute your favorite other wire joining method.  |
| **Frame** |  |  |  |  |  |  |  |
| 20x20mm aluminum extrusion  | 8020.com | 20-2020 | https://8020.net/20-2020.html | 1 | 90 | 90 | Need 4x24", 4x22", 4x4.2" |
| 22x24" acrylic panel | Generic |  | https://www.amazon.com/24-Black-Acrylic-Plexiglass-Opaque/dp/B00IWACJ3Q?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A1FWWCVO9POVQF&gQT=0 | 1 | 30 | 30 | May need to cut down a larger panel |
| M5 blind T nuts | Generic |  | https://www.amazon.com/Sutemribor-Hammer-Fastener-Aluminum-Profile/dp/B07FPLZXTF?crid=1RMG9CIN2T3RG&dib=eyJ2IjoiMSJ9.pTijVLUi_yVyINyHNamxRnyzEUhkVrU07S6UTNAbBOfK3mhbBgH1SxNQ6-oLwuky8Z7Pgy39Vl5lFZHqmB8zgrgCnj7ymOOK7yH02snKvP7XTlgZv8teL1m3F_Jdv_RNKK-xQ2Eu1RN3kGUXaJl8_KPqOX0A46K0Q0eK_eRK3DqYKHAmrwWON3CvSYlc2M2ar11Ol3K25LLa-1aprmuLA2P_ntfdGE3JCDbzptZyRow.0SaKrworAj7GL95DA03-WE4Tcv0PxuGOkd3Ii63D2l4&dib_tag=se&keywords=metric%2Bt%2Bnuts%2Bfor%2Bextrusion&qid=1747976894&sprefix=metric%2Bt%2Bnuts%2Bfor%2Bextrusion%2Caps%2C157&sr=8-4&th=1 | 1 | 8 | 8 | Suggest getting an assortment |
| 2020 corner bracket plates | Generic |  | https://www.amazon.com/Outside-Bracket-Aluminum-Profile-Connector/dp/B07J6B9FJ1?crid=3OBDWME13RQOC&dib=eyJ2IjoiMSJ9.udQxPygCfvgcuiG9xjtB_h3Ez7JIClfbX0eXMIENgoQ0aAZLEI7hLOOmbnr8QMmxDfyUcqNDr6RtHhxpNlGriLbu0h3X50kGI1sGVvpaftMYgPhMkPImwVi-fV5lfU4FR7tUa7oRCyGcXv-Sd-2t-O1rCkCoPMkOzGG-oZPH0svPKecM_sWjz-UrAOJz96s_8nK76LUX7DDgYm92Ri64oZkJ9-6-rXK5_lTGnJfGZKQ.jofeUdOJkzeTsphOCOnuF4TUhI6Ueld691kt9iLkUbs&dib_tag=se&keywords=2020+corner+bracket+plate&qid=1747976832&sprefix=2020+corner+%2Caps%2C152&sr=8-5 | 2 | 17 | 34 | Need 12 brackets total. |
| Panel mount diverting valve | McMaster | 4149T42 | https://www.mcmaster.com/4149T42/ | 1 | 47 | 47 |  |
| 1/4" push to connect panel mount pass through fittings | McMaster | 5779K677 | https://www.mcmaster.com/5779K677/ | 3 | 7.22 | 21.66 |  |
| 1/8" push to connect panel mount pass through fittings | McMaster | 5779K675 | https://www.mcmaster.com/5779K675/ | 4 | 6.22 | 24.88 |  |
| Panel mount 4-pin M12 connector - male | Amazon |  | https://www.amazon.com/gp/product/B0BBQTDLHP?smid=A3EPS00U1KMPT0&th=1 | 1 | 17 | 17 | Need 2 |
| M12 connector female housing | Amazon |  | https://www.amazon.com/gp/product/B09YLP4K5W?smid=A3EPS00U1KMPT0&th=1 | 1 | 18 | 18 | Need 2 |
| Metric buttonhead hardware assortment | Amazon |  | https://www.amazon.com/dp/B07L9MMN9K?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1&th=1 | 1 | 28 | 28 |  |

Notes on purchasing:
- Nothing here implies an endorsement of a particular vendor. Links are provided to give example sources.
- Many of the specific-sized fasteners may be better purchased from a vendor that allows for small quantities, such as Bolt Depot in the US.



## Build guide:

### Build the frame
The frame is assembled from the extrusion pieces and the corner braces. Assemble it so it is 24" "tall" x 22" "wide" by 4 1/4" "deep". Don't put any brackets on the bottom.

<img src="frame.JPEG" alt="frame" width="600"/>



### Wire solenoid valves

We suggest wiring the solenoid valves with a quick-connect connector of your choice to make the rest of assembly and travel easier. Connect the male plug end of your quick connector to the supplied solenoid wiring if the valve came with wires. For the 5/2 valve for the clamp arm, you will need to add wires by removing the screws on the wire caps, removing the caps, and adding wires to the terminals. For the Burkert whisper valve for the piston vent, you will need to either wire your own lead using the specified connectors or buy a cable along with the valve. The Burkert valve mounts to the Jubilee-mounted catch assembly, so make sure the wire for this is long enough to reach. For this valve, pay attention to wiring polarity. Also wire yourself a ~48" connector 'extension' for each valve. Terminate one end of this extension with the female socket of your quick connector and leave the other end unterminated. Use red and black wire for this. All the wire pairs should be a single cable, so either use dual-conductor wire or place both strands in some sort of sheathing like the one suggested in the BOM. At this point, it is a good idea to label every valve. 

| Label | AFL internal name |Valve type | Relay plate number | 
| --- | --- | --- | --- |
| Sample Hold | 'postsample' Mini solenoid cylinder | 1|
| Vent | 'piston-vent' | Burkert whisper | 2 |
| Sample push | 'blow' | Mini solenoid cylinder | 3 |
| Rinse 2 | 'rinse2' | Mini solenoid cylinder | 4 |
| Rinse 1 | 'rinse1' | Mini solenoid cylinder | 5|
| Arm up | 'arm-up' | 5/2 valve A | 6 |
| Arm down | 'arm-down' | 5/2 valve B | 7 | 


<img src='valvewire.JPEG' width = "600"/>


<img src='wireextension.JPEG' width = "600"/>


### Wire the compute control box

This is a rats nest. This box contains the raspberry pi that controls everything, the PiPlates relayplate that actuates the pneumatics, and power wiring. It is easiest to route all the wires into the box where they need to go, but keep the power distribution block and relay plate loose (don't screw them down yet). Make sure everything will still fit/wires reach/etc once it goes in the box. 


1. Connect a red wire to one of the 'A' terminals on the end of the power distribution block, and a black wire to one of the 'B' blocks. These will be the +24v and ground from your power supply.

2. For each of the 7 solenoid valves you need to: 
    1. Connect an 'A' terminal from the power distribution block to the relay terminal.
    2. connect the red wire from your valve extension wire from above to the other terminal of the relay.
    3. Connect the black wire from the valve extension to the corresponding 'B' terminal on the power distribution block.

<img src='controlboxwiring.png' width = "600"/>


3. Now screw everything down to the box using M3 (? maybe 2.5?) screws.

4. Mount the raspberry pi to the standoffs on the lid.

5. Use the raspberry pi female-female ribbon cable to connect the pi to the relay plate, minding the orientation as shown here. 

<img src='pi_relayplate_connect.JPEG' width = "600"/>


### Mount connectors to valves

Mount the connectors to the valves as described in the main pneumatic connections figure. Use teflon tape to prevent leaks on NPT connectors.

### Physically mount everything to the frame

Mounte everything to the frame using the 3D printed mounts and brackets. The specific arrangement isn't critical as long as everything clears. Pay attention to which side your panel is going to be on if you are using one - make sure to put the 90* elbow connectors on that side. 

<img src="frame_layout.png" width="600"/>

- Most components mount with dedicated 3D printed mounting brackets
- Things mounting to the extrusion use blind-insert T nuts
- The solenoid valves may require a few wraps of PTFE tape to stay secure in their mounting brackets
- The static regulators mount to manufacturer purchased brackets. These brackets mount to the 3D printed mounts with M5 hardware
- Everything else uses M3 hardware directly threaded into plastic, or heat-set M3 inserts. 



### Make electronic connections

Wire everything remaining as shown in the electronic connections diagram.

<img src='AFL_wiring.png'/>


Notes:
- On our M12 cable for the digital regulator, the yellow cable matches to the analog in pin on the regulator. Double check your cable and the regulator's manual.
- The regulator runs on 24V power
- The bubble sensor does not run on 24V power and in fact will spark and pop if it is asked too. It likes 5V. Buy extras they are cheap.
- Wiring for 1 solenoid valve is shown in the diagram. Again, wire all 7 in the same manner.
- Double check you wire your 120V power entry module to the power supply correctly. Make sure to put fuses in your power entry module.

### Make pneumatic and fluidic connections
Make physical tubing connections as shown in the diagram below. You will need to select appropriate fittings for each tubing connection. Generally speaking,
- 1/16" OD tubing requires a 1/4-28 fitting. Use a 10-32 male to 1/4-28 female adapter to mount these fittings to the solenoid valves.
- 1/8" tubing uses either a 1/4-28 fitting or push to connect fitting
- 1/4" tubing uses push to connect fittings

<img src='AFL_control_physical_connections.png'/>

### Assemble front panel

### Assemble catch assembly

<img src='catch_assembly.JPEG' width = "600"/>


1. Drill and tap M5 holes in Jubilee deck on slot 1 for catch, using the catch block as a template. If you are using the original lab automation deck template, you will also need to remove some material from the back edge. The modified AFL automation deck template does not have this material. 

2. Connect the 1/4" OD x NPT ? push to connect fittings to the clamp. 

3. Mount the clamp to the catch base using the 5/32 x 3" screws. Use washers and assembly lube.

4. Loosely mount the piston to the catch arm by assembling the hardware stack as shown in the picture. The 1/4-20 screw threads into the top of the piston, washers are used to space the piston down from the arm, and a washer and 2 nuts are used on top of the arm to tighten down the assembly. Leave this loose as the number of washers between the arm and the piston may need adjusting. 

<img src='piston_detail.JPEG' width = "600"/>


5. Mount a sufficiently long amount of 1/16" OD tubing to reach your flow cell to the bottom of the catch, using a 1/4-28 fitting. Be extremely careful not to cross-thread the soft HDPE threads. 

6. Connect a short piece of tubing between the piston and the normally closed port of the whisper valve, using 1/4-28 fittings.

7. Mount the piston arm to the clamp, aligning it so that it is lined up with the catch when closing.

8. Fine tune the washer stack for the piston so that the piston just clears the rim of the catch when the clamp swings over it. 

9. Make the fluidic connections for the piston. Again don't cross thread the HDPE fittings.

<img src='AFL_catch_physical_connections.png' width = "600"/>



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

### Assemble to flow cell components

The flow cell components include the Anton-Paar flow cell, a bubble sensor to detect the presence of the sample, and a solenoid valve to hold the sample in place. When a sample is loaded, the bubble detector senses the liquid sample in the tubing, then the system closes the sample hold solenoid valve to hold the sample in place. The solenoid valve needs to be placed down-stream of the flow cell and within a few inches of the flow cell. If it is too far away, the sample will 'drift' after stopping. The sensor should ideally be placed between the flow cell and the solenoid, but its placement is flexible. Timing configurations can be adjusted later in software to get the sample stopping tuned in well.
    Here, we use an Anton-Paar Saxess flow cell. We use these because we have a lot on hand, but they are not readily purchased as far as I can tell. Alternatives include any capillary flow cell that will mount to 1/16" OD tubing that you may have access too. We have also heard that gluing a piece of appropriately sized Kapton tubing into the ends of two pieces of tubing makes a perfectly functional sample cell for SAXS. 

#### Prepare the flow cell
Assuming you are starting from a broken or fouled flow cell:
1. Drill out the old glass and epoxy using a lathe. Have the machine shop take care of this for you.
2. Epoxy a new capillary into place. Completely sealing the edges of the capillary without getting epoxy all over the center of the glass where the beam will be is an art form. 
3. Score the ends of the capillary flush with the end of the threads
4. Sand the ends of the assembled flow cell so that the capillary and the brass are flush, with no rough edges or epoxy protrusions. *This is essential to preventing leaks in the next step.*
5. Determine the appropriate number of shims to include on each end of the flow cell fittings. You need enough shims that the inner O-ring compresses enough to seal before the outer O-ring and threads bottom out. This is a trial and error process. Start with ~3 per side. 
6. Assemble the tubing-shim-o-ring-fitting stack, as shown in the picture. Make sure to start with a clean, square tubing end cut using a tubing cutter tool. The order is 
    - Put the tubing on the tube, with the threaded end facing the end of the tubing you will mount to the flow cell. This will eventually be the tubing that comes from the AFL Jubilee catch bottom, but start with some spare tubing to leak test first.
    - Next put 1 inner O-ring on the tubing
    - Next, the determined number of shims
    - Flange the end of the tubing using a tubing flanging tool.
    - Place an outer O-ring in the seat of the threaded fitting
    - Thread the fitting onto the end of the flow cell, making sure the outer O-ring doesn't get munched.



<img src='flowcellassembly.png' width = "600"/>

7. Leak test the flow cell. Carefully clamp one end of the tubing with a c-clamp or similar, enough to stop water flow but not enough to tear the tubing. Install a syringe filled with water onto the other tubing end, using a Luer lock to 1/4-28 adapter and a 1/4-28 fitting. Release the clamp and flow some water through the tubing. Close the clamp and gently apply pressure to the syringe, making sure not to burst the capillary. Watch for leaks.
- If water leaks out of the inside of the flow cell, between the brass and the capillary: The epoxy seal is inadequate, drill out the capillary again and start over.
- If water leaks out the inside of the fitting between the stainless fitting and the tubing: Add more shims
- If water leaks out the outside of the fitting, between the brass and the stainless fitting: Less shims or check O-rings are lined up right.
You can also vacuum leak test if using under vacuum.

8. Re-assemble the tubing with the tubing used for the system.

#### Install AFL flow cell components on instrument:

Mount this installation to your instrument as appropriate. At APS, we just taped everything to the sample stage and this worked great. The flow cell was held using a 3D printed holder that mounted in our APS USAXS cartridge plate holder. More details on flow cell [here](https://github.com/pozzo-research-group/Automation-Hardware/tree/master/Cartridge%20Sample%20Holder%20for%20SAS%20Experiments/SAXS-USAXS_AntonPaar_FlowCellHolder) and holder [here](https://github.com/pozzo-research-group/Automation-Hardware/tree/master).  If you are working in a vacuum, you will need to route your input tubing, output waste tubing, sensor wires and valve wires into the vacuum chamber, or experiment with sample stopping settings so you can keep the electronics outside the vacuum. 

- Clip the sensor onto the tubing downstream of the flow cell
- Install the sample hold solenoid valve a few inches downstream of the tubing, using a 10-32 to 1/4-28 adapter and 1/4-28 fitting.
- Route the outlet of the sample hold solenoid valve to a waste container


Flow cell O-rings and spacers:

| Part | Size | McMaster Link |
|---|---|---|
|Inner o rings | 001-1/2 | https://www.mcmaster.com/9464K181/ |
| Inner shims | 0.005" thick x 1/16" ID | https://www.mcmaster.com/99040A945/ |
| Clock pin side outer O-ring | 1mm wide x 6mm ID | https://www.mcmaster.com/9263K111/|
| Non-clock pin side outer O-ring | 1mm wide x 5mm ID | https://www.mcmaster.com/9263K285/ |

### Provision Pi

Assuming you are starting from a fresh install of Raspberry Pi OS 64 bit:
1. Configure raspberry pi networking for your equipment LAN. These instructions assume you are using our default Jubilee Lan configuration, but you can change these values as needed. Our standard network configuration is to give devices a static IP address in the range 192.168.1.x. Here we will assign the AFL pi the ip 192.168.1.4
- Log into your pi for the first time, give it a reasonable username and password, and connect to your wifi network for internet access.
- Plug your pi into the network switch using an ethernet cable. 
- Check if your pi is using NetworkManager of DHCPCD for networking. New installs should use NetworkManager and that is what is shown here. You can do the same setup with DHCPCD although the commands are different. Check by running `systemctl status NetworkManager`, you should see a bunch of active services.
- Get the current wired connection name by running `nmcli connection show`.
- Update the wired connection to assign a static ip: 

```nmcli con modify "Wired connection 1" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.4/24 \
    ipv4.gateway "" \
    ipv4.dns "" \
    connection.autoconnect yes
```

- Reboot
- You should now be able to connect to the pi over your LAN (ie `ping 192.168.1.4` from another connected computer), and also reach the internet.

2. Install the labjack LJM libary. You will need the ARM linux version for the raspberry pi. It currently lives [here](https://support.labjack.com/docs/ljm-software-installer-downloads-t4-t7-t8-digit#LJMSoftwareInstallerDownloads-T4,T7,T8,Digit-LinuxARMv7LJMSoftwareInstallerDownloads). Follow their installation instructions.

3. Create and activate a virtual environment for 

3. Install this version of the AFL control software: 
- Clone the repository somewhere sane
- Install the requirements in `requirements.txt`
- Install this libary - `pip install -e .` from the root of the repo.



## Comissioning 

### Test valve function

Next, check that the valves are all working correctly. Use the [TestSolenoidValves.ipynb](../TestSolenoidValves.ipynb) notebook to step through all the relays and solenoids. When turning a relay on, you should hear a click and be able to feel it if you hold the solenoid valve. If you hear a quiet click from the control box but don't feel the solenoid click, check your wiring and that the power to the solenoids is on. If you hear nothing, check the RelayPlate configuration. 

### Connect and prepare:
In the next few steps, you will make sure everything works and test things out. 

- Back the supply static regulators all the way out to their lowest pressure by 'unscrewing' the knob. 
- Connect your air supply to the inlet fitting.
- Slowly dial the static regulators in to their target pressures (80 PSI for the clamp arm side and 20PSI for the fluidic side). Stop and investigate if you hear or see anything leaking at this point. 
- Fill the rinse bottles with DI water and put the caps on
- Set the Jubilee module in a safe place on a workbench. The arm wil move in the next few steps, so stay clear.
- Lay out your tubing, flow cell, and flow cell components on your workbench.

### Final software configurations
You will be setting configurations for your system in multiple places. You should take the time to read through each of these and understand what is going on where. 
- `server_scripts/LoaderPneumaticJubilee.py`: This is the script to actually launch the AFL loader process. Configuration here includes the relay number to solenoid assignment, Labjack wiring, and science-jubilee IP address.
- `AFL/automation/loading/PneumaticPressureSampleCellJubilee.py`: This is the main python class that runs the AFL sample loader. Configuration related to the load sequencing including rinse programs and timing are set as class variables of the PneumaticPressureSampleCell class.
- `AFL/automation/loading/LoadStopperDriver.py`: Configurations related to the detection of samples by the bubble detector are set here, as class variables of the LoadStopperDriver class. 

Note that configurations are saved automatically in the `~/.afl` directory. If you make config changes, you need to delete the `LoadStopperDriver.config.json` and/or `PneumaticSampleCell.config.json` files from here then re-boot the flask app for changes to take effect. 

Read through these files and make sure the values there make sense. If you followed the setup directions here, you should not need to change anything. 

### Connect a Jubilee and move it to a safe position

This version of the NIST-AFL is modified to integrate with Jubilee. It contains some low-level Jubilee-dependent safety checks that cannot be disabled. Thus, testing the system will require a Jubilee to connected to the network and positioned in a 'safe' position. By default, safe Jubilee positions are x < 5, y > 200, and z > 100. This can be modified in the instantiation of the jubilee object in the `server_scripts/LoaderPneumaticJubilee.py` file.

1. Connect a Jubilee to the same LAN as your AFL
2. Home the Jubilee
3. Move the Jubilee to satisfy the safe position criteria.

You don't need to actually have the catch assembly mounted on the Jubilee yet. 

### Bring up the app

To start the app, just run the `LoaderPneumaticJubilee.py` script:
`python LoaderPneumaticJubilee.py` from the appropriate directory.

### Connect with the web app GUI:

The AFL comes with a web app that lets you run the main functionality of the system from a GUI. This is useful for testing and development. To access the GUI:

1. Navigate to `http://localhost:5000/app` in the browser
2. Click on the 'Add Server' button in the top right
3. Enter the address of the AFL server: `http://localhost:5000` and click enter

You should now see a GUI panel with buttons to load a sample, rinse the cell, and so on. 



### Connect with Science-Jubilee

The NIST-AFL sample loader is defined in the Science-Jubilee library as the Pneumatic Sample Loader tool. To initialize it:
1. Set up a python Jupyter notebook as usual for Jubilee:
```
from science_jubilee import Machine as Jub
from science_jubilee.tools import PneumaticSampleLoader

jubilee = Jub.Machine(address = '192.168.1.2')
deck = jubilee.load_deck('name_of_deck_config.json')
```
2. Define constants for the Pneumatic sample loader configuration:
```
safe_pos = (5, 200, 100) # safe position, should match what is defined in AFL LoaderPneumaticJubilee.py file
cell_pos = (217.5, 69.0, 61.5) # position of catch on Jubilee deck
url = 'http://192.168.1.4' # URL for AFL pi
port = '5000'
name = 'PSL' 
username = 'controlpc' # credentials to log in, username can be whatever
password = 'domo_arigato' 
```

3. Instantiate and load the PSL tool:

```
psl = PneumaticSampleLoader.PneumaticSampleLoader(url, port, name, cell_pos, safe_pos, username, password)
jubilee.load_tool(psl)
```

#### Connect with HTTP
Under the hood, the AFL runs on an HTTP api. If you are using it with Jubilee, it is strongly suggested to use the Science-Jubilee interface to gain the benefits of tested position management. The HTTP API has been loosely modified to integrate with science-jubilee and you may run into unexpected edge cases running on HTTP requests. HTTP access is included here for completeness. If you are using this system without Jubilee, you should remove the jubilee references and position checking from the PneumaticPressureSampleCellJubilee.py file. HTTP docs written in python requests format.

```
import requests

url = 'http://192.168.1.4:5000'
username = 'controlpc'
password = 'domo_arigato'
```

1. Send a login request:

```
r = requests.post(
    url + "/login",
    json={"username": username, "password": password},
)

```
2. Store the auth token for use with future requests

```
token = r.json()["token"]
self.auth_header = {"Authorization": f"Bearer {token}"}
```

### Basic use 

#### Prepare the cell
Before doing anything, the system needs to be prepared. The system needs to be rinsed, and Science-Jubilee needs to set the arm state to a known value before working with the AFL. 

Using the science-jubilee interface (again, with the Jubilee in a safe position):

```
psl.prepare_cell()
```

This will rinse the cell if the cell is not currently rinsed and raise the arm

Using the web GUI: 
1. Click the 'Rinse cell' button and let the rinse cycle run
2. Raise the arm by clicking the 'Prepare Load' button

Using the HTTP interface:
Under the hood, the AFL uses a task queue. Rather than directly calling an endpoint for an action, you request an action by adding a task to the queue using the `enqueue` endpoint. 

1. Rinse the cell:
```
task = {"task_name": "rinseCell"}
r = requests.post(self.url + "/enqueue", headers=self.auth_header, json=task)
```
`enqueue` will return immediately. You can monitor the rinse status to wait until the rinsing is down by checking the system status:

```
# Get status from HTTP endpoint
r = requests.get(self.url + "/driver_status", headers=self.auth_header)
print("status r code", r.status_code)
print("status: ", r.content)
status_str = r.content.decode("utf-8")
status_list = json.loads(status_str)
```
Watch the 'State' of the cell to change from RINSING to RINSED

2. Prepare the cell by raising the arm:
```
task = {"task_name": "prepareLoad"}
r = requests.post(self.url + "/enqueue", headers=self.auth_header, json=task)
```

#### Load a sample

Now that the cell is rinsed and the arm is raised, you can load your sample into the cell. Again, this is easiest with the Jubilee tool:

```
psl.load_sample(syringe_tool, sample_location, volume)
```
This should work with any tool that exposes aspirate and dispense methods, such as the Digital Pipette/HTTP syringe tool or OT2 Pipette integration. 

If doing it via GUI or HTTP, you are responsible for getting your sample into the catch. Once this is done, click the 'Load sample' button on the GUI, or enqueue the following task with the HTTP API:

```
task = {"task_name": "loadSample", "sampleVolume": volume}
```
Typically, sample volumes of 500 uL -> 1000 uL work well. More than that and it may spray out of the vent valve, less and timing the load stop needs to be really precise. 

Now that the sample is loaded, you can trigger your measurement.
#### Rinse the cell
Once the measurement is complete, you need to rinse the catch/flow cell/tubing system out to prepare for the next sample.

With Jubilee:
```
psl.rinse_cell()
```

With HTTP:
```
task = {"task_name": "rinseCell"}
r = requests.post(afl_url + "/enqueue", headers=auth_header, json=task)
```

With GUI: Just click the "Rinse Cell" button.



### Troubleshooting
When doing any troubleshooting, it is best to run the AFL server directly (ie `python LoaderPneumaticJubilee.py`) as opposed to as a systemd service, so that you can watch the outputs of the process. Software errors that throw an error are best dealt with by following the stack trace. Generally speaking:
- If the request is successfully received by the AFL-server as shown in the logs, the issue is on the AFL-server side of things, not the science-jubilee client code. If the requests is not recieved, look at the client.
- Assertion errors relating to machine state not being met: Look at condition causing assertion to flag.

#### Queue pausing
The queue is set up to pause anytime something goes awry, and even when things are done out of order, for example trying to prepare the cell before rinsing it. If something pauses the queue, first fix the issue, then 'unpause' the queue using the button on the GUI or the unpause_queue method of the science-jubilee tool

#### Solenoid valves aren't switching when they are supposed to
You can follow the state the valves are supposed to be in by watching the status on the web GUI. If you suspect a valve isn't switching correctly, test it by manually toggling it with the valve test notebook linked above. Check the wiring if you are having issues, this is the most likely cause.

#### Sample stopping problems

The sample stopping process is tricky and needs to be tuned. When the sample is being loaded, the bubble sensor is constantly outputting a voltage. That voltage is supposed to change significantly (~1.5V) when the phase present in the tube changes from air to liquid. This voltage is constantly read by the Labjack and processed by the StopLoadCBV2.process_signal() function in `loading/SensorCallbackThread.py`. This function runs in a separate thread from the main AFL sample loading process, and calls back to stop the load process by closing the sample hold solenoid valve once the sample is detected. Getting this to work reliably will probably require some tuning

**Tuning the sensor hardware**
The sensitivity of the sensor itself can be changed by moving the jumper between the 3 pins. This is documented in the sensor data sheet. Test different positions by manually flowing a representative liquid through tubing inside the sensor and manually watching the sensor voltage (ex with a multimeter) (while the sensor is plugged into an appropriate 5V power supply). You want to see a decent sized (1-2V) change between liquid and no liquid, without a lot of noise. Move the jumper until you find a position that works for your sample and ambient lighting conditions. 

**Tuning the edge detection parameters**
The above-mentioned sensor callback signal process function checks for several conditions to be satisfied before stopping the load. Read through the code to understand all of them. Important parameters are the amount of time to take a baseline signal for before looking for changes indicating a sample, the voltage step required to stop a load, the number of points above the threshold that must be measured for a load to register (eliminating false positives due to small amounts of remaining wash solution). To change these values, edit them in the `loading/LoadStopperDriver.py` by changing the default class constants, then delete the cached constants by deleting the file `~/.afl/LoadStopperconfig.json` or whatever the cache is called. It is helpful to print the actual observed values for these criteria when diagnosing load stopping issues. If the load stopping is not sensitive enough, i.e. samples flow right past the sensor without being stopped, try decreasing the voltage threshold or decreasing the number of points that the threshold must be observed for. If the load stopping is too sensitive, i.e. the system stops the load before the sample reaches the flow cell, try increasing these values or increasing the minimum sample load time. 

#### Samples and rinse solution leak out of the catch
- Add a few wraps of teflon thread tape underneath the piston O-ring
- Make sure the piston is aligned in the catch and the clamp arm is closing all the way

### Registering the AFL server as a systemd service 

Once you get everything set up and working well, it is convenient to set up the AFL server as a systemd service so it starts automatically at boot.

1. Write a shell script that activates the virtual environment, moves to the repo directory, and launches the AFL server script:, called `start_afl.sh`

```
cd <path to venv>/bin

source activate  

cd <path to where AFL repo is>/AFL-sample-loader/server_scripts

python LoaderPneumaticJubilee.py
```

2. Set this script to run at startup as a systemd service: 

- cd to `/etc/systemd/system`
- create a new file named afl_server.service: `sudo nano afl_server.service`
- Enter the following contents:
```
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash <absolute path to script from step 1>/start_afl.sh
WorkingDirectory=<absolute path to home directory>
StandardOutput=inherit
StandardError=inherit
Restart=always
User=<name of pi username>
#Group=user_group

[Install]
WantedBy=multi-user.target 
```

3. Reload systemd: `sudo systemctl daemon-reload`
4. Register the service to start at bootup: `sudo systemctl enable afl_server.service`
5. reboot
6. Make sure it came up at boot: `systemctl status afl_server.service`

## Additional resources
Once again, it is highly suggested to get up to speed with the NIST version of this system before replicating what is documented here.

Documentation for the AFL software including overall architecture, web app: [https://pages.nist.gov/AFL-automation/en/add-docs/index.html](https://pages.nist.gov/AFL-automation/en/add-docs/index.html)


