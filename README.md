# Introduction

This repo consists of the submodules that define the powlib library. The major components of the library include *hdl*, *sim*, and *tcf*. hdl defines common hardware descriptions necessary for the developemnt of digital circuit designs on FPGAs. sim defines verification sources roughly inspired by the Universal Verification Methodology, albeit implemented in Python. tcf contains all the regression tests.

# File Structure

The following describes the file structure of this library.

+ cocotb --- Submodule that contains cocotb, a dependency of the regression tests.
+ hdl --- Submodule that contains the powlib hardware description library. 
+ sim --- Submodule that contains the powlib simulation library.
+ tcf --- Submodule that contains all the test regressions.

# Contact

Author: Andrew Powell
Contact: andrewandrepowell2@gmail.com
Blog: https://hackaday.io/andrewandrepowell

