import tkinter, copy, codecs
from tkinter import *
from tkinter import messagebox
from random import *
from PIL import ImageTk, Image

turn = 1

class Enemy:
    def __init__(self, name, hp, attack, speed, sprite, ctn):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.sprite = sprite
        self.ctn = ctn

    def turnCounter(self):
        global turn
        turn += 1
        hturn.config(text="Turn: " + str(turn))

    def crit(self, speed, attack):
        chance = randint(1, 100)
        if chance <= speed:
            return attack
        else:
            return attack * 0.5

    def getDamageM(self, att_attack, att_speed, crit, targ_speed, turnCounter, heroname, ctrln):
            turnCounter()
            att_attack=float(crit(att_speed, att_attack))
            chdodge = 2 * targ_speed
            chance = randint(1, 100)
            if chdodge <= chance:
                self.hp -= att_attack
                mHp.config(text="HP: " + str(self.hp))
            else:
                self.hp = self.hp

            if self.hp <= 0:
                global turn
                messagebox.showinfo("CONGRATULATIONS", "You won in "+str(turn)+" turns")
                if ctrln == 1:
                    with codecs.open('ld.txt','a', "utf-8") as ld:
                        ld.write(heroname)
                        ld.write(",")
                        ld.write(str(turn))
                        ld.write('\n')
                switchFrames(frmBattle, frmMain)
                turn = 1
                del self


class Hero(Enemy):
    def __init__(self, hp, attack, speed, name):
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.name = name

    def getDamageH(self, att_attack, att_speed, crit, targ_speed):
            att_attack=float(crit(att_speed, att_attack))
            chdodge = 2 * targ_speed
            chance = randint(1, 100)
            if chdodge <= chance:
                self.hp -= att_attack
                hHP.config(text="HP: " + str(self.hp))
            else:
                self.hp = self.hp

            if self.hp <= 0:
                messagebox.showinfo("FAILURE", "You lost")
                switchFrames(frmBattle, frmMain)
                global turn
                turn = 1
                del self

    def healSelf(self, turnCounter):
        turnCounter()
        self.hp += 20

    def changeName(self, e, f):
        self.name = e.get()
        f.config(text="Current name: "+self.name)

def switchFrames(a, b):
        a.grid_forget()
        b.grid(row=0, column=0, sticky=" ")
        b.grid_rowconfigure(0, weight=1)
        b.grid_columnconfigure(0, weight=1)

def leaderboard(frm):
    limit = 5
    scores = []
    file = codecs.open('ld.txt', 'r', "utf-8")
    for line in file:
        name, score = line.split(",")
        score = int(score)
        scores.append((score, name))

    sorted_scores = sorted(scores, reverse=False)
    i=0
    for register in sorted_scores[:limit]:
        line = f"%s: %s turns" % (register[1], register[0])
        l_i = Label(frm, text=line)
        l_i.grid(row=i+1)
        i+=1
    file.close()

def battle(a, b, c, d):
    turn=1
    a.grid_forget()
    b.grid(row=0, column=0, sticky="N")
    b.grid_rowconfigure(0, weight=1)
    b.grid_columnconfigure(0, weight=1)
    mStats = LabelFrame(b, text="Enemy Stats:", width=25, height=11)
    mStats.grid(row=0, column=0, sticky="w")
    mName = Label(mStats, text=f"Name: {str(c.name)}").grid(row=0, column=0)
    mAttack = Label(mStats, text="Attack: " + str(c.attack)).grid(row=1, column=0)
    global mHp
    mHp = Label(mStats, text="HP: " + str(c.hp))
    mHp.grid(row=2, column=0)
    mSpeed = Label(mStats, text="Speed: " + str(c.speed)).grid(row=3, column=0)
    phMS = Label(mStats, text="", width=25, height=4).grid(row=4, columnspan=1)

    hStats = LabelFrame(b, text="Hero Stats:", width=25, height=11)
    hStats.grid(row=1, sticky="w")
    hName = Label(hStats, text="Name: "+d.name).grid(row=1)
    hAttack = Label(hStats, text="Attack: " + str(d.attack)).grid(row=2)
    global hHP
    hHP = Label(hStats, text="HP: " + str(d.hp))
    hHP.grid(row=3)
    hSpeed = Label(hStats, text="Speed: " + str(d.speed)).grid(row=4)
    phHS = Label(hStats, text="", width=25, height=4).grid(row=5)
    global hturn
    hturn = Label(hStats, text="Turn: "+str(turn))
    hturn.grid(row=6)

    mSprite = LabelFrame(b, text="Monster Sprite:", width=60, height=17)
    phms1 = Label(mSprite, text=" ", width=60, height=2).grid()
    mSprite.grid(row=0, column=1, sticky="e")
    mSpritee = Label(mSprite, image=c.sprite, anchor=CENTER).grid()
    phms2 = Label(mSprite, text=" ", width=60, height=2).grid()

    hOptions = LabelFrame(b, text="Hero's Options:", width=60, height=8)
    hOptions.grid(row=1, column=1, sticky="e")
    phOp1 = Label(hOptions, text=" ", width=60, height=2).grid(row=0, columnspan=3)
    damageButton = Button(hOptions, text="Attack!", width=15, height=5,command=lambda: [c.getDamageM(d.attack,d.speed, d.crit, c.speed, c.turnCounter, d.name,c.ctn),d.getDamageH(c.attack,c.speed,c.crit,d.speed)])
    damageButton.grid(row=1, column=0,sticky="")
    healButton = Button(hOptions, text="Heal!", width=15, height=5, command=lambda: [d.healSelf(c.turnCounter), d.getDamageH(c.attack,c.speed,c.crit,d.speed)]).grid(row=1,column=2,sticky="")
    phOp2 = Label(hOptions, text=" ", width=60, height=2).grid(row=2, columnspan=3)
    if c.speed > d.speed:
        messagebox.showinfo("The Enemy is faster!", c.name+" moves first!")
        d.getDamageH(c.attack,c.speed,c.crit,d.speed)


