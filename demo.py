from nes_py.wrappers import JoypadSpace
from my_gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from my_gym_super_mario_bros import make
env = make('SuperMarioBros-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)


# from nes_py.wrappers import JoypadSpace
# import gym_super_mario_bros
# from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
# env = gym_super_mario_bros.make('SuperMarioBros-v0')
# env = JoypadSpace(env, SIMPLE_MOVEMENT)


done = True
for step in range(100):
    if done:
        state = env.reset()
    cur_act = env.action_space.sample()
    state, reward, done, info = env.step(cur_act)
    print("Current Step State:",state.shape)
    print("Current Step Reward:",reward)
    # env.render()

env.close()