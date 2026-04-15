from game_state import GameState

from piece import Piece

def main() -> None:
    init_state = GameState.default_from_dimensions(8,8)

    new_states = init_state.generate_states(Piece.WHITE)

    print(f"\nGenerated {len(new_states)} possible moves for WHITE:")
    for i, state in enumerate(new_states, 1):
        print(f"Move {i}:")
        print(state)
    
if __name__ == "__main__":
    main()