from schema import Schema, Optional, Or

# https://github.com/keleshev/schema

create_game_client_schema = Schema(
    {
        "protocol_type": "create_game",
        "board_state": [[int]],
        "rules": str,
        Or("p1_account_id", "p2_account_id", only_one=True): int,
        Optional("ai_difficulty"): int,
    }
)

create_game_server_schema = Schema(
    {
        "protocol_type": "create_game",
        "success": bool,
        "game_id": int,
    }
)

save_game_client_schema = Schema(
    {
        "protocol_type": "save_game",
        "game_id": int,
        "complete": bool,
        "board_state": [[int]],
        "next_turn": int,
    }
)

save_game_server_schema = Schema(
    {
        "protocol_type": "save_game",
        "success": bool,
    }
)
