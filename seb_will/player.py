import referee.board
import util


class Player:
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
        self.red_tokens = []
        self.blue_tokens = []

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
            self.blue_tokens.append((self.red_tokens[0][1], self.red_tokens[0][0]))
            self.red_tokens.clear()
        else:
            self.n_tokens += 1
            caps = self.board.place(player, (action[1], action[2]))
            if player == "red":
                self.red_tokens.append((action[1], action[2]))
                if caps:
                    for cap in caps:
                        self.red_tokens.append(cap)
                        self.blue_tokens.append(cap)
            else:
                self.blue_tokens.append((action[1], action[2]))
                if caps:
                    for cap in caps:
                        self.blue_tokens.append(cap)
                        self.red_tokens.remove(cap)

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