#root window
root = Tk()
root.title("BrawlSim")
root.geometry("640x480")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#main menu window
frmMain = tkinter.Frame(root)
frmMain.grid(row=0, column=0, sticky="N")
frmMain.grid_rowconfigure(0, weight=1)
frmMain.grid_columnconfigure(0, weight=1)

welcomeSign = Label(frmMain, text = "BrawlSimulator",font=("Courier", 44)).grid(row=0, column=0, sticky='e')
fButton = Button(frmMain, text="Fight!", width=30, height=5, borderwidth=6, command=lambda: switchFrames(frmMain, frmFight)).grid(row=1, column=0,sticky='')
lButton = Button(frmMain, text="Leaderboard", width=30, height=5, borderwidth=6, command=lambda: [switchFrames(frmMain, frmLeader), leaderboard(frmLeader)]).grid(row=2, column=0,sticky='')
oButton = Button(frmMain, text="Change Your name", width=30, height=5, borderwidth=6, command=lambda: switchFrames(frmMain, frmOptions)).grid(row=3, column=0,sticky='')
eButton = Button(frmMain, text="Exit", width=30, height=5, borderwidth=6, command=root.destroy).grid(row=4, column=0,sticky='')

#fight button window
frmFight = tkinter.Frame(root)
fightMenuText = Label(frmFight, text = "Choose your oponent!",font=("Courier", 38)).grid(row=0, column=0, sticky='e')
easyFButton = Button(frmFight, text="Bandit", width=30, height=5, borderwidth=6, command=lambda: battle(frmFight, frmBattle, copy.copy(Bandit), copy.copy(Me))).grid(row=1, column=0,sticky='')
mediumFButton = Button(frmFight, text="Zombie", width=30, height=5, borderwidth=6, command=lambda: battle(frmFight, frmBattle, copy.copy(Zombie), copy.copy(Me))).grid(row=2, column=0,sticky='')
hardFButton = Button(frmFight, text="Minotaur", width=30, height=5, borderwidth=6, command=lambda: battle(frmFight, frmBattle, copy.copy(Minotaur), copy.copy(Me))).grid(row=3, column=0,sticky='')
backButton = Button(frmFight, text="Back", width=30, height=5, borderwidth=6, command=lambda: switchFrames(frmFight, frmMain)).grid(row=4, column=0,sticky='')

#leaderboard window
frmLeader = tkinter.Frame(root)
Placeholder = Label(frmLeader, text = "Best Minotaur fighters!",font=("Courier", 33)).grid(row=0, column=0, sticky=' ')
phLabLeader = Label(frmLeader, text=" ").grid(row=1,column=0, sticky=' ')
backButton1 = Button(frmLeader, text="Back", width=30, height=5, borderwidth=6, command=lambda: switchFrames(frmLeader, frmMain)).grid(row=8,sticky=S)

#battle window
frmBattle = tkinter.Frame(root)

Me = Hero(60,25,13, "Frey")

#options window
frmOptions = tkinter.Frame(root)
currName = Label(frmOptions, text="Current name: "+Me.name)
currName.grid()
chname = Entry(frmOptions)
chname.grid()
chButton = Button(frmOptions, text="Change name", width=30, height=5, borderwidth=6, command=lambda: Me.changeName(chname,currName)).grid()
backButton2 = Button(frmOptions, text="Back", width=30, height=5, borderwidth=6, command=lambda: switchFrames(frmOptions, frmMain)).grid()

Bandit = Enemy("Bandit",50,20,10,ImageTk.PhotoImage(Image.open("images\enemy1.jpg")),0)
Zombie = Enemy("Zombie",60,30,12,ImageTk.PhotoImage(Image.open('images\enemy2.jpg')),0)
Minotaur = Enemy("Minotaur",70,35,16,ImageTk.PhotoImage(Image.open('images\enemy3.jpeg')),1)


mainloop()