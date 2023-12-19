# This file is based on https://github.com/Ahmednull/L2CS-Net/blob/main/demo.py

# Notes:
# - file needs to be run with python3 (python3 ExtractFeatures.py args), otherwise torch is not available


import argparse
import pathlib
import cv2
import torch

from l2cs import select_device, Pipeline, render
import math

def parse_args():

    parser = argparse.ArgumentParser(description='Gaze estimation using model pretrained on Gaze360 dataset.')
    
    parser.add_argument(
        '--video',
        dest='video_path',
        help='path of the video to proccess',  
        type=str
        )
    
    parser.add_argument(
        '-v',
        help='visualize output (creates a new video with estimated gaze)',
        action='store_true'
        )
    
    return parser.parse_args()


# File will be written to
# CWD/Output/filename_of_video_without_file_extension.csv
# where filename_of_video_without_file_extension is a parameter of this function.
def write_estimated_gaze_to_file(filename_of_video_without_file_extension, timestamp_by_frame, pitch_by_frame, yaw_by_frame):

    output_path = str(pathlib.Path.cwd()) + '/Output/' + filename_of_video_without_file_extension + '.csv'
    
    with open(output_path, 'w') as f:
        
        f.write('frame,timestamp in s,success,yaw in radians,pitch in radians\n')

        for i in range(0, len(pitch_by_frame)):
            f.write('{},{},{},{},{}\n'.format(
                i+1,
                str(round(timestamp_by_frame[i], 3)), # +/- 0.001 radians (less 0.1 degrees) can be rounded off (easier to compare output file to output from OpenFace)
                0 if math.isnan(yaw_by_frame[i]) else 1,
                str(round(yaw_by_frame[i], 3)),
                str(round(pitch_by_frame[i], 3)))
                )


if __name__ == '__main__':
    
    args = parse_args()

    if not args.video_path:
        print('argument --video required')
        exit()

    gaze_pipeline = Pipeline(
        weights= str(pathlib.Path.cwd()) + '/models/Gaze360/L2CSNet_gaze360.pkl', # if you change to weights from MPIIGaze their code crashes
        arch='ResNet50', # specifying different network architecture (e.g. 'ResNet18') makes their code crash as well
        device = select_device('cuda:0', batch_size=1) # when I put anything else than 'cpu' it still works, seemingly without any differences
    )
    

    video_capture = cv2.VideoCapture(args.video_path)

    # Check if the file opened correctly
    if not video_capture.isOpened():
        raise IOError('Failed to open video file \"' + args.video_path + '\"')
    

    # timestamp of frame in the video
    timestamp_by_frame = []
    # vertical gaze angles
    pitch_by_frame = []
    # horizontal gaze angles
    yaw_by_frame = []

    video_writer = None

    # read first frame here already as its shape is needed to initialize VideoWriter
    success, frame = video_capture.read()

    if args.v:
        video_writer = cv2.VideoWriter(
            str(pathlib.Path.cwd()) + '/Output/' + pathlib.Path(args.video_path).stem + '.avi',
            cv2.VideoWriter_fourcc(*'XVID'),
            video_capture.get(cv2.CAP_PROP_FPS), # use same frame rate as source video
            (frame.shape[1], frame.shape[0])
            )

    with torch.no_grad():

        current_frame = 1

        while True:

            if not success:
                # no further frames available
                break

            print('processing frame {} of approx. {}'.format(current_frame, int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))))

            # estimate gaze
            results = gaze_pipeline.step(frame)

            # cv2.CAP_PROP_POS_MSEC is sometimes very far off! For the final frame of an approx. 29.000 ms long video (.webm) it
            # returned me a timestamp of almost 35.000 ms!
            #timestamp_by_frame.append(video_capture.get(cv2.CAP_PROP_POS_MSEC))
            # ... So instead I'm going to estimate the timestamp like OpenFace does it
            # (see /OpenFace/lib/local/Utilities/src/SequenceCapture.cpp, line 457)
            current_timestamp = round((current_frame-1) * (1.0 / video_capture.get(cv2.CAP_PROP_FPS)), 3)
            timestamp_by_frame.append(current_timestamp)
            


            if len(results.yaw) > 1:
                # If there is more than one person in the frame I don't know whose gaze to use
                pitch_by_frame.append(math.nan)
                yaw_by_frame.append(math.nan)
            else:
                # 1. Insert current yaw into pitch list and vice versa, because L2CS-Net for some reason
                # confuses the two.
                # 2. Adjust to output format of OpenFace by negating pitch and yaw.
                pitch_by_frame.append(-results.yaw[0])
                yaw_by_frame.append(-results.pitch[0])


            if args.v:
                # visualize output
                frame = render(frame, results)
                video_writer.write(frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            current_frame += 1
            success, frame = video_capture.read()

    write_estimated_gaze_to_file(pathlib.Path(args.video_path).stem, timestamp_by_frame, pitch_by_frame, yaw_by_frame)
    
    video_capture.release()

    if args.v:
        video_writer.release()    
    
    cv2.destroyAllWindows()