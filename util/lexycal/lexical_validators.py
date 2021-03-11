def is_valid_number(lexeme: str) -> bool:
    has_dot = False
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
    return True
