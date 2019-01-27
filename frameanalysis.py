from scipy.spatial import distance as dist
import numpy as np
import time


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
    if center_left[0]>p2l[0] and center_right[0]>p2r[0]:
        print("You are seeing right")
        return ("right")
    elif center_left[0]<p6l[0] and center_right[0]<p6r[0]:
        print("You are seeing left")
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

 
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMESshort = 3
#EYE_AR_CONSEC_FRAMESlong=10
confirm=30

# initialize the frame counters and the total number of blinks,left and right 
COUNTERblink = 0
COUNTERleft=0
COUNTERright=0
TOTALblink = 0
TOTALleft=0
TOTALright=0
#totallong=0
word=[]


*****************************************************************************************   
#NOW ENTER THE CODE TO RUN ON THE DRISHTI HERE> AT THE END SHOULD GIVE A JSON FILE 
#return response 
#where response is the JSON file
*****************************************************************************************

# coordinates to compute the eye aspect ratio for both eyes
leftEAR = eye_aspect_ratio_left(response)
rightEAR = eye_aspect_ratio_right(response)

# average the eye aspect ratio together for both eyes
ear = (leftEAR + rightEAR) / 2.0


# check to see if the eye aspect ratio is below the blink
# threshold, and if so, increment the blink frame counter
if ear < EYE_AR_THRESH:
	COUNTERblink += 1

	# check to see if the gaze is left
	# , and if so, increment the left frame counter
elif l_or_r(response)=="left":
	COUNTERleft+=1

        # check to see if the gaze is right
		# , and if so, increment the right frame counter
elif l_or_r(response)=="right":
	COUNTERright+=1
        

# otherwise, the eye aspect ratio is not below the blink
# threshold
else:
	# if the eyes were closed for a sufficient number of
	# then increment the total number of blinks
	if COUNTERblink >= EYE_AR_CONSEC_FRAMESshort:
		TOTALblink += 1
		word.append(1)
    elif COUNTERleft >= EYE_AR_CONSEC_FRAMESshort:
        TOTALleft += 1
        word.append(3)
    elif COUNTERright >= EYE_AR_CONSEC_FRAMESshort:
        TOTALright += 1
        word.append(2)
# 		elif COUNTER>=EYE_AR_CONSEC_FRAMESlong and COUNTER<confirm:
# 			totallong+=1
# 			word.append(0)

#If the User closes eyes for more that "confirm" no of frames then it means that he/she wants to send the message. 
	elif COUNTERblink>=confirm:
		print("message encoded")
            #we pass the encoded info into the message_decoder
        return message_decoder(word)
            #reset the word array as we are sending only one command at a time
		word=[]
            
            

		# reset the eye frame counter
    COUNTERblink = 0
    COUNTERleft=0
    COUNTERright=0


