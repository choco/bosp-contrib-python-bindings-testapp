#!/usr/bin/env python
import sys
import os
script_path = os.path.dirname(os.path.abspath(__file__))
barbeque_path = (script_path + "/../../lib/bbque/bindings/python" +
		str(sys.version_info[0]) + "." + str(sys.version_info[1]))
sys.path.append(barbeque_path)
import barbeque

class SimpleEXC(barbeque.BbqueEXC):
    # Custom constructor
    def __init__(self, name, recipe, rtlib_services, cycle_ms, cycles_total):
        # Need to call base class constructor
        super(SimpleEXC, self).__init__(name, recipe, rtlib_services)
        self.cycle_ms = cycle_ms
        self.cycles_total = cycles_total
        self.cycle_lenght = 0
        self.n_core_max = 4

        self.logger.Notice("New SimpleEXC with: cycle time {}[ms], cycles count {}"
              .format(cycle_ms, cycles_total))
        self.logger.Info("EXC Unique Identifier (UID): {}".format(self.GetUniqueID()))

    def onSetup(self):
        self.logger.Notice("SimpleEXC.onSetup()")
        return barbeque.RTLIB_ExitCode.RTLIB_OK

    def onConfigure(self, awm_id):
        self.logger.Notice("SimpleEXC.onConfigure(): EXC [{}], AWM[{:02d}]"
                           .format(self.exc_name, awm_id))

        res_w = barbeque.RTLIB_Resources_Amount_Wrapper()
        ret = self.GetAssignedResources(barbeque.RTLIB_ResourceType.PROC_ELEMENT, res_w)
        proc_quota = res_w.amount
        ret = self.GetAssignedResources(barbeque.RTLIB_ResourceType.PROC_NR, res_w)
        proc_nr = res_w.amount
        ret = self.GetAssignedResources(barbeque.RTLIB_ResourceType.MEMORY, res_w)
        mem = res_w.amount

        self.logger.Notice("SimpleEXC.onConfigure(): EXC [{}], AWM[{:02d}] => "
                           "R<PROC_quota>={:3d}, R<PROC_nr>={:2d}, R<MEM>={:3d}"
                           .format(self.exc_name, awm_id, proc_quota, proc_nr, mem))

        # Deal with unmanaged mode
        if proc_nr < 1:
            proc_nr = 1

        self.cycle_lenght = 1000 * self.cycle_ms * (self.n_core_max / proc_nr)
        self.logger.Notice("SimpleEXC.onConfigure(): EXC [{}], AWM[{:02d}] => "
                           "cycle time {}[ms]"
                            .format(self.exc_name, awm_id, self.cycle_lenght/1000))
        ret = self.SetMinimumCycleTimeUs(self.cycle_lenght)
        return barbeque.RTLIB_ExitCode.RTLIB_OK

    def onRun(self):
        wmp = self.WorkingModeParams()

        if (self.Cycles() >= self.cycles_total):
            return barbeque.RTLIB_ExitCode.RTLIB_EXC_WORKLOAD_NONE

        self.logger.Notice("SimpleEXC.onRun(): EXC [{}], AWM[{:02d}] => "
                           "processing {}[ms]"
                            .format(self.exc_name, wmp.awm_id, self.cycle_lenght/1000))
        return barbeque.RTLIB_ExitCode.RTLIB_OK

    def onMonitor(self):
        wmp = self.WorkingModeParams()
        self.logger.Notice("SimpleEXC.onMonitor(): EXC [{}], AWM[{:02d}] => "
                           "cycles [{}/{}], CPS = {:.2f}"
                            .format(self.exc_name, wmp.awm_id, self.Cycles(),
                                    self.cycles_total, self.GetCPS()))
        return barbeque.RTLIB_ExitCode.RTLIB_OK

def main():
    # Wrapper for RTLIB_Services
    services_wrapper = barbeque.RTLIB_Services_Wrapper()
    # Initialize rpc channel with bbque
    error_check = barbeque.RTLIB_Init("BbqPythonTestApp", services_wrapper)
    if (error_check != barbeque.RTLIB_ExitCode.RTLIB_OK) or (not services_wrapper.services):
        print "RTLIB initialization failed"
        return

    # Register new execution
    testexec = SimpleEXC("SimpleEXC", "BbqRTLibPythonBindingsTestApp", services_wrapper.services, 100, 5)

    testexec.Start()
    testexec.WaitCompletion()

if __name__ == '__main__':
    main()
