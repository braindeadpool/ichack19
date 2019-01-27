from scipy.spatial import distance as dist
import numpy as np
import time
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


#eye is the json file of the detected image
def eye_aspect_ratio_left(eye):
    g=eye["Face"]["faces"][0]["eye-full-left"]["value1"]
    a=list(g["eyelids"][11].values())
    b=list(g["eyelids"][5].values())
    e=list(g["eyelids"][12].values())
    c=list(g["eyelids"][13].values())
    d=list(g["eyelids"][3].values())
    f=list(g["eyelids"][4].values())
    h1=list(g["eyelids"][8].values())
    h2=list(g["eyelids"][0].values())
    #vertical distance
    A=dist.euclidean(a, b)
    B=dist.euclidean(e, f)
    C=dist.euclidean(c, d)
    #horizontal distance
    D=dist.euclidean(h1,h2)
    
    ear = (A+B+C) / (3 * D)
    return ear

def eye_aspect_ratio_right(eye):
    g=eye["Face"]["faces"][0]["eye-full-right"]["value1"]
    a=list(g["eyelids"][11].values())
    b=list(g["eyelids"][5].values())
    e=list(g["eyelids"][12].values())
    c=list(g["eyelids"][13].values())
    d=list(g["eyelids"][3].values())
    f=list(g["eyelids"][4].values())
    h1=list(g["eyelids"][8].values())
    h2=list(g["eyelids"][0].values())
    #vertical distance
    A=dist.euclidean(a, b)
    B=dist.euclidean(e, f)
    C=dist.euclidean(c, d)
    #horizontal distance
    D=dist.euclidean(h1,h2)
    
    ear = (A+B+C) / (3 * D)
    return ear
    
def l_or_r(eye):
    gleft=eye["Face"]["faces"][0]["eye-full-left"]["value1"]
    gright=eye["Face"]["faces"][0]["eye-full-right"]["value1"]
    p2l=list(gleft["eyelids"][2].values())
    p2r=list(gright["eyelids"][2].values())
    p6l=list(gleft["eyelids"][6].values())
    p6r=list(gright["eyelids"][6].values())
    center_left=list(eye["Face"]["faces"][0]["eye-full-left"]["value1"]["pupil"]["center"].values())
    center_right=list(eye["Face"]["faces"][0]["eye-full-right"]["value1"]["pupil"]["center"].values())
    print(f"Center left = {center_left}")
    print(f"Center right = {center_right}")
    if center_left[0]>p2l[0] and center_right[0]>p2r[0]:
        logging.debug("You are seeing right")
        return ("right")
    elif center_left[0]<p6l[0] and center_right[0]<p6r[0]:
        logging.debug("You are seeing left")
        return ("left")
    
def message_decoder(message_array):
    if message_array==[1]:
        return "Yes"
    elif message_array==[1,1]:
        return "No"
    elif message_array==[1,1,1]:
        return "I'm Okay"
    elif message_array==[3,2,1]:
        return "Im not okay"
    elif message_array==[1,3]:
        return "call guardian"
    elif message_array==[1,2]:
        return "call doctor"


