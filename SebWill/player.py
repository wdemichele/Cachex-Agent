import referee.board
from SebWill import util
from random import randint


class Player:
    _STEAL = tuple("STEAL", )
    _PLACE = ("PLACE",)

    def __init__(self, player, n):

        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.player = player
        self.board = util.referee.board.Board(n)
        self.n_tokens = 0
        self.opp_tokens = []
        self.player_tokens = []
        self.corners = [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1)]
        self.token_to_build_on = None

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        return self.employ_strategy()

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        if action[0] == "STEAL":
            self.board.swap()
            if self.player == "blue":
                self.player_tokens.append((self.opp_tokens[0][1], self.opp_tokens[0][0]))
                self.opp_tokens.clear()
            else:
                self.opp_tokens.append((self.player_tokens[0][1], self.player_tokens[0][0]))
                self.player_tokens.clear()
        else:
            self.n_tokens += 1
            caps = self.board.place(player, (action[1], action[2]))
            if player != self.player:
                self.opp_tokens.append((action[1], action[2]))
            else:
                self.player_tokens.append((action[1], action[2]))
            if caps:
                for cap in caps:
                    if player != self.player:
                        self.player_tokens.remove(cap)
                    else:
                        self.opp_tokens.remove(cap)

    def employ_strategy(self):
        if self.n_tokens < 2:
            if self.player == "blue" and self.opp_tokens in self.corners:
                self.token_to_build_on = (self.opp_tokens[0][1], self.opp_tokens[1][0])
                return self._STEAL
            else:
                for corner in self.corners:
                    if not self.board.is_occupied(corner):
                        self.token_to_build_on = corner
                        return self._PLACE + corner
        if self.board.n < 6:
            return self._PLACE + self.alpha_beta_minimax(0, self.board, True,
                                                         util.MINIMAX_MIN, util.MINIMAX_MAX)[1]
        if self.n_tokens >= self.board.n:
            return self._PLACE + self.alpha_beta_minimax(0, self.board, True,
                                                         util.MINIMAX_MIN, util.MINIMAX_MAX)[1]
        if self.n_tokens <= self.board.n / 2:
            return self.build()
        return self.block()

    def build(self):
        steps = util.get_left_hex_steps()
        if self.player == "blue":
            if self.token_to_build_on[1] >= self.board.n / 2:
                steps = util.get_right_hex_steps()
        else:
            if self.token_to_build_on[0] < self.board.n / 2:
                steps = util.get_up_hex_steps()
            else:
                steps = util.get_down_hex_steps()
        for move in steps:
            new_spot = tuple(map(lambda x, y: x + y, move, self.token_to_build_on))
            if self.board.inside_bounds(new_spot) and not self.board.is_occupied(new_spot):
                self.token_to_build_on = new_spot
                return self._PLACE + new_spot
        return self.fallback_strategy()

    def block(self):
        spot_closest_to_end = None
        min_dist = 100
        direction_to_block = None
        if self.player == "blue":
            # if enemy is red, blocking a row is more efficient
            index = 0
        else:
            # if enemy is blue, blocking an adjacent column is more efficient
            index = 1
        # find the token closest to a opposite-half boundary
        for token in self.opp_tokens:
            # if left or bottom side
            if token[index] < self.board.n / 2:
                if (self.board.n - 1) - token[index] < min_dist:
                    spot_closest_to_end = token
                    if index:
                        direction_to_block = "right"
                    else:
                        direction_to_block = "up"
            else:
                if token[index] < min_dist:
                    spot_closest_to_end = token
                    if index:
                        direction_to_block = "down"
                    else:
                        direction_to_block = "left"

        if spot_closest_to_end:
            if direction_to_block == "up":
                block_spots = util.get_up_hex_steps()
            elif direction_to_block == "down":
                block_spots = util.get_down_hex_steps()
            elif direction_to_block == "right":
                block_spots = util.get_right_hex_steps()
            else:
                block_spots = util.get_left_hex_steps()
            for move in block_spots:
                new_spot = tuple(map(lambda x, y: x + y, move, spot_closest_to_end))
                if self.board.inside_bounds(new_spot) and not self.board.is_occupied(new_spot):
                    self.token_to_build_on = new_spot
                    return self._PLACE + new_spot

        return self.fallback_strategy()

    def fallback_strategy(self):
        while True:
            x = randint(0, self.board.n)
            y = randint(0, self.board.n)
            if self.board.inside_bounds((x, y)) and not self.board.is_occupied((x, y)):
                return self._PLACE + (x, y)

    def alpha_beta_minimax(self, depth, game_state, is_maximizing, alpha, beta):

        if depth == util.DEPTH_LIMIT:
            return util.eval_func(game_state), game_state

        if is_maximizing:
            # set to number below minimum of eval func
            curr_max = util.MINIMAX_MIN
            curr_best_move = None

            for move in util.get_reasonable_moves(self.board, self.n_tokens, self.player,
                                                  self.player_tokens, self.opp_tokens):

                move_state = util.make_state_from_move(game_state, move, self.player)
                value = self.alpha_beta_minimax(depth + 1, move_state, False, alpha, beta)[0]

                if value > curr_max:
                    curr_max = value
                    curr_best_move = move
                alpha = max(alpha, curr_max)

                if beta <= alpha:
                    # pruning principle
                    break

            return curr_max, curr_best_move
        else:

            curr_min = util.MINIMAX_MAX
            curr_best_move = None
            # Generate children
            for move in util.get_reasonable_moves(self.board, self.n_tokens, self.player,
                                                  self.player_tokens, self.opp_tokens):

                move_state = util.make_state_from_move(game_state, move, self.player)
                value = self.alpha_beta_minimax(depth + 1, move_state, True, alpha, beta)[0]

                if value < curr_min:
                    curr_min = value
                    curr_best_move = move
                beta = min(beta, curr_min)

                if beta <= alpha:
                    break

            return curr_min, curr_best_move
