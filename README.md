TITLE: LANE DETECTION
Description:
What This Project Does
This project is a real-time lane detection system built in Python. It takes a dashcam road video, processes it frame by frame, draws green lines over the lane markings it finds on the road & warns you if the car looks like it's drifting out of its lane
I built this for two reasons. The first is personal. When I was younger I got hit by a car while crossing the road. That stayed with me .When I started learning Python I kept thinking about vehicle safety and eventually ended up looking into how modern cars actually detect lanes. I figured the best way to understand it was to kinda build it myself , but obviouldy i didnt know how to then
The second reason is that I want to work in engineering, specifically where software and physical systems meet. This project felt like a real step in that direction rather than just another coding exercise

How It Works
The project has 4 main functions in project.py plus a main function that runs everything.
load_video(file)
This takes a file path, opens the video using OpenCV and exits with an error message if the file doesn't exist or can't be opened. Same pattern I used throughout CS50P with sys.exit() in problem sets like Scourgify and CS50P P-Shirt
detect_lanes(frame)
This is the most involved function. It takes one frame from the video, basically just a single image, and runs it through a few steps
First it converts the frame to grayscale. Colour isn't actually useful for finding lane markings so dropping it makes things faster and simpler
Then it blurs the image slightly using a Gaussian blur. The reason for this is that tiny variations in pixel brightness can trick the edge detector into seeing edges that aren't really there. Blurring smooths that out
After that it runs Canny edge detection which looks for places in the image where brightness changes sharply. Lane markings are bright against a darker road so they show up clearly as edges.
Then a triangular mask gets applied to the frame. The sky and trees above the road aren't useful so the mask cuts all that out and only keeps the bottom portion where the lanes actually are
Finally it runs the Hough Line Transform on the masked edges. This algorithm takes all those edges and tries to find straight lines within them. The parameters I passed in control things like how long a line needs to be and how big a gap is allowed before it stops counting as one line. Any lines it finds get drawn on a copy of the original frame in green
The function returns both the annotated frame and the raw line data so calculate_drift can use it.
calculate_drift(lines, frame)
This figures out whether the car is drifting left or right. It splits the detected lines into left side and right side based on where they appear in the frame, averages the x positions of each group, finds the midpoint between those two averages as an estimated lane center, then compares that to the actual center of the frame. If the difference is more than 50 pixels in either direction it flags a drift warning
main()
main() handles the command line argument, calls load_video, then loops through every frame of the video running detect_lanes and calculate_drift on each one. It shows the result in a window and lets you quit by pressing Q

Design Choices
The fixed triangle works fine for straight road footage which is what I tested with.
I also considered averaging all the detected lines down into just 2 clean lines, 1o for each side, instead of drawing all of them raw. It would look neater but adds complexity and I wanted the code to stay readable. Something to improve in a future version maybe
The 50 pixel drift threshold came from trying different values until it felt right. Too small and it was triggering warnings on every slight curve. Too large and it wasn't catching actual drift

Files In This Project

project.py — the main program with all 4 functions
test_project.py — pytest tests for detect_lanes, calculate_drift and load_video
requirements.txt — the two pip libraries needed to run this project
README.md — this file


How To Run This Project
Instal the required libraries:
py -m pip install opencv-python numpy
Run the program with a video file:
py project.py road.mp4
Run the tests:
py -m pytest test_project.py

What I Learned
This course has helpmed me so drastically. I feel like I now have a little confidence when it comes to talking about coding. I alreadh had expereinec in web design when I was younger where I leanrt the basics of Java, CSS and HTMl...but Python is different because its kinda a different language, but one that I feel open more doors for me as an aspiring software engineer.
Before this I had no idea that a video is just a sequence of images or that an image is just a grid of numbers. Understanding that changed how I think about what computers actually process. It also made me appreciate how much is going on every second a modern car is on the road and that is honestly what made this project worth building.
