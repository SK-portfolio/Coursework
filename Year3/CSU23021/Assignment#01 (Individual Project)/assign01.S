#include "hardware/regs/addressmap.h"
#include "hardware/regs/io_bank0.h"
#include "hardware/regs/timer.h"
#include "hardware/regs/m0plus.h"

.syntax unified
.cpu    cortex-m0plus
.thumb
.global main_asm
.align  4

.equ    DFLT_STATE_STRT, 1            @ Specify the value to start flashing
.equ    DFLT_STATE_STOP, 0            @ Specify the value to stop flashing
.equ    DFLT_ALARM_TIME, 1000000      @ Specify the default alarm timeout

.equ    GPIO_BTN_DN_MSK, 0x00040000   @ Bit-18 for falling-edge event on GP20
.equ    GPIO_BTN_EN_MSK, 0x00400000   @ Bit-22 for falling-edge event on GP21
.equ    GPIO_BTN_UP_MSK, 0x04000000   @ Bit-26 for falling-edge event on GP22

.equ    GPIO_BTN_DN,  20              @ Specify pin for the "down" button
.equ    GPIO_BTN_EN,  21              @ Specify pin for the "enter" button
.equ    GPIO_BTN_UP,  22              @ Specify pin for the "up" button
.equ    GPIO_LED_PIN, 25              @ Specify pin for the built-in LED
.equ    GPIO_DIR_IN,   0              @ Specify input direction for a GPIO pin
.equ    GPIO_DIR_OUT,  1              @ Specify output direction for a GPIO pin

.equ    LED_VAL_ON,    1              @ Specify value that turns the LED "on"
.equ    LED_VAL_OFF,   0              @ Specify value that turns the LED "off"

.equ    GPIO_ISR_OFFSET, 0x74         @ GPIO is int #13 (vector table entry 29)
.equ    ALRM_ISR_OFFSET, 0x40         @ ALARM0 is int #0 (vector table entry 16)

@ Entry point to the ASM portion of the program
main_asm:
    bl      init_LED                    @ Jump to init_LED
    bl      init_BTNS                   @ Jump to init_BTNS
    bl      install_ALRM                @ Jump to install_ALRM
    bl      install_GPIO                @ Jump to install_GPIO
    ldr     r0, =msg_RESET              @ Load reset message address 
    bl      printf                      @ Print reset message

main_loop:
    ldr   r0, =ltimer                   @ Load ltimer address into r0
    ldr   r0, [r0]                      @ Load value stored in r0 address into r0
    bl    alarm_setup                   @ Jump to alarm_setup with r0
    wfi                                 @ Wait for interrupt
    b     main_loop                     @ Jump back to beginning main_loop

init_LED:
    push    {lr}                        @ Enter subroutine and store link register to stack
    movs    r0, #GPIO_LED_PIN           @ Load GPIO pin for LED into r0
    bl      asm_gpio_init               @ Jump to subroutine to initialise GPIO pin specified by r0
    movs    r0, #GPIO_LED_PIN           @ Load GPIO pin for LED into r0
    movs    r1, #GPIO_DIR_OUT           @ Setup GPIO pin as output
    bl      asm_gpio_set_dir            @ Jump to subroutine to set GPIO pin direction
    pop     {pc}                        @ Pop program counter from stack and return

init_BTNS:
    push    {lr}                        @ Enter subroutine and store link register to stack
    @ down button(20)
    movs    r0, #GPIO_BTN_DN            @ Load GPIO pin for down button into r0
    bl      BTN_init                    @ Jump to BTN_init to initialize down button
    @ enter button(21)
    movs    r0, #GPIO_BTN_EN            @ Load GPIO pin for enter button into r0
    bl      BTN_init                    @ Jump to BTN_init to initialize enter button
    @ up button(22)
    movs    r0, #GPIO_BTN_UP            @ Load GPIO pin for up button into r0
    bl      BTN_init                    @ Jump to BTN_init to initialize up button
    pop     {pc}                        @ Pop program counter from stack and return

