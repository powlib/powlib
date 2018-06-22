from cocotb          import test, coroutine, fork
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Transaction
from powlib.drivers  import SfifoDriver
from powlib.utils    import TestEnvironment
from random          import randint

@coroutine
def perform_setup(dut):
    '''
    Prepares the test environment.
    '''

    # Create the test environment.
    te = TestEnvironment(dut=dut.dut, name="testbench")

    # Add the clocks and resets.
    te._add_clock(clock=te.dut.clk, period=(5,"ns"))
    te._add_reset(reset=te.dut.rst, associated_clock=te.dut.clk)

    # Add the synchronous fifo driver to the environment.
    te.sfd=SfifoDriver(entity=te.dut, clock=te.dut.clk)

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)

@test()
def test_fifo(dut):

    te = yield perform_setup(dut)

    width = te.sfd.W
    total = 1<<width
    depth = te.sfd.D
    size  = depth*4
    data  = lambda : randint(0, total-1)
    exps  = []
    acts  = []

    # Write the data.    
    exps.extend([data() for _ in range(size)])
    for exp in exps: te.sfd.append(Transaction(wrdata=exp))    
    te.sfd.append(Transaction())

    # Wait some amount of clock cycles.
    yield te.sfd.cycle(amount=depth+4)

    # Read a bunch of data.
    act = yield te.sfd.read(rdrdy=1)
    acts.append(act)
    for _ in range(size-1): 
        act = yield te.sfd.read()
        acts.append(act)    
    yield te.sfd.read(rdrdy=0)

    # Verify data.
    for act, exp in zip(acts,exps):
        te.log.info("Act: {}, Exp: {}".format(act, exp))
        if act!=exp: raise TestFailure()

    raise TestSuccess()






