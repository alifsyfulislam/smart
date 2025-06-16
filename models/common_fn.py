def check_role(task_id):
    current_url = request.env.path_info
    
    if not session.prev_url:
        session.prev_url = current_url
        
    if session.prev_url != current_url:
        session.search_type=None
        session.search_value=''
        session.prev_url = current_url
    
    t_id=task_id
    is_valid_role=False
    task_listStr=session.task_listStr
    taskList=str(task_listStr).split(',')
    for i in range(len(taskList)):
        taskid=taskList[i]
        if taskid==t_id:
            is_valid_role=True
            break
        else:
            continue
    return is_valid_role

def check_special_char(strData):
    strData=strData.replace("@", " ")
    strData=strData.replace("<", " ")
    strData=strData.replace(">", " ")
    strData=strData.replace("(", " ")
    strData=strData.replace(")", " ")
    strData=strData.replace("{", " ")
    strData=strData.replace("}", " ")
    strData=strData.replace("[", " ")
    strData=strData.replace("]", " ")
    strData=strData.replace(",", " ")
    strData=strData.replace("`", " ")
    strData=strData.replace("'", " ")
    strData=strData.replace('"', ' ')
    strData=strData.replace("*", " ")
    strData=strData.replace("#", " ")
    strData=strData.replace(";", " ")
    strData=strData.replace("-", " ")
    strData=strData.replace("/", " ")    
    return strData