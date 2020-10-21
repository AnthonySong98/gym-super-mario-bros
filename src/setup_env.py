"""A method to setup an environment based on its string ID."""
import gym
from nes_py.wrappers import JoypadSpace#, wrap as nes_py_wrap
from my_gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from src.environment.atari import build_atari_environment


def setup_env(env_id: str, monitor_dir: str=None) -> gym.Env:
    """
    Make and environment and set it up with wrappers.

    Args:
        env_id: the id for the environment to load
        output_dir: the output directory to route monitor output to

    Returns:
        a loaded and wrapped Open AI Gym environment

    """
    if 'Tetris' in env_id:
        import gym_tetris
        env = gym_tetris.make(env_id)
        env = gym_tetris.wrap(env, clip_rewards=False)
    elif 'SuperMarioBros' in env_id:
        from my_gym_super_mario_bros import make
        env = make(env_id)
        env = JoypadSpace(env, SIMPLE_MOVEMENT)
        # env = JoypadSpace(env)
    else:
        env = build_atari_environment(env_id)

    if monitor_dir is not None:
        env = gym.wrappers.Monitor(env, monitor_dir, force=True)

    return env


# explicitly define the outward facing API of this module
__all__ = [setup_env.__name__]
