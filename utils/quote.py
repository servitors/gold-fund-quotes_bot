def quote_destructor(message: str) -> dict:
    quote_data = {'content': '', 'author': '', 'tags': []}
    for word in message.split()[1:]:
        if word.startswith('#'):
            quote_data['tag'].append(word)
        elif word.startswith('Ⓒ'):
            quote_data['author'] = word
        else:
            quote_data['content'] += word

        return quote_data


def quote_constructor(text: str, author: str) -> str:
    return text + "\n" + u"\u061C" + author
