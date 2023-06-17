'''Functions to help you'''

def list_to_string(list_name):
    '''This function converts a list to a punctuated string'''
    string = ""
    for index, p in enumerate(list_name):
        if index != len(list_name)-1:
            string += '"' + str(p) + '", '
        else:
            string += 'or "' + p + '". '
    return string
