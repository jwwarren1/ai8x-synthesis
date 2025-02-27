#!/usr/bin/env python3
###################################################################################################
# Copyright (C) Maxim Integrated Products, Inc. All Rights Reserved.
#
# Maxim Integrated Products, Inc. Default Copyright Notice:
# https://www.maximintegrated.com/en/aboutus/legal/copyrights.html
###################################################################################################
"""
Test the conv1d operator.
"""
import os
import sys

import numpy as np
import torch

# Allow test to run outside of pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from izer import compute, state  # noqa: E402 pylint: disable=wrong-import-position


def convolve1d(groups, data, weight, bias, pad, expected, stride=1):
    """Convolve 1d data"""
    print('Input:\n', data)

    t = torch.nn.functional.conv1d(
        torch.as_tensor(data, dtype=torch.float).unsqueeze(0),  # Add batch dimension
        torch.as_tensor(weight, dtype=torch.float),
        bias=torch.as_tensor(bias, dtype=torch.float) if bias is not None else None,
        stride=stride,
        padding=pad,
        groups=groups,
        dilation=1,
    ).int().squeeze(axis=0).numpy()

    output = compute.conv1d(
        data,
        weight,
        bias,
        data.shape,
        expected.shape,
        kernel_size=9,
        stride=stride,
        pad=pad,
        dilation=1,
        groups=groups,
    )

    print("PYTORCH OK" if np.array_equal(output, t) else "*** FAILURE ***")
    assert np.array_equal(output, t)

    print('Output before division:\n', output)
    output += 64
    output //= 128
    print('Output:\n', output)

    expected += 64
    expected //= 128

    print('Expected:\n', expected)
    print("SUCCESS" if np.array_equal(output, expected) else "*** FAILURE ***")

    assert np.array_equal(output, expected)


