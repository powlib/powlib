
from cocotb.monitors import BusMonitor

class FlipflopMonitor(BusMonitor):

    _signals = ['q']
    
    def __init__(self, *args, **kwargs):

        BusMonitor.__init__(self, name="", bus_separator="", *args, **kwargs)

    @coroutine
    def _monitor_recv(self):

        # Wait until the reset is in a valid state before continuing to
        # the main loop.
        reset_str = str(self.reset.value)        
        while reset_str=='Z' or reset_str=='X' or int(self.reset.value)==1:
            yield Edge(self.reset)
            reset_str = str(self.reset.value)

        yield ReadOnly()
        yield RisingEdge(self.clock)

        while True: pass

