"""
This Module contains metrics implemented using the Tensorflow Backend
"""

from keras import backend as K


def spIndex(y_true, y_pred):
    num_classes = K.int_shape(y_pred)[1]    # y_true returns (None, None) for int_shape
                                            # y_pred returns (None, num_classes)

    true_positives = K.sum(K.cast(y_true * K.one_hot(K.argmax(y_pred, axis=1), num_classes), dtype='float32'))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    sp_tf = K.sqrt(K.mean(recall) * K.prod(K.pow(recall, 1 / num_classes)))

    return sp_tf

def effAcc(y_true, y_pred):
    num_classes = K.int_shape(y_pred)[1]  # y_true returns (None, None) for int_shape
                                          # y_pred returns (None, num_classes)

    true_positives = K.sum(K.cast(y_true * K.one_hot(K.argmax(y_pred, axis=1), num_classes), dtype='float32'))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())

    return K.mean(recall)