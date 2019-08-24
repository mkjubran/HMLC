# HMLC

# Learnable Coding

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
--mcu | maximum CU size [64]
--mpd | maximum partition depth [4]
--nf | number of frames to be encoded [900000000]
--fps | frames per second [30]
--path | path for results [../HMLC_Results]
--w | video width [640]
--h | video hight [480]
--rate | target bitrate [100k]
--cfg | HM configuration file [./encoder_lowdelay_P_main.cfg]

A successful run will produce the following:
