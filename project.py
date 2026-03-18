import cv2
import numpy as np
import sys
def main():
    #check if user gave a video file
    if len(sys.argv)<2:
        sys.exit("Usage: python project.py road.mp4")

    video_file = sys.argv[1]

    #try to load the video
    cap =load_video(video_file)

    #read & process each frame
    while True:
        ret,frame=cap.read()

        # if no more frames stop
        if not ret:
            break

        frame = cv2.resize(frame, (800, 450))

        lane_image, lines =detect_lanes(frame)

        drift=calculate_drift(lines, frame)

        if drift== "left":
            cv2.putText(lane_image, "WARNING: Drifting Left!", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0,255), 2)
        elif drift == "right":
            cv2.putText(lane_image, "WARNING: Drifting Right!",(50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)

        cv2.imshow("Lane Detection",lane_image) 
        cv2.waitKey(30)

        #stop
        if cv2.waitKey(1) & 0xFF== ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

def load_video(file):
    cap =cv2.VideoCapture(file)

    if not cap.isOpened():
        sys.exit(f"Could not open video file: {file}")
    return cap

def detect_lanes(frame):
    #draw
    lane_image=frame.copy()

    #edge
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred =cv2.GaussianBlur(gray,(5,5),0)
    edges=cv2.Canny(blurred, 50, 150)

    # u only look at the bottom half of the frame where d lanes r
    height =frame.shape[0]
    width =frame.shape[1]

    mask=np.zeros_like(edges)
    triangle = np.array([
    [(-50,height),(width+50, height),(width // 2, int(height * 0.6))]
], dtype=np.int32)
    cv2.fillPoly(mask, triangle, 255)

    masked_edges=cv2.bitwise_and(edges, mask)

    #find straight line
    lines = cv2.HoughLinesP(
    masked_edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=40,
    maxLineGap=150
)

    if lines is not None:
        for line in lines:
            x1, y1,x2,y2=line[0]
            cv2.line(lane_image, (x1,y1),(x2,y2), (0, 255,0),3)

    return lane_image,lines

def calculate_drift(lines,frame):
    if lines is None:
        return "none"

    width=frame.shape[1]
    center =width//2
    left_lines=[]
    right_lines =[]

    for line in lines:
        x1, y1,x2, y2=line[0]
        mid_x =(x1 + x2)// 2
        if mid_x<center:
            left_lines.append(mid_x)
        else:
            right_lines.append(mid_x)

    # find center 
    if left_lines and right_lines:
        left_avg =sum(left_lines)// len(left_lines)
        right_avg =sum(right_lines) //len(right_lines)
        lane_center =(left_avg + right_avg) //2

        offset=lane_center - center
        if offset<-50:
            return "left"
        elif offset>50:
            return "right"
    return "none"
if __name__ =="__main__":
    main()