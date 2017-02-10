from django import template

register = template.Library()


@register.filter(name='access')
def access(dictionary, key):
    return dictionary[key]


@register.filter(name='entry')
def entry(list, index):
    return list[index]


@register.filter(name='keys')
def keys(dictionary):
    return dictionary.keys()


@register.filter(name='contains')
def contains(value, arg):
    return str(arg) in value


@register.filter(name='name')
def name(value):
    name_index = value.find('Name: ')
    value = value[name_index + len('Name: '):]
    name_end = value.find(' ')
    first_name = value[:name_end]
    value = value[name_end + 1:]
    name_end = value.find(' ')
    last_name = value[:name_end]
    return first_name + " " + last_name


@register.filter(name='position')
def position(value):
    position_index = value.find('Position: ')
    value = value[position_index + len('Position: '):]
    position_end = value.find(' ')
    return value[:position_end]


@register.filter(name='playerid')
def playerid(value):
    id_index = value.find('Player ID: ')
    value = value[id_index + len('Player ID: '):]
    id_end = value.find(' ')
    return str(value[:id_end])
