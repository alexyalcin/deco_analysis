Decobubbles Screenshot Utility Documentation:

This is the documentation for how to use the first version of the Decobubbles screenshot utility (feel free to propose a better name).

The program runs in three parts, and as of now, each must be run manually. This will hopefully change in the near future.

Dependencies:
You will need to install Python 3 in addition to the following Python libraries, either via pip or another Python package manager. The versions I use are listed in parantheses. Other versions may or may not work, so I recommend using the ones I list, but feel free to try on whichever version you may already have installed.

I personally use anaconda environments, which allow for easier package version control. You can find the documentation here: [https://docs.conda.io/en/latest/]

Python (3.7.10)
opencv (4.5.2)
selenium (3.141.0)
numpy (1.20.3)

Everything else you need should be contained in the Github repository.

Step 1: Clone the Github repository
If you are not familiar with the console, the simplest way to do this is to navigate to the project URL at which is at [github.com/?], click the green box named code in the upper right corner, and click download zip. Then unzip the file at whichever location you would like to save it. Remember this path, as you will need it in the next steps.

Step 2: Enter your username/password. 
You must be an admin or have access to an admin account on decobubbles.com in order for this to work.

Find the ScreenshotApp folder in your file explorer (wherever you unzipped it), and first find the login_info.txt file. Replace the text that says “EMAIL” with your email and replace the text that says “PASSWORD” with your password. Make sure you don’t add/remove any lines, i.e., your email should be on line 1 and your password should be on line 2 with no extraneous spaces. 

*SECURITY NOTICE* Obviously storing your password in plaintext is not very secure, and a different method will be used in the final version of the app. However, as long as no one has access to your computer, and you don’t upload the file to Github (like I did), the app should work securely. In any case, especially if this is a password you use for other websites as well, I would strongly recommend deleting it from the file when not using the app. 

If you are getting stuck at the login page in the steps 4 and 5, double check to make sure you formatted the file correctly.

Step 3: Navigate to the directory in terminal
First, navigate in terminal/command prompt to the folder where the scripts are contained. If you are using anaconda, make sure to activate the correct environment. You can also use an IDE (I use Visual Studio Code) which can allow you to skip using command line, but command line requires the least software installation.

In my case (Ubuntu 18.04), this looks like:
>cd ~/Documents/Bubbles/ScreenshotApp
>source activate ssbubbles (only if using anaconda)

*Note* If you run all three scripts in succession from the same console window, you will only have to do the above once. However, if you use a new console window, you will have to change to the correct directory each time.

Step 4: Run get_completed_information.py
Simply type the following in your console window: 
>python get_completed_information.py

*Potential Issues*
-If you get an error along the lines of python is not a command, you likely did not install python globally. Search how to add python to PATH. 

-If you get stuck on the login page, see step 2.

Assuming everything works as intended, a chrome browser window should open up, log you in, then start clicking through the information for all completed videos. Wait until this is over. It should take less than a minute, so hold off on the coffee break till step 5. The browser window should close automatically once the program is finished running.

Step 5: Run take_screenshots.py
Now type in the same console window:
>python take_screenshots.py

The browser window should open up again, but this time it is going to take significantly longer, probably around two hours or longer depending on the number of completed videos. 

If the program crashes for any reason, look at your console for the last video number that was completed. Each time all screenshots for a video have been taken, the program will print “Completed: [num]” to the console. If you don’t want to sit through all the completed videos again, open the python script in your favorite text editor, and on line 16, change the value of video_complete_num to whatever video was last completed. By default, it should be 0. 

Again, when the program finishes, the browser window should close automatically. The text “All videos completed” should also print to the console. If this does not print, there was likely an error and you should run it from where it left off. 

Step 6: Run crop_images.py
Type in the same console window:
>python crop_images.py

This will also take some time, but likely less than an hour. No internet connection is required for this portion. If it fails to crop a screenshot automatically, then that screenshot will be displayed for a second. If this happens, please inform me of which one, and I will try to fix my algorithm at some point. For the time being, your best bet is to ignore that video, or go through cropping the 30+ screenshots for it manually. 

Results:
At the end, you should have two folders of screenshots: screenshots and sc_cropped. You will likely only need sc_cropped in the future. The folder hierarchy is organized by video_name>rater_name>ss<#>_cropped.png. 
The screenshot number is unique and assigned in order of processing, and information pertaining to that screenshot is stored in screenshot_data.json and can be accessed using functions in screenshot_utilities.py. This will require some basic coding knowledge.

