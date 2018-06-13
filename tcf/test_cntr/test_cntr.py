from cocotb          import test, coroutine, fork
from cocotb.triggers import Timer
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Transaction, Namespace
from powlib.drivers  import CntrDriver
from powlib.monitors import FlipflopMonitor
from powlib.utils    import TestEnvironment
from random          import randint


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
        te.c = Namespace(d=CntrDriver(entity=te.dut, clock=te.dut.clk),
                         m=FlipflopMonitor(entity=te.dut.cntr_inst, clock=te.dut.clk, 
                                           reset=te.dut.rst))

        # Start the environment.
        rc = fork(te.start())

        # Add the objects to their associated lists.
        tes.append(te)
        rcs.append(rc)

    # Yield on the running coroutines.
    for rc in rcs: yield rc.join()

    # Return the test environments.
    raise ReturnValue(tes)

@test(skip=False)
def test_advance(dut):

    # Prepare the test envrionments.
    tes = yield perform_setup(dut)    

    for te in tes:

        width = te.c.d.W
        aval  = te.c.d.X
        init  = te.c.d.INIT
        total = width*2

        te.c.d.append(Transaction(adv=1))



        pass

    yield Timer(10000,"ns")