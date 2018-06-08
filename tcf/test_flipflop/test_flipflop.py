import random
import logging

from cocotb import test, coroutine

from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure

from powlib.drivers import FlipflopDriver
from powlib.utils   import TestEnvironment

import powlib

@test()
def test_flipflop(dut):
    """
    
    """

    yield Timer(50,"us")

