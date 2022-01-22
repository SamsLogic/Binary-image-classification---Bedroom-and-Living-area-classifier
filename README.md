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

![image](https://user-images.githubusercontent.com/41964069/150639500-914ca33e-9a92-4908-822f-6b83a082d08b.png)

## Approach

## Preprocessing

The preprocssing of the data includes billateral filteration. canny edge detection and dilusion of the image to get an edge based visualization of the images. As shown below the edges are also enough to identify if the location shown in the image is a bedroom or a living room.

![image](https://user-images.githubusercontent.com/41964069/150639031-6f154e2e-41aa-4cc1-9a5b-95e6afb58088.png)

## Model

For this problem CNN model was used with a residual network approach. The model includes 5 CNN layers, 2 residual layers and 4 feedforward networks. The CNN stacks were created keeping in mind to starting with Huge kernels to look through the global data in the image and then with smaller kernels to look though the minute details in the images.

## Training and validation

Cross validated training with 5 Kfolds was done with to traing the images and validate the performace over 5 diffferent datatypes. As per the validation. the AUDO score of the validation data is 0.74. whcih is a fairly good score gien the type of dataset and the low size of the deep neural network.

## Testing results

The testing was done on a totally different set of images from a hotel room that i was staying at during my vacation. I took 8 pictures of the bedroom and the living room fom the dataset and tested the results. Shockingly the results were pretty amazing (Only after some fail iterations and improving my model and preprocssing).

Preprocessed images -

![image](https://user-images.githubusercontent.com/41964069/150639486-7edce848-e8c0-44d8-94b3-47633c167019.png)

Final Prediction - 

![image](https://user-images.githubusercontent.com/41964069/150639471-2562a4a2-4da9-4929-8265-85387041e0ab.png)

## Future Possible Approaches

1. Using a better preprocessing with lower loss in data feature
2. Increasing the CNN layers and trying different kernel sizes
3. Using a new activation fuinction like the swish activation
4. Increasing the test data for better and accurate test results
