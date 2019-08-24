from __future__ import division
import numpy as np
import os, sys, subprocess, pdb
import argparse, re
import matplotlib.pyplot as plt
import datetime, math, time
import pickle
from array import *

###--------------------------------------------------------------
# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

# Optional argument
parser.add_argument('--f',nargs='?',default ='park_joy_640480.mp4', type=str, help='file name [mp4]')
parser.add_argument('--qp',nargs='?',default =30, type=int, help='qp value [30]')
parser.add_argument('--mcu',nargs='?',default =64, type=int, help='maximum CU size [64]')
parser.add_argument('--mpd',nargs='?',default =4, type=int, help='maximum partition depth [4]')
parser.add_argument('--nf',nargs='?',default =3000000, type=int, help='number of frames to be encoded [900000000]')
parser.add_argument('--fps',nargs='?',default =30, type=int, help='frames per second [30]')
parser.add_argument('--path',nargs='?',default ='../HMLC_Results/', type=str, help='path for results [../HMLC_Results]')
parser.add_argument('--w',nargs='?',default =640, type=int, help='width [640]')
parser.add_argument('--h',nargs='?',default =480, type=int, help='hight [480]')
parser.add_argument('--rate',nargs='?',default ='100k', type=str, help='rate [100k]')
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
def produce_training_data(finfo):
    with open(finfo) as fi:
       lines = fi.readlines()
    Bits=[]
    for cnt in range(len(lines)):
       line = re.sub(' +', ' ', lines[cnt]).split(' ')
       POC = line[1]
       Frame = str(int(line[1])+1) ## Frame=POC+1
       osout = call('cp -rf {} {}'.format(video_path+'/POC/'+Frame+'.jpg',video_path+'/HMLCPOC/P'+POC+'.jpg'))
       Bits.append(int(line[3]))
       L0 = re.sub(' +', ' ', lines[cnt]).split('L0')[1].split(' ')[1:-1]
       L1 = re.sub(' +', ' ', lines[cnt]).split('L1')[1].split(' ')[1:-1]
       if (L0 != []):
          for cnt2 in range(len(L0)):
             L0Frame= str(int(L0[cnt2])+1)
             L0POC=L0[cnt2]
             osout = call('cp -rf {} {}'.format(video_path+'/POC/'+L0Frame+'.jpg',video_path+'/HMLCPOC/P'+POC+'_L0_'+L0POC+'.jpg'))
       if (L1 != []):
          for cnt2 in range(len(L1)):
             L1Frame= str(int(L1[cnt2])+1)
             L1POC=L1[cnt2]
             osout = call('cp -rf {} {}'.format(video_path+'/POC/'+L1Frame+'.jpg',video_path+'/HMLCPOC/P'+POC+'_L1_'+L1POC+'.jpg'))

    fb = open(video_path+'/HMLCPOC/rate.bin','wb')
    pickle.dump(Bits,fb)
    fb.close()
#    print(Bits)
#    fb = open(video_path+'/HMLCPOC/rate.bin','rb')
#    Bitsnew=pickle.load(fb)
#    print(Bitsnew)
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

 if (rate[-1]=='m') or (rate[-1]=='M'):
   rate=int(rate[:-1])*1000000
 elif (rate[-1]=='k') or (rate[-1]=='K'):
   rate=int(rate[:-1])*1000
 else:
  rate=int(rate)
 #pdb.set_trace();

 vid=filename.split('/')[-1]
 video_path=path+vid[:-4]+'/'
 
 if (not os.path.isdir(path[:-1])):
    osout = call('mkdir {}'.format(path[:-1]))

 if (os.path.isdir(video_path[:-1])):
    osout = call('rm -rf {}'.format(video_path[:-1]))

 osout = call('mkdir {}'.format(video_path[:-1]))
 osout = call('rm -rf {}'.format(video_path+'/POC'))
 osout = call('mkdir {}'.format(video_path+'/POC'))
 osout = call('rm -rf {}'.format(video_path+'/HMLCPOC'))
 osout = call('mkdir {}'.format(video_path+'/HMLCPOC'))

 export_frames(filename);
 osout = call('ffmpeg -y -i {} -vcodec rawvideo -pix_fmt yuv420p {}'.format(filename,filename[:-3]+'yuv'))

 if ( rate == 0 ):
   ratectl=0
 else:
   ratectl=1

 if ( nf == 0 ):
   nf=900000000


 osout = call('rm -rf ../vid/HMEncodedVideo.bin')
 osout = call('rm -rf encoder.log')
 osout = call('./HM/bin/TAppEncoderStatic -c {} --InputFile={} --SourceWidth={} --SourceHeight={} --SAO=1 --QP={} --FrameRate={} --FramesToBeEncoded={} --MaxCUSize={} --MaxPartitionDepth={} --QuadtreeTULog2MaxSize=4 --BitstreamFile={} --RateControl={} --TargetBitrate={}'.format(cfg,filename[:-3]+'yuv',w,h,qp,fps,nf,mcu,mpd,path+'/HMEncoded.bin',ratectl,rate))
 osout = call('mv HMLC_InfoPerFrame.txt {}'.format(video_path+'/HMLCPOC/HMLC_InfoPerFrame.txt'))
 produce_training_data(video_path+'/HMLCPOC/HMLC_InfoPerFrame.txt')
