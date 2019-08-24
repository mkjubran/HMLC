#python ./Compare_Rate_PSNR_Frame.py --fn1=../HMSsync/HMSResu --fn2=../HMSsync/HMSRe

from __future__ import division
import numpy as np
import os, sys, subprocess, pdb
import argparse, re
import matplotlib.pyplot as plt
import datetime, math, time

###--------------------------------------------------------------
# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

# Optional argument
parser.add_argument('--f',nargs='?',default ='park_joy_640480.mp4', type=str, help='file name [mp4]')
parser.add_argument('--qp',nargs='?',default =30, type=int, help='qp value [30]')
parser.add_argument('--mcu',nargs='?',default =64, type=int, help='maximum CU size [64]')
parser.add_argument('--mpd',nargs='?',default =4, type=int, help='maximum partition depth [4]')
parser.add_argument('--nf',nargs='?',default =3000000, type=int, help='number of frames to be encoded [3000000]')
parser.add_argument('--fps',nargs='?',default =30, type=int, help='frames per second [30]')
parser.add_argument('--path',nargs='?',default ='../HMLC_Results/', type=str, help='path for results [../HMLC_Results]')
parser.add_argument('--w',nargs='?',default =640, type=int, help='width [640]')
parser.add_argument('--h',nargs='?',default =480, type=int, help='hight [480]')
parser.add_argument('--rate',nargs='?',default =10000, type=int, help='rate [10000]')
parser.add_argument('--cfg',nargs='?',default ='./encoder_lowdelay_P_main.cfg', type=str, help='configuration file [./encoder_lowdelay_P_main.cfg]')
args = parser.parse_args()

###--------------------------------------------------------------
def call(cmd):
    # proc = subprocess.Popen(["cat", "/etc/services"], stdout=subprocess.PIPE, shell=True)
    proc = subprocess.Popen(cmd, shell=True)
    #proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return (out, err)

###--------------------------------------------------------------
def call_bg(cmd):
    #proc = subprocess.Popen(cmd, shell=True)
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    return proc

###--------------------------------------------------------------
def export_frames(fn):
    osout = call('ffmpeg -r 1 -i {} -r 1 {}/POC/%d.jpg'.format(fn,video_path))
    return 

###--------------------------------------------------------------
def export_YUVframes(fn): ## not ready, kept in case needed inthe future
    osout = call('rm -rf {}'.format(video_path))
    osout = call('mkdir {}'.format(video_path))
    osout = call('mkdir {}/pngparallel'.format(video_path))
    fYUVCnt=1;
    FSize=(Width*Hight)+((Width/2)*(Hight/2))+((Width/2)*(Hight/2));

    fnYUV=(fn[0:(len(fn)-4)]+'.yuv')
    with open(fnYUV, "rb") as fYUVR:
       content = fYUVR.read(int(FSize))
       while content != '':
          with open('{}/pngparallel/{}.yuv'.format(path,fYUVCnt),"wb") as fW:
             fW.write(content)
          fW.close()
          fYUVCnt=fYUVCnt+1;
          content = fYUVR.read(int(FSize))
    fYUVR.close()
    return 

###--------------------------------------------------------------
if __name__ == '__main__':

 filename=args.f;
 qp=args.qp;
 mcu=args.mcu;
 mpd=args.mpd;
 nf=args.nf;
 fps=args.fps
 path=args.path;
 w=args.w;
 h=args.h;
 rate=args.rate;
 cfg=args.cfg;

 vid=filename.split('/')[-1]
 print(vid)
 video_path=path+vid[:-4]+'/'
 osout = call('rm -rf {}'.format(path))
 osout = call('mkdir {}'.format(path[:-1]))
 osout = call('mkdir {}'.format(video_path[:-1]))
 osout = call('rm -rf {}'.format(video_path+'/POC'))
 osout = call('mkdir {}'.format(video_path+'/POC'))
 osout = call('rm -rf {}'.format(video_path+'/HMLCPOC'))
 osout = call('mkdir {}'.format(video_path+'/HMLCPOC'))

 export_frames(filename);
 osout = call('ffmpeg -y -i {} -vcodec rawvideo -pix_fmt yuv420p {}'.format(filename,filename[:-3]+'yuv'))

 if (rate == 0 ):
   ratectl=0
 else:
   ratectl=1

 osout = call('rm -rf ../vid/HMEncodedVideo.bin')
 osout = call('rm -rf encoder.log')
 print(rate)
 osout = call('./HM/bin/TAppEncoderStatic -c {} --InputFile={} --SourceWidth={} --SourceHeight={} --SAO=1 --QP={} --FrameRate={} --FramesToBeEncoded={} --MaxCUSize={} --MaxPartitionDepth={} --QuadtreeTULog2MaxSize=4 --BitstreamFile={} --RateControl={} --TargetBitrate={}'.format(cfg,filename[:-3]+'yuv',w,h,qp,fps,nf,mcu,mpd,path+'/HMEncoded.bin',ratectl,rate))
 osout = call('mv HMLC_InfoPerFrame.txt {}'.format(video_path+'/HMLCPOC/HMLC_InfoPerFrame.txt'))
