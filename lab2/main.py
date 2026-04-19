from core.game_state import GameState
from ai.player.player import Player
from core.piece import Piece
from ai.strategies.defensive import Defensive 
from ai.strategies.fast_lane import FastLane
from ai.strategies.zui_quan import ZuiQuan
from time import perf_counter

def main() -> None:
    
    current_state: GameState = GameState()
    player1: Player = Player(Piece.WHITE, Defensive(), 6)
    player2: Player = Player(Piece.BLACK, Defensive(), 6)

    player1_turn = True

    end: bool = False
    winner: Piece | None = None

    while(not end):
        
        print(current_state)

        active_player = player1 if player1_turn else player2
        active_name = "White" if player1_turn else "Black"

        print(f"Turn: {active_name}")
        turn_start = perf_counter()

        current_state = active_player.get_best_move(current_state)

        elapsed = perf_counter() - turn_start
        print(f"{active_name} thought for {elapsed:.3f}s")

        player1_turn = not player1_turn
        end, winner = current_state.is_game_over()

    print("Final position")
    print(current_state)
    print(f"Winner {winner}")


if __name__ == "__main__":
    main()