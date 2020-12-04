class Pion:    def __init__(self, color):        self.color = color    def __str__(self):        return "Pion " + self.color    def getLayout(self):        print(self.color)        if(self.color == 'black'):            return 'x'        else:            return 'o'class Fleche:    def __init__(self):        self.list_pions = []    def addPion(self, color):        # print("add pion of color on fleche " + str(color))        self.list_pions.append(Pion(color))    def debug(self):        if(len(self.list_pions) == 0):            print("Aucun pion")        else:            for i in self.list_pions:                # print("i = "+str(i))                if(i != None):                    print(i)    def getLayout(self):        if(len(self.list_pions) == 0):            return None        else:            return str(len(self.list_pions))+"-"+self.list_pions[0].getLayout()class Bar:    def __init__(self):        self.list_pions = []    def debug(self):        if(len(self.list_pions) == 0):            print("Aucun pion sur barre")        else:            for i in self.list_pions:                # print("i = "+str(i))                if(i != None):                    print(i)    def addPion(self, color):        # print("add pion of color on bar " + str(color))        self.list_pions.append(Pion(color))    def getLayout(self):        black_token_count = 0        white_token_count = 0        print("bar get layout")        print(self.list_pions)        for i in self.list_pions:            if(i.color == "black"):                black_token_count += 1            else:                white_token_count += 1        layout = "="        if(black_token_count != 0):            layout += str(black_token_count) + "-x"            if(white_token_count != 0):                layout += "-" + str(white_token_count) + "-o"        elif(white_token_count != 0):            layout += str(white_token_count) + "-o"        return layoutclass BackGamon:    def __init__(self, player_color):        other_color = ("blanc", "noir")[player_color != "noir"]        self.bar = Bar()        self.fleche_list = []        for i in range(24):            self.fleche_list.append(Fleche())        # init game         # fleche 1        # self.fleche_list[0].addPion(player_color)        # self.fleche_list[0].addPion(player_color)        # # fleche 6        # self.fleche_list[5].addPion(other_color)        # self.fleche_list[5].addPion(other_color)        # self.fleche_list[5].addPion(other_color)        # self.fleche_list[5].addPion(other_color)        # self.fleche_list[5].addPion(other_color)        # # fleche 8        # self.fleche_list[7].addPion(other_color)        # self.fleche_list[7].addPion(other_color)        # self.fleche_list[7].addPion(other_color)        # # fleche 12        # self.fleche_list[11].addPion(player_color)        # self.fleche_list[11].addPion(player_color)        # self.fleche_list[11].addPion(player_color)        # self.fleche_list[11].addPion(player_color)        # self.fleche_list[11].addPion(player_color)        # # fleche 13        # self.fleche_list[12].addPion(other_color)        # self.fleche_list[12].addPion(other_color)        # self.fleche_list[12].addPion(other_color)        # self.fleche_list[12].addPion(other_color)        # self.fleche_list[12].addPion(other_color)        # # fleche 17        # self.fleche_list[16].addPion(player_color)        # self.fleche_list[16].addPion(player_color)        # self.fleche_list[16].addPion(player_color)        # # fleche 19        # self.fleche_list[18].addPion(player_color)        # self.fleche_list[18].addPion(player_color)        # self.fleche_list[18].addPion(player_color)        # self.fleche_list[18].addPion(player_color)        # self.fleche_list[18].addPion(player_color)        # # fleche 24        # self.fleche_list[23].addPion(other_color)        # self.fleche_list[23].addPion(other_color)    def set_dice(self, dice_tuple):        self.dice = dice_tuple    def reset_board(self):        self.bar = Bar()        self.fleche_list = []        for i in range(24):            self.fleche_list.append(Fleche())    def add_fleche_by_id(self, id_fleche, color):        self.fleche_list[id_fleche-1].addPion(color)    def add_bar(self, color):        self.bar.addPion(color)    def debugPlateau(self):        print("-- Bar --")        print(self.bar.debug())        fleche_nb = 1        for fleche in self.fleche_list:            print("fleche "+str(fleche_nb))            fleche.debug()            fleche_nb += 1            print("---------")        print("end debug")    def getLayout(self):        ai_layout = ""        fleche_nb = 0        for fleche in self.fleche_list:            fleche_layout = fleche.getLayout()            if(fleche_layout is not None):                actual_layout = str(fleche_nb)+"-"+fleche_layout+","                ai_layout += actual_layout            fleche_nb += 1                # kick last ","        ai_layout = ai_layout[:len(ai_layout)-1]        bar_layout = self.bar.getLayout()        self.bar.debug()        print(bar_layout)        ai_layout += bar_layout        ai_layout += "^"+str(self.dice[0])+'-'+str(self.dice[1])        print(ai_layout)        return ai_layout