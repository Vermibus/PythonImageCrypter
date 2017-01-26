 Implementation of pure steganography. 
---

I have created a simple implementation of pure steganography in python.  
In my encrypt/decrypt scripts I'm changing/reading 2 last bits of each RGB pixel. 

Required: 
---
**Python 3.4.3** (PySide is not supported on Python 3.5.0)

**PySide 1.2.2** (I didn't make research with older versions) 

**Pillow 4.0.0** (I didn't make research with older versions) 

PySide and Pillow can be easily downloaded via [PIP](https://pypi.python.org/pypi/pip)

``` 
pip install PySide Pillow
```

About AoPIC
---

Main file is app/main_app.py.  
There is still a lot to code in this project, but feel free to share/coment.   
  
The program converts the image to sixty four color equivalent. 

#### Screens of app:  

![Alt text](/readmeSRC/encode.png?raw=true)
![Alt text](/readmeSRC/decode.png?raw=true)

Next milestone:
* Implement RSA encryption
* Create nice UI 

_Version:_
_1.1_


 *Feel free to use*  
 *~Vermibus*
