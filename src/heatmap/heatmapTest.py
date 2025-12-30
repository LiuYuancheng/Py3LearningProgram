import matplotlib.pyplot as plt
import numpy as np
from PIL import Image 
import scipy.ndimage as sp

a = np.random.random((24, 36))
for i in range(len(a)):
    for j in range(len(a[i])):
        if a[i][j] < 0.5:
            a[i][j] = 0

plt.imshow(a, cmap='hot', interpolation='nearest')

#plt.imshow(a, origin='lower', cmap='hot', interpolation='bilinear')

#plt.show()
#plt.savefig('foo.png')
plt.axis('off')

plt.savefig('foo.png', transparent=True, bbox_inches='tight')


# x = [i[0] for i in a ]
# y = [i[1] for i in a ]
# X = sp.filters.gaussian_filter(x, sigma = 2, order = 0)
# Y = sp.filters.gaussian_filter(y, sigma = 2, order = 0)


# heatmap, xedges, yedges = np.histogram2d(X, Y, bins=40)
# extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

# fig1 = plt.subplot(2,2,2)
# plt.imshow(heatmap, extent=extent)
# plt.savefig('foo2.png', transparent=True, bbox_inches='tight')
  
img = Image.open('foo.png') 
rgba = img.convert("RGBA") 
datas = rgba.getdata() 
  
newData = [] 
for item in datas: 
        newData.append((item[0], item[1], item[2], 40))  # other colours remain unchanged 
  
rgba.putdata(newData) 
rgba.save("transparent_image.png", "PNG") 