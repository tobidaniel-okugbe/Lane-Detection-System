import numpy as np
import pytest
from project import detect_lanes, calculate_drift, load_video
def test_detect_lanes():
    fake_frame =np.zeros((480, 640, 3),dtype=np.uint8)

    #left white line
    import cv2
    cv2.line(fake_frame,(100, 480),(200,240),(255, 255, 255),3)
    result_frame, lines=detect_lanes(fake_frame)
    assert result_frame.shape==fake_frame.shape

def test_calculate_drift():
    # create a fake frame
    fake_frame=np.zeros((480, 640, 3), dtype=np.uint8)

    #if no lines drift should be 0
    result=calculate_drift(None,fake_frame)
    assert result=="none"

    #create fake lines that are all on the left
    fake_lines_left=np.array([[[50,400,100, 200]]])
    result = calculate_drift(fake_lines_left,fake_frame)
    assert result =="none"

    #create fake lines on both sides
    fake_lines_both= np.array([
        [[50,400, 150,200]],
        [[500, 400,580,200]]
    ])
    result=calculate_drift(fake_lines_both,fake_frame)
    assert result in ["none","left","right"]

def test_load_video():
    with pytest.raises(SystemExit):
        load_video("this_file_does_not_exist.mp4")