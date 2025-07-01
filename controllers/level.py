def territory_town_level_code_incr(input_str):
    prefix, numeric_part = input_str[:-4], input_str[-4:]
    incremented_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
    result_str = prefix + incremented_numeric_part
    return result_str

def route_beat_level_code_incr(input_str):
    prefix, numeric_part = input_str[:-7], input_str[-7:]
    incremented_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
    result_str = prefix + incremented_numeric_part
    return result_str

def territory_validation(form):
    level_name = (form.vars.level_name or '').strip()
    level_id = ''
    if not level_name:
        form.errors.level_name='Territory can not be empty'
        
    record=db(
        (db.sm_level.cid==session.cid) & 
        (db.sm_level.depth=='0')
    ).select(
        db.sm_level.ALL,
        orderby=~db.sm_level.id,
    ).first()
    
    if record:
        level_id = territory_town_level_code_incr(record.level_id)
        form.vars.cid = session.cid
        form.vars.level_id = level_id.upper()
        form.vars.level_name = level_name.upper()
        form.vars.level0 = level_id.upper()
        form.vars.level0_name = level_name.upper()
        form.vars.parent_level_id = '0'
        form.vars.parent_level_name = ''
        form.vars.depth = '0'
        form.vars.is_leaf = '0'
    else:
        form.errors.level_name='Demo Territory'
        
def town_validation(form):
    level_name = (form.vars.level_name or '').strip()
    level0     = (form.vars.level0 or '').strip()
    level_id = ''
    
    if not level0:
        form.errors.level_name='Territory can not be empty'
    
    if not level_name:
        form.errors.level_name='Town can not be empty'
        
    records=db(
        (db.sm_level.cid==session.cid) & 
        (db.sm_level.depth=='1')
    ).select(
        db.sm_level.ALL,
        orderby=~db.sm_level.id,
    )
    
    p_records = [r for r in records if r.parent_level_id == level0]
    
    record = max(
        records,
        key=lambda r: int(r.level_id[1:]) if r.level_id[1:].isdigit() else -1
    )
    
    if p_records:
        if record:
            level_id = territory_town_level_code_incr(record.level_id)
            
            form.vars.cid = session.cid
            form.vars.level_id = level_id.upper()
            form.vars.level_name = level_name.upper()
            
            form.vars.level0_name = p_records[0].level0_name.upper()
            form.vars.parent_level_id = p_records[0].level0.upper()
            form.vars.parent_level_name = p_records[0].level0_name.upper()
            
            form.vars.level1 = level_id.upper()
            form.vars.level1_name = level_name.upper()
            
            form.vars.depth = '1'
            form.vars.is_leaf = '0'
        else:
            form.errors.level_name='Demo Area'
    else:
        row=db(
            (db.sm_level.cid==session.cid) & 
            (db.sm_level.level_id==level0)
        ).select(
            db.sm_level.ALL,
            orderby=~db.sm_level.id,
        ).first()
        
        if row:
            level_id = territory_town_level_code_incr(record.level_id)
            
            form.vars.cid = session.cid
            form.vars.level_id = level_id.upper()
            form.vars.level_name = level_name.upper()
            
            form.vars.level0_name = row.level0_name
            form.vars.parent_level_id = row.level0
            form.vars.parent_level_name = row.level0_name
            
            form.vars.level1 = level_id.upper()
            form.vars.level1_name = level_name.upper()
            
            form.vars.depth = '1'
            form.vars.is_leaf = '0'
        else:
            form.errors.level_name='Town can not be empty'
        
