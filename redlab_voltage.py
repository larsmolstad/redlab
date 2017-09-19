import redlab

# to make the interface compatible with
# a serial port regarding flushInput
# (used by voltage_logger)
class Dummy:
    def flushInput(self):
        pass
fd2 = Dummy()

def voltage():
    return redlab.read_channel_voltage(0)

