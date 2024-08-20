from microbit import *

input_A1 = pin0
input_B1 = pin1
input_A0 = pin8
input_B0 = pin9

for pin in [input_A0, input_A1, input_B0, input_B1]:
    pin.write_digital(0)
    pin.set_pull(pin.PULL_DOWN)

output_OR = pin2

output_OR.set_pull(pin.PULL_DOWN)

def test_or_gate():
    for i in range(4):
        input_A1.write_digital(i & 1)
        input_B1.write_digital((i >> 1) & 1)
        sleep(100)

        result_A0_B0 = input_A0.read_digital() & input_B0.read_digital()
        result_A1_B1 = input_A1.read_digital() & input_B1.read_digital()
       
        result = result_A0_B0 | result_A1_B1
        display.show(str(result))
        sleep(1000)
        display.clear()
        sleep(10)

while True:
    test_or_gate()