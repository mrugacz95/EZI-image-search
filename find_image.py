import argparse
import os
import re

import numpy as np
import pandas as pd
import sys


def sigmoid(x):
    return 1 / (1 + np.exp(-8 + 2 * x))


def find(image_files, features, image_agg='avg', feature_agg_func='avg', ):
    for image_path in image_files:
        image_path = os.path.join('images/', image_path)
        if not os.path.isfile(image_path):
            print('Image not found: ' + image_path)
            return
    for feature in features:
        feature_path = os.path.join('features', feature + '.dat')
        if not os.path.isfile(feature_path):
            print('Feature not found')
    all_features = []
    names = None

    def read_features(feature):
        feature_path = os.path.join('features', feature + '.dat')
        full = pd.read_csv(feature_path, delimiter=' ')
        full = full.dropna(axis=1, how='all')
        names = full.iloc[:, 0]
        features = full.iloc[:, 1:].values
        normalized = (features - features.mean(axis=0)) / features.std(axis=0)
        return names, normalized

    for feature in features:
        names, normalized = read_features(feature)
        all_features.append(normalized)

    def similarity(data1, data2):
        return np.linalg.norm(data1 - data2, ord=3)

    sim = np.empty((len(names), len(image_files), len(features)))
    for image_idx, image_file in enumerate(image_files):
        for feature_idx, feature in enumerate(features):
            normalized = all_features[feature_idx]
            current_img_idx = np.where(names == image_file)[0]
            for row_idx, row in enumerate(normalized):
                sim[row_idx, image_idx, feature_idx] = sigmoid(similarity(row, normalized[current_img_idx][0]))
    agg_dict = {
        'ave': np.average,
        'min': np.min,
        'max': np.max
    }
    img_agg_func = agg_dict[image_agg]
    feature_agg_func = agg_dict[feature_agg_func]
    sim = img_agg_func(sim, axis=1)
    sim = feature_agg_func(sim, axis=1)
    for result_idx in np.argsort(-sim):
        print(f'{names[result_idx]:<80} {sim[result_idx]:.2f}')


def main():
    arguments = ' '.join(sys.argv[1:])
    match = re.match('((?P<images_agg>(min|ave|max))\s)?'
                     '((?P<images_num>\d+)\s)?'
                     '(?P<images>(\s?\d+\.jpeg)+)\s'
                     '(?P<features_agg>(min|ave|max))?\s?'
                     '(?P<features_num>\d+)?\s?'
                     '(?P<features>(\s?(ColorHCLCov|ColorHist256|ColorHist64|ColorLabCov|ColorRGBCov|TextureLumGabor))+)',
                     arguments)
    if match == None:
        print('Usage:\n<[min|avg|max]> <images_num> [image1, image2, ...]'
              ' <[min|avg|max]> <features_num> [feature1, feature2, ...]')
        return
    match_dict = match.groupdict()
    images = match_dict['images'].split(' ')
    features = match_dict['features'].split(' ')
    images_num = match_dict['images_num']
    if images_num is None:
        images_num = 1
    else:
        images_num = int(images_num)
    if len(images) != images_num:
        print('Wrong number of images')
        return
    features_num = match_dict['features_num']
    if features_num is None:
        features_num = 1
    else:
        features_num = int(features_num)
    if len(features) != features_num:
        print('Wrong number of features')
        return
    image_agg = match_dict['images_agg']
    if image_agg == None:
        image_agg = 'avg'
    features_agg = match_dict['features_agg']
    if features_agg == None:
        features_agg = 'avg'
    find(images, features, image_agg, features_agg)


if __name__ == '__main__':
    main()
