from core.piece import Piece
from core.game_state import GameState
from ai.strategies.strategy import Strategy
from core.game_utils import enemy_color


class EvaluatedState:
    """
    A wrapper class representing a game state and its heuristic evaluation score.

    :param GameState state: The game state being evaluated.
    :param float score: The heuristic score assigned to this state.
    Higher scores indicate a more favorable position for the maximizing player.
    """

    def __init__(self, state: GameState, score: float) -> None:
        self.state = state
        self.score = score


class Player:
    """
    An AI player that uses the minimax algorithm with alpha-beta pruning to determine optimal moves.

    The player evaluates future game states using a specified heuristic strategy.

    :param Piece color: The color of the pieces controlled by this player.
    :param Strategy strategy: The heuristic scoring strategy used to evaluate board positions.
    :param int future_sight_depth: The search depth for the minimax algorithm (number of plies/half-moves to look ahead).
    """

    def __init__(
        self, color: Piece, strategy: Strategy, future_sight_depth: int = 4
    ) -> None:
        self.color = color
        self.enemy_color = enemy_color(color)
        self.strategy = strategy
        self.depth = future_sight_depth
        self.visited_nodes = 0

    def __str__(self) -> str:
        return f"Piece color: {self.color}\nStrategy: {self.strategy.__class__.__name__}\nReasoning depth: {self.depth}"

    def get_best_move(self, state: GameState) -> GameState:
        """
        Predicted best move based on minimax algorithm.

        :param GameState state: Current game state
        :return GameState: Game state after the predicted best move.
        """
        self.visited_nodes = 0
        return self._minimax(state, self.depth, True, float("-inf"), float("inf")).state

    def _minimax(
        self,
        state: GameState,
        depth: int,
        maximizing: bool,
        alpha: float,
        beta: float,
    ) -> EvaluatedState:
        """
        Recursive minimax algorithm with alpha-beta pruning.

        :param GameState state: The current game state node in the search tree.
        :param int depth: The remaining depth to search before evaluating the board heuristically.
        :param bool maximizing: True if it's the maximizing player's turn, False if minimizing (opponent's turn).
        :param float alpha: The best (highest) score the maximizing player can guarantee at this level or above.
        :param float beta: The best (lowest) score the minimizing player can guarantee at this level or above.
        
        :return EvaluatedState: An object containing the optimal outcome state and its computed score.
        """

        self.visited_nodes += 1

        # Rate state for leaves
        if depth == 0 or state.is_game_over()[0]:
            return EvaluatedState(
                state, self.strategy.rate_position(state.board, self.color)
            )

        if maximizing:
            children = state.generate_states(self.color)

            best_state: EvaluatedState = EvaluatedState(state, float("-inf"))

            for child in children:

                eval_pos: EvaluatedState = self._minimax(
                    child, depth - 1, False, alpha, beta
                )

                if best_state.score < eval_pos.score:
                    best_state = EvaluatedState(child, eval_pos.score)

                alpha = max(alpha, eval_pos.score)
                if beta <= alpha:
                    break

            return best_state

        else:
            children = state.generate_states(self.enemy_color)

            best_state: EvaluatedState = EvaluatedState(state, float("inf"))

            for child in children:

                eval_pos: EvaluatedState = self._minimax(
                    child, depth - 1, True, alpha, beta
                )

                if best_state.score > eval_pos.score:
                    best_state = EvaluatedState(child, eval_pos.score)

                beta = min(beta, eval_pos.score)
                if beta <= alpha:
                    break

            return best_state
