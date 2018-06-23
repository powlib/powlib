from cocotb          import test, coroutine, fork
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Transaction
from powlib.drivers  import SfifoDriver
from powlib.monitors import SfifoMonitor
from powlib.utils    import TestEnvironment
from random          import randint

@coroutine
def perform_setup(dut, wrclk_prd, wrclk_phs, rdclk_prd, rdclk_phs):
    '''
    Prepares the test environment.
    '''

    # Create the test environment.
    te = TestEnvironment(dut=dut.dut, name="testbench")

    # Add the clocks and resets.
    te._add_clock(clock=te.dut.wrclk, period=wrclk_prd, phase=wrclk_phs)
    te._add_reset(reset=te.dut.wrrst, associated_clock=te.dut.wrclk)
    te._add_clock(clock=te.dut.rdclk, period=rdclk_prd, phase=rdclk_phs)
    te._add_reset(reset=te.dut.rdrst, associated_clock=te.dut.rdclk)

    # Add the aynchronous fifo driver to the environment. The
    # asynchronous FIFO driver is regarded as two synchronous FIFOs,
    # one for each domain.
    te.wrffd = SfifoDriver(entity=te.dut, clock=te.dut.wrclk)
    te.rdffd = SfifoDriver(entity=te.dut, clock=te.dut.rdclk)
    te.rdffm = SfifoMonitor(wrrddriver=te.rdffd, reset=te.dut.rdrst)

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)
    
@test()
def test_afifo(dut):
    '''
    Performs a basic test of the asynchronous FIFO.
    '''

    # Create the test environment.
    te = yield perform_setup(dut=dut,
                             wrclk_prd=(5,"ns"),
                             wrclk_phs=(2,"ns"),
                             rdclk_prd=(2,"ns"),
                             rdclk_phs=(0,"ns"))
                          
    width = te.wrffd.W
    total = 1<<width
    depth = te.wrffd.D
    size  = depth*4
    data  = lambda : randint(0, total-1)
    exps  = []
    acts  = []

    # Write the data.    
    exps.extend([data() for _ in range(size)])
    for exp in exps: te.wrffd.append(Transaction(wrdata=exp))    
    te.wrffd.append(Transaction())
    
    # Wait an arbitrary amount of time.
    yield te.wrffd.cycle(amount=20)
    
    # Start the reading in the monitor.
    te.rdffm.start()
    
    # Wait another arbitrary amount of time.
    yield te.rdffd.cycle(amount=20)
    
    # Stop the monitor for a while. What this really means is that
    # the rdrdy signal is placed in a low state after one more word
    # is read from the asynchronous FIFO.
    te.rdffm.stop()
    
    yield te.rdffd.cycle(amount=10)
    