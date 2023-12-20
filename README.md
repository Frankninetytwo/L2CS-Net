NOTE: The $ symbol means that the text that follows must be executed in terminal. All other instructions without a $ you need to do manually (e.g. downloading some stuff and putting it into some folder).

01. $ conda create -n L2CS-Net python=3.9
02. $ conda activate L2CS-Net
03. $ git clone https://github.com/Frankninetytwo/L2CS-Net.git
04. $ cd L2CS-Net
05. $ pip install git+https://github.com/edavalosanaya/L2CS-Net.git@main
06. Now we need to fix an error in an installed package. In order to do this we need to run one of my scripts first. Adjust the path in command below with a path to a video.<br>
$ python3 ExtractFeatures.py --video path/to/a/video/videoname.fileextention<br>
When executing this, it should tell you that 'date_modified' is not defined. In the error output it will also show the path of the package where the error comes from (the name of that file is utils.py). Edit this file (e.g. with nano: $ nano path/to/file/utils.py) as follows: delete the part " or date_modified()".

Now let's do the **feature extraction** (conda environment L2CS-Net still needs to be active!).<br>
Open ExtractFeaturesFromSITVideos.py from main folder (/L2CS-Net) and fill the empty list named "paths_of_SIT_videos". Then save the script and do:<br>
$ python3 ExtractFeaturesFromSITVideos.py<br>
It should generate .csv files in the L2CS-Net/Output folder.

Regarding the **output format** (.csv files):<br>
For the purpose of my Bachelor's Thesis I can't consider more than one gaze per frame as it is unclear which gaze belongs to the person of interest. For this reason the column "success" is only 1 if exactly one person is detected in the corresponding frame, otherwise it is 0.
