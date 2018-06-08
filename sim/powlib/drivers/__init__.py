from cocotb                 import coroutine
from cocotb.triggers        import RisingEdge, ReadOnly, Lock
from cocotb.drivers			import BusDriver as OriginalBusDriver

class BusDriver(OriginalBusDriver):
	'''
	This BusDrive was created to extend the functionality
	of the original BusDriver defined in cocotb.
	'''

    def __init__(self, entity, name, clock, *args, **kwargs):
    	'''
    	See the OriginalBusDriver definition.
    	'''

        OriginalBusDriver.__init__(self, entity, name, clock)
        self.bus = Bus(self.entity, self.name, self._signals,
                       self._optional_signals, *args, **kwargs)	

class FlipflopDriver(BusDriver):
	'''
	Really simple cocotb driver.
	'''

	_signals          = ['d','q']
	_optional_signals = ['vld']
	_default_values   = {'d':0,'vld':0}

	def __init__(self, *args, default_values=_default_values, **kwargs):
		'''
		See the BusDriver definition.
		'''

		BusDriver.__init__(self, *args, bus_separator="", **kwargs)

		# Set default values
		self.bus.d.setimmediatevalue(default_values['d'])
		self.bus.vld.setimmediatevalue(default_values['vld'])

	@coroutine
	def write(self, d=0, vld=1):
		'''
		Writes new data to the flip flop.
		'''

		self.bus.d.value   = d
		self.bus.vld.value = vld

		yield ReadOnly()
		yield RisingEdge(self.clock)

	def read(self):
		'''
		Read the output of the flip flop.
		'''

		return int(self.bus.q.value)