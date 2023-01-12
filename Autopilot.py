import glob
import os
import sys
import random
import time
import numpy as np
import cv2
from PIL import Image

# from keras.models import load_model
# import tensorflow as tf

# MODEL = load_model("grayscale_model_2.h5")

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

IM_WIDTH = 800
IM_HEIGHT = 600

# img_name = 1
def preProcess(img):
    i = np.array(img.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]

    # cv2.imshow("", i3)
    # cv2.waitKey(1)

    # img = i3[250:480, :, :]
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # img = cv2.GaussianBlur(img, (3, 3), 0)
    # img = cv2.resize(img, (200, 66))
    name = img.frame_number
    print(name)
    im = Image.fromarray(np.uint8(i3))
    # im.save('DataSet/Images/{}.jpg'.format(name))

    # cv2.imshow("", i3)
    cv2.waitKey(1)

    # img = img[..., np.newaxis]
    # img = img / 255

    # img2 = tf.reshape(img, [1, 66, 200, 1])
    # steering = float(MODEL.predict(img2))
    # print(steering)
    # vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=steering))
    return img

actor_list = []


try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(5.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.filter("model3")[0]
    print(bp)


    list = world.get_map().get_spawn_points()
    print(list)
    spawn_point = list[4]

    # spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp,spawn_point)
    vehicle.set_autopilot(True)
    # vehicle.apply_control(carla.VehicleControl(throttle = 0.0, steer = 0.0))
    actor_list.append(vehicle)

    cam_bp = blueprint_library.find("sensor.camera.rgb")
    cam_bp.set_attribute('image_size_x', f'{IM_WIDTH}')
    cam_bp.set_attribute('image_size_y', f'{IM_HEIGHT}')
    cam_bp.set_attribute('fov', '110')

    # spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    spawn_point = carla.Transform(carla.Location(x=2.5, z=2))

    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to = vehicle)
    actor_list.append(sensor)
    # sensor.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame_number))
    sensor.listen(lambda data: preProcess(data))

    time.sleep(10)

finally:
    for actor in actor_list:
        actor.destroy()
    print("All cleaned up!")