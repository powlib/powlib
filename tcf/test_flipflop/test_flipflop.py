from cocotb         import test, coroutine, fork
from cocotb.result  import TestFailure, TestSuccess, ReturnValue
from powlib.drivers import FlipflopDriver
from powlib.utils   import TestEnvironment
from random         import randint

test_enables = {'sequential' : True,
                'valid'      : True,
                'random'     : True}

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

    # Add the driver.
    te.ffd = FlipflopDriver(entity=te.dut, clock=te.dut.clk)

    # Start the environment.
    yield te.start()    

    # Return the test environment.
    raise ReturnValue(te)

@test(skip = not test_enables['sequential'])
def test_sequential(dut):
    '''
    Simply writes data sequentially into the flip flop
    and checks for the correct output.
    '''

    # Prepare test environment.
    te = yield perform_setup(dut)

    width = te.ffd.W
    total = 1<<width
    te.log.info("Total transactions <{}>...".format(total))

    # Perform the test.
    te.log.info("Performing the test...")
    for d in range(total):

        yield te.ffd.write(d=d)
        q = yield te.ffd.read()        

        te.log.info("Wrote <{}>, Read <{}>...".format(d,q))
        if d!=q: raise TestFailure()

    te.log.info("Test completed successfully...")
    raise TestSuccess()

@test(skip = not test_enables['valid'])
def test_valid(dut):
    '''
    Checks to see if the valid flag is working properly.
    '''

    # Prepare test environment.
    te = yield perform_setup(dut)

    width = te.ffd.W
    total = 1<<width
    te.log.info("Total transactions <{}>...".format(total))

    # Perform the test.
    te.log.info("Performing the test...")

    prev_vld_q = yield te.ffd.read()        
    for d in range(total):

        vld = randint(0,1)
        yield te.ffd.write(d=d,vld=vld)
        q = yield te.ffd.read()                 
        
        if vld==1:
            prev_vld_q = q
            te.log.info("Valid, Wrote <{}>, Read <{}>...".format(d,q))
            if d!=q: raise TestFailure()
        else:
            te.log.info("Invalid, Wrote <{}>, Read <{}>, Last Valid <{}>...".format(d,q,prev_vld_q))
            if prev_vld_q!=q: raise TestFailure()    
                

    te.log.info("Test completed successfully...")
    raise TestSuccess()

@test(skip = not test_enables['random'])
def test_random(dut):
    '''
    Verifies the flip flop with random data. This test
    also ensures a clock cycle isn't wasted between
    transactions.
    '''

    # Prepare test environment.
    te = yield perform_setup(dut)

    width = te.ffd.W
    total = 1<<width
    te.log.info("Total transactions <{}>...".format(total))    

    # Perform the test.
    te.log.info("Performing the test...")

    prev_d = None
    for each_trans in range(total):

        d = randint(0,total-1) 

        wr = fork(te.ffd.write(d=d))
        rd = fork (te.ffd.read())

        yield wr.join()
        yield rd.join()

        q = rd.retval
        
        if prev_d is not None:
            te.log.info("Previous <{}>, Read <{}>...".format(prev_d,q))
            if prev_d!=q: raise TestFailure()

        prev_d = d

    te.log.info("Test completed successfully...")
    raise TestSuccess()

    

