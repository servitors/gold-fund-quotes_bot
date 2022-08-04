def quote_destructor(message: str) -> tuple:
    quote, author, tags = '', '', []
    for word in message.split()[1:]:
        if word.startswith('#'):
            tags.append(word)
        elif word.startswith('Ⓒ'):
            author = word
        else:
            quote += word
        return quote, author, tags


def quote_constructor(text: str, author: str) -> str:
    right_to_left_mark = u'\u061C'
    return f'"{text}"\n{right_to_left_mark}Ⓒ{author}'
