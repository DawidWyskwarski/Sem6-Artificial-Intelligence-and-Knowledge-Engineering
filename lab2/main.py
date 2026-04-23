from core.game_state import GameState
from ai.player.player import Player
from core.piece import Piece
from ai.strategies.defensive import Defensive 
from ai.strategies.fast_lane import FastLane
from ai.strategies.zui_quan import ZuiQuan
from time import perf_counter
import argparse
import sys

def get_strategy(name: str):
    strategies = {
        "defensive": Defensive,
        "fast_lane": FastLane,
        "zui_quan": ZuiQuan
    }
    return strategies.get(name.lower(), Defensive)()

def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument("--p1-strategy", type=str, choices=["defensive", "fast_lane", "zui_quan"], default="defensive", help="Strategy for Player 1 (White)")
    parser.add_argument("--p1-depth", type=int, default=6, help="Search depth for Player 1")
    parser.add_argument("--p2-strategy", type=str, choices=["defensive", "fast_lane", "zui_quan"], default="defensive", help="Strategy for Player 2 (Black)")
    parser.add_argument("--p2-depth", type=int, default=6, help="Search depth for Player 2")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dimensions", type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'), help="Board dimensions (width height)")
    group.add_argument("--board-file", type=str, help="Path to a file containing custom board layout")

    return parser.parse_args()
    

def main() -> None:
    
    parser = argparse.ArgumentParser(description="Run the AI board game.")
    args = parse_args(parser)

    if args.board_file:
        with open(args.board_file, "r") as f:
            lines = f.read().splitlines()
            board = [[Piece(char) for char in line] for line in lines]
        current_state: GameState = GameState(board=board)
    elif args.dimensions:
        width, height = args.dimensions
        current_state: GameState = GameState.default_from_dimensions(width, height)
    else:
        current_state: GameState = GameState()

    player1: Player = Player(Piece.WHITE, get_strategy(args.p1_strategy), args.p1_depth)
    player2: Player = Player(Piece.BLACK, get_strategy(args.p2_strategy), args.p2_depth)

    player1_turn = True

    end: bool = False
    winner: Piece | None = None
    
    move_count = 1

    print("=======Player 1=======")
    print(player1)
    
    print("\n=======Player 2=======")
    print(player2)

    print("\n====Starting State====")

    total_visited_nodes = 0
    total_time = 0.0

    while(not end):
        
        print(current_state)
        print('')

        active_player = player1 if player1_turn else player2
        active_name = "White" if player1_turn else "Black"

        print(f"Move: {move_count}, Turn: {active_name}")
        turn_start = perf_counter()

        current_state = active_player.get_best_move(current_state)
        move_count += 1

        elapsed = perf_counter() - turn_start
        total_time += elapsed
        total_visited_nodes += active_player.visited_nodes
        print(f"{active_name} thought for {elapsed:.3f}s")

        player1_turn = not player1_turn
        end, winner = current_state.is_game_over()

    print("Final position")
    print(current_state)
    print(f"Winner {winner}")

    print(f"Visited nodes: {total_visited_nodes}", file=sys.stderr)
    print(f"Total execution time: {total_time:.3f}s", file=sys.stderr)


if __name__ == "__main__":
    main()