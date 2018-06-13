
from cocotb          import coroutine
from cocotb.monitors import BusMonitor
from cocotb.triggers import ReadOnly, RisingEdge

def _in_reset(bus_monitor, active=1):
    '''
    Intended to replace the in_reset property of BusMonitor, so that it
    interprets invalid states of the reset as inactive.
    '''

    reset_str = str(bus_monitor._reset.value)        
    if reset_str=='z' or reset_str=='x' or int(bus_monitor._reset.value)==active:
        return True
    return False

class FlipflopMonitor(BusMonitor):
    '''
    A simple monitor for powlib_flipflop. 
    '''

    _signals = ['q']
    
    def __init__(self, *args, **kwargs):
        '''
        Constructor is overloaded only to ensure the correct
        parameters are used such that the Bus is configured properly.
        '''
        BusMonitor.__init__(self, name="", bus_separator="", *args, **kwargs)

    def clear(self):
        '''
        Clears the queue.
        '''

        self._recvQ.clear()

    @coroutine
    def cycle(self):
        '''
        Waits a cycle.
        '''

        yield ReadOnly()             # Switches to simulator until all deltas have completed.
        yield RisingEdge(self.clock) # Switches to simulator until the rising edge of the clock.

    @coroutine
    def _monitor_recv(self):

        # Wait until the reset is in a valid state before continuing to
        # the main loop.
        while _in_reset(bus_monitor=self):
            yield self.cycle()

        # For every cycle, sample q.
        while True:

            q = int(self.bus.q.value)
            self._recv(transaction=q)

            yield self.cycle()



