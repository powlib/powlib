from cocotb          import test, coroutine, fork
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Transaction
from powlib.drivers  import CntrDriver
from powlib.monitors import FlipflopMonitor
from powlib.utils    import TestEnvironment
from random          import randint

@coroutine
def perform_setup(dut):
    '''
    Prepares the test environment.
    '''

    # Create the test environment.
    te = TestEnvironment(dut=dut, name="testbench")

    # Add the clocks and resets.
    te._add_clock(clock=dut.clk, period=(5,"ns"))
    te._add_reset(reset=dut.rst, associated_clock=dut.clk)

    # Add the synchronous fifo driver to the environment.
    te.cd = CntrDriver(entity=dut.cntr_inst, clock=dut.clk)                               # Counter Driver
    te.cm = FlipflopMonitor(entity=dut.cntr_inst.cntr_inst, clock=dut.clk, reset=dut.rst) # Counter Monitor
    te.em = FlipflopMonitor(entity=dut.encode_inst, clock=dut.clk, reset=dut.rst)         # Gray-encoded Monitor
    te.dm = FlipflopMonitor(entity=dut.decode_inst, clock=dut.clk, reset=dut.rst)         # Gray-decoded Monitor
    
    #te.sfd=SfifoDriver(entity=te.dut, clock=te.dut.clk)

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)
    
@test()
def test_gray(dut):

    te = yield perform_setup(dut)
    
    width = te.cd.W
    total = 1<<width
    itrs  = total*8
    edly  = 1
    ddly  = 2
    
    te.cd.append(Transaction(adv=1))
    yield te.cd.cycle(amount=itrs)
    
    for i in range(len(te.cm)-ddly):
        cntr = te.cm[i]
        en   = te.em[i+edly]
        de   = te.dm[i+ddly]
        te.log.info("Cntr: {}, En: {}, De: {}".format(cntr,en,de))
        if cntr!=de: raise TestFailure()
    raise TestSuccess()