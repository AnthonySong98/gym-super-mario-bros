"""The original Deep-Q model used by DeepMind."""
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Lambda
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Multiply
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import RMSprop
from .losses import huber_loss


def build_deep_q_model(
    image_size: tuple=(84, 84),
    num_frames: int=4,
    num_actions: int=6,
    loss=huber_loss,
    optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01)
) -> Model:
    """
    Build and return the Deep Mind model for the given domain parameters.

    Notes:
        Color Space: this CNN expects single channel images (B&W)

    Args:
        image_size: the shape of the image states for the model
                     Atari games are (192, 160), but DeepMind reduced the
                     size to (84, 84) to reduce computational load
        num_frames: the number of frames being stacked together
                    DeepMind uses 4 frames in their original implementation
        num_actions: the output shape for the model, this represents the
                     number of discrete actions available to a game
        loss: the loss metric to use at the end of the network
        optimizer: the optimizer for reducing error from batches

    Returns:
        a blank DeepMind CNN for image classification in a reinforcement agent

    """
    # build the CNN using the functional API
    cnn_input = Input((*image_size, num_frames), name='cnn')
    cnn = Lambda(lambda x: x / 255.0)(cnn_input)
    cnn = Conv2D(32, (8, 8), strides=(4, 4))(cnn)
    cnn = Activation('relu')(cnn)
    cnn = Conv2D(64, (4, 4), strides=(2, 2))(cnn)
    cnn = Activation('relu')(cnn)
    cnn = Conv2D(64, (3, 3), strides=(1, 1))(cnn)
    cnn = Activation('relu')(cnn)
    cnn = Flatten()(cnn)
    cnn = Dense(512)(cnn)
    cnn = Activation('relu')(cnn)
    cnn = Dense(num_actions)(cnn)
    # build the mask using the functional API
    mask_input = Input((num_actions,), name='mask')
    # put the two pieces of the graph together
    output = Multiply()([cnn, mask_input])

    # build the model
    model = Model(inputs=[cnn_input, mask_input], outputs=output)
    # compile the model with the default loss and optimization technique
    model.compile(loss=loss, optimizer=optimizer)

    return model


# explicitly define the outward facing API of this module
__all__ = [build_deep_q_model.__name__]