alarm_setup:
    movs    r1, #1                                      @ Store 1 value to r1
    ldr     r2, =(TIMER_BASE + TIMER_INTE_OFFSET)       @ Load address of TIMER_INTE_OFFSET into r2
    str     r1, [r2]                                    @ Set TIMER_INTE_OFFSET to value in r1 to enable alarm timer interrupts
    ldr     r2, =(TIMER_BASE + TIMER_TIMELR_OFFSET)     @ Load address of TIMER_TIMELR_OFFSET into r2
    ldr     r1, [r2]                                    @ Load current timer count from TIMER_TIMELR_OFFSET into r1
    adds    r0, r1                                      @ Add time delay to current timer count
    ldr     r2, =(TIMER_BASE + TIMER_ALARM0_OFFSET)     @ Load address of TIMER_ALARM0_OFFSET into r2
    str     r0, [r2]                                    @ Set TIMER_ALARM0_OFFSET to updated value in r1
    bx      lr                                          @ Return from subroutine

install_ALRM:
    ldr     r2, =(PPB_BASE + M0PLUS_VTOR_OFFSET)       @ Load Vector Table Offset Register address into r1
    ldr     r1, [r2]                                   @ Load value from Vector Table Offset Register into r1
    movs    r2, #ALRM_ISR_OFFSET                       @ Load ALRM_ISR_OFFSET into r2
    add     r2, r1                                     @ Add offset to base address to get address of ALRM ISR
    ldr     r0, =alrm_isr                              @ Load address of alrm_isr into r0
    str     r0, [r2]                                   @ Store address of alrm_isr in interrupt vector table
    ldr     r2, =(PPB_BASE + M0PLUS_NVIC_ICPR_OFFSET)  @ Load address of NVIC_ICPR register into r2
    movs    r1, #1                                     @ Load value 1 into r1    
    str     r1, [r2]                                   @ Set interrupt clear-pending register to clear any pending interrupts
    ldr     r2, =(PPB_BASE + M0PLUS_NVIC_ISER_OFFSET)  @ Load address of NVIC_ISER register into r2
    movs    r1, #1                                     @ Load value 1 into r1    
    str     r1, [r2]                                   @ Set interrupt enable register to enable corresponding interrupt
    bx      lr                                         @ Return from function

