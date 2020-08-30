"""
p1 = [[-6, 0], [-10, -1]]
p2 = [[-6, 0], [-10, -1]]
"""
p1 = [[0, 2], [10, -1]]
p2 = [[0, 11], [2, 0]]
"""
p1 = [[0, 6, 4], [6, 0, 4], [3, 3, 5]]
p2 = [[6, 0, 3], [0, 6, 3], [3, 3, 5]]
"""
def nashEquilibrium(p1, p2):
    betterPayoff = False
    equil = []
    equiList = []
    print("# Nash Equilibrium :")
    for strP1 in range(len(p1)):
        for strP2 in range(len(p2)):
            betterPayoff = False
            equil = []
            if p1[strP1][strP2] < max(p1[strP1]):
                betterPayoff = True
            for str in p1:
                if p1[strP1][strP2] < str[strP2]:
                    betterPayoff = True
            if p2[strP2][strP1] < max(p2[strP2]):
                betterPayoff = True
            for str in p2:
                if p2[strP2][strP1] < str[strP1]:
                    betterPayoff = True
            if not betterPayoff:
                print("Found Equilibrium : (", p1[strP1][strP2], ",", p2[strP2][strP1], ")")
                equil.append(p1[strP1][strP2])
                equil.append(p2[strP2][strP1])
                equiList.append(equil)
            else:
                print("Not Equilibrium : (", p1[strP1][strP2], ",", p2[strP2][strP1], ")")
    print("Nash Equilibriums :", equiList)
def main():
    print("# Players :")
    global p1
    print("Player 1: ", p1)
    global p2
    print("Player 2: ", p2)
    nashEquilibrium(p1, p2)

main()