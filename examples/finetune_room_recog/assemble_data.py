#!/usr/bin/env python
"""
List images from a directory and write
Caffe ImagesDataLayer training file.
"""
import os
import argparse
import multiprocessing
import itertools

example_dirname = os.path.abspath(os.path.dirname(__file__))
caffe_dirname = os.path.abspath(os.path.join(example_dirname, '../..'))
training_dirname = os.path.join(caffe_dirname, 'data/room_recog')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='List images and output training output.')
    parser.add_argument(
        '-i', '--images', nargs='+',
        help="Images sorted grouped by directory")
    parser.add_argument(
        '-t', '--test', nargs='+',
        help="Images sorted grouped by for use in test set")

    args = parser.parse_args()
    rooms = itertools.groupby(args.images, lambda i: os.path.basename(os.path.dirname(i)))
    test = itertools.groupby(args.test, lambda i: os.path.basename(os.path.dirname(i)))

    if not os.path.exists(training_dirname):
        os.makedirs(training_dirname)
        
    with open(os.path.join(training_dirname, 'test.txt'), 'w') as t:
        with open(os.path.join(training_dirname, 'train.txt'), 'w') as f:
            for idx, room in enumerate(rooms):
                for image_file in room[1]:
                    if image_file in args.test:
                        t.write('%s %s\n' % (image_file, idx))
                    else:
                        f.write('%s %s\n' % (image_file, idx))