def route_validation(form):
    level_name = (form.vars.level_name or '').strip()
    level1     = (form.vars.level1 or '').strip()
    level_id = ''
    
    if not level1:
        form.errors.level_name='Town can not be empty'
    
    if not level_name:
        form.errors.level_name='Route can not be empty'
        
    records=db(
        (db.sm_level.cid==session.cid) & 
        (db.sm_level.depth=='2')
    ).select(
        db.sm_level.ALL,
        orderby=~db.sm_level.id,
    )
    
    p_records = [r for r in records if r.parent_level_id == level1]
    record = max(
        records,
        key=lambda r: int(r.level_id[1:]) if r.level_id[1:].isdigit() else -1
    )
    if p_records:
        if record:
            level_id = route_beat_level_code_incr(record.level_id)
            
            form.vars.cid = session.cid #smart
            form.vars.level_id = level_id.upper() #zone
            form.vars.level_name = level_name.upper() #zone
            # National
            form.vars.level0 = p_records[0].level0.upper() #hos
            form.vars.level0_name = p_records[0].level0_name.upper() #hos
            #Area
            form.vars.level1 = p_records[0].level1.upper() #area
            form.vars.level1_name = p_records[0].level1_name.upper() #area
            #parent
            form.vars.parent_level_id = p_records[0].level1.upper() #area
            form.vars.parent_level_name = p_records[0].level1_name.upper() #area
            #zone
            form.vars.level2 = level_id.upper() #zone
            form.vars.level2_name = level_name.upper() #zone
            form.vars.depth = '2'
            form.vars.is_leaf = '0'
        else:
            form.errors.level_name='Demo Route'
    else:
        row=db(
            (db.sm_level.cid==session.cid) & 
            (db.sm_level.level_id==level1)
        ).select(
            db.sm_level.ALL,
            orderby=~db.sm_level.id,
        ).first()
        
        if row:
            level_id = route_beat_level_code_incr(record.level_id)
            
            form.vars.cid = session.cid
            form.vars.level_id = level_id.upper()
            form.vars.level_name = level_name.upper()
            #National
            form.vars.level0 = row.level0
            form.vars.level0_name = row.level0_name
            #Area
            form.vars.level1 = row.level1
            form.vars.level1_name = row.level1_name
            #parent
            form.vars.parent_level_id = row.level1
            form.vars.parent_level_name = row.level1_name
            #zone
            form.vars.level2 = level_id.upper()
            form.vars.level2_name = level_name.upper()
            form.vars.depth = '2'
            form.vars.is_leaf = '0'
        else:
            form.errors.level_name='Demo Route'

def beat_validation(form):
    level_name = (form.vars.level_name or '').strip()
    level2     = (form.vars.level2 or '').strip()
    
    if not level2:
        form.errors.level_name='Zone can not be empty'
    
    if not level_name:
        form.errors.level_name='Beat can not be empty'
        
    records=db(
        (db.sm_level.cid==session.cid) & 
        (db.sm_level.depth=='3')
    ).select(
        db.sm_level.ALL,
        orderby=~db.sm_level.id,
    )
    
    p_records = [r for r in records if r.parent_level_id == level2]
    record = max(
        records,
        key=lambda r: int(r.level_id[1:]) if r.level_id[1:].isdigit() else -1
    )
    if p_records:
        if record:
            level_id = route_beat_level_code_incr(record.level_id)
            form.vars.cid = session.cid #smart
            form.vars.level_id = level_id.upper() #ter
            form.vars.level_name = level_name.upper() #ter
            # National
            form.vars.level0 = p_records[0].level0.upper() #hos
            form.vars.level0_name = p_records[0].level0_name.upper() #hos
            #Area
            form.vars.level1 = p_records[0].level1.upper() #area
            form.vars.level1_name = p_records[0].level1_name.upper() #area
            #Zone
            form.vars.level2 = p_records[0].level2.upper() #zone
            form.vars.level2_name = p_records[0].level2_name.upper() #zone
            #parent
            form.vars.parent_level_id = p_records[0].level2.upper() #area
            form.vars.parent_level_name = p_records[0].level2_name.upper() #area
            #zone
            form.vars.level3 = level_id.upper() #ter
            form.vars.level3_name = level_name.upper() #ter
            form.vars.depth = '3'
            form.vars.is_leaf = '1'
        else:
            form.errors.level_name='Demo Beat'
    else:
        row=db(
            (db.sm_level.cid==session.cid) & 
            (db.sm_level.level_id==level2)
        ).select(
            db.sm_level.ALL,
            orderby=~db.sm_level.id,
        ).first()
        
        if row:
            level_id = route_beat_level_code_incr(record.level_id)
            form.vars.cid = session.cid
            form.vars.level_id = level_id.upper()
            form.vars.level_name = level_name.upper()
            #National
            form.vars.level0 = row.level0
            form.vars.level0_name = row.level0_name
            #Area
            form.vars.level1 = row.level1
            form.vars.level1_name = row.level1_name
            #Zone
            form.vars.level2 = row.level2
            form.vars.level2_name = row.level2_name
            #parent
            form.vars.parent_level_id = row.level2
            form.vars.parent_level_name = row.level2_name
            #ter
            form.vars.level3 = level_id.upper()
            form.vars.level3_name = level_name.upper()
            form.vars.depth = '3'
            form.vars.is_leaf = '1'
        else:
            form.errors.level_name='Demo Beat'
    
