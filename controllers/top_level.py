def top_level_code_incr(input_str):
    prefix, numeric_part = input_str[:-2], input_str[-2:]
    incremented_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
    result_str = prefix + incremented_numeric_part
    return result_str

def top_level_2_code_incr(input_str):
    prefix, numeric_part = input_str[:-2], input_str[-2:]
    incremented_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
    result_str = prefix + incremented_numeric_part
    return result_str

def national_validation(form):
    level_name = (form.vars.level_name or '').strip()
    level_id = ''
    if not level_name:
        form.errors.level_name='National name can not be empty'
        
    record=db(
        (db.sm_top_level.cid==session.cid) & 
        (db.sm_top_level.depth=='0') &
        (db.sm_top_level.level0 !='ITHOS')
    ).select(
        db.sm_top_level.ALL,
        orderby=~db.sm_top_level.id,
    ).first()
    
    if record:
        level_id = top_level_code_incr(record.level_id)
        form.vars.cid = session.cid
        form.vars.level_id = level_id.upper()
        form.vars.level_name = level_name.upper()
        form.vars.level0 = level_id.upper()
        form.vars.level0_name = level_name.upper()
        form.vars.parent_level_id = '0'
        form.vars.parent_level_name = ''
        form.vars.depth = '0'
        form.vars.is_leaf = '0'
        