def test_conv1d():
    """Main program to test compute.conv1d."""
    state.debug = True

    d0 = np.array(
        [[-31, 45, 119, 29, 103, 127, -92, -42, 13, 127, 127, 105, -128, 40, -128, 25, -34],
         [-81, 127, 54, -25, -23, 49, 19, 96, 127, 67, -128, -8, -128, 108, 80, 127, -90],
         [-128, -128, 64, 25, 127, 26, 127, -112, -128, -62, -60, 127, -47, 61, -128, -67, -33]],
        dtype=np.int64)

    w0 = np.array(
        [[[-1, -56, -24, 125, 90, 127, -55, 37, -33],
          [-119, 127, -33, -128, 97, 101, -128, -128, -12],
          [-60, 116, -128, -62, -56, 85, 108, -11, 42]],
         [[60, 127, -128, -117, -128, 87, 127, -128, 127],
          [7, 120, -92, -128, -51, -44, -128, -128, 97],
          [-70, 127, 127, 36, 124, -80, 44, 127, -82]],
         [[-82, 42, 48, 127, -92, 63, 127, 127, -128],
          [91, -5, 4, -33, 83, -28, -128, 127, -119],
          [-22, 97, 118, -49, -128, -128, 60, -128, 69]],
         [[-84, 127, -128, -70, 19, -58, -128, 127, -2],
          [127, 81, -60, 33, -128, -55, 10, -46, 127],
          [-71, -114, 98, 105, 64, -2, -67, 64, 82]],
         [[-71, 78, -128, 127, 1, -128, -81, 127, -64],
          [-9, 127, -83, -128, -61, -65, 127, 118, -67],
          [-56, 127, 127, 127, -119, 77, 95, 4, 99]]],
        dtype=np.int64)

    e00 = np.array(
        [[28176, -23269, -80134, -5457, 20372, 60838, 43704, -25237, -29043],
         [5219, -24047, -24911, 13560, 35007, 24223, -106564, -18514, -51368],
         [-31662, -18736, 38504, 49859, 95049, -6485, -21362, -18296, 23517],
         [14631, 45702, -15616, -18696, -32693, -79537, 12559, 4471, 51313],
         [-13630, 77478, 3115, -9839, -25421, -89124, -25032, 3245, 69909]],
        dtype=np.int64)
    e01 = np.array(
        [[-10105, 28176, -23269, -80134, -5457, 20372, 60838, 43704, -25237, -29043, -72560],
         [-32032, 5219, -24047, -24911, 13560, 35007, 24223, -106564, -18514, -51368, 26843],
         [-60506, -31662, -18736, 38504, 49859, 95049, -6485, -21362, -18296, 23517, -17603],
         [-40116, 14631, 45702, -15616, -18696, -32693, -79537, 12559, 4471, 51313, 8520],
         [-73880, -13630, 77478, 3115, -9839, -25421, -89124, -25032, 3245, 69909, -42416]],
        dtype=np.int64)
    e02 = np.array(
        [[50031, -10105, 28176, -23269, -80134, -5457, 20372,
          60838, 43704, -25237, -29043, -72560, 50788],
         [-57260, -32032, 5219, -24047, -24911, 13560, 35007,
          24223, -106564, -18514, -51368, 26843, 49440],
         [36496, -60506, -31662, -18736, 38504, 49859, 95049,
          -6485, -21362, -18296, 23517, -17603, 28969],
         [-10400, -40116, 14631, 45702, -15616, -18696, -32693,
          -79537, 12559, 4471, 51313, 8520, -21330],
         [-3311, -73880, -13630, 77478, 3115, -9839, -25421,
          -89124, -25032, 3245, 69909, -42416, 20639]],
        dtype=np.int64)
    e06 = np.array(
        [[-16821, -58373, 3847, 69949, 50031, -10105, 28176, -23269, -80134,
          -5457, 20372, 60838, 43704, -25237, -29043, -72560, 50788, -49841,
          34629, -971, 13255],
         [-22370, -19874, 14910, 16757, -57260, -32032, 5219, -24047, -24911,
          13560, 35007, 24223, -106564, -18514, -51368, 26843, 49440, -61755,
          -3474, -33109, 20187],
         [19737, 13245, 35841, 7580, 36496, -60506, -31662, -18736, 38504,
          49859, 95049, -6485, -21362, -18296, 23517, -17603, 28969, -3082,
          -11840, -18915, 8622],
         [15283, 26137, -13012, -22805, -10400, -40116, 14631, 45702, -15616,
          -18696, -32693, -79537, 12559, 4471, 51313, 8520, -21330, -60662,
          7915, -10600, 57618],
         [-4645, 23736, 7925, -17220, -3311, -73880, -13630, 77478, 3115,
          -9839, -25421, -89124, -25032, 3245, 69909, -42416, 20639, -87881,
          18736, -42547, 32737]],
        dtype=np.int64)
    e06s = np.array(
        [[-16821, 69949, 28176, -5457, 43704, -72560, 34629],
         [-22370, 16757, 5219, 13560, -106564, 26843, -3474],
         [19737, 7580, -31662, 49859, -21362, -17603, -11840],
         [15283, -22805, 14631, -18696, 12559, 8520, 7915],
         [-4645, -17220, -13630, -9839, -25032, -42416, 18736]],
        dtype=np.int64)

    convolve1d(1, d0, w0, None, 0, e00)
    convolve1d(1, d0, w0, None, 1, e01)
    convolve1d(1, d0, w0, None, 2, e02)
    convolve1d(1, d0, w0, None, 6, e06)
    convolve1d(1, d0, w0, None, 6, e06s, stride=3)

    d1 = np.array(
        [[-31, 45, 119, 29, 103, 127, -92, -42, 13, 127, 127, 105, -128, 40, -128, 25, -34],
         [-81, 127, 54, -25, -23, 49, 19, 96, 127, 67, -128, -8, -128, 108, 80, 127, -90],
         [-128, -128, 64, 25, 127, 26, 127, -112, -128, -62, -60, 127, -47, 61, -128, -67, -33]],
        dtype=np.int64)

    w1 = np.array(
        [[[-1, -56, -24, 125, 90, 127, -55, 37, -33]],
         [[60, 127, -128, -117, -128, 87, 127, -128, 127]],
         [[-56, 127, 127, 127, -119, 77, 95, 4, 99]]],
        dtype=np.int64)

    e10 = np.array(
        [[26756, 3816, -2161, -28225, 8166, 23386, 55516, -2426, 5599],
         [20743, 20195, -5507, 9722, -50736, -12422, -14995, 37782, 41703],
         [-11951, 23995, -23063, 44075, -1292, 4867, -45440, -45560, 2398]],
        dtype=np.int64)
    e11 = np.array(
        [[22219, 26756, 3816, -2161, -28225, 8166, 23386, 55516, -2426, 5599, -41048],
         [-15679, 20743, 20195, -5507, 9722, -50736, -12422, -14995, 37782, 41703, 24549],
         [-25690, -11951, 23995, -23063, 44075, -1292, 4867, -45440, -45560, 2398, -17600]],
        dtype=np.int64)
    e12 = np.array(
        [[22832, 22219, 26756, 3816, -2161, -28225, 8166,
          23386, 55516, -2426, 5599, -41048, -4410],
         [-20358, -15679, 20743, 20195, -5507, 9722, -50736,
          -12422, -14995, 37782, 41703, 24549, -15569],
         [-13461, -25690, -11951, 23995, -23063, 44075, -1292,
          4867, -45440, -45560, 2398, -17600, 28205]],
        dtype=np.int64)

    convolve1d(3, d1, w1, None, 0, e10)
    convolve1d(3, d1, w1, None, 1, e11)
    convolve1d(3, d1, w1, None, 2, e12)

    d2 = d1
    w2 = w1

    b2 = np.array(
        [100, -200, 300],
        dtype=np.int64)

    e20 = np.array(
        [[26856, 3916, -2061, -28125, 8266, 23486, 55616, -2326, 5699],
         [20543, 19995, -5707, 9522, -50936, -12622, -15195, 37582, 41503],
         [-11651, 24295, -22763, 44375, -992, 5167, -45140, -45260, 2698]],
        dtype=np.int64)
    e21 = np.array(
        [[22319, 26856, 3916, -2061, -28125, 8266, 23486, 55616, -2326, 5699, -40948],
         [-15879, 20543, 19995, -5707, 9522, -50936, -12622, -15195, 37582, 41503, 24349],
         [-25390, -11651, 24295, -22763, 44375, -992, 5167, -45140, -45260, 2698, -17300]],
        dtype=np.int64)
    e22 = np.array(
        [[22932, 22319, 26856, 3916, -2061, -28125, 8266, 23486,
          55616, -2326, 5699, -40948, -4310],
         [-20558, -15879, 20543, 19995, -5707, 9522, -50936, -12622,
          -15195, 37582, 41503, 24349, -15769],
         [-13161, -25390, -11651, 24295, -22763, 44375, -992, 5167,
          -45140, -45260, 2698, -17300, 28505]],
        dtype=np.int64)

    convolve1d(3, d2, w2, b2, 0, e20)
    convolve1d(3, d2, w2, b2, 1, e21)
    convolve1d(3, d2, w2, b2, 2, e22)


if __name__ == '__main__':
    test_conv1d()
