# import pandas as pd
# from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split

from utlis import *
import pandas as pd

path = 'E:/CARLA_0.9.5/PythonAPI/MyProject/carla_dataset/'

data = pd.read_csv((path+'out.csv'))
# print(type(data))
# print(data)
# print(len(data))

# img_name = int(data['Center'][0])
# print(img_name)

# data = balanceData(data, display=False)
# data = pd.DataFrame(data)
# print(len(data))

imagesPath, steering, throttle = loadData(path, data)

# print(imagesPath)
# print(steerings[0])
# print(throttle[0])
# data_frame = pd.DataFrame(imagesPath)
# data_frame.to_csv("imagesPath.csv")

xTrain, xVal, yTrain, yVal = train_test_split(imagesPath, steering, test_size=0.2,random_state=10)
print('Total Training Images: ',len(xTrain))
print('Total Validation Images: ',len(xVal))

model = createModel()
model.summary()
# batch = batchGenerator(xTrain, yTrain, 100, 0)

history = model.fit(batchGenerator(xTrain, yTrain, 10, 1),
                                  steps_per_epoch=300,
                                  epochs=10,
                                  validation_data=batchGenerator(xVal, yVal, 10, 0),
                                  validation_steps=200)

model.save('Models/Model_1.h5')
print('Model Saved')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()

