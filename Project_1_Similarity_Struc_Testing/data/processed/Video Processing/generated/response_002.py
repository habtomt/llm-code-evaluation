import cv2
import numpy as np

cap =cv2 .VideoCapture ('input.mp4')

n_frames =int (cap .get (cv2 .CAP_PROP_FRAME_COUNT ))
width =int (cap .get (cv2 .CAP_PROP_FRAME_WIDTH ))
height =int (cap .get (cv2 .CAP_PROP_FRAME_HEIGHT ))
fps =cap .get (cv2 .CAP_PROP_FPS )

fourcc =cv2 .VideoWriter_fourcc (*'mp4v')
out =cv2 .VideoWriter ('output.mp4',fourcc ,fps ,(width ,height ))

_ ,prev =cap .read ()
prev_gray =cv2 .cvtColor (prev ,cv2 .COLOR_BGR2GRAY )

transforms =np .zeros ((n_frames -1 ,3 ),np .float32 )

for i in range (n_frames -1 ):
    try :

        prev_pts =cv2 .goodFeaturesToTrack (prev_gray ,
        maxCorners =200 ,
        qualityLevel =0.01 ,
        minDistance =30 ,
        blockSize =3 )

        success ,curr =cap .read ()
        if not success :
            break

        curr_gray =cv2 .cvtColor (curr ,cv2 .COLOR_BGR2GRAY )

        curr_pts ,status ,err =cv2 .calcOpticalFlowPyrLK (prev_gray ,curr_gray ,prev_pts ,None )

        assert prev_pts .shape ==curr_pts .shape

        idx =np .where (status ==1 )[0 ]
        prev_pts =prev_pts [idx ]
        curr_pts =curr_pts [idx ]

        m ,_ =cv2 .estimateAffine2D (prev_pts ,curr_pts )

        dx =m [0 ,2 ]
        dy =m [1 ,2 ]

        da =np .arctan2 (m [1 ,0 ],m [0 ,0 ])

        transforms [i ]=[dx ,dy ,da ]

        prev_gray =curr_gray

    except Exception as e :
        print (f"Error occurred: {e}")
        cap .release ()
        out .release ()
        cv2 .destroyAllWindows ()
        break

trajectory =np .cumsum (transforms ,axis =0 )

smoothed_trajectory =np .copy (trajectory )

SMOOTHING_RADIUS =30
for i in range (3 ):
    smoothed_trajectory [:,i ]=np .convolve (trajectory [:,i ],np .ones ((SMOOTHING_RADIUS ,))/SMOOTHING_RADIUS ,mode ='same')

difference =smoothed_trajectory -trajectory

transforms_smooth =transforms +difference

cap .set (cv2 .CAP_PROP_POS_FRAMES ,0 )

for i in range (n_frames -1 ):
    try :

        success ,frame =cap .read ()
        if not success :
            break

        dx =transforms_smooth [i ,0 ]
        dy =transforms_smooth [i ,1 ]
        da =transforms_smooth [i ,2 ]

        m =np .zeros ((2 ,3 ),np .float32 )
        m [0 ,0 ]=np .cos (da )
        m [0 ,1 ]=-np .sin (da )
        m [1 ,0 ]=np .sin (da )
        m [1 ,1 ]=np .cos (da )
        m [0 ,2 ]=dx
        m [1 ,2 ]=dy

        frame_stabilized =cv2 .warpAffine (frame ,m ,(width ,height ))

        frame_stabilized =cv2 .copyMakeBorder (frame_stabilized ,10 ,10 ,10 ,10 ,cv2 .BORDER_REPLICATE )

        frame_out =cv2 .hconcat ([frame ,frame_stabilized ])

        if frame_out .shape [1 ]>1920 :
            frame_out =cv2 .resize (frame_out ,(1920 ,int (frame_out .shape [0 ]*1920 /frame_out .shape [1 ])))

        out .write (frame_out )

    except Exception as e :
        print (f"Error occurred: {e}")
        cap .release ()
        out .release ()
        cv2 .destroyAllWindows ()
        break

cap .release ()
out .release ()

cv2 .destroyAllWindows ()