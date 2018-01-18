import os
import argparse
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pickle
from PIL import Image
import glob
import sys
import shannonfano
import pickle
import copy
import ast
from collections import Counter

def Encoding(img):
    img = img.astype(int)
    endcode =copy.deepcopy(img)
    image_endcode = copy.deepcopy(img)
    for i in range(1,img.shape[0]):
        for j in range(1,img.shape[1]):
            for h in range(0,3):
                if(image_endcode[i-1,j-1][h]>=max(image_endcode[i,j-1][h],image_endcode[i-1,j][h])):
                    endcode[i,j][h] = image_endcode[i,j][h] - min(image_endcode[i,j-1][h],image_endcode[i-1,j][h])
                elif(image_endcode[i-1,j-1][h]<=min(image_endcode[i,j-1][h],image_endcode[i-1,j][h])):
                    endcode[i,j][h] = image_endcode[i,j][h] - max(image_endcode[i,j-1][h],image_endcode[i-1,j][h])
                else:
                    endcode[i,j][h] = image_endcode[i,j][h] - (image_endcode[i,j-1][h]-image_endcode[i-1,j][h]+image_endcode[i-1,j-1][h])
    listword =covertImageToList(endcode)
    encoded_doc, code_list = shannonfano.encode(listword)
    return encoded_doc, code_list 

def Decoding(encoded_doc, code_list):
    listword = shannonfano.decode(encoded_doc, code_list)
    image =convertListToImage(listword)
    
    image_decode =image
    for i in range(1,image_decode.shape[0]):
        for j in range(1,image_decode.shape[1]):
            for h in range(0,3):
                if(image_decode[i-1,j-1][h]>=max(image_decode[i,j-1][h],image_decode[i-1,j][h])):
                    image_decode[i,j][h] = image_decode[i,j][h] + min(image_decode[i,j-1][h],image_decode[i-1,j][h])
                elif(image_decode[i-1,j-1][h]<=min(image_decode[i,j-1][h],image_decode[i-1,j][h])):
                    image_decode[i,j][h] = image_decode[i,j][h] + max(image_decode[i,j-1][h],image_decode[i-1,j][h])
                else:
                    image_decode[i,j][h] = image_decode[i,j][h] + (image_decode[i,j-1][h]-image_decode[i-1,j][h]+image_decode[i-1,j-1][h])
    return image_decode

def Result_encode(strDirect,newFolder):
    for filename in glob.glob(strDirect+'/*.*'):
        name = filename.split('/')[-1].split('.')[0]
        image = cv2.imread(filename)
        image = cv2.resize(image,(500,500))
        encoded_doc, code_list = Encoding(image)
        savefile(encoded_doc, code_list,newFolder,name)

def Result_decode(strDirect,newFolder):
    N_FILES = 14
    for i in range(14, N_FILES+1):
        print('image ',i)
        encoded_file = strDirect+'/{}.txt'.format(i)
        code_list_file = strDirect+'/{}.pkl'.format(i)
        decoded_file = newFolder+'/{}.jpg'.format(i)
        encoded,coded=loadFile(encoded_file,code_list_file)
        image = Decoding(encoded,coded)
        cv2.imwrite(decoded_file,image)


# compute all images in folder
def Process_encode(strDirect,newFolder):
    #input folder images and folder to save endcoded and coded
    for filename in glob.glob(strDirect+'/*.*'):
        name = filename.split('/')[-1].split('.')[0]
        image = cv2.imread(filename)
        image = cv2.resize(image,(500,500))
        encoded_doc, code_list = Encoding(image)
        savefile(encoded_doc, code_list,newFolder,name)

def Process_decode(strDirect,newFolder):
    #input the folder of encoded and coded, and the folder to save
    N_FILES = 14
    for i in range(14, N_FILES+1):
        print('image ',i)
        encoded_file = strDirect+'/{}.txt'.format(i)
        code_list_file = strDirect+'/{}.pkl'.format(i)
        decoded_file = newFolder+'/{}.jpg'.format(i)
        encoded,coded=loadFile(encoded_file,code_list_file)
        image = Decoding(encoded,coded)
        cv2.imwrite(decoded_file,image)

import math
def entropy(image):
    size = image.shape[0]* image.shape[1]* image.shape[2]
    cvtImage2List = covertImageToList(image)
    list_value_image = Counter(cvtImage2List)
    value  = list(dict(list_value_image).values())
    measure = 0.0
    for i in range(len(value)):
        measure = measure + (value[i]/size)*(math.log((size/value[i]),2))
    return measure

#change type from Image to List
def covertImageToList(image):
    lin_img = image.flatten()
    image_list = []
    pixel_list = lin_img.tolist()
    pixel_str_list = map(str, pixel_list)
    img_str = ' '.join(pixel_str_list)
    sizeOfImage = image.shape
    words = img_str.split(' ')
    size = [str(x) for x in sizeOfImage]
    words = size + words
    return words

#change type from List to Image
def convertListToImage(words):
    size = tuple([int(x) for x in words[0:3]])
    convert = np.array(words[3:],dtype=int)
    convert = convert.reshape(size)
    return convert

#save file encoded, coded 
def savefile(encoded, coded, direct,strName):
    with open(direct+'/'+strName+'.txt', "w") as text_file:
        text_file.write(encoded)
    with open(direct+'/'+strName+'.pkl', "w") as text_file:
        text_file.write(str(coded))

