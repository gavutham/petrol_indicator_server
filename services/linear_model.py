from sklearn.linear_model import SGDRegressor
import numpy as np
from firebase import save_model, retrieve_model, get_all_refills

# x = np.array([[2], [3]])
# y = np.array([4, 6])


def train_model():
    vid = "e9c12f48-ba6c-4679-be86-c450e6f15aa7"
    refill_data = get_all_refills(vid)
    x = []
    y = []

    for i in range(1, len(refill_data)):
        km = int(refill_data[i]["kilometers"]) - int(refill_data[i - 1]["kilometers"])
        fuel = int(refill_data[i]['after']) - int(refill_data[i - 1]["before"])
        x.append([fuel])
        y.append(km)

    model = SGDRegressor()
    model.fit(x, y)

    save_model(model, vid)


def fit_partially(model):
    model.partial_fit(np.array([[4]]), np.array([9]))


