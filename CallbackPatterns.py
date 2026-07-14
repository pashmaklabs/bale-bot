from Types import SearchResult

def back_pattern(data: object):
    return True if (type(data) == tuple and "back" in data) else False

def result_display_pattern(data: object):
    return True if type(data) == SearchResult else False

def comment_display_pattern(data: object):
    return True if (type(data) == tuple and "comments" in data) else False