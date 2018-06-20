from cocotb          import test, coroutine, fork
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Namespace, Transaction
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

    # Add the pipe namespace to the environment.
    te.sfd=SfifoDriver(entity=te.dut, clock=te.dut.clk)

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)

@test()
def test_fifo(dut):

    te = yield perform_setup(dut)
