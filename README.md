# Pynq-Frontend
Contains code for WIP Frontend code for pynq supported boards powering our farming rack.

![alt text](https://github.com/ProjectHydroTech/Pynq-Frontend/blob/main/images/homepage.png?raw=true)
# Features
Frontend is hosted locally on the Pynq board, allowing for easy user setup of wifi, firebase login and camera feed monitoring. 
Currently only allows for up to 2 webcams connected through usb with firebase image uploading every set interval with timestamps. This problaby due to USB Bandwidth limitations as any higher than 2 webcams returns empty frame that cannot be shown.

# Pre-Requisites 
Flask, OpenCV, Pyrebase

# How to use

```
#clone this repo with 
git clone https://github.com/ProjectHydroTech/Pynq-Frontend.git
```
```
#then run this at the directory before the cloned repo
set FLASK_APP=Pynq-Frontend
flask run
```
Then go to localhost:5000 in any web browser to access frontend

# How the Wifi Works
![alt text](https://github.com/ProjectHydroTech/Pynq-Frontend/blob/main/images/wifi.png?raw=true)

```
@main.route('/wifi', methods=['POST'])
def wifi_post():
    wifissid = request.form.get('email')
    wifipassword = request.form.get('password')
    print(wifissid)
    print(wifipassword)

    from pynq.lib import Wifi
    port = Wifi()

    port.connect(wifissid, wifipassword)

    response = os.system("ping -c 1 " + "www.google.com")
    
    if response == 0:
        return render_template('wifi.html')
    else:
        return redirect(url_for('main.wifi'))
```
This section at the end of main.py defines the wifi login process, which is essentially integrating the getting-started/wifi file in the root directory of Pynq. The code then checks internet connection by pinging google and redirects u back to the main page if successful.

# How Webcam Feed works
![alt text](https://github.com/ProjectHydroTech/Pynq-Frontend/blob/main/images/webcam%20feed.png?raw=true)

Code here pulls from my other repo:
https://github.com/ProjectHydroTech/Stream-Camera-over-HTTP

Essentially works the same, but camera portion of code is defined as flask blueprint in init.py and local import locations for base_camera and camera_opencv changed to be neater.

-Marcus
