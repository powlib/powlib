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
                             wrclk_prd=(3,"ns"),
                             wrclk_phs=(2,"ns"),
                             rdclk_prd=(10,"ns"),
                             rdclk_phs=(0,"ns"))
                          
    width  = te.wrffd.W
    total  = 1<<width
    depth  = te.wrffd.D
    size   = depth*4
    data   = lambda : randint(0, total-1)
    cycles = lambda : randint(1, size)
    exps   = []
    acts   = []

    # Create and write the data. 
    yield te.wrffd.cycle()
    exps.extend([data() for _ in range(size)])
    for exp in exps: te.wrffd.append(Transaction(wrdata=exp))    
    te.wrffd.append(Transaction())
    
    # Randomly start and stop the monitor; that is,
    # toggle the rdrdy signal.
    yield te.wrffd.cycle(amount=cycles())
    te.rdffm.start()
    yield te.rdffd.cycle(amount=cycles())
    te.rdffm.stop()
    yield te.rdffd.cycle(amount=cycles())
    te.rdffm.start()
    yield te.wrffd.cycle(amount=cycles())
    
    # Just wait a bunch of time to ensure all data has been read
    # out of the asynchronous FIFO.
    yield te.wrffd.cycle(amount=size)
    yield te.rdffd.cycle(amount=size)
    
    for i, exp in enumerate(exps):
        act = te.rdffm[i]
        te.log.info("Exp: {}, Act: {}".format(exp,act))
        if exp!=act: raise TestFailure()
        
    raise TestSuccess()
    
    