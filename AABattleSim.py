# The goal of this program is to provide engagement result forecasting to an Axis and Allies player. 
# Using expected value principles, the user can look ahead at the expected result of their engagement and determine if it is worth pursuing.

print("Welcome to the Axis & Allies battle simulator!\nThis tool will help inform your decisions on how to conduct engagements in the game.\n")

wants_to_continue = True #This is useful later when it lets the user decide to repeat the program wihtout reopening the file
wants_to_export = True #Keep true to export to CSV/Excel

# Seed the random number generator
import random
random.seed()

if wants_to_export:
    import csv
    f = open('AABattleSim.csv','w')
    writer = csv.writer(f)
    writer.writerow(["This is an export of data comparing predictions from the python code and real game battles."])
    writer.writerow(["Attacker","Defender","Attacker Units","Defender Units","Predicted Winner","Actual Winner","Predicted Units Remaining","Actual Units Remaining"])

# FUNCTIONS
# This function flips a string and returns the mirror of the original string
def flipString(string):
    origString = string
    newString = ""
    for x in range(len(string)-1,-1,-1):
        newString += origString[x]
    return newString

# This function checks if a player is still alive, meaning if he has any units. It returns a boolean true/false.
def isPlayerAlive(player):
    checksum = 0
    checksum += (player.infantry)
    checksum += (player.inf_arty)
    checksum += (player.artillery)
    checksum += (player.tank)
    checksum += (player.fighter)
    checksum += (player.bomber)
    checksum += (player.submarine)
    checksum += (player.cruiser)
    checksum += (player.carrier)
    checksum += (player.battleship2)
    checksum += (player.battleship1)
    if checksum <= 0:
        return False
    else:
        return True

# This function uses probabilty to round numbers it accepts a float expected hits and returns an int expected hits
def probRound(floatHits):
    if floatHits>0:
        prob = floatHits % 1
        intHits = int(floatHits - prob)
        if random.randint(0,1000) < prob*1000:
            intHits += 1
    else:
        intHits = 0
    return intHits

# This function is the expected value engine that drives the engagements. It returns the expected hits from the given player.
def expectedHits(player,atk_or_def):
    EV = 0.0
    if atk_or_def == "atk":
        EV += (player.infantry)*(inf.a)
        EV += (player.inf_arty)*(com.a)
        EV += (player.artillery)*(art.a)
        EV += (player.tank)*(tnk.a)
        EV += (player.fighter)*(ftr.a)
        EV += (player.bomber)*(bmb.a)
        EV += (player.submarine)*(sub.a)
        EV += (player.cruiser)*(cru.a)
        EV += (player.carrier)*(car.a)
        EV += (player.battleship2)*(bat.a)
        EV += (player.battleship1)*(bat.a)
    elif atk_or_def == "def":
        EV += (player.infantry)*(inf.d)
        EV += (player.artillery)*(art.d)
        EV += (player.tank)*(tnk.d)
        EV += (player.fighter)*(ftr.d)
        EV += (player.bomber)*(bmb.d)
        EV += (player.submarine)*(sub.d)
        EV += (player.cruiser)*(cru.d)
        EV += (player.carrier)*(car.d)
        EV += (player.battleship2)*(bat.d)
        EV += (player.battleship1)*(bat.d)
    return probRound(EV)

# This function decrements units from a player based on the hits the player received. It assumes the kill priority goes:
# infantry, artillery, armor, fighters, bombers (for land battles)
# healthy battleship, submarine, destroyer, carrier, cruiser, fighter, bomber, listing battleship (for naval battles)
def killUnits(player,hits):
    for x in range(hits,0,-1):
        if player.battleship2 > 0:
            player.battleship2 -= 1
            player.battleship1 += 1 #this is the only odd occurrance. I have to account for battleships have two hitpoints.
        elif player.infantry > 0:
            player.infantry -= 1
        elif player.inf_arty > 0:
            player.inf_arty -= 1
        elif player.artillery > 0:
            player.artillery -= 1
        elif player.tank > 0:
            player.tank -= 1
        elif player.submarine > 0:
            player.submarine -= 1
        elif player.destroyer > 0:
            player.destroyer -= 1
        elif player.carrier > 0:
            player.carrier -= 1
        elif player.cruiser > 0:
            player.cruiser -= 1
        elif player.fighter > 0:
            player.fighter -= 1
        elif player.bomber > 0:
            player.bomber -= 1
        elif player.battleship1 > 0:
            player.battleship1 -= 1


