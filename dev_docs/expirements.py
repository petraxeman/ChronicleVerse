import cvlib.database as dbl



# spells
a = {
    'general': {
        'title': 'Заклинания',
        'shortname': 'spells',
        'posts_count': 1,
        },
    'uix': [
        ['HeaderImageField', 'header_image', 'Верхнее изображение', 1],
        ['AvatarImageField', 'avatar_image', 'Аватар', .3],
        ['LineTextField', 'spell_name', 'Название заклинания', 1],
        ['LineTextField', 'magic_circle', 'Магический круг', 1],
        ['LineTextField', 'cast_time', 'Время накладывания', 1]
        ['LineTextField', 'distance', 'Дистанция применения', 1]
        ['LineTextField', 'school', 'Школа магии', 1],
        ['MultilineTextField', 'description', 'Описание', 1]],
}
'''
[general]
title = Заклинания
icon = ./resources/spell_icon.png

[image]
title = 
placeholder =
dbtype = BLOB
uitype = image

[spell_name] 
title = Название заклинания
placeholder = @title
dbtype = TEXT
uitype = string

[magic_circle]
title = Магический круг
placeholder = @empty
dbtype = INT
uitype = int

[cast_time]
title = Время накладывания
placeholder = @text
dbtype = TEXT
uitype = string

[distance]
title = Дистанция применения
placeholder = @text
dbtype = TEXT
uitype = string

[school]
title = Школа магии
placeholder = @text
dbtype = TEXT
uitype = string

[description]
title = Описание
placeholder = Описание функционирования скилла
dbtype = TEXT
uitype = text
'''