def loadFile(directEncoded,directCoded):
    with open(directEncoded, 'r') as myfile:
        encoded=myfile.read()
    with open(directCoded, 'r') as myfile:
        coded=myfile.read()
    coded = ast.literal_eval(coded)
    return encoded,coded


def saveImage(strName):
    cv2.imwrite(strName,img)

def validateEncode(drtEncoded):
    StatisticBit=[]
    N_FILES = 14
    for i in range(0, N_FILES+1):
        print('image ',i)
        encoded_file = strDirect+'/{}.txt'.format(i)
        code_list_file = strDirect+'/{}.pkl'.format(i)
        decoded_file = newFolder+'/{}.jpg'.format(i)
        
        with open(encoded_file, 'r') as myfile:
            encoded=myfile.read()
        StatisticBit.append((i,len(encoded)))
    return StatisticBit


def encode_file(Folder_encoding, real_Image, ratio_file=None):
    """Shannon-Fano encoding with text file.

    Parameters
    ----------
    in_file: Input file (.txt).
    out_file: Output file (.txt).
    code_list_file: File stores code_list (.pkl).
    ratio_file: Compression ratio file (.csv).
    """
    N_FILES = 15
    for i in range(0, N_FILES):
        #original_file = '../data/text/{}.txt'.format(str(i))
        #Folder_encoding='../bin/shannon-fano/encode/text/'
        #encoded_file = '../bin/shannon-fano/encode/text/{}.txt'.format(i)
        encoded_file = Folder_encoding+'/{}.txt'.format(i)
        #Folder_encoding = '../bin/Jpeg/encode/'
        code_list_file = Folder_encoding+'/{}.pkl'.format(i)
        #real_Image= '/home/shjfu/Downloads/compression-algorithms-develop/data/Image/'
        real_file = real_Image+'{}.jpg'.format(i)
        with open(encoded_file, 'r') as myfile:
            encoded=myfile.read()
        with open(code_list_file, 'r') as file_reader:
            coded = file_reader.read()
        coded = ast.literal_eval(coded)
        img = cv2.imread(real_file)
        size = img.shape[0]*img.shape[1]*24
        print(size)
        if ratio_file != None:
            ratio = size / len (encoded)
            with open(ratio_file, 'a') as file_writter:
                file_writter.write('{},{},{},{},{}\n'.format('{}.jpg'.format(i), size, len(encoded), entropy(img),ratio))
    return 0


def decode_file(in_file, out_file, code_list_file):
    """Shannon-Fano decoding with text file.

    Parameters
    ----------
    in_file: Input file (.txt).
    out_file: Output file (.txt).
    code_list_file: File stores code_list (.pkl).
    """
    with open(code_list_file, 'rb') as file_reader:
        code_list = pickle.load(file_reader)
    with open(in_file, 'r') as file_reader:
        encoded_doc = file_reader.read()
    decoded_doc = decode(encoded_doc, code_list)
    with open(out_file, 'w') as file_writter:
        file_writter.write(decoded_doc)
    return 0


def validate(file_1, file_2):
    """Compare two text files

    Returns
    -------
    Whether they are the same or not.
    """

    with open(file_1, 'r') as file_reader:
        doc_1 = file_reader.read()

    with open(file_2, 'r') as file_reader:
        doc_2 = file_reader.read()

    return doc_1 == doc_2

def run_on_data():
    N_FILES = 16
    for i in range(0, N_FILES):
        original_file = '../data/text/{}.txt'.format(str(i))
        encoded_file = '../bin/shannon-fano/encode/text/{}.txt'.format(i)
        code_list_file = '../bin/shannon-fano/encode/text/{}.pkl'.format(i)
        decoded_file = '../bin/shannon-fano/decode/text/{}.txt'.format(i)
        encode_file(original_file, encoded_file, code_list_file, ratio_file='../bin/shannon-fano/ratio.csv')
        decode_file(encoded_file, decoded_file, code_list_file)
        print( 'i = {}: {}'.format(i, validate(original_file, decoded_file)))

    
def Encode__fromDirect(drtImage):
    image = cv2.imread(drtImage)
    encoded, coded = Encoding(image)

    encodedFile = drtImage + ".encoded"
    codedFile = drtImage + ".coded.pkl"
    
    with open(encodedFile, 'w') as file_writter:
        file_writter.write(encoded)
    with open(codedFile, 'wb') as file_writter:
        pickle.dump(coded, file_writter)
    

def Decode_fromDrice(drtEncode,drtCode):
    with open(drtCode, 'rb') as file_reader:
        code_list = pickle.load(file_reader)
    with open(drtEncode, 'r') as file_reader:
        encoded_doc = file_reader.read()
    return Decoding(encoded_doc,code_list)


if __name__ == '__main__':
    currentPath = os.path.dirname(os.path.realpath(__file__)) + "/"

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--input', help='Description for foo argument', required=True)
    parser.add_argument('--operation', help='Description for bar argument', required=True)
    args = vars(parser.parse_args())

    pathInput = args['input']
    operation = args['operation']

    if operation == 'encode':
        Encode__fromDirect(pathInput)
        
    elif operation == 'decode':
        pklPath =  os.path.dirname(pathInput) + '/*.pkl'
        print pklPath
        code_list_file = glob.glob(pklPath)[0]
        Decode_fromDrice(pathInput, code_list_file)

    print "Done"
