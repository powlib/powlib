from cocotb          import coroutine, fork
from cocotb.clock    import Clock
from cocotb.triggers import RisingEdge, ReadOnly, Timer

@coroutine
def start_clock(self, clock, period, phase):
	'''
	Starts a clock.
	clock  = SimHandle of the clock.
	period = Tuple-pair describing the period, for instance  (5,"ns").
	phase  = Tuple-pair describing the phase, for instance (5, "ns").
	'''
	yield Timer(*phase)
	fork(Clock(clock,*period).start())

@coroutine
def start_reset(self, reset, active_mode=1, associated_clock=None, wait_cycles=4, wait_time=(50,"ns")):
	'''
	reset            = SimHandle of the reset.
	active_mode      = Specifies the active state of the reset.
	associated_clock = If set to the SimHandle of an associated clock, the
	                   reset will become inactive after the specified amount
	                   of wait cycles. If set to None, the reset will instead
	                   become inactive after the specified amount of time.
	wait_cycles      = Specifies the amount of clock cycles needed before the 
	                   reset becomes inactive.
    wait_time        = Specifies the amount of time needed before the reset
    				   becomes inactive.
    '''

	reset.value = active_mode

	if associated_clock is not None:
		for each_cycle in range(wait_cycles):
			yield ReadOnly()
			yield RisingEdge(associated_clock)
	else:
		yield Timer(*wait_time)

	reset.value = 1-active_mode


class TestEnvironment(object):
	'''
	Facilitates the creation of the testbench environment. Each
	testbench environment can be used to represent a system in
	terms of its clocks, resets, and the components on the specified
	clock domains.
	'''

	def __init__(self, dut, name=""):
		'''
		dut  = SimHandle of the device-under-test.
		name = String identifier used in logging.
		'''

		self.__dut  = dut
		self.__name = name
		self.__rsts = []
		self.__clks = []

	@property
	def dut(self):
		'''
		Safely returns the dut SimHandle.
		'''
		return self.__dut
	

	def _add_clock(self, clock, period, phase):
		'''
		Adds a clock to the environment.
		clock  = SimHandle of the clock.
		period = Tuple-pair describing the period, for instance  (5,"ns").
		phase  = Tuple-pair describing the phase, for instance (5, "ns").
		'''		
		self.__clks.append((clock, period, phase))

	def _add_reset(self, reset, active_mode=1, associated_clock=None, wait_cycles=4, wait_time=(50,"ns")):
		'''
		Adds a reset to the environment.
		reset            = SimHandle of the reset.
		active_mode      = Specifies the active state of the reset.
		associated_clock = If set to the SimHandle of an associated clock, the
		                   reset will become inactive after the specified amount
		                   of wait cycles. If set to None, the reset will instead
		                   become inactive after the specified amount of time.
		wait_cycles      = Specifies the amount of clock cycles needed before the 
		                   reset becomes inactive.
        wait_time        = Specifies the amount of time needed before the reset
        				   becomes inactive.
		'''
		self.__rsts.append((reset, active_mode, associated_clock, wait_cycles, wait_time))

	@coroutine
	def start():
		'''
		Starts the testbench environment by starting the clocks and resetting all
		the resets.
		'''

		# Start indefinitely each clock.
		for clock, period, phase in self.__clks:
			fork(start_clock(clock, period, phase))

		# Reset the test environment. 
		rst_frks = []
		for reset, active_mode, associated_clock, wait_cycles, wait_time in self.__rsts:
			rst_frks.append(fork(start_reset(reset, active_mode, associated_clock, wait_cycles, wait_time)))

		# Block until all the resets become inactive.
		for rst_frk in rst_frks:
			yield rst_frk.join()




