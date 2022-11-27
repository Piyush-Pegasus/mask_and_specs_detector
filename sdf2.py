from keras.models import load_model
from PIL import Image, ImageOps #Install pillow instead of PIL
import numpy as np

from flask import Flask,request
import werkzeug

app= Flask(__name__)



@app.route('/api1', methods=["POST"])
def upload_and_detect1():
			if(request.method=="POST"):
					imagefile= request.files['image']
					filename=werkzeug.utils.secure_filename(imagefile.filename)
					imagefile.save("./uploaded1/"+filename)
					
			res={}

			# Disable scientific notation for clarity
			np.set_printoptions(suppress=True)

			# Load the model
			model = load_model('MASK.h5', compile=False)
			file="./uploaded1/"+filename
			
			# Load the labels
			class_names = open('labels_mask.txt', 'r').readlines()

			# Create the array of the right shape to feed into the keras model
			# The 'length' or number of images you can put into the array is
			# determined by the first position in the shape tuple, in this case 1.
			data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

			# Replace this with the path to your image
			image = Image.open(file).convert('RGB')

			#resize the image to a 224x224 with the same strategy as in TM2:
			#resizing the image to be at least 224x224 and then cropping from the center
			size = (224, 224)
			image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

			#turn the image into a numpy array
			image_array = np.asarray(image)

			# Normalize the image
			normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

			# Load the image into the array
			data[0] = normalized_image_array

			# run the inference
			prediction = model.predict(data)
			index = np.argmax(prediction)
			class_name = class_names[index]
			confidence_score = prediction[0][index]
			res['output']=class_name
			res['confidence']=str(confidence_score-0.00923)
			return res
			# print('Class:', class_name, end='')
			# print('Confidence score:', confidence_score)
# @app.route('/api2', methods=["POST"])
# def upload_and_detect2():
# 			if(request.method=="POST"):
# 					imagefile= request.files['image']
# 					filename=werkzeug.utils.secure_filename(imagefile.filename)
# 					imagefile.save("./uploaded2/"+filename)
					
# 			res={}

# 			# Disable scientific notation for clarity
# 			np.set_printoptions(suppress=True)

# 			# Load the model
# 			model = load_model('SPECS.h5', compile=False)
# 			file="./uploaded2/"+filename
			
# 			# Load the labels
# 			class_names = open('labels_specs.txt', 'r').readlines()

# 			# Create the array of the right shape to feed into the keras model
# 			# The 'length' or number of images you can put into the array is
# 			# determined by the first position in the shape tuple, in this case 1.
# 			data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# 			# Replace this with the path to your image
# 			image = Image.open(file).convert('RGB')

# 			#resize the image to a 224x224 with the same strategy as in TM2:
# 			#resizing the image to be at least 224x224 and then cropping from the center
# 			size = (224, 224)
# 			image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# 			#turn the image into a numpy array
# 			image_array = np.asarray(image)

# 			# Normalize the image
# 			normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# 			# Load the image into the array
# 			data[0] = normalized_image_array

# 			# run the inference
# 			prediction = model.predict(data)
# 			index = np.argmax(prediction)
# 			class_name = class_names[index]
# 			confidence_score = prediction[0][index]
# 			res['output']=class_name
# 			res['confidence']=str(confidence_score-0.00923)
# 			return res

if __name__=="__main__":
        app.run(debug=True,port=4000)

