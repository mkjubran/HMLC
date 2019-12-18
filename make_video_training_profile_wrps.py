import os, sys, subprocess
import pdb
import re


gop_length = 4
nrps = 1
crf = 40
# Code for pre processing:
# ffmpeg -i sintel.mp4  -crf 16 -bf 0 sintel_2.mp4

def call(cmd):
   print(cmd)
   return subprocess.check_output(cmd, shell=True)


# Returns gop per P frame .. will probably not be used
def predictors_ip_gop(frame_type, gop_length):
   last_i_frame = 0
   frame_predictors = []
   for i in range(len(frame_type)):
      if frame_type[i] == 'I':
         frame_predictors.append([])
         last_i_frame = i

      if frame_type[i] == 'P':
         frame_predictors.append(range(last_i_frame, last_i_frame + gop_length))
       
   return frame_predictors

###--------------------------------------------------------------
#To extract the encoding data from coding log file ()
def produce_training_data(finfo):
    with open(finfo) as fi:
       lines = fi.readlines()
    for cnt in range(len(lines)):
       line = re.sub(' +', ' ', lines[cnt]).lstrip().split(' ')
       POC.append(line[0])
       POCtype.append(line[1])
       Frame.append(str(int(line[0])+1)) ## Frame=POC+1
       Bits.append(int(line[2])/8)
       L0 = re.sub(' +', ' ', lines[cnt]).split('L0')[1].split(' ')[1:-1]
       L1 = re.sub(' +', ' ', lines[cnt]).split('L1')[1].split(' ')[1:-1]

       L0 = list(set(L0));
       L1 = list(set(L1));

       #L0 = [ elem for elem in L0 if elem != '-1' ]
       #L1 = [ elem for elem in L1 if elem != '-1' ]
      
       L0 = [ str(int(elem)+1) for elem in L0 if elem != '-1' ]
       L1 = [ str(int(elem)+1) for elem in L1 if elem != '-1' ]

       while len(L0)<nrps:
         L0.append(L0[-1])

       while len(L1)<nrps:
         L1.append(L1[-1])

       L0_predictors.append(L0)
       L1_predictors.append(L1)
    return

input_dir = sys.argv[-1]

# Prepare output dir ..
cmd = 'rm -rf train_frames' ; output = call(cmd)
cmd = 'mkdir  train_frames' ; output = call(cmd)
for filename in os.listdir(input_dir):
    if filename.endswith(".mp4"): 

         # define global variable
         Bits=[]
         POC=[]
         POCtype=[]
         Frame=[]
         L0_predictors=[]
         L1_predictors=[]

         # Clean dir ..
         cmd = 'rm -rf tmp' ; output = call(cmd)
         cmd = 'mkdir  tmp' ; output = call(cmd)
         cmd = 'rm -rf tmp_e' ; output = call(cmd)
         cmd = 'mkdir  tmp_e' ; output = call(cmd)
         cmd = 'rm -f tmp_e.mp4' ; output = call(cmd)


         cmd = 'rm -rf x265LC_InfoPerFrame.txt'; output = call(cmd)
         # Make x and x_e; modify encoding as necessary ..  (e.g., adjust CRF/B-frames/etc)
         #cmd = 'ffmpeg -i {}/{} -crf 25 tmp_e.mp4'.format(input_dir, filename)
         cmd = '../../ffmpeg/ffmpeg -i {}/{} -c:v libx265 -x265-params "preset=superfast:crf={}:bframes=0:ref={}" tmp_e.mp4'.format(input_dir, filename,crf, nrps)
         output = call(cmd)

         cmd = 'ffmpeg -i {}/{}  tmp/%5d.png'.format(input_dir, filename)
         output = call(cmd)

         cmd = 'ffmpeg -i tmp_e.mp4 tmp_e/%5d.png'
         output = call(cmd)

         #cmd = 'ffprobe -show_entries frame=pkt_size,pict_type tmp_e.mp4'
         #output = call(cmd)

         # Parse necessary info ..
         #frame_string = [_.replace('[/FRAME]','') for _ in output.split(b'[FRAME]')]
         #frame_size = [int(_.split('\n')[1].split('=')[1]) for _ in frame_string[1:]]
         #frame_type = [_.split('\n')[2].split('=')[1] for _ in frame_string[1:]]
         #frame_predictors = predictors_ip_gop(frame_type,gop_length)
         # [_.split('\n')[2].split('=')[1] for _ in frame_strings[1:]]

         produce_training_data('x265LC_InfoPerFrame.txt')
         frame_size=Bits;
         frame_type=POCtype;
         frame_predictors=L0_predictors;

         #pdb.set_trace()

         # Output preprocessed model inputs
         print('Output for {}'.format(filename))
         # for i in range(len(frame_type)):
         frame_skip = 10
         for i in range(0, len(frame_type), frame_skip):
             if frame_type[i] != 'I':
                # Note: i+1 because ffmpeg frame indices START FROM 1
                fo = '{}_{}_{}.png'.format(format(frame_size[i], '05d'), format(int(Frame[i]),'05d'), filename[:-4])
                if ( nrps == 4):
                  #-- nrps=4
                  cmd = 'montage tmp/{}.png tmp_e/{}.png tmp_e/{}.png tmp_e/{}.png tmp_e/{}.png tmp_e/{}.png -tile 6x1 -font DejaVu-Sans -geometry +0+0 PNG24:train_frames/{}'.format(format(int(Frame[i]),'05d'), format(int(Frame[i]),'05d'), format(int(frame_predictors[i][0]),'05d'),format(int(frame_predictors[i][1]),'05d'),format(int(frame_predictors[i][2]),'05d'), format(int(frame_predictors[i][3]),'05d'),fo)
                elif ( nrps == 2 ):
                  #-- nrps=2
                  cmd = 'montage tmp/{}.png tmp_e/{}.png tmp_e/{}.png tmp_e/{}.png -tile 4x1 -font DejaVu-Sans -geometry +0+0 PNG24:train_frames/{}'.format(format(int(Frame[i]),'05d'), format(int(Frame[i]),'05d'), format(int(frame_predictors[i][0]),'05d'),format(int(frame_predictors[i][1]),'05d'),fo)
                elif ( nrps == 1 ):
                  #-- nrps=1
                  cmd = 'montage tmp/{}.png tmp_e/{}.png tmp_e/{}.png  -tile 3x1 -font DejaVu-Sans -geometry +0+0 PNG24:train_frames/{}'.format(format(int(Frame[i]),'05d'), format(int(Frame[i]),'05d'), format(int(frame_predictors[i][0]),'05d'),fo)
                else:
                  print('No montage command for nrps={}'.format(nrps))

                output = call(cmd)
    else:
        continue

