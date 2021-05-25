from back_gammon_structure import BackGamonfrom gui_structure import BackGamonIMGfrom process_img import get_circles_positions_and_color# from calibration import calibration# import timefrom BGBlitzClient import BgBlitzClientimport numpy as npimport cv2from mss import mssimport osimport matplotlib.pyplot as pltbase_path = "../data/games/"def take_screen(sct, bounding_box, game_save_path):    # print("save screen at : "+ game_save_path)    # bounding_box = {'top': 100, 'left': 0, 'width': 400, 'height': 300}    sct_img = sct.grab(bounding_box)    open_cv_screen = np.array(sct_img)    cv2.imwrite(game_save_path, open_cv_screen)if __name__ == "__main__":    sct = mss()    arr = os.listdir(base_path)    game_id = len(arr)    if(".DS_Store" in arr):        game_id -= 1    game_save_path = base_path + str(game_id)    os.mkdir(game_save_path)    print("game save path " + game_save_path)    bounding_box_all = {'top': 0, 'left': 0, 'width': 1600, 'height': 1000}    all_screen_img_path = game_save_path+"/all_screen.png"    take_screen(sct, bounding_box_all, all_screen_img_path)    # hardcode calibration uncomment this to use template matching    # -> error can be thrown for spectator matches, the template image is matched to mid image    # haut_gauche, bas_droite = calibration(all_screen_img_path)    # print("calibration haut_gauche at {}".format(haut_gauche))    # print("calibration bas_droite at  {}".format(bas_droite))    # hardcode haut gauche for chrome    haut_gauche = (0, 270)    bas_droite = (2175, 1975)    width = (bas_droite[0] - haut_gauche[0]) / 2    height = (bas_droite[1] - haut_gauche[1]) / 2    top = int(haut_gauche[1]/2)    left = int(haut_gauche[0]/2)    bounding_box = {'top': top , 'left': left, 'width': width , 'height': height}    print(bounding_box)    # time.sleep(4)    bg = BackGamon('blanc')    # debug_img = cv2.imread(game_save_path + "/game_screen.png")    bg_img = BackGamonIMG(game_save_path)    # bg_img.debug_by_img()    bg_client = BgBlitzClient()    list_probas = [0.5]    fig, ax = plt.subplots()    plt.ion()    plt.ylim(0, 1)    # line1, = ax.plot(list_probas, 'r-')    plt.show()    plt.title("Probabilite de victoire")    while(1):        img_path = game_save_path + "/game_screen.png"        take_screen(sct, bounding_box, img_path)        df_cicles, resized_img, scale, sub_dice_img, img_debug = get_circles_positions_and_color(img_path)        # print("------------ scale factor -----------------")        # print(scale)        # print(resized_img.shape)        # print("------------ scale factor -----------------")        cv2.imwrite("debug.png", img_debug)        # cv2.imwrite("debug-dice.png", sub_dice_img)        bg_img.set_bar_position(resized_img.shape[1], resized_img.shape[0])        bg_img.set_debug_img(resized_img)        debug_dice_img1, debug_dice_img2 = bg_img.setDiceTuple(sub_dice_img)        # cv2.imwrite("debug-dice-left.png", debug_dice_img1)        # cv2.imwrite("debug-dice-right.png", debug_dice_img2)        dice_tuple = bg_img.getDiceTuple()        for pion_id in range(len(df_cicles)):            df_line = df_cicles.iloc[pion_id]            fleche_id = bg_img.getFlechePlusPres(df_line['center'], df_line['verticality'], df_line['height'])            # print("fleche_id")            # print(fleche_id)            if(fleche_id is None):                continue            if(fleche_id == -1):                bg.add_bar(df_line['color'])            else:                bg.add_fleche_by_id(fleche_id, df_line['color'])        # bg.debugPlateau()        bg_img.debug_by_img()        bg.set_dice(dice_tuple)        bg_img.rest_debug_grid()        if(dice_tuple[0] is not None or dice_tuple[1] is not None):            # custom AI            # layout = bg.getLayout()            # getAIPredFromLayout(layout)            # print("layout")            # print(layout)            print("pip_count white: {}".format(bg.getPipCount("white")))            print("pip_count black: {}".format(bg.getPipCount("black")))            layout, bar, out = bg.getLayoutBgBlitz()            print("layout BgBlitz : {}".format(layout))            prob = bg_client.getPrediction(layout, bar, out, dice_tuple)            # print(prob)            if(prob):                list_probas.append(float(prob))                print(list_probas)                # line1.set_data(prob, len(list_probas))                ax.plot(list_probas)                plt.draw()                plt.pause(0.001)                fig.savefig("Win_proba.png")            bg.reset_board()            val = input("continue ?")            if(val != "n"):                continue            else:                break        else:            print("no dice detected continuing to analyse")# img_path = "../data/test/beginning.png"# df_cicles = get_circles_positions_and_color(img_path)# bg = BackGamon('blanc')# bg_img = BackGamonIMG()# for pion_id in range(len(df_cicles)):#     # print(df_cicles.iloc[pion_id])#     df_line = df_cicles.iloc[pion_id]#     fleche_id = bg_img.getFlechePlusPres(df_line['center'], df_line['verticality'])#     if(fleche_id == -1):#         bg.add_bar(df_line['color'])#     else:#         bg.add_fleche_by_id(fleche_id, df_line['color'])# bg.debugPlateau()