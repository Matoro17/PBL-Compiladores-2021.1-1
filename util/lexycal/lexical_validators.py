def is_valid_number(lexeme: str) -> bool:
    has_dot = False
    previous_character = ""
    for index in range(0, len(lexeme)):
        character = lexeme[index]
        if index == 0 and character == "-":
            continue
        if character == ".":
            if has_dot:
                return False
            has_dot = True
        elif not character.isdigit():
            return False
        previous_character = character
    if not previous_character.isdigit():
        return False
    return True
