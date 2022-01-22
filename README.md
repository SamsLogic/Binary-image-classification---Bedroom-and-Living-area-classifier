# Binary image classification - Bedroom and Living area classifier

## Libraries Used

1. Numpy
2. OpenCV
3. Tensorflow
4. Keras
5. Pandas
6. Sklearn
7. Matplotlib

## Dataset

This is the Original data provided by MIT. Indoor scene recognition is a challenging open problem in high level vision. Most scene recognition models that work well for outdoor scenes perform poorly in the indoor domain. The main difficulty is that while some indoor scenes (e.g. corridors) can be well characterized by global spatial properties, others (e.g., bookstores) are better characterized by the objects they contain. More generally, to address the indoor scenes recognition problem we need a model that can exploit local and global discriminative information.

The dataset for this image classification model is a kaggle dataset maintained by Muhammad Ahmad with title - MIT Indoor Scenes. The dataste includes images of multiple indoor areas and for this problewm we are using the dataset for Bedroom and Living area only.

Link to the dataset - https://www.kaggle.com/itsahmad/indoor-scenes-cvpr-2019

Below is the image including the label as title (1 - Bedroom, 0- Living room)
![image](https://user-images.githubusercontent.com/41964069/150638320-7a8b7cd8-1214-46e2-871f-615d22d10f0b.png)

## Approach

## Preprocessing

The preprocssing of the data includes billateral filteration. canny edge detection and dilusion of the image to get an edge based visualization of the images. As shown below the edges are also enough to identify if the location shown in the image is a bedroom or a living room
![image](https://user-images.githubusercontent.com/41964069/150639031-6f154e2e-41aa-4cc1-9a5b-95e6afb58088.png)

## Model

For this problem CNN model was used with a residual network approach. The model includes 5 CNN layers, 2 residual layers and 4 feedforward networks. The CNN stacks were created keeping in mind to starting with Huge kernels to look through the global data in the image and then with smaller kernels to look though the minute details in the images.

## Training and validation

Cross validated training with 5 Kfolds was done with to traing the images and validate the performace over 5 diffferent datatypes. As per the validation. the AUDO score of the validation data is 0.74. whcih is a fairly good score gien the type of dataset and the low size of the deep neural network.

## Testing results

The testing was done on a totally different set of images from a hotel room that i was staying at during my vacation. I took 8 pictures of the bedroom and the living room fom the dataset and tested the results. Shockingly the results were pretty amazing (Only after some fail iterations and improving my model and preprocssing).

Preprocessed images -

![image](https://user-images.githubusercontent.com/41964069/150639318-88227840-0ef8-485e-a3a5-60b2acc93fd0.png)

Final Prediction - 

![image](https://user-images.githubusercontent.com/41964069/150639342-d794e073-6223-4222-8f91-53d8cd76f507.png)
