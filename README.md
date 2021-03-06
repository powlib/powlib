# Introduction

This repo consists of the submodules that define the powlib library. The major components of the library include *hdl*, *sim*, and *tcf*. hdl defines common hardware descriptions necessary for the developemnt of digital circuit designs on FPGAs. sim defines verification sources roughly inspired by the Universal Verification Methodology, albeit implemented in Python. tcf contains all the regression tests. More information will be added as powlib is developed.

# Plans

This section will briefly describe some of the future additions to this library, including some of the major plans. The descriptions will also change as time goes.

I plan on working on my implementation of a contention-free NoC---basically, a simple NoC that utilizes a TDM-based arbitration to ensure deterministic throughput and latency,

- **tcf**: Test case files will be added as more IP gets added. 
- **sim**: The simulation library will continue to be developed.
- **hdl**: The HDL library will continue to be developed.
    - **std**: Probably going to call it quits with what is already here, but make small changes and additions will be made as they become needed. 
    - **fifo**: Created my own implementations of fifos. Future implementations will be added in the future.
        - **Synchronous**: A simple fifo that assumes writing and reading interfaces share the same clock domain. Recently changed such that block RAM is inferred.
        - **Asynchronous**: A fifo that's built to allow clock domain crossings. It utilizes the typical gray-coding and flip-flop synchronization to safely cross the fifo's pointers. Recently changed such that block RAM is inferred.
        - **Swiss**: My swiss fifo combines the pipe and both fifos into a single, convenient module. In effort not to over complicate it, this will likely be left alone.
    - **ip**: Defined the powlib bus interface.
        - **ipram**: RAM accessible through the powlib bus interface.
        - **ipmaxi**: Converts the powlib bus interface to the Master AXI interface.
        - **ipsaxi**: Converts the Slave AXI interface to the powlib bus interface.
    - **bus**: Defines some of the common interconnect architectures.
        - **Crossbar**: Pipelined crossbar that utilizes the powlib bus interface.
        - **Standard Bus**: Will put this on hold so that I can get a head start on the TDM-based NoC.
    - **noc**: The ultimate goal is to start implementing Network-on-Chip (NoC) interconnect architectures suitable for FPGAs and compare them to standard bus-based interconencts.
        - **noc_worm**: *best effort services (bes)* noc will be created, implementing wormhole style routing. 
        - **noc_tdm**: *guaranteed services (gs)* noc will be created, implementing time-division-multiplexing (tdm) style routing. Inspired by the Æthereal noc.

# Prerequisites 

It should be noted most of these prerequisites are optional. The **hdl** submodule references the powlib hardware descriptions, so any simulator or EDA tool that support Verilog 2001 can build the sources. Most of the prerequisites are necessary to run the powlib test cases and simulation library. 

- **cocotb**: This is already included and only necessary for running the test case files. Cocotb provides a python layer that can interface with a simulator, provided that the simulator of choice implements an API supported by cocotb.
- **Anaconda2**: Only python 2.7 is currently necessary to run the simulation library and test cases, however more tools from Anaconda2 will be utilized in the future.
- **Icarus**: Simulations are all done with Icarus Verilog.
- **Msys2**: This is only needed for Windows. 
        
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

It is worth noting simply downloading the release through GitHub will not include the submodules.

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

