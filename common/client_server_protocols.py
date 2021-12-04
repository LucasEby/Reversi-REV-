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

credential_check_client_schema = Schema(
    {
        "protocol_type": "login",
        "username": str,
        "password": str,
    }
)

credential_check_server_schema = Schema(
    {
        "protocol_type": "login",
        "success": bool,
        "credential_check": bool,
        "account_id": Optional[int],
    }
)

create_account_client_schema = Schema(
    {
        "protocol_type": "create_account",
        "username": str,
        "password": str,
        "elo": int,
        "pref_board_length": int,
        "pref_board_color": str,
        "pref_disk_color": str,
        "pref_opp_disk_color": str,
        "pref_line_color": str,
        "pref_rules": str,
        "pref_tile_move_confirmation": bool,
    }
)

create_account_server_schema = Schema(
    {
        "protocol_type": "create_account",
        "success": bool,
        "account_id": int,
    }
)

matchmaker_client_schema = Schema(
    {
        "protocol_type": "matchmaker",
        "my_account_id": int,
        "pref_rule": str,
    }
)

matchmaker_server_schema = Schema(
    {
        "protocol_type": "matchmaker",
        "success": bool,
        "game_id": int,
        "opp_account_id": int,
    }
)
