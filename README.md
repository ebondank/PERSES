# PERSES
Python 3 Water System Simulation using EPANET, extended to simulate failure component.

**Requirements:** 
- Windows Vista/7/8/10, EPANET .DLL will require service packs on Vista and 7
- Python 3.5 (may work on others, only tested for 3.5 currently)        
- EPANET network (Not provided in this distribution)


**To simulate and existing system:**
1. Modify PERSES_configuration.py to work for the pumps defined in your network (Pipes automatically discovered by system)
2. Confirm that the temperature projections, exposure-failure distributions, and simulation types are correct
3. In Command prompt:
    *"{python3.5 path} PERSES.py"*
4. Simulation takes a moderate amount of time depending on parameters
5. Simulation progress at each year is printed to console