def area_validation(form):
    level_name = (form.vars.level_name or '').strip()
    level0     = (form.vars.level0 or '').strip()
    level_id = ''
    
    if not level0:
        form.errors.level_name='National name can not be empty'
    
    if not level_name:
        form.errors.level_name='National name can not be empty'
        
    records=db(
        (db.sm_top_level.cid==session.cid) & 
        (db.sm_top_level.depth=='1') &
        (db.sm_top_level.level1 !='ITAREA')
    ).select(
        db.sm_top_level.ALL,
        orderby=~db.sm_top_level.id,
    )
    
    record = max((r for r in records if r.level0 == level0),key=lambda r: r.id,default=None)
    
    if record:
        level_id = top_level_2_code_incr(record.level_id)
        form.vars.cid = session.cid
        form.vars.level_id = level_id.upper()
        form.vars.level_name = level_name.upper()
        form.vars.level0_name = record.level0_name.upper()
        form.vars.parent_level_id = record.level0.upper()
        form.vars.parent_level_name = record.level0_name.upper()
        form.vars.level1 = level_id.upper()
        form.vars.level1_name = level_name.upper()
        form.vars.depth = '1'
        form.vars.is_leaf = '0'
    else:
        form.errors.level_name='Demo Field'
        
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
    
    response.title='National'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    
    
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
        redirect(URL(c='top_level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value
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
        
    # db.sm_top_level.level_id.readable  = True
    form =SQLFORM(db.sm_top_level,
        fields=['level_name'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=national_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_top_level.cid == session.cid) & (db.sm_top_level.depth == '0')
    
    if (session.btn_filter and session.search_type=='NationalID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_top_level.level0 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_top_level.ALL,orderby=[db.sm_top_level.level_id,db.sm_top_level.level_name])
    # return str(db._lastsql)
    totalCount=db(qset).count() 
    return locals()

def area():
    
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
    
    response.title='Area'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    national_id=request.vars.national_id if request.vars.national_id else ''
    
    
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
        redirect(URL(c='top_level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value
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
        
    # db.sm_top_level.level_id.readable  = True
    form =SQLFORM(db.sm_top_level,
        fields=['level_name'],
        submit_button='Save'
    )
    form.vars.level0 = national_id
    
    if form.accepts(request.vars,session,onvalidation=area_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_top_level.cid == session.cid) & (db.sm_top_level.depth == '1')
    
    if (national_id):
        qset &= (db.sm_top_level.level0 == national_id)
    
    if (session.btn_filter and session.search_type=='AreaID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_top_level.level1 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_top_level.ALL,orderby=[~db.sm_top_level.level_id,db.sm_top_level.level_name])
    # return str(db._lastsql)
    totalCount=db(qset).count() 
    return locals()

def zone():
    
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
    
    response.title='Zone'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    national_id=request.vars.national_id if request.vars.national_id else ''
    area_id=request.vars.area_id if request.vars.area_id else ''
    
    
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
        redirect(URL(c='top_level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value
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
        
    # db.sm_top_level.level_id.readable  = True
    form =SQLFORM(db.sm_top_level,
        fields=['level_name'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=zone_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_top_level.cid == session.cid) & (db.sm_top_level.depth == '2')
    
    if (national_id):
        qset &= (db.sm_top_level.level0 == national_id)
        
    if (area_id):
        qset &= (db.sm_top_level.level1 == area_id)
    
    if (session.btn_filter and session.search_type=='ZoneID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_top_level.level2 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_top_level.ALL,orderby=[db.sm_top_level.level_id,db.sm_top_level.level_name])
    totalCount=db(qset).count() 
    return locals()

def territory():
    
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
    national_id=request.vars.national_id if request.vars.national_id else ''
    area_id=request.vars.area_id if request.vars.area_id else ''
    zone_id=request.vars.area_id if request.vars.zone_id else ''
    
    
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
        redirect(URL(c='top_level', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value
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
        
    # db.sm_top_level.level_id.readable  = True
    form =SQLFORM(db.sm_top_level,
        fields=['level_name'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=territory_validation):
        session.flash = 'Data inserted successfully!'
        
    # items_per_page = int(session.items_per_page)
    # limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset = (db.sm_top_level.cid == session.cid) & (db.sm_top_level.depth == '2')
    
    if (national_id):
        qset &= (db.sm_top_level.level0 == national_id)
        
    if (area_id):
        qset &= (db.sm_top_level.level1 == area_id)
    
    if (session.btn_filter and session.search_type=='TerritoryID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset &= (db.sm_top_level.level3 == searchParams[0].strip().upper())
    
    records=db(qset).select(db.sm_top_level.ALL,orderby=[db.sm_top_level.level_id,db.sm_top_level.level_name])
    totalCount=db(qset).count() 
    return locals()

def download_excel():
    response.title = 'Top Level'
    wb = Workbook()
    ws = wb.active
    ws.title = response.title

    # Get filters
    depth=str(request.vars.depth)
    btn_download=str(request.vars.btn_download)
    search_type=str(request.vars.search_type)
    search_value=str(request.vars.search_value)

    # Query
    qset = (db.sm_top_level.cid == session.cid)
    
    if btn_download and search_type == 'NationalID':
        searchValue = str(search_value).split('|')[0].strip()
        qset &= (db.sm_top_level.level0 == searchValue.upper())
        
    if btn_download and search_type == 'AreaID':
        searchValue = str(search_value).split('|')[0].strip()
        qset &= (db.sm_top_level.level1 == searchValue.upper())
        
    records = db(qset).select(
        db.sm_top_level.level_id,
        db.sm_top_level.level_name,
        db.sm_top_level.level0,
        db.sm_top_level.level0_name,
        db.sm_top_level.level1,
        db.sm_top_level.level1_name,
        db.sm_top_level.level2,
        db.sm_top_level.level2_name,
        db.sm_top_level.level3,
        db.sm_top_level.level3_name,
        db.sm_top_level.depth,
        db.sm_top_level.updated_on,
        db.sm_top_level.updated_by,
        orderby=[db.sm_top_level.level0,db.sm_top_level.level1,db.sm_top_level.level2,db.sm_top_level.level3]
    )
    
    # return session.btn_filter
    # return str(db._lastsql)
    alias_map = {
        'level0': 'National Code',
        'level0_name': 'National Name',
        'level1': 'Region Code',
        'level1_name': 'Region Name',
        'level2': 'Area Code',
        'level2_name': 'Area Name',
        'level3': 'Territory Code',
        'level3_name': 'Territory Name',
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
    filename = 'top_level.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=''
    
    return output.read()

