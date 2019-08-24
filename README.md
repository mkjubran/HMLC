# HMLC

# Sequence-Level Reference Frames In Video Coding

## Introduction

This repository contains our public tools for .... 

## Prerequisites

In order to compile and run the tools provided in this repository you will need:
1. Python 2.7 
2. ffmpeg (version 2.8.15 or higher)

## Rate and reference framesSequence-Level Reference Frames
To produce a binary file of rates per frame and a folder containing the encoded pictures and all candidate predictors run

```
python Produce_HM_InfoPerFrame.py --f=../vid/park_joy_640480.mp4
```

Option | Description [default]
---|---
--f | input file name 
--qp | quantization parameter [30]
--fps | frame per second [30]
--mcu
--gp | minimum distance (number of frames) between two stitching frames
--wd | weight of dissimilarity score
--wpp | weight of popularity score
--maxf | number of original video frames to be considered for stitching frames [maxf=0; consider all of frames in the input video]
--maxn | number of stitch frames [maxn=0; number of stitch frames equals the number of scene cuts]
--suffix | text to be appended to the output file name

--f',nargs='?',default ='park_joy_640480.mp4', type=str, help='file name [mp4]')
parser.add_argument('--qp',nargs='?',default =30, type=int, help='qp value [30]')
parser.add_argument('--mcu',nargs='?',default =64, type=int, help='maximum CU size [64]')
parser.add_argument('--mpd',nargs='?',default =4, type=int, help='maximum partition depth [4]')
parser.add_argument('--nf',nargs='?',default =3000000, type=int, help='number of frames to be encoded [900000000]')
parser.add_argument('--fps',nargs='?',default =30, type=int, help='frames per second [30]')
parser.add_argument('--path',nargs='?',default ='../HMLC_Results/', type=str, help='path for results [../HMLC_Results]')
parser.add_argument('--w',nargs='?',default =640, type=int, help='width [640]')
parser.add_argument('--h',nargs='?',default =480, type=int, help='hight [480]')
parser.add_argument('--rate',nargs='?',default =10000, type=str, help='rate [100k]')
parser.add_argument('--cfg',nargs='?',default ='./encoder_lowdelay_P_main.cfg', type=str, help='configuration file [./encoder_lowdelay_P_main.cfg]')

A successful run will produce an OrderedFrames.txt file which includes a list of stitch frames ordered based on popularity and dissimilarity scores.
