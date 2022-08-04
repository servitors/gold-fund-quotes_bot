def quote_destructor(message: str) -> tuple:
    author, tags = '', []
    quote_end = message.index('"', -1)
    quote = message[1:quote_end]
    for word in message[quote_end + 1:].split():
        if word.startswith('#'):
            tags.append(word)
        elif word.startswith('Ⓒ'):
            author = word
    return quote, author, tags


def quote_constructor(text: str, author: str) -> str:
    right_to_left_mark = u'\u061C'
    return f'"{text}"\n{right_to_left_mark}Ⓒ{author}'
