
import cv2
import numpy as np
import matplotlib
import skimage
import sklearn
import pandas as pd

print("Ambiente de Processamento de Imagens")
print(f"OpenCV: {cv2.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")
print(f"scikit-image: {skimage.__version__}")
print(f"scikit-learn: {sklearn.__version__}")
print(f"Pandas: {pd.__version__}")

# Teste básico de processamento
imagem = np.zeros((100, 100), dtype=np.uint8)
cv2.rectangle(imagem, (25, 25), (74, 74), 255, -1)

print(f"Dimensões da imagem de teste: {imagem.shape}")
print(f"Intensidade máxima: {imagem.max()}")

print("Ambiente validado com sucesso!")
