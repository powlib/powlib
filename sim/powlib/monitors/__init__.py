
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

class WrRdDriverMonitor(BusMonitor):
    '''
    A general purpose monitor that takes a WrRdDriver as a parameter,
    and uses its read method to acquire transactions.
    '''
    
     _signals = []
     
    def __init__(self, wrrddriver, *args, **kwargs):
        '''
        Takes a WrRdDriver as an inputer so that its read
        method can be utilized.
        '''
        BusMonitor.__init__(self, name="", bus_separator="", *args, **kwargs)
        self.__driver = wrrddriver
        
    @coroutine
    def cycle(self, amount=1):
        '''
        Uses the driver cycle method to
        wait a specified amount of clock cycles.
        '''
        self.driver.cycle(amount)
        
    @coroutine
    def read(self):
        '''
        Uses the driver read method to perform
        a read.
        
        *This method can be overloaded if more sophisticated 
         behavior is necessary.
        '''
        value = yield self.driver.read()
        raise ReturnValue(value)
        
    def clear(self):
        '''
        Clears the queue.
        '''
        self._recvQ.clear()
        
    @property
    def in_reset(self):
        '''
        Override the original in_reset property. The other one fails under
        certain conditions. This version assumes the 'z' and 'x' states as
        the reset just being inactive.
        '''
        
        if self._reset is not None:
            reset = self._reset
            active = 1
        elif self._reset_n is not None:
            reset = self._reset_n
            active = 0
        else: raise ValueError("No associated reset.")
        reset_str = str(reset.value)        
        if reset_str=='z' or reset_str=='x' or int(reset.value)==active:
            return True
        return False
        
    @property
    def driver(self):
        '''
        Safely returns the WrRdDriver.
        '''
        return self.__driver
        
    @coroutine
    def _monitor_recv(self):
        '''
        This method is forked as a running coroutine.
        '''

        # Wait until the reset is in a valid state before continuing to
        # the main loop.
        while self.in_reset:
            yield self.cycle()

        # For every cycle, perform a read.
        while True:
            value = yield self.read()
            if value is not None:
                self._recv(transaction=value)

