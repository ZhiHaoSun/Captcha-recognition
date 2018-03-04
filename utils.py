import os
import cv2
import numpy as np

APPEARED_LETTERS = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
]
CAT2CHR = dict(zip(range(len(APPEARED_LETTERS)), APPEARED_LETTERS))
CHR2CAT = dict(zip(APPEARED_LETTERS, range(len(APPEARED_LETTERS))))

def load_img(fn, flags=None):
    img = cv2.imread(fn)
    return img

def save_img(img, fn):
    status = cv2.imwrite(fn, img)
    if status is False:
        print(img)
        cv2.imshow(fn, img)
        cv2.waitKey(0)

def distinct_char(folder):
    chars = set()
    for fn in os.listdir(folder):
        if fn.endswith('.png'):
            for letter in fn.split('.')[0]:
                chars.add(letter)
    return sorted(list(chars))


def load_data(folder):
    img_list = [i for i in os.listdir(folder) if i.endswith('png')]

    images_num = len(img_list)
    print('total images:', images_num)
    data = np.empty((images_num, 60, 120, 3), dtype="uint8")  # channel last
    label = np.empty((images_num, 4))
    for index, img_name in enumerate(img_list):
        raw_img = load_img(os.path.join(folder, img_name))

        data[index, :, :, :] = raw_img / 255
        label[index, :] = [CHR2CAT[c] for c in img_name.split('.')[0]]
        if index % 100 == 0:
            print('{} letters loads'.format(index*4))
    print(data.shape)
    return data, label


if __name__ == '__main__':
    # print(distinct_char('../data'))
    d, l = load_data('images')
    for n, i in enumerate(d):
        cv2.imshow(CAT2CHR[l[n]], i*255)
        print(CAT2CHR[l[n]])
        cv2.waitKey(0)
