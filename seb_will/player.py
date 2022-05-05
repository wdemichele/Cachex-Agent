import referee.board
import util


class Player:
    _STEAL = tuple("STEAL", )
    _PLACE = ("PLACE", )

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
        self.corners = [(0, 0), (0, self.board.n), (self.board.n, 0), (self.board.n, self.board.n)]

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # figure out change


        #  don't need to apply it to your own board here

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
                self.player_tokens.append((self.opp_tokens[0][1], self.opp_tokenss[0][0]))
                self.opp_tokens.clear()
            else:
                self.opp_tokens.append((self.player_tokens[0][1], self.player_tokens[0][0]))
                self.player_tokens.clear()
        else:
            self.n_tokens += 1
            caps = self.board.place(player, (action[1], action[2]))
            if player != self.player_tokens:
                self.opp_tokens.append((action[1], action[2]))
                if caps:
                    for cap in caps:
                        self.opp_tokens.append(cap)
                        self.player_tokens.remove(cap)
            else:
                self.player_tokens.append((action[1], action[2]))
                if caps:
                    for cap in caps:
                        self.player_tokens.append(cap)
                        self.opp_tokens.remove(cap)

    def employ_strategy(self):
        if self.n_tokens < 2:
            if self.player == "blue" and self.opp_tokens in self.corners:
                return self._STEAL
            else:
                for corner in self.corners:
                    if not self.board.is_occupied(corner):
                        return self._PLACE + corner
        if self.board.n < 5:
            return self._PLACE + self.alpha_beta_minimax(util.DEPTH_LIMIT, self.board, True,
                                                         util.MINIMAX_MIN, util.MINIMAX_MAX)
        if self.n_tokens >= self.board.n:
            return self._PLACE + self.alpha_beta_minimax(util.DEPTH_LIMIT, self.board, True,
                                                         util.MINIMAX_MIN, util.MINIMAX_MAX)
        else:
            # Employ basic starting strat
            # if their structures are bigger, block
            # otherwise, continue building
            if self.n_tokens <= self.board.n/2:
                return self.build()
            return self.block()

    def alpha_beta_minimax(self, depth, game_state, is_maximizing, alpha, beta):

        if depth == util.get_depth_limit():
            return eval_func(game_state)

        if is_maximizing:
            # set to number below minimum of eval func
            curr_max = util.MINIMAX_MIN
            curr_best_move = None

            for move in util.get_reasonable_moves(self.board, self.n_tokens, self.player,
                                                  self.red_tokens, self.blue_tokens):

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
                                                  self.red_tokens, self.blue_tokens):

                move_state = util.make_state_from_move(game_state, move, self.player)
                value = self.alpha_beta_minimax(depth + 1, move_state, True, alpha, beta)[0]

                if value < curr_min:
                    curr_min = value
                    curr_best_move = move
                beta = min(beta, curr_min)

                if beta <= alpha:
                    break

            return curr_min, curr_best_move
