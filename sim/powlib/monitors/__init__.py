
from cocotb          import coroutine
from cocotb.monitors import BusMonitor
from cocotb.triggers import ReadOnly, RisingEdge, Event
from cocotb.result   import ReturnValue

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
        self.__driver = wrrddriver
        BusMonitor.__init__(self, entity=wrrddriver.entity, 
                                  clock=wrrddriver.clock,
                                  name="", 
                                  bus_separator="", 
                                  *args, **kwargs)
        
    @coroutine
    def cycle(self, amount=1):
        '''
        Uses the driver cycle method to
        wait a specified amount of clock cycles.
        '''
        yield self.driver.cycle(amount)
        
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
            reset  = self._reset
            active = 1
        elif self._reset_n is not None:
            reset  = self._reset_n
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

class SfifoMonitor(WrRdDriverMonitor):
    '''
    Monitors the reading interface of a powlib_sfifo.
    '''

    def __init__(self, *args, **kwargs):
        '''
        This constructor simply creates the state and event objects needed
        to implement the read method defined for the monitor.
        '''
        self.__state = "stopped"
        self.__evt   = Event()
        WrRdDriverMonitor.__init__(self, *args, **kwargs)

    def start(self):
        '''
        Indicate to the read method it should start its operation.
        '''
        self.__evt.set()
        
    def stop(self):
        '''
        After one more read, stop further read transactions.
        '''
        self.__state = "stopped"

    @coroutine
    def read(self):
        '''
        Implements the behavior of the monitor's read method. Initially,
        the monitor is in a stopped state, until the user decides to start it.
        Once started, the read method will call the drivers read method that 
        sets the rdrdy signal and set the state of the monitor to started. While
        in its started state, the monitor will call the driver's read method, 
        without any arguments, indicating it should simply read whenever the rdvld 
        is high.
        '''
        
        if self.__state=="stopped":
            '''
            Stopped state indicates the monitor is waiting.
            '''
            yield self.driver.read(rdrdy=0)
            yield self.__evt.wait()
            self.__evt.clear()
            self.__state = "started"
            yield self.cycle()
            value = yield self.driver.read(rdrdy=1)
            raise ReturnValue(value)
            
        elif self.__state=="started":
            '''
            Once started, the monitor will continue to read valid data from
            the read interface.
            '''
            value = yield self.driver.read()
            raise ReturnValue(value)
            
        else: raise ValueError("Unknown state occurred.")
            

    