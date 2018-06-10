from cocotb         import test, coroutine, fork
from cocotb.result  import TestFailure, TestSuccess, ReturnValue
from powlib         import Transaction
from powlib.drivers import FFSyncDriver
from powlib.utils   import TestEnvironment
from random         import randint

@coroutine
def perform_setup(dut, aperiod=(8,"ns"), aphase=(0,"ns"), 
                       bperiod=(5,"ns"), bphase=(0,"ns")):
    '''
    Prepares the test environment.
    xperiod = Period of the xclock as a tuple-pair, where x is either the 
              a or b domains.
    xphase  = Phase of the xclock as a tuple-pair, where x is either the a 
              or b domains.
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
def test_sequential(dut):
    '''
    Simply writes data sequentially into the flip flop syncrhonizer
    and checks for the correct output.

    ***This test isn't really thought out. A better should eventually
       be created instead.
    '''

    # Prepare the test environment.
    te = yield perform_setup(dut)

    width = te.ffsd.W
    total = 1<<width
    te.log.info("Total transactions <{}>...".format(total))

    # Perform the test.
    te.log.info("Performing the test...")

    te.log.info("Writing out the non-zero, sequential data...")
    ds = [value+1 for value in range(total-1)]
    for d in ds: te.ffsd.append(transaction=Transaction(d=d,vld=1))

    prev_q = 0
    q      = 0
    for d in ds:

        # Keep reading until a different value is seen.
        while prev_q==q:             
            q = yield te.ffsd.read()            

        te.log.info("D=<{}>, Q=<{}>...".format(d,q))
        if d!=q: raise TestFailure()

        prev_q = q

    te.log.info("Test completed successfully...")
    raise TestSuccess()