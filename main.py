import logging
import bibtexparser


# log = logging.getLogger(__name__)


def fio2fio(fio: str) -> str:
    """
    >>> fio2fio('Михайлов Борис Борисович')
    'Михайлов\xa0Б.Б.'
    """
    ls = fio.split()
    if len(ls) == 2:
        return f'{ls[0]}\xa0{ls[1][0]}.'
    if len(ls) == 3:
        return f'{ls[0]}\xa0{ls[1][0]}.{ls[2][0]}.'
    raise ValueError(fio)


def fio2iof(fio: str) -> str:
    ls = fio.split()
    if len(ls) == 2:
        return f'{ls[1][0]}.\xa0{ls[0]}'
    # if len(ls) == 3:
    return f'{ls[1][0]}.{ls[2][0]}.\xa0{ls[0]}'
    # raise ValueError(fio)


def do(text: str) -> str:
    result = []
    for i in bibtexparser.loads(text).entries:
        if i['ENTRYTYPE'] in ('article', 'inproceedings'):
            authors = i['author'].replace(',', '').split(' and ')
            if len(authors) == 1:
                prefix = f"{fio2fio(authors[0])} {i['title']}"
            elif len(authors) in (2, 3):
                prefix = f"{fio2fio(authors[0])} {i['title']}\xa0/ {', '.join(map(fio2iof, authors))}"
            # elif len(authors) >= 4:
            else:
                prefix = f"{i['title']}\xa0/ {', '.join(map(fio2iof, authors))}"

            ls = []
            if 'journal' in i:
                ls.append('\xa0// ' + i['journal'])
            elif 'organization' in i:
                if 'booktitle' in i:
                    ls.append('\xa0// ' + i['booktitle'] + ', ' + i['organization'])
                else:
                    ls.append('\xa0// ' + i['organization'])
            else:
                if 'booktitle' in i:
                    ls.append('\xa0// ' + i['booktitle'])
                else:
                    ls.append('')
            ls.append(i['year'])
            if 'volume' in i:
                ls.append('v.\xa0' + i['volume'])
            if 'number' in i:
                ls.append('no.\xa0' + i['number'])
            if 'pages' in i:
                ls.append('pp.\xa0' + i['pages'].replace('--', '–'))
            suffix = '.\xa0— '.join(ls)

            result.append(f'{prefix}{suffix}')
        else:
            result.append(str(i))
    return '\n'.join(result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('ref.bib') as f:
        print(do(f.read()))
