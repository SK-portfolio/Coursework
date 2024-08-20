from microbit import *

and_gate_output = pin0
xor_gate_output = pin1
or_gate_output = pin2

and_gate_output.write_digital(0)
xor_gate_output.write_digital(0)
or_gate_output.write_digital(0)

def test_or_gate():
    for i in range(4):
        and_gate_output.write_digital(i & 1)
        xor_gate_output.write_digital((i >> 1) & 1)
        sleep(100)
        result = or_gate_output.read_digital()
        display.show(result)
        sleep(1000)
        display.clear()
        sleep(10)
        
while True:
    test_or_gate()