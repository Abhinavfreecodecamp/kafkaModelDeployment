import tensorflow as tf; print(tf.__version__)
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.optimizers import SGD


fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


train_images = train_images.reshape((train_images.shape[0], 28, 28, 1))
test_images = test_images.reshape((test_images.shape[0], 28, 28, 1))


train_images, train_labels = train_images / 255.0, to_categorical(train_labels)
test_images, test_labels = test_images / 255.0, to_categorical(test_labels)



def define_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(64, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='softmax'))
    return model


optimizer = SGD(lr=0.001, momentum=0.9)
model = define_model()
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])


validation_callback = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    verbose=1,
    mode="auto",
    patience = 5,
    baseline=None,
    restore_best_weights=True,
)

history = model.fit(train_images, train_labels,
                     epochs=50, batch_size=64,
                     verbose=1, callbacks = [validation_callback],
                   validation_split=0.2)




model.save("baselineMnistClassifier")