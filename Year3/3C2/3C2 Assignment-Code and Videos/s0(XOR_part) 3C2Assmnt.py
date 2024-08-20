from microbit import *

input_pins = [pin0, pin1]
output_pin = pin2

for pin in input_pins:
    pin.write_digital(0)
    pin.set_pull(pin.PULL_DOWN)
output_pin.write_digital(0)

# function to test XOR gate + display output
def test_xor_gate():
    for i in range(4):
        input_pins[0].write_digital(i & 1)
        input_pins[1].write_digital((i >> 1) & 1)
        sleep(100)
        result = output_pin.read_digital()
        display.show(result)
        sleep(1000)

while True:
    test_xor_gate()
