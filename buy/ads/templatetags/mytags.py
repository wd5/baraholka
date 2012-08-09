# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def cutlen(value, length):
    return value[:length]

@register.filter
def category_icon_class(value):
    name_to_icon = {u'Все': '155_show_thumbnails',
                    u'Авто': '005_car',
                    u'Бытовая техника': '297_kettle',
                    u'Книги/Учебники': '071_book',
                    u'Компьютеры и комплектующие': '086_display',
                    u'Мебель': '061_keynote',
                    u'Развлечения': '049_star',
                    u'Спорт': '356_dumbbell',
                    u'Телефоны/Смартфоны': '163_iphone',
                    u'Электроника': '011_camera',
                    u'Разное': '248_asterisk'}
    if value in name_to_icon.keys():
        return 'sprite-glyphicons_' + name_to_icon[value]
    else:
        return 'sprite-glyphicons_223_thin_right_arrow'