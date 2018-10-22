# Introduction

This repo consists of the submodules that define the powlib library. The major components of the library include *hdl*, *sim*, and *tcf*. hdl defines common hardware descriptions necessary for the developemnt of digital circuit designs on FPGAs. sim defines verification sources roughly inspired by the Universal Verification Methodology, albeit implemented in Python. tcf contains all the regression tests. More information will be added as powlib is developed.

# Plans

This section will briefly describe some of the future additions to this library, including some of the major plans. The descriptions will also change as time goes.

Currently, the next task is to build a hardware test for the crossbar. The standard bus will be implemented afterward.

- **tcf**: Test case files will be added as more IP gets added.
- **sim**: The simulation library will continue to be developed.
- **hdl**: The HDL library will continue to be developed.
    - **std**: Probably going to call it quits with what is already here, but make small changes and additions will be made as they become needed. 
    - **fifo**: Created my own implementations of fifos. Future implementations will be added in the future.
        - **Synchronous**: A simple fifo that assumes writing and reading interfaces share the same clock domain. This is pretty much complete, though different implementations will be explored in the future.
        - **Asynchronous**: A fifo that's built to allow clock domain crossings. It utilizes the typical gray-coding and flip-flop synchronization to safely cross the fifo's pointers. Similar to the synchronous, it's done though in the future other implementations will be explored.
        - **Swiss**: My swiss fifo combines the pipe and both fifos into a single, convenient module. In effort not to over complicate it, this will likely be left alone.
    - **bus**: Development is currently occurring in this section.
        - **Crossbar**: Recently finished the crossbar. Will need to redo the test bench since it's rather confusing. Will probably build a hardware test first.
        - **Standard Bus**: This is the next target, a simple bus-based interconnect where only a single write-read interface pair can access to the bus.
    - **noc**: The ultimate goal is to start implement network-on-chip (noc) interconnect architectures suitable for FPGAs and compare them to standard bus-based interconencts.
        - **noc_worm**: *best effort services (bes)* noc will be created, implementing wormhole style routing. 
        - **noc_tdm**: *guaranteed services (gs)* noc will be created, implementing time-division-multiplexing (tdm) style routing. Inspired by the Æthereal noc.

# File Structure

The following describes the file structure of this library.

+ cocotb --- Submodule that contains cocotb, a dependency of the regression tests.
+ hdl --- Submodule that contains the powlib hardware description library. 
+ sim --- Submodule that contains the powlib simulation library.
+ tcf --- Submodule that contains all the test regressions.

# Downloading / Cloning

Downloading this repo will not include the repos the submodules refer to as part of the zip file. Instead, the user will have to either download the repos separately or perform a recursive clone. The latter method is recommended. A recursive clone is performed with the following.

````
git clone https://github.com/powlib/powlib.git --recursive
````

# Contact

Author: Andrew Powell
Contact: andrewandrepowell2@gmail.com
Blog: https://hackaday.io/andrewandrepowell

# References

Æthereal Network on Chip: Concepts, Architectures, and Implementations
- *Authors*: Kess Goossens, John Dielissen, and Andrei Radulescu
- *Lab*: Philips Research Laboratories
- *Journal*: IEEE Design & Test of Computers
- *Date*: October 2005

