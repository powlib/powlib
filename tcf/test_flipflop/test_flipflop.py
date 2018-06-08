import random
import logging

from cocotb import test, coroutine
from cocotb.result import TestFailure, TestSuccess, ReturnValue

from powlib.drivers import FlipflopDriver
from powlib.utils   import TestEnvironment

@coroutine
def perform_setup(dut):
    '''
    Prepares the test environment.
    '''

    # Create the test environment.
    te = TestEnvironment(dut=dut, name="testbench")

    # Add the clocks and resets.
    te._add_clock(clock=te.dut.clk, period=(5,"ns"))
    te._add_reset(reset=te.dut.rst, associated_clock=te.dut.clk)

    # Add the driver.
    te.ffd = FlipflopDriver(entity=te.dut, clock=te.dut.clk)

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)

@test(skip = False)
def test_flipflop_0(dut):
    '''
    Description
        Simply writes data sequentially into the flip flop
        and checks for the correct output.
    '''

    # Prepare test environment.
    te = yield perform_setup(dut)


    width = te.ffd.W
    total = 1<<width
    te.log.info("Total transactions <{}>...".format(total))

    for d in range(total):
        te.log.info("Writing <{}>...".format(d))
        yield te.ffd.write(d=d)
        q = te.ffd.read()
        te.log.info("Read <{}>...".format(q))
        if d!=q: raise TestFailure()

    te.log.info("Test completed successfully...")
    raise TestSuccess()
    

