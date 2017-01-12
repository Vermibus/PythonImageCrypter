 Application for Python Image Crypter
---

#### *Feel free to use*

I have created a simple implementation of pure steganography in python.  
In my encrypt/decrypt scripts I'm changing/reading only the least important bit from each color of RGB pixel.

Required: 
---
**Python 3.4.3** (PySide is not supported on Python 3.5.0)

**PySide 1.2.2** (I didn't make research with older versions) 

PySide can be easly downloaded via [PIP](https://pypi.python.org/pypi/pip)
``` 
pip install PySide
```

About AoPIC
---

Main file is app/main_app.py. 
There is still a lot to code in this project, but feel free to coment. 

Next milestone:
* Implement RSA encryption
* Add one more bit for hidden image on each pixel color. From 3bit-8colors to 6bit-64colors ! 
* Create nice UI 

_Version:_
_1.0_