.thumb_func
alrm_isr:                                           @ Alarm Interrupt Service Routine
    push    {lr}                                    @ Enter subroutine and store link register to stack
    ldr     r2, =TIMER_BASE                         @ Load TIMER_BASE address into r2
    movs    r1, #1                                  @ Set r1 to 1
    str     r1, [r2, #TIMER_INTR_OFFSET]            @ Store 1 at TIMER_INTR_OFFSET in TIMER_BASE
    ldr     r0, =lstate                             @ Load lstate address into r0
    ldr     r0, [r0]                                @ Load value stored in r0 address into r0
    cmp     r0, DFLT_STATE_STOP                     @ Compare r0 with DFLT_STATE_STOP
    beq     blink_disable                           @ If same - Jump to blink_disable
    bl      sub_toggle                              @ Else - Jump to sub_toggle
blink_disable:  
    pop     {pc}                                    @ Pop program counter and return
install_GPIO:
    ldr     r2, =(PPB_BASE + M0PLUS_VTOR_OFFSET)       @ Load Vector Table Offset Register address into r1
    ldr     r1, [r2]                                   @ Load value from Vector Table Offset Register into r1
    movs    r2, #GPIO_ISR_OFFSET                       @ Load GPIO_ISR_OFFSET into r2
    add     r2, r1                                     @ Add offset to base address to get address of ALRM ISR
    ldr     r0, =gpio_isr                              @ Load address of gpio_isr into r0
    str     r0, [r2]                                   @ Store address of gpio_isr in interrupt vector table
    ldr     r2, =(PPB_BASE + M0PLUS_NVIC_ICPR_OFFSET)  @ Load address of NVIC_ICPR register into r2
    movs    r0, #1                                     @ Load value 1 into r1
    lsls    r0, #13                                    @ Shift bits left by 13 positions (Since GPIO is int #13)
    str     r0, [r1]                                   @ Set interrupt clear-pending register to clear any pending interrupts
    ldr     r1, =(PPB_BASE + M0PLUS_NVIC_ISER_OFFSET)  @ Load address of NVIC_ISER register into r2
    str     r0, [r1]                                   @ Set interrupt enable register to enable corresponding interrupt
    bx      lr                                         @ Return from function

.thumb_func
gpio_isr:                                                           @ Alarm Interrupt Service Routine
    push    {lr}                                                    @ Enter subroutine and store link register to stack
    ldr     r0, =(IO_BANK0_BASE + IO_BANK0_PROC0_INTS2_OFFSET)      @ Load GPIO interrupt register address into r0
    ldr     r0, [r0]                                                @ Load GPIO interrupt register value
    movs    r1, r0                                                  @ Copy value to r1
@-------------Down pressed?-------------
    ldr     r2, =GPIO_BTN_DN_MSK                                    @ Load bitmask for Down button
    ands    r0, r2                                                  @ Bitwise AND to check if Down button is pressed
    cmp     r0, #0                                                  @ Compare result with 0
    bne     press_BTN_DN                                            @ If same (Down button has been pressed)- Jump to press_BTN_DN
@-------------Enter pressed?-------------
    movs    r0, r1                                                  @ Copy value from r1 to r0
    ldr     r2, =GPIO_BTN_EN_MSK                                    @ Load bitmask for Enter button
    ands    r0, r2                                                  @ Bitwise AND to check if Enter button is pressed
    cmp     r0, #0                                                  @ Compare result with 0
    bne     press_BTN_EN                                            @ If same (Enter button has been pressed)- Jump to press_BTN_EN
@--------------UP pressed?--------------
    movs    r0, r1                                                  @ Copy value from r1 to r0
    ldr     r2, =GPIO_BTN_UP_MSK                                    @ Load bitmask for Up button
    ands    r0, r2                                                  @ Bitwise AND to check if Up button is pressed
    cmp     r0, #0                                                  @ Compare result with 0
    bne     press_BTN_UP                                            @ If same (Up button has been pressed)- Jump to press_BTN_UP

@LED functionallity
sub_toggle:                                             @ From blink_asm.S
    push    {lr}                                        @ Enter subroutine and store link register to stack
    movs    r0, #GPIO_LED_PIN                           @ Set LED GPIO pin number to r0 for use by asm_gpio_get
    bl      asm_gpio_get                                @ Get current value of LED GPIO pin (returns to r0)
    cmp     r0, #LED_VAL_OFF                            @ Check if LED GPIO pin value is "off"
    beq     led_set_on                                  @ If it is "off" then then jump code to to turn it on
led_set_off:
    movs    r1, #LED_VAL_OFF                            @ LED is currently "on" so we want to turn it "off"
    b       led_set_state                               @ Jump to portion of code where we set state of LED
led_set_on:
    movs    r1, #LED_VAL_ON                             @ LED is currently "off" so we want to turn it "on"
led_set_state:
    movs    r0, #GPIO_LED_PIN                           @ Set LED GPIO pin number to r0 for use by asm_gpio_put
    bl      asm_gpio_put                                @ Update value of LED GPIO pin (based on value in r1)
    bl      alarm_setup                                 @ Jump to alarm_setup
    ldr     r2, =(TIMER_BASE + TIMER_INTE_OFFSET)       @ Enable Alarm
    movs    r1, #1                                      @ Set r1 to 1 
    str     r1, [r2]                                    @ Store 1 at r2 memory address
    pop     {pc}                                        @ Pop program counter from stack and return

@button functionallity
BTN_init:
    push    {r4, lr}                    @ Store r4 value and link register on stack
    movs    r4, r0                      @ Copy value from r0 (button identifier) to r4
    bl      asm_gpio_init               @ Jump to subroutine to initialise GPIO pin
    movs    r0, r4                      @ Restore the original value of r0
    movs    r1, #GPIO_DIR_IN            @ Set r1 to GPIO_DIR_IN (input direction)
    bl      asm_gpio_set_dir            @ Jump to subroutine to set GPIO pin direction
    movs    r0, r4                      @ Restore the original value of r0
    bl      asm_gpio_set_irq            @ Jump to subroutine to set GPIO interrupt
    pop     {r4, pc}                    @ Pop r4 and program counter (pc) from the stack and return

@Down----------------------------------------
press_BTN_DN:
    ldr     r0, =lstate                 @ Load lstate address into r0
    ldr     r0, [r0]                    @ Load value stored in r0 address into r0
    cmp     r0, #DFLT_STATE_STRT        @ Compare r0 value with DFLT_STATE_STRT
    beq     faster_bgn                  @ If same - Jump to faster_bgn
    ldr     r0, =ltimer                 @ Else - Load ltimer address into r0
    ldr     r1, =DFLT_ALARM_TIME        @ Load DFLT_ALARM_TIME value into r1
    str     r1, [r0]                    @ Store value in r1 to r0 memory address
    b       faster_end                  @ Jump to faster_end
faster_bgn:
    ldr     r0, =msg_FAST               @ Load of msg_FAST into r0
    bl      printf                      @ Print msg_FAST in Serial Monitor
    ldr     r0, =ltimer                 @ Load ltimer address into r0
    ldr     r1, [r0]                    @ Load value from r0 memory address into r1
    lsrs    r1, #1                      @ Logical shift right by 1 bit in r1
    str     r1, [r0]                    @ Store value in r1 to r0 memory address
faster_end:
    ldr     r1, =GPIO_BTN_DN_MSK        @ Load GPIO_BTN_DN_MSK address into r1
    b       stop_BTN_check              @ Jump to stop_BTN_check

@Enter----------------------------------------
press_BTN_EN:
    ldr     r0, =msg_BEGIN              @ Load of msg_BEGIN into r0
    bl      printf                      @ Print msg_BEGIN in Serial Monitor
    ldr     r0, =lstate                 @ Load lstate address into r0
    ldr     r1, [r0]                    @ Load value from r0 memory address into r1
    cmp     r1, #DFLT_STATE_STOP        @ Compare r1 value with DFLT_STATE_STOP
    beq     toggle_bgn                  @ If same - Jump to toggle_bgn
    movs    r1, #DFLT_STATE_STOP        @ Else - Set r1 to #DFLT_STATE_STOP
    b       toggle_end                  @ Jump to toggle_end
toggle_bgn:
    ldr     r0, =lstate                 @ Load lstate address into r0
    movs    r1, #DFLT_STATE_STRT        @ Set r1 to #DFLT_STATE_STRT
toggle_end:
    str     r1, [r0]                    @ Store shifted value in r1 to r0 memory address
    ldr     r1, =GPIO_BTN_EN_MSK        @ Load bitmask for Enter button
    b       stop_BTN_check              @ Jump to stop_BTN_check 
@Up----------------------------------------
press_BTN_UP:
    ldr     r0, =lstate                 @ Load lstate address into r0
    ldr     r0, [r0]                    @ Load value stored in r0 address into r0
    cmp     r0, #DFLT_STATE_STRT        @ Compare r0 value with DFLT_STATE_STRT
    beq     slower_bgn                  @ If same - Jump to slower_bgn
    ldr     r0, =ltimer                 @ Load ltimer address into r0
    ldr     r1, =DFLT_ALARM_TIME        @ Load DFLT_ALARM_TIME value into r1
    str     r1, [r0]                    @ Store value in r1 to r0 memory address
    b       slower_end                  @ Jump to slower_end 
slower_bgn:
    ldr     r0, =msg_SLOW               @ Load of msg_SLOW into r0
    bl      printf                      @ Print msg_SLOW in Serial Monitor
    ldr     r0, =ltimer                 @ Load ltimer address into r0
    ldr     r1, [r0]                    @ Load value from r0 memory address into r1
    lsls    r1, #1                      @ Logical shift left by 1 bit in r1
    str     r1, [r0]                    @ Store value in r1 to r0 memory address
slower_end:
    ldr     r1, =GPIO_BTN_UP_MSK        @ Load bitmask for UP button
    b       stop_BTN_check              @ Jump to stop_BTN_check
@-------------------------------------------
stop_BTN_check:                                             @ Stop checking for button inputs
    ldr     r0, =(IO_BANK0_BASE + IO_BANK0_INTR2_OFFSET)    @ Load GPIO raw interrupt register address into r0
    str     r1, [r0]                                        @ Store value in r1 to r0 memory address
    pop     {pc}                                            @ Pop program counter from stack and return

.align 4
msg_BEGIN:  .asciz        "Toggling State...\n"
msg_SLOW:   .asciz        "Slowing Down...       (sleep x2)\n"
msg_FAST:   .asciz        "Speeding Up...        (sleep x0.5)\n"
msg_RESET:  .asciz        "Default Speed         (sleep reset)\n"

.data
lstate: .word   DFLT_STATE_STRT
ltimer: .word   DFLT_ALARM_TIME