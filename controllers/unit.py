def dynamic_code_incr(input_str):
    prefix, numeric_part = input_str[:-3], input_str[-3:]
    incremented_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
    result_str = prefix + incremented_numeric_part
    return result_str

def unit_validation(form):
    cat_type_name = form.vars.cat_type_name
    if cat_type_name == '' or cat_type_name == None:
        form.errors.cat_type_name='Unit name can not be empty'
        
    records=db(
        (db.sm_category_type.cid==session.cid) & 
        (db.sm_category_type.type_name=='ITEM_UNIT')
    ).select(
        db.sm_category_type.id,
        db.sm_category_type.type_name,
        db.sm_category_type.cat_type_id,
        db.sm_category_type.cat_type_name,
        orderby=~db.sm_category_type.id,
    )
    
    if records:
        max_un_number = max(int(re.search(r'\d+', item['cat_type_id']).group()) for item in records if item['cat_type_id'].startswith('UN'))
        new_un_number = str(max_un_number + 1).zfill(3)
        cat_type_id = f"UN{new_un_number}"
        
        for row in records:
            if row.cat_type_name == cat_type_name:
                form.errors.cat_type_name='Unit name already exists'
                
        form.vars.cid = session.cid
        form.vars.type_name = 'ITEM_UNIT'
        form.vars.cat_type_id = cat_type_id
        form.vars.cat_type_name = cat_type_name.upper()

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
    task_id='rm_item_cat_unit_manage'
    task_id_view='rm_item_cat_unit_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Unit'
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
    
    # return str(session)
    
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
        redirect(URL(c='unit', f='download_excel',vars=dict(
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
        
    db.sm_category_type.field1.requires=IS_IN_SET(('ACTIVE','INACTIVE'))
    db.sm_category_type.field1.default='ACTIVE'
    form =SQLFORM(db.sm_category_type,
        fields=['cat_type_name','field1'],
        submit_button='Save'
    )
    
    if form.accepts(request.vars,session,onvalidation=unit_validation):
        session.flash = 'Data inserted successfully!'
        
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_category_type.cid==session.cid)&
        (db.sm_category_type.type_name=='ITEM_UNIT')
    )
    
    # return str(session.btn_filter)
    if (session.btn_filter and session.search_type=='UnitID'):
        searchValue=str(session.search_value).split('|')[0]        
        qset=qset(db.sm_category_type.cat_type_id==searchValue.upper())
    
    records=qset.select(db.sm_category_type.ALL,orderby=[~db.sm_category_type.cat_type_id,db.sm_category_type.cat_type_name],limitby=limitby)
    totalCount=qset.count() 
    return locals()

def bulk_unit():
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
    task_id='rm_item_cat_unit_manage'
    task_id_view='rm_item_cat_unit_view'
    access_permission=check_role(task_id)
    access_permission_view=check_role(task_id_view)
    if (access_permission==False) and (access_permission_view==False):
        session.flash='Access is Denied !'
        redirect (URL('home','index'))
    # =============================== Middleware
    
    response.title='Unit'
    cid = session.cid
    type_name = 'ITEM_UNIT'
    total_row = 0
    count_inserted = 0
    count_error = 0
    error_str = ''
    btn_upload=request.vars.btn_upload
    valid_row = True
    
    if btn_upload:
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')
            
            if len(coloum_list)!=2:
                error_data=row_data+'\n(2 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                cat_type_name=str(coloum_list[0]).strip()
                field1=str(coloum_list[1]).strip()
                
                records_exists = db(
                    (db.sm_category_type.cid == cid) &
                    (db.sm_category_type.type_name == type_name) &
                    (db.sm_category_type.cat_type_name == cat_type_name)
                ).select(
                    db.sm_category_type.ALL,
                    orderby = [~db.sm_category_type.id],
                    limitby = (0,1)
                )
                
                if records_exists:
                    error_data=row_data+'\n(Unit name already exists)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
                else:
                    record = db(
                        (db.sm_category_type.cid == cid) &
                        (db.sm_category_type.type_name == type_name)
                    ).select(
                        db.sm_category_type.ALL,
                        orderby = [~db.sm_category_type.id],
                        limitby = (0,1)
                    ).first()
                    
                    if record:
                        cat_type_id = dynamic_code_incr(record.cat_type_id)
                    else:
                        cat_type_id = 'UN0001'
                    
                    db.sm_category_type.insert(
                        cid=cid,
                        type_name = type_name,
                        cat_type_id = cat_type_id,
                        cat_type_name = cat_type_name,
                        field1 = field1
                    )
                    count_inserted+=1
    return locals()

def download_excel():
    response.title = 'Brand'
    wb = Workbook()
    ws = wb.active
    ws.title = response.title

    # Get filters
    depth=str(request.vars.depth)
    btn_download=str(request.vars.btn_download)
    search_type=str(request.vars.search_type)
    search_value=str(request.vars.search_value)

    # Query
    qset = db()
    qset = qset(
        (db.sm_category_type.cid == session.cid) &
        (db.sm_category_type.type_name == 'ITEM_UNIT')
    )
    
    
    if btn_download and search_type == 'UnitID':
        searchValue = str(search_value).split('|')[0].strip()
        qset = qset(db.sm_category_type.cat_type_id == searchValue.upper())
        
    records = qset.select(
        db.sm_category_type.type_name,
        db.sm_category_type.cat_type_id,
        db.sm_category_type.cat_type_name,
        db.sm_category_type.field1,
        db.sm_category_type.updated_on,
        db.sm_category_type.updated_by,
        orderby=[db.sm_category_type.cat_type_id]
    )
    
    # return session.btn_filter
    # return db._lastsql
    alias_map = {
        'type_name': 'Type Name',
        'cat_type_id': 'Unit Code',
        'cat_type_name': 'Unit Name',
        'field1': 'Status',
        'updated_by': 'Updated By',
        'updated_on': 'Updated On'
    }
    
    ws.append([
        alias_map['type_name'], 
        alias_map['cat_type_id'],
        alias_map['cat_type_name'], 
        alias_map['field1'],
        alias_map['updated_by'],
        alias_map['updated_on'] 
    ])
    
    for row in records:
        updated_on_str = row.updated_on.strftime('%Y-%m-%d %H:%M:%S') if row.updated_on else ''
        ws.append([
            row.type_name, 
            row.cat_type_id,
            row.cat_type_name, 
            row.field1,
            row.updated_by,
            updated_on_str
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = 'unit.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=''
    
    return output.read()
