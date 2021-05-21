#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 18:06:25 2021

@author: slejamble
"""
from app.src.gui_structure import BackGamonIMG
import cv2



def test_dice(img):
    bg_img = BackGamonIMG("./")
    bg_img.setDiceTuple(img)

    return bg_img.left_dice_value, bg_img.right_dice_value

def test_dice_list():
    list_dice_img = [(1,1),(2,1),(3,2),(4,1),(5,4), (5,5), (6,3), (6,6)]
    for dice1, dice2 in list_dice_img:
        img_name = "app/data/test_unit/dice/{}-{}.png".format(dice1, dice2)
        img = cv2.imread(img_name)

        left, right = test_dice(img)
        assert left == dice1
        assert right == dice2

    print("all dice tested")

test_dice_list()