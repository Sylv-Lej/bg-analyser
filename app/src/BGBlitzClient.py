#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 10:28:50 2021

@author: slejamble
"""

import socket
import xml.etree.ElementTree as ET
from art import text2art

HOST = '65.21.184.121'
PORT = 12344

# message = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<PingRequest/>\n"

class BgBlitzClient():
    def __init__(self):
        self.connect()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        print('Connexion vers ' + HOST + ':' + str(PORT) + ' reussie.')

    def predict(self, layout, bar, out, dice):
        nb_out = 1
        # if(dice[1]== dice [0]):
        #     nb_out = 2

        msg_pred = """
            <?xml version="1.0" encoding="UTF-8" ?>
            <TutorRequest id='1234ab'>
              <comment>A comment describing the request, just for debugging</comment>
              <attr name="noise" value="0.0"/>
              <attr name="cubeful" value="false"/>
              <attr name="gammons" value="off"/>
              <attr name="backgammons" value="off"/>
              <attr name="noOfMoves"   value="{}"/>        <!-- any value greater 0 -->
              <attr name="ply" value="2"/>                <!-- optional; if missing taking the value from setup -->
              <position>
                <dice red='{}' green='{}'/>
                <score red='0' green='0'/>
                <attr name='matchLength' value='0'/>       <!-- if matchLength is 0 then it is a money game -->
                <attr name='whosOn' value='green'/>
                <attr name='crawford' value='false'/>
                <attr name='usecube' value='false'/>
                <attr name="jacoby" value="false"/>
                <attr name="beaver" value="false"/>
                <attr name='board'>
                  <board cube='1' cubeowner='none'>       <!-- cubeowner may be red,green or none -->
                    <points>{}</points>
                    <bar red='{}' green='{}'/>              <!--optional if no checker on the bar -->
                    <off red='{}' green='{}'/>             <!--optional if no checker off -->
                  </board>
                </attr>
              </position>
            </TutorRequest>""".format(nb_out, dice[0], dice[1], layout, bar[0], - bar[1], out[0], - out[1])

        # n = self.client.sendall(msg_pred.encode('utf-8'))
        for i in range(10):
            try:
                n = self.client.send(msg_pred.encode())
                if (n != len(msg_pred)):
                    print ('Erreur sur la reception, retrying')
                    self.connect()
                    self.predict(layout, bar, out, dice)
                else:
                    break
            except:
                print ("Erreur sur l'envoie, retrying")
                self.connect()
                self.predict(layout, bar, out, dice)
        else:
            print ('Envoi ok.')

        donnees = self.client.recv(4096)
        prob = 0
        try:
            root = ET.fromstring(donnees)
            if(root.tag == "Error"):
                print("Error tag in response, retrying")
                self.predict(layout, bar, out, dice)
            for child in root:

                # print("Rank {}".format(child.attrib['rank']))
                for moove in child:
                    if(moove.tag == "movePart"):
                        art=text2art("{} - {}".format(moove.attrib['from'], moove.attrib['to']))
                        print(art)
                        # print("{} -> {}".format(moove.attrib['from'], moove.attrib['to']))
                    if(moove.tag == "probabilities"):
                        if(child.attrib['rank'] == '1'):
                            prob = moove.attrib['greenWin']
                        print("Win chance : {} ".format(moove.attrib['greenWin']))
                    if(moove.tag == "moneyEquity"):
                        print("Equity    : {} ".format(moove.attrib['green']))
                print()
            return prob
        except:
            print('error parsing in XML')
            self.connect()
            self.predict(layout, bar, out, dice)
            return None

# print('Envoi de : ' + msg_test)

# if (n != len(message)):
#         print ('Erreur envoi.')
# else:
#         print ('Envoi ok.')

# print ('Reception...')



# print('Deconnexion.')
# client.close()