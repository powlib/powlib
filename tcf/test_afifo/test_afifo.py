from cocotb          import test, coroutine, fork
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Transaction
from powlib.drivers  import SfifoDriver
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

    # Add the synchronous fifo driver to the environment.
    #te.sfd=AfifoDriver(entity=te.dut, clock=te.dut.clk)

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