# L2CS-Net
NOTE: The $ symbol means that the text that follows must be executed in terminal. All other instructions without a $ you need to do manually (e.g. downloading some stuff and putting it into some folder).

01. $ conda create -n L2CS-Net python=3.9
02. $ conda activate L2CS-Net
03. $ git clone https://github.com/Frankninetytwo/L2CS-Net.git
04. $ cd L2CS-Net
05. $ pip install git+https://github.com/edavalosanaya/L2CS-Net.git@main
06. Now we need to fix an error in an installed package. In order to do this we need to run one of my scripts first. Adjust the path in command below with a path to a video.
$ python3 ExtractFeatures.py --video path/to/a/video/videoname.fileextention
When executing this, it should tell you that 'date_modified' is not defined. In the error output it will also show the path of the package where the error comes from (the name of that file is utils.py). Edit this file (e.g. with nano: $ nano path/to/file/utils.py) as follows: delete the part " or date_modified()".

Now let's start with the feature extraction (conda environment L2CS-Net still needs to be active!).
1. In the command below adjust the path to where you have all SIT videos (ONLY videos must be in that folder):<br>
$ python3 ExtractFeaturesFromMultipleVideos.py --videos /path/to/folder/that/contains/all/SIT_videos
It should generate .csv files in the L2CS-Net/Output folder. While it runs it will first tell you which video is currently analyzed and then how many frames of that video were already processed.
If you want that my script generates videos that show the estimated gaze with an arrow, then you need to add -v to the parameters:<br>
$ python3 ExtractFeaturesFromMultipleVideos.py --videos /path/to/folder/that/contains/all/SIT_videos -v
