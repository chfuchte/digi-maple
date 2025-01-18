def search_by_id(list_dicts, int id):
    cdef int i
    for i in range(len(list_dicts)):
        if list_dicts[i]["id"] == id:
            return list_dicts[i]
    return None
