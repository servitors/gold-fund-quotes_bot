def message_destructor(message: str) -> dict:
    meta = {'content': '', 'author': '', 'tags': []}
    for i in message.split():
        if i.startswith('#'):
            meta['tags'].append(i)
        elif i.startswith('@'):
            meta['author'] = i
        else:
            meta['content'] += i

        return meta


def message_constructor(text: str, author: str) -> str:
    return text + u"\u061C" + author
