from django import template

register = template.Library()

WORDS = {'один', 'два', 'iPhone', 'Apple'}


@register.filter()
def censor(value):
    text = value
    try:
        for word in WORDS:
            repl = word[0] + '*' * (len(word)-1)
            text = text.replace(word, repl)
    except Exception as e:
        print(f'Попытка применить censor-фильтр к переменной типа {type(value)}')
    return text
