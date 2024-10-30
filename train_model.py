import os
import numpy as np  # type: ignore
import tensorflow as tf  # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore

# Directory paths
base_dir = 'gestures'

# Create an image data generator with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,  # Use 20% of data for validation
    rotation_range=20,      # Data augmentation: Random rotation
    width_shift_range=0.2,  # Horizontal shift
    height_shift_range=0.2, # Vertical shift
    zoom_range=0.2,         # Random zoom
    horizontal_flip=True    # Randomly flip images
)

# Load images from the directory (training set)
train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(64, 64),  # Resize images to 64x64
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

# Load images from the directory (validation set)
validation_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Build the CNN model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),  # Regularization to prevent overfitting
    tf.keras.layers.Dense(len(train_generator.class_indices), activation='softmax')  # Output layer
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=20  # Adjust the number of epochs based on training needs
)

# Save the model
model.save('gesture_model.keras')

print("Model training completed and saved successfully.")
