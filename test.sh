#!/usr/bin/env bash
python find_image.py 10049.jpeg ColorRGBCov > 10049_ColorRGBCov.txt
python find_image.py 1975.jpeg TextureLumGabor > 1975_TextureLumGabor.txt
python find_image.py findimage 2136.jpeg ColorHist64 > 2136_ColorHist64.txt
python find_image.py max 1 11643.jpeg min 2 TextureLumGabor ColorHist256 > max_1_11643_min_2_TextureLumGabor_ColorHist256.txt
python find_image.py ave 2 3161.jpeg 2677.jpeg max 1 ColorHCLCov > ave_2_3161_2677_max_1_ColorHCLCov.txt
python find_image.py max 2 3163.jpeg 3754.jpeg ave 3 ColorRGBCov ColorHist64 TextureLumGabor > find_image.py_max_2_3163_3754_ave_3_ColorRGBCov_ColorHist64_TextureLumGabor.txt