# This just makes things easier to read in the main code
def printMenu():
    print("Please type the number of units using the follwing syntax: number of units immediately followed by the type of units\nFor example, one infantry and two tanks would be: 1I 2T")
    print("The shorthand for units that you must use is as follows:\nInfantry = I\nArtillery = A\nTank = T\nFighter = F\nBomber = B\nSubmarine = S\nDestroyer = D\nCruiser = R\nCarrier = E\nBattleship = G")

# Prints the Units class in a readable fashion, useful for debugging.
def printPlayer(player):
    print("Selected player has:\n")
    print("Infantry: ",player.infantry,"\n")
    print("Inf w arty: ",player.inf_arty,"\n")
    print("Artillery: ",player.artillery,"\n")
    print("Tanks: ",player.tank,"\n")
    print("Fighters: ",player.fighter,"\n")
    print("Bombers: ",player.bomber,"\n")
    print("Submarines: ",player.submarine,"\n")
    print("Destroyers: ",player.destroyer,"\n")
    print("Carriers: ",player.carrier,"\n")
    print("Cruisers: ",player.cruiser,"\n")
    print("Battleships: ",player.battleship2,"\n")
    print("Listing Battleships: ",player.battleship1,"\n")

def fancyString(player):
    result = ""
    if (player.infantry > 0) or (player.inf_arty > 0):
        result += " "
        result += str(player.infantry + player.inf_arty)
        result += " infantry,"
    if player.artillery > 0:
        result += " "
        result += str(player.artillery)
        result += " artillery,"
    if player.tank > 0:
        result += " "
        result += str(player.tank)
        result += " tank(s),"
    if player.fighter > 0:
        result += " "
        result += str(player.fighter)
        result += " fighter(s),"
    if player.bomber > 0:
        result += " "
        result += str(player.bomber)
        result += " bomber(s),"
    if player.submarine > 0:
        result += " "
        result += str(player.submarine)
        result += " submarine(s),"
    if player.destroyer > 0:
        result += " "
        result += str(player.destroyer)
        result += " destroyer(s),"
    if player.cruiser > 0:
        result += " "
        result += str(player.cruiser)
        result += " cruiser(s),"
    if player.carrier > 0:
        result += " "
        result += str(player.carrier)
        result += " carrier(s),"
    if (player.battleship2 > 0) or (player.battleship1 > 0):
        result += " "
        result += str(player.battleship2 + player.battleship1)
        result += " battleship(s),"
    if result[len(result)-1] == ",":
        result = flipString(result)
        result = result.replace(",",".",1)
        result = flipString(result)
    return result

# DEFINTIONS
# This class represents what each player brings to the fight
class Units:
    def __init__(player, infantry, inf_arty, artillery, tank, fighter, bomber, submarine, destroyer, cruiser, carrier, battleship2, battleship1):
        #                I         C         A          T     F        B       S          D          R        E        G
        player.infantry = infantry
        player.inf_arty = inf_arty
        player.artillery = artillery
        player.tank = tank
        player.fighter = fighter
        player.bomber = bomber
        player.submarine = submarine
        player.destroyer = destroyer
        player.cruiser = cruiser
        player.carrier = carrier
        player.battleship2 = battleship2
        player.battleship1 = battleship1

class Prob:
    def __init__(unit, a, d):
        unit.a = a
        unit.d = d

inf = Prob(0.167,0.333)
com = Prob(0.333,0)
art = Prob(0.333,0.333)
tnk = Prob(0.5  ,0.5)
ftr = Prob(0.5  ,0.667)
bmb = Prob(0.667,0.167)
sub = Prob(0.333,0.167)
des = Prob(0.333,0.333)
cru = Prob(0.5  ,0.5)
car = Prob(0.167,0.333)
bat = Prob(0.667,0.667)
aaa = Prob(0    ,0.167)



