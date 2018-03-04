import numpy as np
import train, utils


model = train.build_model()


def predict(pic_path, model_path):
    model.load_weights(model_path)
    data = np.empty((1, 60, 120, 3), dtype="uint8")
    raw_img = utils.load_img(pic_path)
    data[0] = raw_img / 255

    out = model.predict(data)
    result = np.array([np.argmax(i) for i in out])
    return ''.join([utils.CAT2CHR[i] for i in result])


if __name__ == '__main__':
    answer = predict('images/0092.png', 'models/12.hdf5')
    print(answer)
