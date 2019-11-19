# -*- coding: utf-8 -*-

import numpy as np
#from scipy import misc

import pywt
import imageio
#import pywt._dwt as pywt

def getPlaneBits(planeId, binary_image):
    return [int(b[planeId]) for b in binary_image]

def getBitPlanes(img):
    bin_image = []
    bit_planes = []

    for i in range(0, 512):
        for j in range(0, 512):
            bin_image.append(np.binary_repr(img[i][j], width = 8))
            
    for i in range(0, 8):
        bit_planes.append(np.array(getPlaneBits(i, bin_image)).reshape(512, 512))
            
    return bit_planes

from scipy.stats import pearsonr

def autocor(A, k, l):
    Xk = A[0:512 - k, 0:512 - l]
    Xl = A[k:512, l:512]
    return pearsonr(Xk.flatten(), Xl.flatten())

def getHl1(img_hist, l):
    return img_hist[0:256 - l]

def getHl2(img_hist, l):
    return img_hist[l:256]

def getCHl(img_hist, l):
    return pearsonr(getHl1(img_hist, l), getHl2(img_hist, l))

def getModifiedWavelet(C, t):
    for i, row in enumerate(C):
        for j, val in enumerate(row):
            if abs(val) < t:
                C[i][j] = 0
    return C

def getE(img, t):
    coeffs = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs

    LH = getModifiedWavelet(LH, t)
    HL = getModifiedWavelet(HL, t)
    HH = getModifiedWavelet(HH, t)

    img_denoised = pywt.idwt2((LL, (LH, HL, HH)), 'haar')

    E = img - img_denoised
    
    return E

def getCE(img, t, k, l):
    E = getE(img, t)
    return autocor(E, k, l)

#import pywt
#import pywt._dwt as dwt

def getFeatures(filename):
    features = []
    
    img = imageio.imread(filename, pilmode='RGB')
    bit_planes = getBitPlanes(img)

    autocor_kl_pairs = [[1, 0], [2, 0], [3, 0], [4, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 1], [2, 2], [3, 3], [4, 4],
                       [1, 2], [2, 1]]

    M1 = bit_planes[0]
    M2 = bit_planes[1]

    features.append(pearsonr(M1.flatten(), M2.flatten())[0])

    for pair in autocor_kl_pairs:
        features.append(autocor(M1, pair[0], pair[1])[0])

    img_hist, bin_edges = np.histogram(img.flatten(), bins = list(range(0, 257)), density = True)

    He = [img_hist[i] for i in range(0, 256, 2)]
    Ho = [img_hist[i] for i in range(1, 256, 2)]

    features.append(pearsonr(He, Ho)[0])

    for i in range(1, 5):
        features.append(getCHl(img_hist, i)[0])
        
    autocor_tkl_triplets = [[1.5, 0, 1], [1.5, 1, 0], [1.5, 1, 1], [1.5, 0, 2], [1.5, 2, 0], [1.5, 1, 2], [1.5, 2, 1],
                       [2, 0, 1], [2, 1, 0], [2, 1, 1], [2, 0, 2], [2, 2, 0], [2, 1, 2], [2, 2, 1], [2.5, 0, 1],
                       [2.5, 1, 0], [2.5, 1, 1], [2.5, 0, 2], [2.5, 2, 0], [2.5, 1, 2], [2.5, 2, 1]]

    for triplet in autocor_tkl_triplets:
        features.append(getCE(img, triplet[0], triplet[1], triplet[2])[0])

    return features

import csv

n_images = 200
n_test = 5

feature_set = []

# Generate csv file that stores CF data for stega and original images
for i in range(1, n_images + 1):
    #features = getFeatures('original/' + str(i) + '.pgm')
    features = getFeatures("C:\\Users\\user pc\\Desktop\\dataset\\learn dataset\\"+str(i)+".bmp")
    feature_set.append(features)
    print (i, features)
    
dataset = open('original.csv', 'w')

#use this to store stega extraction feature in stega.csv file
#dataset = open ('stega.csv', 'w')

print ("Writing to csv file...")

with dataset:
    writer = csv.writer(dataset)
    writer.writerows(feature_set)

print ("Write complete.")