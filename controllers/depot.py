def store_validation(form):
    depot = str(form.vars.depot_id).strip() if form.vars.depot_id else ''        
    store_name = check_special_char(form.vars.store_name) if form.vars.store_name else ''
    
    if not depot:
        form.errors.depot_id='Distributor can not be empty'
    if not store_name:
        form.errors.depot_id='Distributor can not be empty'
        
    if store_name == 'Commercial':
        store_id = depot.split('|')[0].strip()+'140'
    else:
        store_id = depot.split('|')[0].strip()+'170'
        
    record=db(
        (db.sm_depot_store.cid==session.cid) & 
        (db.sm_depot_store.store_id==store_id)
    ).select(
        db.sm_depot_store.ALL,
        orderby=~db.sm_depot_store.id,
    )
    
    if record:
        form.errors.store_name='Store already exists'
        
    form.vars.cid = session.cid
    form.vars.depot_id = depot.split('|')[0].strip()
    form.vars.store_id = store_id
    form.vars.field1 = depot.split('|')[1].strip()
    form.vars.store_name = store_name
    form.vars.note = 'ACTIVE'
    

def branch_validation(form):
    name = check_special_char(form.vars.name) if form.vars.name else ''        
    name_bn = check_special_char(form.vars.name_bn) if form.vars.name_bn else ''         
    form.vars.cid = session.cid
    form.vars.name = name.upper()
    form.vars.name_bn = name_bn

