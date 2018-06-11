from cocotb         import test, coroutine, fork
from cocotb.result  import TestFailure, TestSuccess, ReturnValue
from powlib         import Transaction
from powlib.drivers import FlipflopDriver
from powlib.utils   import TestEnvironment
from random         import randint


@coroutine
def perform_setup(dut):
    '''
    Prepares the test environments.
    '''

    T   = 2  # Number of counters to test. 
    tes = [] # List of test environments.
    rcs = [] # List of running coroutines.

    # Configure each test environment.
    for each_cntr in range(T):

        # Create the test environment.
        te = TestEnvironment(dut=getattr(dut,"dut{}".format(each_cntr)), 
                             name="testbench{}".format(each_cntr))

        # Add the clocks and resets.
        te._add_clock(clock=te.dut.clk, period=(5,"ns"))
        te._add_reset(reset=te.dut.rst, associated_clock=te.dut.clk)

        # Add the driver and monitor.

        # Start the environment.
        rc = fork(te.start())

        # Add the objects to their associated lists.
        tes.append(te)
        rcs.append(rc)

    # Yield on the running coroutines.
    for rc in rcs: yield rc.join()

    # Return the test environments.
    raise ReturnValue(te)

@test(skip=False)
def test_advance(dut):

    # Prepare the test envrionments.
    tes = yield perform_setup(dut)