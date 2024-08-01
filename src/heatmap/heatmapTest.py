import matplotlib.pyplot as plt
import numpy as np
from PIL import Image 

a = np.random.random((16, 16))
plt.imshow(a, cmap='hot', interpolation='nearest')
#plt.show()
#plt.savefig('foo.png')
plt.axis('off')

plt.savefig('foo.png', transparent=True, bbox_inches='tight')




  
img = Image.open('foo.png') 
rgba = img.convert("RGBA") 
datas = rgba.getdata() 
  
newData = [] 
for item in datas: 
        newData.append((item[0], item[1], item[2], 40))  # other colours remain unchanged 
  
rgba.putdata(newData) 
rgba.save("transparent_image.png", "PNG") 