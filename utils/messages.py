def quote_destructor(message: str) -> dict:
    meta = {'content': '', 'author': '', 'tag': []}
    for i in message.split()[1:]:
        if i.startswith('#'):
            meta['tag'].append(i)
        elif i.startswith('@'):
            meta['author'] = i
        else:
            meta['content'] += i

        return meta


def quote_constructor(text: str, author: str) -> str:
    return text + "\n" + u"\u061C" + author
