import runloop
import motor_pair
from hub import port

FORWARD_FAST = 800
BACKWARD_FAST = -800
FORWARD_SLOW = 300
BACKWARD_SLOW = -300

STEER_RIGHT_BIG = 60
STEER_LEFT_BIG = -60
STEER_RIGHT_SMALL = 30
STEER_LEFT_SMALL = -30
SPIN = 100

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

async def steps():
  await move(FORWARD_FAST, 0)
  await time(2000)
  await move(BACKWARD_FAST, 0)
  await time(2000)
  await move(FORWARD_SLOW, 0)
  await time(2000)
  await move(BACKWARD_SLOW, 0)
  await time(2000)
  await move(FORWARD_SLOW, STEER_LEFT_SMALL)
  await time(2000)
  await move(BACKWARD_SLOW, STEER_RIGHT_SMALL)
  await time(2000)
  await move(FORWARD_SLOW, STEER_LEFT_BIG)
  await time(2000)
  await move(BACKWARD_SLOW, STEER_RIGHT_BIG)
  await time(2000)
  await move(FORWARD_FAST, SPIN)
  await time(4000)

async def move(v, theta):
    motor_pair.move(motor_pair.PAIR_1, theta, velocity=v)

async def time(t):
  await runloop.sleep_ms(t)
  motor_pair.stop(motor_pair.PAIR_1)

runloop.run(steps())