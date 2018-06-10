from cocotb          import test, coroutine, fork
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Namespace, Transaction
from powlib.drivers  import PipeDriver
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
    te._add_clock(clock=te.dut.clk, period=(5,"ns"))
    te._add_reset(reset=te.dut.rst, associated_clock=te.dut.clk)

    # Add the pipe namespace to the environment.
    te.p = Namespace(d=PipeDriver(entity=te.dut, clock=te.dut.clk),
                     m=FlipflopMonitor(entity=te.dut, clock=te.dut.clk, reset=te.dut.rst))    

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)

@test(skip=False)
def test_sequential(dut):
    '''
    Simply writes data sequentially into the flip flop
    and checks for the correct output.
    '''

    # Prepare test environment.
    te = yield perform_setup(dut)    

    width  = te.p.d.W
    stages = te.p.d.S
    total  = 1<<width
    te.log.info("Total transactions <{}>, total stages <{}>...".format(total,stages))        

    # Perform the test.
    te.log.info("Performing the test...")    

    # Write out the randomly generated values.
    ds = [randint(0,total-1) for _ in range(total)]
    for d in ds: te.p.d.append(transaction=Transaction(d=d,vld=1))

    # Wait until all the stages has been collected by the monitor.
    for _ in range(total+stages): yield te.p.d.cycle()

    # Verify the results.
    for idx, d in enumerate(ds):
        q = te.p.m[idx+stages]
        te.log.info("Wrote <{}>, Read <{}>...".format(d,q))
        if d!=q: raise TestFailure()        

    te.log.info("Test completed successfully...")
    raise TestSuccess()

