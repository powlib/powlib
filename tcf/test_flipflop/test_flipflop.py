import random
import logging

import cocotb

from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly
from cocotb.drivers import BitDriver
from cocotb.drivers.avalon import AvalonSTPkts as AvalonSTDriver
from cocotb.drivers.avalon import AvalonMaster
from cocotb.monitors.avalon import AvalonSTPkts as AvalonSTMonitor
from cocotb.regression import TestFactory
from cocotb.scoreboard import Scoreboard
from cocotb.result import TestFailure


@cocotb.test()
def test_flipflop(dut):
    """
    
    """
    yield Timer(50,"us")
