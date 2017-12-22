# PERSES
Python 3 Water System Simulation using EPANET, extended to simulate failure component.
Requirements: Windows Vista/7/8/10, EPANET .DLL will require service packs on Vista and 7
               Python 3.5 (may work on others, only tested for 3.5 currently)
               EPANET network (Not provided in this distribution)
# To simulate and existing system:
     Modify PERSES_configuration.py to work for the pumps defined in your network (Pipes automatically discovered by system)
     Confirm that the temperature projections, exposure-failure distributions, and simulation types are correct
     In Command prompt:
         "{python3.5 path} PERSES.py"
     Simulation takes a moderate amount of time depending on parameters
     Values printed to console are the year interval from 0 the simulation is at
