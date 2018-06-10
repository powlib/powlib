from cocotb                 import coroutine
from cocotb.bus             import Bus
from cocotb.result          import ReturnValue
from cocotb.triggers        import RisingEdge, ReadOnly, Lock
from cocotb.drivers         import BusDriver

class FlipflopDriver(BusDriver):
    '''
    cocotb driver for powlib_flipflop.
    '''

    _signals          = []
    _wrsignals        = ['d']
    _rdsignals        = ['q']
    _optional_signals = ['vld']
    _default_values   = {'d':0,'vld':0}

    def __init__(self, entity, name="", default_values=_default_values, *args,**kwargs):
        '''
        See the BusDriver definition for more information on the inputs.
        '''

        BusDriver.__init__(self, entity=entity, name=name, *args, **kwargs)

        # Create separate write and read buses.
        self.__wrbus = Bus(entity=entity, 
                           name="", # Intentionally done this way.
                           signals=FlipflopDriver._wrsignals, 
                           optional_signals=FlipflopDriver._optional_signals, 
                           bus_separator="")
        self.__rdbus = Bus(entity=entity, 
                           name="", # Intentionally done this way.
                           signals=FlipflopDriver._rdsignals, 
                           bus_separator="")

        # The Bus assigned in the BusDriver shall be the write Bus.
        self.bus = self.__wrbus

        # Set default values
        self.__wrbus.d.setimmediatevalue(default_values['d'])
        self.__wrbus.vld.setimmediatevalue(default_values['vld'])

    @coroutine
    def _driver_send(self, transaction, sync=True):
        '''
        *** Needs to be overloaded to prevent BusDriver from referencing the wrong operation
            and bus.
        *** The sync flag is intentionally ignored so that all transactions are synchronized.
        '''
        yield self.write(d=transaction.d,vld=transaction.vld)

    @property
    def W(self):
        '''
        Gets the specified width.
        '''
        return int(self.entity.W.value)

    @property
    def EVLD(self):
        '''
        Gets the valid enable flag.
        '''
        return int(self.entity.EVLD.value)

    @property
    def wrbus(self):
        '''
        Returns the write Bus.
        '''
        return self.__wrbus
    
    @property
    def rdbus(self):
        '''
        Returns the read Bus.
        '''
        return self.__rdbus

    @coroutine
    def cycle(self):
        '''
        Waits a single clock cycle.
        '''

        yield ReadOnly()
        yield RisingEdge(self.clock)           

    @coroutine
    def write(self, d=0, vld=1, sync=True):
        '''
        Writes new data to the flip flop and then waits 
        untils the data is registered.
        '''
        
        self.__wrbus.d.value   = d
        self.__wrbus.vld.value = vld
        if sync: yield self.cycle()   

    @coroutine
    def read(self, sync=True):
        '''
        Reads the output of the flip flop and then waits 
        until the rise of the next clock cycle.
        '''
        
        value = int(self.__rdbus.q.value)
        if sync: yield self.cycle()
        raise ReturnValue(value)

class FFSyncDriver(FlipflopDriver):
    '''
    cocotb driver for powlib_ffsync.
    '''

    def __init__(self, aclock, bclock, *args, **kwargs):
        '''
        aclock = SimHandle of aclock.
        bclock = SimHandle of bclock.
        '''
        FlipflopDriver.__init__(self, clock=aclock, *args, **kwargs)
        self.__bclock = bclock

    @property
    def S(self):
        '''
        Gets the number of b stages.
        '''
        return int(self.entity.S.value)


    @property
    def aclock(self):
        '''
        Basically allows the user to acquire aclock, without
        knowing it's named clock.
        '''
        return self.clock    

    @property
    def bclock(self):
        '''
        Safely return the bclock SimHandle.
        '''
        return self.__bclock

    @coroutine
    def read(self):
        '''
        Reads the output of the flip flop and then waits 
        until the rise of the next clock cycle.
        '''

        yield ReadOnly()
        value = int(self.rdbus.q.value)
        yield RisingEdge(self.bclock)
        raise ReturnValue(value)      

class PipeDriver(FlipflopDriver):
    '''
    cocotb driver for powlib_pipe.
    '''

    @property
    def S(self):
        '''
        Gets the number of stages.
        '''
        return int(self.entity.S.value)
