# https://engmrk.com/kerasapplication-pre-trained-model/

import keras
import numpy as np
import json

from keras.applications import inception_v3
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from keras.preprocessing.image import ImageDataGenerator, load_img

inception_model = inception_v3.InceptionV3(weights="imagenet")


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(k): v for k, v in x.items()}
    return x

def show_results():
    # Show the results
    for i in range(len(predicted_classes)):
        pred_class = np.argmax(predictions[predicted_classes[i]])
        pred_label = idx2label[pred_class]

        title = 'Original label:{}, Prediction :{}, confidence : {:.3f}'.format(
            fnames[predicted_classes[i]].split('/')[0],
            pred_label,
            predictions[predicted_classes[i]][pred_class])

        original = load_img('{}/{}'.format(validation_dir, fnames[predicted_classes[i]]))
        plt.figure(figsize=[7, 7])
        plt.axis('off')
        plt.title(title)
        plt.imshow(original)
        plt.show()


def get_pil_image(filename, target_size):
    # load an image in PIL format
    original_image = load_img(filename, target_size=(target_size,target_size))

    # convert the PIL image (width, height) to a NumPy array (height, width, channel)
    numpy_image = img_to_array(original_image)

    # Convert the image into 4D Tensor (samples, height, width, channels) by adding an extra dimension to the axis 0.
    input_image = np.expand_dims(numpy_image, axis=0)

    #print("PIL image size = ", original_image.size)
    #print("NumPy image size = ", numpy_image.shape)
    #print("Input image size = ", input_image.shape)
    plt.imshow(np.uint8(input_image[0]))
    return input_image


def predict_inception_v3(filename):
    start = time.time()
    input_image = get_pil_image(filename, 299)

    # preprocess for inception_v3
    processed_image_inception_v3 = inception_v3.preprocess_input(input_image.copy())

    # inception_v3

    predictions_inception_v3 = inception_model.predict(processed_image_inception_v3)
    label_inception_v3 = decode_predictions(predictions_inception_v3)
    print("label_inception_v3 = ", label_inception_v3)
    ende = time.time()
    print('{:5.3f}s'.format(ende - start))


def predict_mymodel(img_path):
    img = image.load_img(img_path, target_size=(244, 244))
    img_tensor = image.img_to_array(img)  # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor,axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.  # imshow expects values in the range [0, 1]

    start = time.time()
    predictions_my = mobilenet_model.predict(img_tensor)
    print(predictions_my)
    # label_MY = decode_predictions(predictions_my)
    # print("My labels = ", label_MY )
    ende = time.time()
    print('{:5.3f}s'.format(ende - start))
    y_classes = predictions_my.argmax(axis=-1)
    print('Best Match', labels[y_classes[0]], predictions_my[0, y_classes[0]])

def predict_vgg16(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img)  # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor,axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.  # imshow expects values in the range [0, 1]

    start = time.time()
    predictions_my = vgg16_model.predict(img_tensor)
    print(predictions_my)
    # label_MY = decode_predictions(predictions_my)
    # print("My labels = ", label_MY )
    ende = time.time()
    print('{:5.3f}s'.format(ende - start))
    y_classes = predictions_my.argmax(axis=-1)
    print('Best Match', labels[y_classes[0]],predictions_my[0,y_classes[0]])


def predict_resnet50(img_path):
    img = image.load_img(img_path, target_size=(244, 244))
    img_tensor = image.img_to_array(img)  # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor,axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.  # imshow expects values in the range [0, 1]

    start = time.time()
    predictions_my = resnet50_model.predict(img_tensor)
    print(predictions_my)
    # label_MY = decode_predictions(predictions_my)
    # print("My labels = ", label_MY )
    ende = time.time()
    print('{:5.3f}s'.format(ende - start))
    y_classes = predictions_my.argmax(axis=-1)



def inception():
    print("------------------------   Inception Orignal    ----------------------------------------")
    # print("Inception - Lego 1x4LRed ")
    # predict_inception_v3( file_1x4LRed )
    print("")
    print("Inception - Rose ")
    predict_inception_v3( file_rose )
    print("")
    print("Inception - Car and People ")
    predict_inception_v3( file_car )
    print("")
    print("Inception - Apple ")
    predict_inception_v3( file_apple )
    print("")
    print("Inception - Sunflower")
    predict_inception_v3( file_sunflower)

def mobilenet():
    # ---------------------------------------------------------------------------------------------
    # My Trained Model MobileNet- Single Image
    # ---------------------------------------------------------------------------------------------
    print("------------------------   Mobilenet  Trained  ----------------------------------------")
    print("")
    print("My Model - 1x5LGreen ")
    predict_mymodel(file_3x5LGreen)
    print("")
    print("My Model  - 1x4LRed ")
    predict_mymodel(file_1x4LRed)

    print("")
    print("Gear Webcam Cropped ")
    predict_mymodel(file_GearW)

    #print("")
    #print("My Model  - Rose ")
    #predict_mymodel(file_rose)
    #print("")
    #print("")
    #print("Inception - Apple ")
    #predict_mymodel(file_apple)
    #print("")
    #print("Inception - Sunflower")
    #predict_mymodel(file_sunflower)


def vgg16():
    # ---------------------------------------------------------------------------------------------
    # My Trained Model MobileNet- Single Image
    # ---------------------------------------------------------------------------------------------
    print("------------------------   VGG16  Trained  ----------------------------------------")
    print("1x5LGreen ")
    predict_vgg16(file_3x5LGreen)
    print("")
    print("1x4LRed ")
    predict_vgg16(file_1x4LRed)
    print("")
    print("Gear Webcam Cropped ")
    predict_vgg16(file_GearW)





    #print("Rose")
    #predict_vgg16(file_rose)
    #print("")
    #print("")
    #print("Apple ")
    #predict_vgg16(file_apple)
    #print("")
    #print("Sunflower")
    #predict_vgg16(file_sunflower)




def resnet50():
    # ---------------------------------------------------------------------------------------------
    # My Trained Model MobileNet- Single Image
    # ---------------------------------------------------------------------------------------------
    print("")
    print("Resnet50 - 1x5LGreen ")
    predict_resnet50(file_3x5LGreen)

if __name__ == '__main__':
    start = time.time()
    labels_file = "./models/labels_8classes.json"
    with open(labels_file) as f:
        labels = json.load(f, object_hook=jsonKeys2int)
    print(labels)

    print("reading model...")

    mobilenet_model = load_model('./models/LegoTrainedMobileNet_epochs20.h5')
    vgg16_model = load_model('./models/LegoTrainedVGG16_classes5_best_model.h5')


    ende = time.time()
    print('{:5.3f}s'.format(ende - start))

    file_3x5LGreen = "./lego_fotos/predict/3x5LGreen/frame20190215-2217332.jpg"
    file_GearW = "./lego_fotos/predict/Gear20Beige/webcam_cropped20190227-224240.jpg"
    file_1x4LRed = "./lego_fotos/predict/3x5LRed/frame20190222-16260317.jpg"

    mobilenet()
    vgg16()



