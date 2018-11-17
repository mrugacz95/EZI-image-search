import os
from argparse import ArgumentParser

import matplotlib.image as mpimg
import pandas as pd


def load_image():
    pass


def main():
    parser = ArgumentParser()
    parser.add_argument('image_path', help='Path to image')
    parser.add_argument('feature', help='Feature used in searching')
    args = parser.parse_args()
    if not os.path.isfile(args.image_path):
        print('Image not found')
        return
    image = mpimg.imread(args.image_path)
    # plt.imshow(image)
    # plt.show()
    feature_path = os.path.join('features', args.feature + '.dat')
    if not os.path.isfile(feature_path):
        print('Feature not found')
    feature = pd.read_csv("Data/sim.csv", sep=" ")
    feature = feature.set_index[0]
    normalized = feature / feature.max(axis=0)
    pass


if __name__ == '__main__':
    main()
