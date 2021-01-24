fullNameList = string.split(' ')
        id = ''
        for i in players:
            if i['first_name'] == fullNameList[0] and i['last_name'] == fullNameList[1]:
                id = i['id']