from cocotb                 import coroutine
from cocotb.triggers        import RisingEdge, ReadOnly, Lock
from cocotb.drivers			import BusDriver as OriginalBusDriver

class BusDriver(OriginalBusDriver):

    def __init__(self, entity, name, clock, *args, **kwargs):
    	'''
    	See the OriginalBusDriver definition for documentation.
    	'''

        OriginalBusDriver.__init__(self, *args, **kwargs)
        self.bus = Bus(self.entity, self.name, self._signals,
                       self._optional_signals, *args, **kwargs)	

class FlipflopDriver(BusDriver):
	'''
	Really simple cocotb driver.
	'''

	_signals = ['d','q']
	_optional_signals = ['vld']