import numpy as np
import cv2
import pandas as pd

PADDING_THRESH = 5

def get_dice_sub_img(full_img):
    # inversed var x -> y
    x = full_img.shape[0]
    y = full_img.shape[1]

    sub_dice_img = full_img[int(y / 3) + 10 : int(y / 3) + 80,
                            int(x * 4 / 5) + 20 :int( x * 4 / 5) + 150]

    # was int(x * 4 / 5) + 30 :int( x * 4 / 5) + 135
    # sauf 6 6 - 1 -1
    # int(x * 4 / 5) + 20 :int( x * 4 / 5) + 145

    return sub_dice_img

def get_circles_positions_and_color(img_path):
    img = cv2.imread(img_path, 1)          # queryImage
    # print(img.shape)
    # print("--------------")

    # hardecoded size of example
    scale_largeur = img.shape[0] / 1145
    scale_hauteur = img.shape[1] / 892

    scale = scale_largeur + scale_hauteur/2

    img = cv2.resize(img, dsize=(int(img.shape[1]/scale), int(img.shape[0]/scale)), interpolation=cv2.INTER_CUBIC)
    # Convert to grayscale.

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # _, gray_th = cv2.threshold(gray_blurred, 127, 255, cv2.THRESH_BINARY)

    # gray_th =  cv2.cvtColor(gray_th, cv2.COLOR_GRAY2RGB)

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                   param2 = 30, minRadius = 15, maxRadius = 40)
    a_list = []
    b_list = []
    r_list = []
    # Draw circles that are detected.
    img_debug = gray_blurred.copy()
    if detected_circles is not None:

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            a_list.append(a)
            b_list.append(b)

            r_list.append(r)
            # Draw the circumference of the circle.

            cv2.circle(img_debug, (a, b), r, (255, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img_debug, (a, b), 1, (0, 0, 255), 3)

        # cv2.imshow("debug", img_debug)
        # cv2.imsave(img_debug, "debug.png")

    df =  non_max_supression(img, a_list, b_list, r_list)

    # if(len(df['center']) == 30): # ok good
    #     print("perfect match number of pieces")
    # elif(len(df['center']) >= 30):
    #     print("too much need more agressive suppression")
    # else:
    #     print("too less need less agressive suppression")

    sub_dice_img = get_dice_sub_img(img)

    return df, img, scale, sub_dice_img, img_debug


def get_circle_color(img):
    black = (42,42,42)
    white = (240,210,140)
    dist_black = 0
    dist_white = 0
    # print(img[0, 0])
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            clr = img[i, j]
            # print(clr)
            dist_black += abs(clr[0] - black[0]) + abs(clr[1] - black[1]) + abs(clr[2] - black[2])
            dist_white += abs(clr[0] - white[0]) + abs(clr[1] - white[1]) + abs(clr[2] - white[2])
            # print("color = []".format(clr))

    # print("dist_black " +str(dist_black))
    # print("dist_white "+str(dist_white))

    return ("white", "black")[dist_black < dist_white]


def non_max_supression(img, a_list, b_list, r_list):
    """
    Remove circle base on knowledge

    Parameters
    ----------
    img : TYPE
        DESCRIPTION.
    a_list : TYPE
        DESCRIPTION.
    b_list : TYPE
        DESCRIPTION.
    r_list : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """

    i = 0

    center_list = []
    height_list = []
    colors_list = []

    for r in r_list:
        a = a_list[i]
        b = b_list[i]
        r = r_list[i]

         # check if center is out of the board
        if(a < 55 or a > 746):
            # print("a to small or too big a :{} b:{}".format(a, b))
            pass
         # check if radius is not too small
        elif(r > np.mean(r_list) * 0.8):
            # print("debug a :{} b:{}".format(a, b))
            # print(r)
            # cv2.circle(img, (a, b), r, (0, 255, 0), 2)
            # y

            # height_list.append(("top", "bot")[b < 224])
            height_list.append(b)
            # x
            center_list.append(a)
            # Draw a small circle (of radius 1) to show the center.
            left = a - r + PADDING_THRESH
            right = a + r - PADDING_THRESH

            top = b - r + PADDING_THRESH
            bot = b + r - PADDING_THRESH
            cropped_piece = img[top:bot, left:right, :]
            # cv2.imshow("cropped_piece", cropped_piece)
            # cv2.waitKey(0)
            colors_list.append(get_circle_color(cropped_piece))
            # print(cir)
            # cv2.imshow("Detected Circle", cropped_piece)
            # cv2.waitKey(0)
        i += 1
    # cv2.imshow("Detected Circle", img)
    # cv2.waitKey(0)
    verticalite = []
    for i in range(len((height_list))):
        if(height_list[i] > 310):   # en bas green
            if(colors_list[i]== "white"):
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            verticalite.append("bot")
        else:                       # haut blue
            if(colors_list[i]== "white"):
                color = (0, 127, 0)
            else:
                color = (127, 0, 0)
            verticalite.append("top")
        cv2.circle(img, (center_list[i], height_list[i]), 2, color, 2)
    # cv2.imshow("Detected Circle", img)
    # cv2.waitKey(0)
    dict_df = {'center': center_list, 'height': height_list,'verticality': verticalite,'color': colors_list}
    df = pd.DataFrame(data=dict_df)
    return df
