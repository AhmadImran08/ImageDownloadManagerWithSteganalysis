#!/usr/bin/env python3 

import os
import sys
import glob
import json
import time
import scipy
import numpy
import pandas
import pickle
import shutil
import random
import tempfile
import subprocess
import imageio

#from scipy import misc

from library import attacks, utils

def main():

    attacks_doc="\n" \
    "  Statistical attacks:\n" \
    "  - rs:            RS attack.\n" \

    if False: pass

    # -- ATTACKS --

    # {{{ rs
    elif sys.argv[1]=="rs":

        if len(sys.argv)!=3:
            print(sys.argv[0], "spa <image>\n")
            sys.exit(0)

        if not utils.is_valid_image(sys.argv[2]):
            print("Please, provide a valid image")
            sys.exit(0)

        threshold=0.05


        I = imageio.imread(sys.argv[2])
        if len(I.shape)==2:
            bitrate=attacks.rs(sys.argv[2], None)
            if bitrate<threshold:
                print("No hidden data found")
            else:
                print("Hidden data found", bitrate)
        else:
            bitrate_R=attacks.rs(sys.argv[2], 0)
            bitrate_G=attacks.rs(sys.argv[2], 1)
            bitrate_B=attacks.rs(sys.argv[2], 2)

            if bitrate_R<threshold and bitrate_G<threshold and bitrate_B<threshold:
                print("No hidden data found")
                sys.exit(0)

            if bitrate_R>=threshold:
                print("Hidden data found in channel R", bitrate_R)
            if bitrate_G>=threshold:
                print("Hidden data found in channel G", bitrate_G)
            if bitrate_B>=threshold:
                print("Hidden data found in channel B", bitrate_B)
            sys.exit(0)
    # }}}
    else:
        print("Wrong command!")


if __name__ == "__main__":
    main()





