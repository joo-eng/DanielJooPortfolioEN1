import force_sensor
import color_sensor
import color
import runloop
import motor
from hub import port

FORWARD_SPEED = -400
BACKWARD_SPEED = 600
STEER_DEGREES = 60
STEER_SPEED = 400
BACKTRACK_TIME_MS = 300
AROUND_TIME_MS = 750
LOOP_DELAY_MS = 10

async def start():
    motor.run(port.A, FORWARD_SPEED)
    while True:
        if force_sensor.pressed(port.C):
            await backtrack()
            await go_around()
            motor.run(port.A, FORWARD_SPEED)
        elif color_sensor.color(port.D) == color.BLUE:
            await courtship()
        await runloop.sleep_ms(LOOP_DELAY_MS)

async def backtrack():
    motor.stop(port.A)
    motor.run(port.A, BACKWARD_SPEED)
    await runloop.sleep_ms(BACKTRACK_TIME_MS)
    motor.stop(port.A)
async def go_around():
    motor.run(port.A, BACKWARD_SPEED)
    await runloop.sleep_ms(100)
    await motor.run_for_degrees(
        port.B,
        STEER_DEGREES,
        STEER_SPEED
    )
    await runloop.sleep_ms(AROUND_TIME_MS)
    await motor.run_for_degrees(
        port.B,
        -STEER_DEGREES,
        STEER_SPEED
    )
    motor.stop(port.A)
    while force_sensor.pressed(port.C):
        await runloop.sleep_ms(LOOP_DELAY_MS)

async def courtship():
    motor.run(port.A, FORWARD_SPEED)
    while not force_sensor.pressed(port.C):
        await runloop.sleep_ms(LOOP_DELAY_MS)
    motor.stop(port.A)
    for _ in range(5):
        await motor.run_for_degrees(port.A, -240, 800)
        await runloop.sleep_ms(80)
        await motor.run_for_degrees(port.A, 240, 800)
        await runloop.sleep_ms(80)
    motor.run(port.A, BACKWARD_SPEED)
    await runloop.sleep_ms(400)
    while force_sensor.pressed(port.C):
        await runloop.sleep_ms(LOOP_DELAY_MS)
    motor.run(port.A, FORWARD_SPEED)
    while not force_sensor.pressed(port.C):
        await runloop.sleep_ms(LOOP_DELAY_MS)
    motor.stop(port.A)

runloop.run(start())