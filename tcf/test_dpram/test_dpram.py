from cocotb          import test, coroutine, fork
from cocotb.triggers import Timer
from cocotb.result   import TestFailure, TestSuccess, ReturnValue
from powlib          import Transaction, Namespace
from powlib.drivers  import DpramDriver
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

        # Add the driver and monitor. 
        te.c = Namespace(d=DpramDriver(entity=te.dut, clock=te.dut.clk))

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
def test_access(dut):
    '''
    This basic test simply involves writing data 
    and reading random data into the ram.
    '''

    # Prepare the test envrionments.
    tes = yield perform_setup(dut)

    # Implement the test coroutine.
    @coroutine
    def test(te):        

        width = te.c.d.W        
        depth = te.c.d.D
        biten = te.c.d.EWBE
        total = 1<<width
        rval  = lambda : randint(0,total-1)
        ens   = {'wrvld':1} if biten==0 else {'wrbe':(1<<width)-1}

        # Write in random values.
        exps = []
        for idx in range(depth):             
            exp = rval()
            exps.append(exp)            
            yield te.c.d.write(wridx=idx, wrdata=exp, **ens)

        # Read random values.
        for idx, exp in enumerate(exps):
            act = yield te.c.d.read(rdidx=idx)
            te.log.info("Idx: {}. Expected: {}, Actual: {}...".format(idx,exp,act))
            if exp!=act: raise ReturnValue(False)

        raise ReturnValue(True)    

    # Run the test for both counters.
    rcs = [fork(test(te)) for te in tes]
    for rc in rcs: yield rc.join()    

    # Check if any of the coroutines failed.
    if any(rc.retval==False for rc in rcs): raise TestFailure()

    raise TestSuccess()    