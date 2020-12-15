def class_to_dict(obj):

    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            a = o.__dict__
            if "_sa_instance_state" in a:
                del a['_sa_instance_state']
            dict.update(a)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        a = obj.__dict__
        if "_sa_instance_state" in a:
            del a['_sa_instance_state']
        dict.update(a)
        return dict

def toJsonList(res):
    count = 0
    jsonList = []
    dict = {}
    for u in res:
        for c in u:
            count += 1
            if (count <= len(u)):
                dict.update(class_to_dict(c))  #函数classclass_to_dict
                if count == len(u):
                    jsonList.append(dict)
            else:
                count = 1
                dict = {}
                dict.update(class_to_dict(c))  #函数classclass_to_dict
    return jsonList;