# MAIN
while wants_to_continue:

    # Ask if prepartory fires, if submarine sneak attack, or if anti-air shots required
    is_prep_snk_aa = int(input("If the attack has preparatory fires please type 1.\nIf the attack has a submarine sneak attack, please type 2.\nIf the attack has an anti-air battle, please type 3.\nIf none of the above, please type 0.\n..."))
    # This if statement protects against numerical inputs outside the range 0-3. Still needs work to accept string inputs.
    if (is_prep_snk_aa < 1) or (is_prep_snk_aa > 3):
        is_prep_snk_aa=0

    # Take user inputs from attacker
    attacker = Units(0,0,0,0,0,0,0,0,0,0,0,0)
    print("\n")
    printMenu()
    atk_input = input("How many units are attacking? ")
    orig_atk_units = atk_input
    atk_input += " "
    atk_input = flipString(atk_input)
    atk_input += " "
    for x in range(len(atk_input)-1):
        if atk_input[x] == "I":
            if atk_input[x+2] == "":
                attacker.infantry += int(atk_input[x+1])
            else:
                attacker.infantry += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "A":
            if atk_input[x+2] == "":
                attacker.artillery += int(atk_input[x+1])
            else:
                attacker.artillery += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "T":
            if atk_input[x+2] == "":
                attacker.tank += int(atk_input[x+1]) 
            else:
                attacker.tank += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "F":
            if atk_input[x+2] == "":
                attacker.fighter += int(atk_input[x+1])
            else:
                attacker.fighter += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "B":
            if atk_input[x+2] == "":
                attacker.bomber += int(atk_input[x+1])
            else:
                attacker.bomber += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "S":
            if atk_input[x+2] == "":
                attacker.submarine += int(atk_input[x+1])
            else:
                attacker.submarine += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "D":
            if atk_input[x+2] == "":
                attacker.destroyer += int(atk_input[x+1])
            else:
                attacker.destroyer += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "R":
            if atk_input[x+2] == "":
                attacker.cruiser += int(atk_input[x+1])
            else:
                attacker.cruiser += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "E":
            if atk_input[x+2] == "":
                attacker.carrier += int(atk_input[x+1])
            else:
                attacker.carrier += int(atk_input[x+2]+atk_input[x+1])
        elif atk_input[x] == "G":
            if atk_input[x+2] == "":
                attacker.battleship2 += int(atk_input[x+1])
            else:
                attacker.battleship2 += int(atk_input[x+2]+atk_input[x+1])
    # gotta move infantry over to the inf_arty class if they have artillery support as the attacker
    if (attacker.artillery > 0) and (attacker.infantry >= attacker.artillery):
        attacker.infantry = attacker.infantry - attacker.artillery
        attacker.inf_arty = attacker.artillery

    # Take user inputs from defender
    defender = Units(0,0,0,0,0,0,0,0,0,0,0,0)
    #printMenu() #style choice--- if you need the menu printed again, uncomment it
    def_input = input("How many units are defending? ")
    orig_def_units = def_input
    def_input += " "
    def_input = flipString(def_input)
    def_input += " "
    for x in range(len(def_input)-1):
        if def_input[x] == "I":
            if def_input[x+2] == "":
                defender.infantry += int(def_input[x+1])
            else:
                defender.infantry += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "A":
            if def_input[x+2] == "":
                defender.artillery += int(def_input[x+1])
            else:
                defender.artillery += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "T":
            if def_input[x+2] == "":
                defender.tank += int(def_input[x+1])
            else:
                defender.tank += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "F":
            if def_input[x+2] == "":
                defender.fighter += int(def_input[x+1])
            else:
                defender.fighter += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "B":
            if def_input[x+2] == "":
                defender.bomber += int(def_input[x+1])
            else:
                defender.bomber += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "S":
            if def_input[x+2] == "":
                defender.submarine += int(def_input[x+1])
            else:
                defender.submarine += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "D":
            if def_input[x+2] == "":
                defender.destroyer += int(def_input[x+1])
            else:
                defender.destroyer += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "R":
            if def_input[x+2] == "":
                defender.cruiser += int(def_input[x+1])
            else:
                defender.cruiser += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "E":
            if def_input[x+2] == "":
                defender.carrier += int(def_input[x+1])
            else:
                defender.carrier += int(def_input[x+2]+def_input[x+1])
        elif def_input[x] == "G":
            if def_input[x+2] == "":
                defender.battleship2 += int(def_input[x+1])
            else:
                defender.battleship2 += int(def_input[x+2]+def_input[x+1])

    # Perform pre-engagement activity
    # Preparatory Fires
    if is_prep_snk_aa == 1:
        num_battleships = int(input("How many battleships are providing preparatory fires? "))
        num_cruisers = int(input("How many cruisers are providing preparatory fires? "))
        prep_fire_hits = num_battleships*bat.a
        prep_fire_hits += num_cruisers*cru.a
        prep_fire_hits = probRound(prep_fire_hits)
        killUnits(defender,prep_fire_hits)
        print("Prep fire hits: ",prep_fire_hits)

    # Submarine Sneak Attack
    elif is_prep_snk_aa == 2:
        snk_atk_hits = probRound(attacker.submarine*sub.a)
        killUnits(defender,snk_atk_hits)
        print("Sneak attack hits: ", snk_atk_hits)

    # Anti-Air
    elif is_prep_snk_aa == 3:
        num_aircraft = attacker.bomber + attacker.fighter
        bomber_hits = probRound(attacker.bomber*aaa.d)
        fighter_hits = probRound(attacker.fighter*aaa.d)
        attacker.bomber -= bomber_hits
        attacker.fighter -= fighter_hits
        print("Anti-Air bomber hits: ", bomber_hits)
        print("Anti-Air fighter hits: ", fighter_hits)

    # Determine expected value of first engagement and then iterate until one side has zero pieces
    is_attacker_alive = True
    is_defender_alive = True
    round_counter = 0
    
    while is_attacker_alive and is_defender_alive:
        round_counter += 1

        attacker_hits = expectedHits(attacker,"atk")
        defender_hits = expectedHits(defender,"def")

        killUnits(attacker,defender_hits)
        killUnits(defender,attacker_hits)

        is_attacker_alive = isPlayerAlive(attacker)
        is_defender_alive = isPlayerAlive(defender)
        print("Round ",round_counter,":")
        print("Attacker scored ",attacker_hits," hits. Defender scored ",defender_hits," hits.\nAttacker is still alive? ",is_attacker_alive," Defender is still alive? ",is_defender_alive)
        #printPlayer(attacker)
        #printPlayer(defender)

    result = "\nAfter "
    result += str(round_counter)
    result += " rounds, "
    if is_attacker_alive:
        result += "the attacker wins.\nThe attacker will retain the following after the battle: "
        result += fancyString(attacker)
    elif is_defender_alive:
        result += "the defender wins.\nThe defender will retain the following after the battle: "
        result += fancyString(defender)
    else:
        result = "everyone dies."
    print(result,"\n")

    # This section here is built to export data to excel to analyze trends of luck in the game. Turn it off by turning wants_to_export false.
    if wants_to_export:
        no_quit = True
        wants_to_quit = input("Do you want to stop the recording of this engagement for any reason? [y/n] ")
        if (wants_to_quit == "y") or (wants_to_quit == "Y"):
            no_quit = False
    if wants_to_export and no_quit:
        atkr = input("Who was the attacker? Type only the first letter of the nation in lowercase: ")
        defd = input("Who was the defender? Type only the first letter of the nation in lowercase: ")
        if is_attacker_alive:
            pre_win = atkr
            pre_unt_rem = attacker.infantry+attacker.inf_arty+attacker.artillery+attacker.tank+attacker.fighter+attacker.bomber+attacker.submarine+attacker.destroyer+attacker.cruiser+attacker.carrier+attacker.battleship1+attacker.battleship2
        elif is_defender_alive:
            pre_win = defd
            pre_unt_rem = defender.infantry+defender.artillery+defender.tank+defender.fighter+defender.bomber+defender.submarine+defender.destroyer+defender.cruiser+defender.carrier+defender.battleship1+defender.battleship2
        else:
            pre_win = "0"
        act_win = input("Who actaully won? Type only the first letter of the nation in lowercase: ")
        act_unt_rem = input("How many total units did the winner retain after the battle? Enter only a total number, not a type of unit: ")
        writer.writerow([atkr,defd,orig_atk_units,orig_def_units,pre_win,act_win,pre_unt_rem,act_unt_rem])

    userInput = input("Would you like to run another simulation? [y/n] ... ")
    if (userInput == "y") or (userInput == "Y"):
        wants_to_continue = True
    else:
        wants_to_continue = False
        break
print("Thanks for running the Axis and Allies battle simulator! \n")

if wants_to_export:
    f.close()