from sklearn.linear_model import SGDRegressor
import numpy as np
from firebase import save_model, retrieve_model

x = np.array([[2], [3]])
y = np.array([4, 6])

model = SGDRegressor()
model.fit(x, y)


model.partial_fit(np.array([[4]]), np.array([9]))


# save_model(model)
model = retrieve_model("sample")

# print(model.predict([[4]]))
