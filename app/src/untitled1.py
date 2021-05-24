#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 14:37:31 2021

@author: slejamble
"""
import xml.etree.ElementTree as ET

data = '<?xml version="1.0" encoding="UTF-8"?>\r\n<TutorResult id="1234ab">\r\n  <move rank="1">\r\n    <movePart from="13" to="7" />\r\n    <movePart from="8" to="7" />\r\n    <probabilities greenWin="0.540" greenWinG="0.146" greenWinBG="0.000" redWin="0.460" redWinG="0.118" redWinBG="0.000" />\r\n    <moneyEquity green="0.153" red="-0.153" />\r\n  </move>\r\n  <move rank="2">\r\n    <movePart from="13" to="7" />\r\n    <movePart from="24" to="23" />\r\n    <probabilities greenWin="0.501" greenWinG="0.126" greenWinBG="0.000" redWin="0.499" redWinG="0.131" redWinBG="0.000" />\r\n    <moneyEquity green="-0.004" red="0.004" />\r\n  </move>\r\n  <move rank="3">\r\n    <movePart from="13" to="7" />\r\n    <movePart from="7" to="6" />\r\n    <probabilities greenWin="0.499" greenWinG="0.130" greenWinBG="0.000" redWin="0.501" redWinG="0.136" redWinBG="0.000" />\r\n    <moneyEquity green="-0.009" red="0.009" />\r\n  </move>\r\n</TutorResult>\r\n'
root = ET.fromstring(data)

for child in root:
    print("Rank {}".format(child.attrib['rank']))
    for moove in child:
        # if(moove.tag == "movePart"):
        #     print("{} -> {}".format(moove.attrib['from'], moove.attrib['to']))

        print(moove.tag, moove.attrib)