def branch():
    
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
    task_id='rm_depot_manage'
    task_id_view='rm_depot_manage_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Branch'
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
        redirect(URL(c='depot', f='download_bra_excel',vars=dict(
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
        
    db.sm_sup_depot.status.requires=IS_IN_SET(('ACTIVE','INACTIVE'))
    db.sm_sup_depot.status.default='ACTIVE'
    form =SQLFORM(db.sm_sup_depot,
        fields=['sup_depot_id','name','name_bn','status'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=branch_validation):
        session.flash = 'Data inserted successfully!'
        
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_sup_depot.cid==session.cid)
    )
    
    if (session.btn_filter and session.search_type=='BranchID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_sup_depot.sup_depot_id == searchParams[0].strip().upper())
    if (session.btn_filter and session.search_type=='Status'):
        searchParams=str(session.search_value).strip()       
        qset=qset(db.sm_sup_depot.status == searchParams.upper())
    
    # return db._lastsql
    records=qset.select(db.sm_sup_depot.ALL,orderby=[~db.sm_sup_depot.id,db.sm_sup_depot.sup_depot_id,db.sm_sup_depot.name],limitby=limitby)
    totalCount=qset.count() 
    return locals()

def download_bra_excel():
    response.title = 'Branch'
    wb = Workbook()
    ws = wb.active
    ws.title = response.title

    # Get filters
    btn_download=str(request.vars.btn_download)
    search_type=str(request.vars.search_type)
    search_value=str(request.vars.search_value)

    # Query
    qset = db()
    qset = qset(
        (db.sm_sup_depot.cid == session.cid)
    )
        
    if (btn_download and search_type=='BranchID'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_sup_depot.sup_depot_id == searchParams[0].strip().upper())
        
    if (btn_download and search_type=='Status'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_sup_depot.status == searchParams[0].strip().upper())
        
    records = qset.select(
        db.sm_sup_depot.ALL,
        orderby=[db.sm_sup_depot.sup_depot_id]
    )
    
    # return session.btn_filter
    # return response.json(records)
    
    alias_map = {
        'sup_depot_id': 'Branch Code',
        'name': 'Branch Name',
        'status': 'Status',
        'updated_by': 'Updated By',
        'updated_on': 'Updated On'
    }
    
    ws.append([
        alias_map['sup_depot_id'], 
        alias_map['name'], 
        alias_map['status'], 
        alias_map['updated_by'],
        alias_map['updated_on'] 
    ])
    
    for row in records:
        
        updated_on_str = row.updated_on.strftime('%Y-%m-%d %H:%M:%S') if row.updated_on else ''
        # expiary_date_str = row.expiary_date.strftime('%Y-%m-%d') if row.expiary_date else ''
        # if depth == "1":
        #     row.level1 = row.level_id
        #     row.level1_name = row.level_name
        # if depth == "2":
        #     row.level2 = row.level_id
        #     row.level2_name = row.level_name
            
        ws.append([
            row.sup_depot_id,
            row.name,
            row.status,
            row.updated_by,
            updated_on_str
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = 'branch.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=''
    
    return output.read()

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
    task_id='rm_depot_manage'
    task_id_view='rm_depot_manage_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Distributor'
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
        redirect(URL(c='depot', f='download_excel',vars=dict(
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
        
    db.sm_depot.status.requires=IS_IN_SET(('ACTIVE','INACTIVE'))
    db.sm_depot.status.default='ACTIVE'
    form =SQLFORM(db.sm_depot,
        fields=['depot_id','name','name_bn','status'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=branch_validation):
        session.flash = 'Data inserted successfully!'
        
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_depot.cid==session.cid)
    )
    
    if (session.btn_filter and session.search_type=='DepotID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_depot.depot_id == searchParams[0].strip().upper())
        
    if (session.btn_filter and session.search_type=='TownID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_depot.town_id == searchParams[0].strip().upper())
        
    if (session.btn_filter and session.search_type=='OperateBy'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_depot.approval_flag == searchParams[0].strip().upper())
        
    if (session.btn_filter and session.search_type=='OperateFlag'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_depot.auto_del_cron_flag == searchParams[0].strip().upper())
        
    if (session.btn_filter and session.search_type=='Status'):
        searchParams=str(session.search_value).strip()       
        qset=qset(db.sm_depot.status == searchParams.upper())
    
    # return db._lastsql
    records=qset.select(db.sm_depot.ALL,orderby=[~db.sm_depot.id,db.sm_depot.depot_id,db.sm_depot.name],limitby=limitby)
    totalCount=qset.count() 
    return locals()

def download_excel():
    response.title = 'Distributor'
    wb = Workbook()
    ws = wb.active
    ws.title = response.title

    # Get filters
    btn_download=str(request.vars.btn_download)
    search_type=str(request.vars.search_type)
    search_value=str(request.vars.search_value)

    # Query
    qset = db()
    qset = qset(
        (db.sm_depot.cid == session.cid)
    )
        
    if (btn_download and search_type=='TownID'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_depot.town_id == searchParams[0].strip().upper())
        
    if (btn_download and search_type=='DepotID'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_depot.depot_id == searchParams[0].strip().upper())
        
    if (btn_download and search_type=='OperateBy'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_depot.approval_flag == searchParams[0].strip().upper())
        
    if (btn_download and search_type=='OperateFlag'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_depot.auto_del_cron_flag == searchParams[0].strip().upper())
        
    if (btn_download and search_type=='Status'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_depot.status == searchParams[0].strip().upper())
        
    records = qset.select(
        db.sm_depot.ALL,
        orderby=[db.sm_depot.depot_id]
    )
    
    # return session.btn_filter
    # return response.json(records)
    
    alias_map = {
        'town_id' : 'Town Code',
        'town_name' : 'Town Name',
        'depot_id': 'Distributor Code',
        'name': 'Distributor Name',
        'contact' : 'Contact No',
        'status': 'Status',
        'updated_by': 'Updated By',
        'updated_on': 'Updated On'
    }
    
    ws.append([
        alias_map['town_id'], 
        alias_map['town_name'], 
        alias_map['depot_id'], 
        alias_map['name'], 
        alias_map['contact'], 
        alias_map['status'], 
        alias_map['updated_by'],
        alias_map['updated_on'] 
    ])
    
    for row in records:
        
        updated_on_str = row.updated_on.strftime('%Y-%m-%d %H:%M:%S') if row.updated_on else ''
        # expiary_date_str = row.expiary_date.strftime('%Y-%m-%d') if row.expiary_date else ''
        # if depth == "1":
        #     row.level1 = row.level_id
        #     row.level1_name = row.level_name
        # if depth == "2":
        #     row.level2 = row.level_id
        #     row.level2_name = row.level_name
            
        ws.append([
            row.town_id,
            row.town_name,
            row.depot_id,
            row.name,
            row.contact,
            row.status,
            row.updated_by,
            updated_on_str
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = 'distributor.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=''
    
    return output.read()

def store():
    
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
    task_id='rm_depot_manage'
    task_id_view='rm_depot_manage_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Distributor Store'
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
        redirect(URL(c='depot', f='download_store_excel',vars=dict(
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
        
    db.sm_depot_store.store_type.requires=IS_IN_SET(('SALES','OTHERS'))
    db.sm_depot_store.store_name.requires=IS_IN_SET(('Commercial','Damage'))

    form =SQLFORM(db.sm_depot_store,
        fields=['depot_id','store_name','store_type'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=store_validation):
        session.flash = 'Data inserted successfully!'
        
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_depot_store.cid==session.cid)
    )
    
    if (session.btn_filter and session.search_type=='DepotID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_depot_store.depot_id == searchParams[0].strip().upper())
    if (session.btn_filter and session.search_type=='StoreType'):
        searchParams=str(session.search_value).strip()       
        qset=qset(db.sm_depot_store.store_type == searchParams.upper())
    
    # return db._lastsql
    records=qset.select(db.sm_depot_store.ALL,orderby=[~db.sm_depot_store.id,db.sm_depot_store.depot_id,db.sm_depot_store.store_id],limitby=limitby)
    totalCount=qset.count() 
    return locals()

def download_store_excel():
    response.title = 'Distributor Store'
    wb = Workbook()
    ws = wb.active
    ws.title = response.title

    # Get filters
    btn_download=str(request.vars.btn_download)
    search_type=str(request.vars.search_type)
    search_value=str(request.vars.search_value)

    # Query
    qset = db()
    qset = qset(
        (db.sm_depot_store.cid == session.cid)
    )
        
    if (btn_download and search_type=='DepotID'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_depot_store.depot_id == searchParams[0].strip().upper())
        
    if (btn_download and search_type=='StoreType'):
        searchParams=str(session.search_value).strip()       
        qset=qset(db.sm_depot_store.store_type == searchParams.upper())
        
    records = qset.select(
        db.sm_depot_store.ALL,
        orderby=[db.sm_depot_store.depot_id]
    )
    
    # return session.btn_filter
    # return response.json(records)
    
    alias_map = {
        'depot_id': 'Depot Code',
        'field1': 'Depot Name',
        'store_id': 'Store Code',
        'store_name': 'Store Name',
        'store_type': 'Store Type',
        'note': 'Status',
        'updated_by': 'Updated By',
        'updated_on': 'Updated On'
    }
    
    ws.append([
        alias_map['depot_id'], 
        alias_map['field1'], 
        alias_map['store_id'],
        alias_map['store_name'],
        alias_map['store_type'],
        alias_map['note'], 
        alias_map['updated_by'],
        alias_map['updated_on'] 
    ])
    
    for row in records:
        
        updated_on_str = row.updated_on.strftime('%Y-%m-%d %H:%M:%S') if row.updated_on else ''
        # expiary_date_str = row.expiary_date.strftime('%Y-%m-%d') if row.expiary_date else ''
        # if depth == "1":
        #     row.level1 = row.level_id
        #     row.level1_name = row.level_name
        # if depth == "2":
        #     row.level2 = row.level_id
        #     row.level2_name = row.level_name
            
        ws.append([
            row.depot_id,
            row.field1,
            row.store_id,
            row.store_name,
            row.store_type,
            row.note,
            row.updated_by,
            updated_on_str
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = 'store.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=''
    
    return output.read()
