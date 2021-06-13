
# Face Analyzer


#### install opencv & dnn from source (optional)
Both opencv dnn & haar cascade are used for face detection, if you want to use haar cascade you can skip this part.

install dependencies
```
$ sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
$ sudo apt-get install libv4l-dev libxvidcore-dev libx264-dev
$ sudo apt-get install libgtk-3-dev
$ sudo apt-get install libatlas-base-dev gfortran
```
Download & install opencv with contrib modules from source
```
sudo apt update && sudo apt install -y cmake g++ wget unzip
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib
cd opencv
mkdir -p build && cd build
cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules ../
cmake --build .
```

if you **don't** want to use **dnn** modules just setup opencv with regular way
```
sudo apt-get install python3-opencv
```

#### Run Camera Demo
##### Live camera demo
```python
$ python3 camera_demo.py

# add '--haar' option if you want to use Haar cascade detector instead of dnn opencv face detector
$ python3 camera_demo.py --haar
```

##### Video / Image demo
```python
# image
$ python3 camera_demo.py --image --path PATH_TO_IMAGE

# video
$ python3 camera_demo.py --path PATH_TO_VIDEO
```


##### Sockets Test
```python
# run the server that stores faces info and send it to the receiver
python3 server.py

# run the upd client which will receive the data preiodically (the GUI or the meeting organizer)
python3 udp_receiver.py

# run the camera_demo to send the data of 1 face to the server
python3 camera_demo.py
```

