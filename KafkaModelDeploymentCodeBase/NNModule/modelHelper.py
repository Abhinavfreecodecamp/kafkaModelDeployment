from tensorflow import keras
from PIL import Image
from io import BytesIO
import numpy as np
import pathlib

class model_helper():
    def __init__(self, logger, model_path):
        self.logger = logger
        self.model = self.initialize_model()
        self.model_path = model_path
        self.classConfig = {0: 'T-Shirt/top',
                            1: 'Trouser',
                            2: 'Pullover',
                            3: 'Dress',
                            4: 'Coat',
                            5: 'Sandal',
                            6: 'Shirt',
                            7: 'Sneaker',
                            8: 'Bag',
                            9: 'Ankle boot'}

    def initialize_model(self):
        path = pathlib.Path(__file__).resolve().parent.parent
        model = keras.models.load_model(os.path.join(path,self.model_path))
        return model

    def decode_image(self, imageStream):
        try:
            stream = BytesIO(imageStream)
            image = Image.open(stream)
            image = np.asarray(image)
            return image
        except Exception as e:
            self.logger.warning(f'failed to convert image array {e}')
            return None


    def get_message_images(self, messageList):
        successImages, successReqId = np.array([]), np.array([])
        for item in messageList:
            try:
                requestId = item['requestId']
                image = self.decode_image(imageStream=item['image'])
                if image is not None:
                    successImages = np.append(successImages, image)
                    successReqId = np.append(successReqId, [requestId])
            except Exception as e:
                self.logger.error(f'failed to consume messages {e}')
                return None, None
    

    def getInference(self, consumedMessage=[]):
        if len(consumedMessage) <= 0:
            return None
        requestId, imageStream = self.get_message_images(messageList=consumedMessage)

        self.logger.info('reshaping/normalizing Images for cnn....')
        imageStream = imageStream.reshape((imageStream.shape[0], 28, 28, 1))
        imageStream = imageStream / 255.0

        self.logger.info('predicting class labels for images....')
        classes = self.model.predict_classes(imageStream)

        classLabelName = []
        for classlabel in classes:
            classLabelName.append(self.classConfig[classlabel])
        
        return requestId, classLabelName
