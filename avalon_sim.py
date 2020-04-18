import numpy as np
import argparse


class Avalon:
    
    """A simulator for Avalon
    """
    
    def __init__(self, players, chars=None, seed=None):
        self.players = players
        self.chars = chars
        self.seed = seed
        
        if chars is not None:                
            if len(players) != len(chars):
                raise RuntimeError("Number of players does not match number of characters")
        else:
            if len(players) == 5:
                self.chars = ["Merlin", "Percival", "Good Guy 1", 
                    "Assassin", "Morgana"]
            elif len(players) == 6:
                self.chars = ["Merlin", "Percival", "Good Guy 1", "Good Guy 2", 
                    "Assassin", "Morgana"]
            elif len(players) == 7:
                self.chars = ["Merlin", "Percival", "Good Guy 1", "Good Guy 2", 
                    "Assassin", "Morgana", "Oberon"]        
            elif len(players) == 8:
                self.chars = ["Merlin", "Percival", "Good Guy 1", "Good Guy 2", "Good Guy 3", 
                    "Assassin", "Morgana", "Bad Guy 1"]  
            elif len(players) == 9:
                self.chars = ["Merlin", "Percival", "Good Guy 1", "Good Guy 2", "Good Guy 3", "Good Guy 4",
                    "Assassin", "Morgana", "Mordred"]
            elif len(players) == 10:
                self.chars = ["Merlin", "Percival", "Good Guy 1", "Good Guy 2", "Good Guy 3", "Good Guy 4",
                    "Assassin", "Morgana", "Oberon", "Mordred"]
            else:
                raise RuntimeError("Too few or too many players")

        print("Characters in {0}-person game: {1}".format(len(players), self.chars))
    
    def _setup(self):
        np.random.seed(self.seed)
        
        self.perm = np.random.permutation(self.chars)
        self.draw = {self.players[i]: {"char": self.perm[i]} for i in range(len(self.players))}
        self.whois = dict(zip(self.perm, self.players))

        self.bad_guys = list(
            {"Mordred", "Morgana", "Assassin", "Oberon", "Bad Guy 1"} & set(self.chars))
        
        self.who_are_bad_guys_no_oberon = list(np.random.permutation([
            self.whois[bad_guy] for bad_guy in self.bad_guys if bad_guy != "Oberon"]))
        self.who_are_bad_guys_no_mordred = list(np.random.permutation([
            self.whois[bad_guy] for bad_guy in self.bad_guys if bad_guy != "Mordred"]))
        
    def _bad_guys_meet(self):
        for bad_guy in self.bad_guys:
            if bad_guy != "Oberon":
                self.draw[self.whois[bad_guy]]["sees"] = [
                    who for who in self.who_are_bad_guys_no_oberon if who != self.whois[bad_guy]]

    def _merlin_sees(self):
        self.draw[self.whois["Merlin"]]["sees"] = {"bad guys but morderd": self.who_are_bad_guys_no_mordred}

    def _percival_sees(self):
        self.draw[self.whois["Percival"]]["sees"] = {
            "merlin-ish": list(np.random.permutation([self.whois["Merlin"], self.whois["Morgana"]]))}
        
    def sim(self):
        self._setup()
        self._bad_guys_meet()
        self._merlin_sees()
        self._percival_sees()
        return self.draw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--playerlist", nargs="+", help="players in game", required=True)
    args = parser.parse_args()

    avalon = Avalon(args.playerlist)
    draw = avalon.sim()

    for key, val in draw.items():
        print(key, val)

if __name__ == "__main__":
    main()