def index():
    
    div_topbar = True
    div_sidebar = True
    div_login_template = False
    
    visited_controller = request.controller
    visited_function = request.function
    reqPage=len(request.args)
    page = 0
    
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL(c='auth', f='login'))
        
    # =============================== Middleware
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Territory'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    territory_id=request.vars.territory_id if request.vars.territory_id else ''
    
    
    session.search_type=search_type
    session.search_value=search_value if search_value is not None else ''
    session.btn_filter=btn_filter
    session.btn_all=btn_all
    session.btn_download=btn_download
    
    if btn_filter:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
    if btn_download:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
        redirect(URL(c='level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value,
            territory_id=territory_id
        )))
    if btn_all:
        session.btn_filter=None
        session.btn_all=None
        session.btn_download=None
        session.search_type=None
        session.search_value=''
        reqPage=0
    
    if len(request.args) > 0:
        try:
            page = int(request.args(0) or 0)
            if page < 0:
                page = 0
        except (ValueError, TypeError):
            page = 0
    else:
        page=0
        
    # db.sm_level.level_id.readable  = True
    form =SQLFORM(db.sm_level,
        fields=['level_name'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=territory_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_level.cid == session.cid) & (db.sm_level.depth == '0')
    
    if (territory_id):
        qset &= (db.sm_level.level0 == territory_id)
    
    if (session.btn_filter and session.search_type=='TerritoryID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_level.level0 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_level.ALL,orderby=[~db.sm_level.level_id,db.sm_level.level_name])
    # return str(db._lastsql)
    totalCount=db(qset).count() 
    return locals()

def town():
    
    div_topbar = True
    div_sidebar = True
    div_login_template = False
    
    visited_controller = request.controller
    visited_function = request.function
    reqPage=len(request.args)
    page = 0
    
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL(c='auth', f='login'))
        
    # =============================== Middleware
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Town'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    territory_id=request.vars.territory_id if request.vars.territory_id else ''
    town_id=request.vars.town_id if request.vars.town_id else ''
    
    
    session.search_type=search_type
    session.search_value=search_value if search_value is not None else ''
    session.btn_filter=btn_filter
    session.btn_all=btn_all
    session.btn_download=btn_download
    
    if btn_filter:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
    if btn_download:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
        redirect(URL(c='level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value,
            territory_id=territory_id,
            town_id=town_id
        )))
    if btn_all:
        session.btn_filter=None
        session.btn_all=None
        session.btn_download=None
        session.search_type=None
        session.search_value=''
        reqPage=0
    
    if len(request.args) > 0:
        try:
            page = int(request.args(0) or 0)
            if page < 0:
                page = 0
        except (ValueError, TypeError):
            page = 0
    else:
        page=0
        
    # db.sm_level.level_id.readable  = True
    form =SQLFORM(db.sm_level,
        fields=['level_name'],
        submit_button='Save'
    )
    form.vars.level0 = territory_id
    
    if form.accepts(request.vars,session,onvalidation=town_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_level.cid == session.cid) & (db.sm_level.depth == '1')
    
    if (territory_id):
        qset &= (db.sm_level.level0 == territory_id)
        
    if (town_id):
        qset &= (db.sm_level.level1 == town_id)
    
    if (session.btn_filter and session.search_type=='TownID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_level.level1 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_level.ALL,orderby=[~db.sm_level.level_id,db.sm_level.level_name])
    # return str(db._lastsql)
    totalCount=db(qset).count() 
    return locals()

def route():
    
    div_topbar = True
    div_sidebar = True
    div_login_template = False
    
    visited_controller = request.controller
    visited_function = request.function
    reqPage=len(request.args)
    page = 0
    
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL(c='auth', f='login'))
        
    # =============================== Middleware
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Route'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    territory_id=request.vars.territory_id if request.vars.territory_id else ''
    town_id=request.vars.town_id if request.vars.town_id else ''
    route_id=request.vars.route_id if request.vars.route_id else ''
    
    
    session.search_type=search_type
    session.search_value=search_value if search_value is not None else ''
    session.btn_filter=btn_filter
    session.btn_all=btn_all
    session.btn_download=btn_download
    
    if btn_filter:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
    if btn_download:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
        redirect(URL(c='level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value,
            territory_id=territory_id,
            town_id=town_id,
            route_id=route_id
        )))
    if btn_all:
        session.btn_filter=None
        session.btn_all=None
        session.btn_download=None
        session.search_type=None
        session.search_value=''
        reqPage=0
    
    if len(request.args) > 0:
        try:
            page = int(request.args(0) or 0)
            if page < 0:
                page = 0
        except (ValueError, TypeError):
            page = 0
    else:
        page=0
        
    # db.sm_level.level_id.readable  = True
    form =SQLFORM(db.sm_level,
        fields=['level_name'],
        submit_button='Save'
    )
    # form.vars.level0 = national_id
    form.vars.level1 = town_id
    
    if form.accepts(request.vars,session,onvalidation=route_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_level.cid == session.cid) & (db.sm_level.depth == '2')
    
    if (territory_id):
        qset &= (db.sm_level.level0 == territory_id)
        
    if (town_id):
        qset &= (db.sm_level.level1 == town_id)
    
    if (session.btn_filter and session.search_type=='RouteID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_level.level2 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_level.ALL,orderby=[~db.sm_level.level_id,db.sm_level.level_name])
    totalCount=db(qset).count() 
    return locals()

def beat():
    
    div_topbar = True
    div_sidebar = True
    div_login_template = False
    
    visited_controller = request.controller
    visited_function = request.function
    reqPage=len(request.args)
    page = 0
    
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL(c='auth', f='login'))
        
    # =============================== Middleware
    task_id='rm_workingarea_manage'
    task_id_view='rm_workingarea_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Beat'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    territory_id=request.vars.territory_id if request.vars.territory_id else ''
    town_id=request.vars.town_id if request.vars.town_id else ''
    route_id=request.vars.route_id if request.vars.route_id else ''
    
    # return str(national_id)+str(area_id)+str(zone_id)
    
    
    session.search_type=search_type
    session.search_value=search_value if search_value is not None else ''
    session.btn_filter=btn_filter
    session.btn_all=btn_all
    session.btn_download=btn_download
    
    if btn_filter:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
    if btn_download:
        session.btn_filter=btn_filter
        session.btn_all=btn_all
        session.btn_download=btn_download
        session.search_type=search_type
        session.search_value=search_value
        reqPage=0
        redirect(URL(c='level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value,
            territory_id=territory_id,
            town_id=town_id,
            route_id=route_id
        )))
    if btn_all:
        session.btn_filter=None
        session.btn_all=None
        session.btn_download=None
        session.search_type=None
        session.search_value=''
        reqPage=0
    
    if len(request.args) > 0:
        try:
            page = int(request.args(0) or 0)
            if page < 0:
                page = 0
        except (ValueError, TypeError):
            page = 0
    else:
        page=0
    
    form =SQLFORM(db.sm_level,
        fields=['level_name'],
        submit_button='Save'
    )
    # form.vars.level0 = national_id
    # form.vars.level1 = area_id
    form.vars.level2 = route_id
    
    if form.accepts(request.vars,session,onvalidation=beat_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_level.cid == session.cid) & (db.sm_level.depth == '3')
    
    if (territory_id):
        qset &= (db.sm_level.level0 == territory_id)
        
    if (town_id):
        qset &= (db.sm_level.level1 == town_id)
        
    if (route_id):
        qset &= (db.sm_level.level2 == route_id)
    
    if (session.btn_filter and session.search_type=='BeatID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_level.level3 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_level.ALL,orderby=[~db.sm_level.level_id,db.sm_level.level_name])
    # return str(db._lastsql)
    totalCount=db(qset).count() 
    return locals()

def download_excel():
    response.title = 'Level'
    wb = Workbook()
    ws = wb.active
    ws.title = response.title

    # Get filters
    depth=str(request.vars.depth)
    btn_download=str(request.vars.btn_download)
    search_type=str(request.vars.search_type)
    search_value=str(request.vars.search_value)
    territory_id=request.vars.territory_id if request.vars.territory_id else ''
    town_id=request.vars.town_id if request.vars.town_id else ''
    route_id=request.vars.route_id if request.vars.route_id else ''

    # Query
    qset = (db.sm_level.cid == session.cid)
    
    if (territory_id):
        qset &= (db.sm_level.level0 == territory_id)
        
    if (town_id):
        qset &= (db.sm_level.level1 == town_id)
        
    if (route_id):
        qset &= (db.sm_level.level2 == route_id)
    
    if btn_download and search_type == 'TerritoryID':
        searchValue = str(search_value).split('|')[0].strip()
        qset &= (db.sm_level.level0 == searchValue.upper())
        
    if btn_download and search_type == 'TownID':
        searchValue = str(search_value).split('|')[0].strip()
        qset &= (db.sm_level.level1 == searchValue.upper())
    
    if btn_download and search_type == 'RouteID':
        searchValue = str(search_value).split('|')[0].strip()
        qset &= (db.sm_level.level2 == searchValue.upper())
        
    if btn_download and search_type == 'BeatID':
        searchValue = str(search_value).split('|')[0].strip()
        qset &= (db.sm_level.level3 == searchValue.upper())
        
    records = db(qset).select(
        db.sm_level.level_id,
        db.sm_level.level_name,
        db.sm_level.level0,
        db.sm_level.level0_name,
        db.sm_level.level1,
        db.sm_level.level1_name,
        db.sm_level.level2,
        db.sm_level.level2_name,
        db.sm_level.level3,
        db.sm_level.level3_name,
        db.sm_level.depth,
        db.sm_level.updated_on,
        db.sm_level.updated_by,
        orderby=[db.sm_level.level0,db.sm_level.level1,db.sm_level.level2,db.sm_level.level3]
    )
    
    # return session.btn_filter
    # return str(db._lastsql)
    alias_map = {
        'level0': 'Territory Code',
        'level0_name': 'Territory Name',
        'level1': 'Town Code',
        'level1_name': 'Town Name',
        'level2': 'Route Code',
        'level2_name': 'Route Name',
        'level3': 'Beat Code',
        'level3_name': 'Beat Name',
        'updated_by': 'Updated By',
        'updated_on': 'Updated On'
    }
    
    ws.append([
        alias_map['level0'], 
        alias_map['level0_name'],
        alias_map['level1'], 
        alias_map['level1_name'],
        alias_map['level2'], 
        alias_map['level2_name'],
        alias_map['level3'], 
        alias_map['level3_name'],
        alias_map['updated_by'],
        alias_map['updated_on'] 
    ])
    
    for row in records:
        
        updated_on_str = row.updated_on.strftime('%Y-%m-%d %H:%M:%S') if row.updated_on else ''
        # if depth == "1":
        #     row.level1 = row.level_id
        #     row.level1_name = row.level_name
        # if depth == "2":
        #     row.level2 = row.level_id
        #     row.level2_name = row.level_name
            
        ws.append([
            row.level0, 
            row.level0_name,
            row.level1, 
            row.level1_name,
            row.level2, 
            row.level2_name,
            row.level3, 
            row.level3_name,
            row.updated_by,
            updated_on_str
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = 'level.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=''
    
    return output.read()

