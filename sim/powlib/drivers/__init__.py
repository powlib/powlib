from cocotb                 import coroutine
from cocotb.bus             import Bus
from cocotb.result          import ReturnValue
from cocotb.triggers        import RisingEdge, ReadOnly, Lock
from cocotb.drivers         import BusDriver

class WrRdDriver(BusDriver):

    _signals          = []
    _wrsignals        = []
    _rdsignals        = []
    _optional_signals = []
    _default_values   = {}

    def __init__(self, entity, name="", default_values=None, *args,**kwargs):
        '''
        See the BusDriver definition for more information on the inputs.
        '''

        BusDriver.__init__(self, entity=entity, name=name, *args, **kwargs)

        # Create separate write and read buses.
        self.__wrbus = Bus(entity=entity, 
                           name="", # Intentionally done this way.
                           signals=self._wrsignals, 
                           optional_signals=self._optional_signals, 
                           bus_separator="")
        self.__rdbus = Bus(entity=entity, 
                           name="", # Intentionally done this way.
                           signals=self._rdsignals, 
                           bus_separator="")

        # The Bus assigned in the BusDriver shall be the write Bus.
        self.bus = self.__wrbus

        # Set default values.
        if default_values is None: 
            self.__default_values = self._default_values
        else:
            self.__default_values = default_values
        self.set_defaults()

    def set_defaults(self):
        '''
        Method for setting the defaults to the wrBus.
        '''
        for sig, value in self.__default_values.items():
            getattr(self.__wrbus, sig).setimmediatevalue(value)

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
    def cycle(self, amount=1):
        '''
        Waits a single clock cycle, by default.
        Specifying the amount causes a wait for
        multiple cycles.
        '''

        for _ in range(amount):
            yield ReadOnly()
            yield RisingEdge(self.clock)    

    @coroutine
    def write(self):
        '''
        Should be implemented by the user. The arguments should be 
        the name of the input signals.
        ''' 
        raise NotImplemented("This method should be implemented by the child.")

    @coroutine
    def _driver_send(self, transaction, sync=True):
        '''
        *** Needs to be overloaded to prevent BusDriver from referencing the wrong operation
            and bus.
        *** The sync flag is intentionally ignored so that all transactions are synchronized.
        '''
        yield self.write(**vars(transaction))

class FlipflopDriver(WrRdDriver):
    '''
    cocotb driver for powlib_flipflop.
    '''

    _wrsignals        = ['d']
    _rdsignals        = ['q']
    _optional_signals = ['vld']
    _default_values   = {'d':0,'vld':0}

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

    @coroutine
    def write(self, d=0, vld=1, sync=True):
        '''
        Writes new data to the flip flop and then waits 
        untils the data is registered.
        '''
        
        self.wrbus.d.value   = d
        self.wrbus.vld.value = vld
        if sync: yield self.cycle()   

    @coroutine
    def read(self, sync=True):
        '''
        Reads the output of the flip flop and then waits 
        until the rise of the next clock cycle.
        '''
        
        value = int(self.rdbus.q.value)
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
    def bcycle(self):
        '''
        Waits a single clock cycle.
        '''

        yield ReadOnly()
        yield RisingEdge(self.bclock)           

    @coroutine
    def read(self, sync=True):
        '''
        Reads the output of the flip flop and then waits 
        until the rise of the next clock cycle.
        '''

        value = int(self.rdbus.q.value)
        if sync: yield self.bcycle()
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

class CntrDriver(WrRdDriver):
    
    _wrsignals        = ['adv','clr']
    _rdsignals        = ['cntr']
    _optional_signals = ['ld','nval']
    _default_values   = {'adv':0,'clr':0,'ld':0,'nval':0}    

    @property
    def W(self):
        '''
        Gets the specified width.
        '''
        return int(self.entity.W.value)

    @property
    def X(self):
        '''
        Gets the advance value.
        '''
        return int(self.entity.X.value)

    @property
    def INIT(self):
        '''
        Gets the initialize value.
        '''
        return int(self.entity.INIT.value) 

    @coroutine
    def write(self, adv=0, clr=0, ld=0, nval=0, sync=True):
        '''
        Writes new data to the counter and then waits 
        untils the data is registered.
        adv  = 1 continues counter. 0 pauses counter.
        clr  = 1 clears counter indefinitely. 0 allows the counter to perform other operations.
        ld   = 1 loads nval into the counter. 0 allows the counter to perform other operations.
        sync = True enables the clock cycle. False disables it.
        '''
        
        self.wrbus.adv.value  = adv
        self.wrbus.clr.value  = clr
        self.wrbus.ld.value   = ld
        self.wrbus.nval.value = nval
        if sync: yield self.cycle() 

    @coroutine
    def read(self, sync=True):
        '''
        Reads the output of the counter and then waits
        until the rise of the next clock cycle.
        '''
        
        value = int(self.__rdbus.cntr.value)
        if sync: yield self.cycle()
        raise ReturnValue(value)


