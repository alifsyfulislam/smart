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
    task_id='rm_item_manage'
    task_id_view='rm_item_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Item Batch'
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
        redirect(URL(c='item_batch', f='download_excel',vars=dict(
            btn_download=btn_download,
            search_type=search_type,
            search_value=search_value
        )))
    if btn_all:
        session.btn_filter=''
        session.btn_all=''
        session.btn_download=None
        session.search_type=None
        session.search_value=None
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
        
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_item_batch.cid==session.cid)
    )
    
    if (session.btn_filter and session.search_type=='ItemID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_item_batch.item_id == searchParams[0].strip().upper())
    
    # return db._lastsql
    records=qset.select(db.sm_item_batch.ALL,orderby=[~db.sm_item_batch.id,db.sm_item_batch.item_id,db.sm_item_batch.name],limitby=limitby)
    totalCount=qset.count() 
    return locals()


def download_excel():
    response.title = 'Item Batch'
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
        (db.sm_item_batch.cid == session.cid)
    )
        
    if (btn_download and search_type=='ItemID'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_item_batch.item_id == searchParams[0].strip().upper())
        
    records = qset.select(
        db.sm_item_batch.ALL,
        orderby=[db.sm_item_batch.item_id]
    )
    
    # return session.btn_filter
    # return response.json(records)
    
    alias_map = {
        'item_id': 'Item Code',
        'name': 'Item Name',
        'batch_id': 'Batch',
        'expiary_date': 'Expiary',
        'updated_by': 'Updated By',
        'updated_on': 'Updated On'
    }
    
    ws.append([
        alias_map['item_id'], 
        alias_map['name'], 
        alias_map['batch_id'], 
        alias_map['expiary_date'], 
        alias_map['updated_by'],
        alias_map['updated_on'] 
    ])
    
    for row in records:
        
        updated_on_str = row.updated_on.strftime('%Y-%m-%d %H:%M:%S') if row.updated_on else ''
        expiary_date_str = row.expiary_date.strftime('%Y-%m-%d') if row.expiary_date else ''
        # if depth == "1":
        #     row.level1 = row.level_id
        #     row.level1_name = row.level_name
        # if depth == "2":
        #     row.level2 = row.level_id
        #     row.level2_name = row.level_name
            
        ws.append([
            row.item_id,
            row.name,
            row.batch_id,
            expiary_date_str,
            row.updated_by,
            updated_on_str
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = 'item_batch.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=None
    
    return output.read()
