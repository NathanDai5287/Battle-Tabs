import board
import random
import ujson
import itertools
import sys

class BattleTabsAI:

    MAX_REWARD = 2
	
    def __init__(self, q=dict(), sidelength=7):
        self.sidelength = sidelength
        # state 0: ship, state 1: unknown, state 2: excluded3
        self.reset()
        self.q = q                  # Q value as a function of state and (row, col) of the next action
        
    def reset(self):
        self.state = [[1 for _ in range(self.sidelength)] for _ in range(self.sidelength)]    # the map of the board
        self.valid = {(row, col) for row in range(self.sidelength) for col in range(self.sidelength)}  # valid candidates for future hits
        self.known = []          # set of groups containing at least one ship unit        
        
    def calculate(self, row, col, dist):
        inner = set((row + i, col + j) for i in range(-dist + 1, dist) for j in range(-dist + 1 + abs(i),dist-abs(i)))
        border = set((row + i, col + dist-abs(i)) for i in range(-dist, dist + 1)) | set((row + i, col - dist + abs(i)) for i in range(-dist+1, dist))
        innder = set((row, col) for row, col in inner if 0 <=row < self.sidelength and 0 <= col < self.sidelength)
        border = set((row, col) for row, col in border if 0 <=row < self.sidelength and 0 <= col < self.sidelength)
        return innder, border
    
    @property
    def state_to_str(self):
        return ''.join([str(self.state[row][col]) for row in range(self.sidelength) for col in range(self.sidelength)])
       
    def assign_reward(self, action, reward):
        state_code = self.state_to_str
        old_q, old_count = self.get_q_value(action)
        new_count = old_count + 1
        self.q[state_code, action] = ((old_q * old_count + reward) / new_count, new_count)
        
    def cleanup_known(self):
        changed = False
        all_pairs = itertools.combinations(self.known, 2)
        for pair in all_pairs:
            common = pair[0] & pair[1]
            for i in range(2):
                if common == pair[i]:
                    changed = True
                    if pair[1-i] in self.known:
                        self.known.remove(pair[i-1])
        if changed:
            self.cleanup_known()
                    
    def add_known(self, new_group):
        """
        Add new_group to self.known
        """
        if new_group:
            self.known.append(new_group)
            self.cleanup_known()
            
    def hit_known(self, action):
        """
        The position of action is a shop.

        """
        remove = [group for group in self.known if action in group]
        for element in remove:
            self.known.remove(element)
            
    def exclude_known(self, action):
        """
        The position of action is not a ship
        """
        empty = None
        for i, knowledge in enumerate(self.known):
            if action in knowledge:
                self.known[i].remove(action)
                if len(self.known[i]) == 0:
                    empty = i
        if empty is not None:
            self.known.pop(empty)
        self.cleanup_known()
                
    @property
    def chance(self):
        if len(self.known) == 0:
            return 0
        else:
            return 1 / min(set(map(len, self.known)))
    
    def update_q_value(self, action, status):
        row, col = action
        if status == 0:
            self.state[row][col] = 0
            self.valid.remove(action)
            self.hit_known(action)
            self.assign_reward(action, self.MAX_REWARD)
        else:
            inner, border = self.calculate(row, col, status)
            exclude = set((row, col) for row, col in inner if self.state[row][col]==1)
            reward = len(exclude) / len(self.valid)
            for row, col in exclude:
                self.state[row][col] = 2
            self.valid -= exclude
            if all([self.state[row][col] != 0 for row, col in border]):
                self.add_known(border)
            for position in exclude:
                self.exclude_known(position)
            new_chance = self.chance
            reward += new_chance - self.chance
            self.assign_reward(action, reward)

    def get_q_value(self, action):
        state_code = self.state_to_str
        if (state_code, action) not in set(self.q.keys()):
            self.q[state_code, action] = (0, 0)
        return self.q[state_code, action]
    
    def best_move(self, training=True):
        if training:
            action = random.sample(self.valid, 1)[0]
        else:
            if self.chance == 1:
                choose = list([action for action in self.known if len(action) == 1][0])
                action = choose[0]
            else:
                choose = [(action, self.get_q_value(action)[0]) for action in self.valid]
                action = max(choose, key=lambda x: x[1])[0]
        return action
    
    def load_q(self,file):
        with open(file) as f:
            q = ujson.load(f)
        new_q = dict()
        for key, value in q.items():
            state, action = key.split(', (')
            state = state.lstrip('(').replace("'", "")
            action = action.rstrip(')').split(', ')
            action = tuple(map(int, action))
            new_q[state, action] = value
        self.q = new_q
    
    def play(self, board, training=False):
        if not training:
            self.load_q('BattleTabsAI.json')
        counter = 1
        while not board.game_over() and self.valid:
            if not training:
                print(f'\nStep {counter}')
                counter += 1
            action = self.best_move(training=training)
            status = board.guess(action, output=not training)
            self.update_q_value(action, status)
        
    def train(self, runs, save=True):
        for i in range(runs):
            print(f'Run {i}')
            self.play(board.Board(), training=True)
            self.reset()
        if save:
            with open('BattleTabsAI.json', 'w') as f:
                f.write(ujson.dumps(self.q))

if __name__ == '__main__':
    player = BattleTabsAI()
    if len(sys.argv) > 1:
        player.train(int(sys.argv[1]))
    else:
        player.play(board.Board())
