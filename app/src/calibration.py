import cv2
BIAS_BOT_RIGHT = 0

def match_keypoint(template, img, debug):
    w, h = template.shape[::-1]
    img2 = img.copy()
    img = img2.copy()
    method = eval('cv2.TM_CCOEFF')

    # Apply template Matching
    res = cv2.matchTemplate(img, template,method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # cv2.rectangle(img, top_left, bottom_right, 255, 2)
    # cv2.imshow(debug, img)
    # cv2.waitKey(0)

    return top_left, bottom_right


# img = cv2.imread('../data/test/full_screen.png', 0)

def getGameBB(img):
    kps = []
    
    # kaze_match(img, template)

    img_full = img.copy()
    # print("img_full {}".format(img_full.shape))

    # create a mask to remove button on the middle which is annoying for template matching
    cv2.rectangle(img_full,
                  (0,0),
                  (img_full.shape[1], int(2* img_full.shape[0]/3)),
                  (0,255,0),
                  -1)

    cv2.rectangle(img_full,
                  (0,0),
                  (int(img_full.shape[1]/2), img_full.shape[0]),
                  (0,255,255),
                  -1)

    cv2.imwrite("calibration_mask.png", img_full)
    #cv2.imshow("test", img_full)
    #cv2.waitKey(0)

    left_side = img[0:int(img.shape[0]/4), 0:int(img.shape[1]/4)]

    template_gauche = cv2.imread('../data/test/menu_small.png', 0)
    kps.append(match_keypoint(template_gauche, left_side, "top_left"))

    template_droite = cv2.imread('../data/test/bas_droite.png', 0)
    kps.append(match_keypoint(template_droite, img_full, "bot_right"))

    # print(kps)

    top_left_pix = (0, kps[0][0][1])
    bot_right_pix = (kps[1][1][0] + BIAS_BOT_RIGHT, kps[1][1][1])

    print("top_left_pix list : ")
    print(top_left_pix)

    return top_left_pix, bot_right_pix

def calibration(full_screen_path):
    # haut_gauche = (int(arg[2]), int(arg[1]))
    # bas_droite = (int(arg[3]), int(arg[4]))
    print("calibration_full_screen at "+full_screen_path)
    img = cv2.imread(full_screen_path, 0)
    top_left_pix, bot_right_pix = getGameBB(img)
    print("calibration done, top_left_pix : {}".format(top_left_pix))
    print("calibration done, bot_right_pix : {}".format(bot_right_pix))
    return top_left_pix, bot_right_pix

# print(top_left_pix)

# print(bot_right_pix)