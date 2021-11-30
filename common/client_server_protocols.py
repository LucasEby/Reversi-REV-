from schema import Schema, Optional, Or  # type: ignore

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

save_preferences_client_schema = Schema(
    {
        "protocol_type": "save_preferences",
        "account_id": int,
        "pref_board_length": int,
        "pref_board_color": str,
        "pref_disk_color": str,
        "pref_opp_disk_color": str,
        "pref_line_color": str,
        "pref_rules": str,
        "pref_tile_move_confirmation": bool,
    }
)

save_preferences_server_schema = Schema(
    {"protocol_type": "save_preferences", "success": bool}
)
