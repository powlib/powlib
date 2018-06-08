from cocotb         import test, coroutine, fork
from cocotb.result  import TestFailure, TestSuccess, ReturnValue
from powlib.drivers import FFSyncDriver
from powlib.utils   import TestEnvironment
from random         import randint

@coroutine
def perform_setup(dut, aperiod=(5,"ns"), aphase=(0,"ns"), 
                       bperiod=(8,"ns"), bphase=(0,"ns")):
    '''
    Prepares the test environment.
    '''

    # Create the test environment.
    te = TestEnvironment(dut=dut, name="testbench")

    # Add the clocks and resets.
    te._add_clock(clock=te.dut.aclk, period=aperiod, phase=aphase)
    te._add_clock(clock=te.dut.bclk, period=bperiod, phase=bphase)
    te._add_reset(reset=te.dut.arst, associated_clock=te.dut.aclk)
    te._add_reset(reset=te.dut.brst, associated_clock=te.dut.bclk)

    # Add the driver.
    te.ffsd = FFSyncDriver(entity=te.dut, aclock=te.dut.aclk, bclock=te.dut.bclk)

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)  

@test(skip = False)
def test_(dut):
    '''
    This is not complete.
    '''

    # Prepare the test environment.
    te = yield perform_setup(dut)

    te.log.info("dfgdfgdfgdf")
    raise TestSuccess()
    pass