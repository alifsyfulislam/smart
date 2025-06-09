
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def brand_code_incr(input_str):
    prefix, numeric_part = input_str[:-2], input_str[-2:]
    incremented_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
    result_str = prefix + incremented_numeric_part
    return result_str

def dynamic_code_incr(input_str):
    prefix, numeric_part = input_str[:-2], input_str[-2:]
    incremented_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
    result_str = prefix + incremented_numeric_part
    return result_str


def validate_brand_form(vars):
    errors = []
    if not vars.level_name:
        errors.append('Brand name is required.')
    if 'image_path' not in vars or vars.image_path is None:
        errors.append('Brand logo is required.')
    else:
        image = vars.image_path
        if not hasattr(image, 'filename') or not image.filename:
            errors.append('Brand logo is required.')
        else:
            ext = image.filename.lower()
            if not ext.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                errors.append('Only JPG, JPEG, PNG, GIF formats are allowed.')
    return errors


def add():
    div_topbar = True
    div_sidebar = True
    div_login_template = False
    
    visited_controller = request.controller
    visited_function = request.function
    
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
    
    response.title='Brand'
    btn_save=request.vars.btn_save
    errors = []
    
    
    if btn_save:
        vars = request.vars
        cid = session.cid
        errors = validate_brand_form(vars)
        
        if not errors:
            c_record = db(
                (db.sm_product_hierarchy.cid == cid) &
                (db.sm_product_hierarchy.depth == '0')
            ).select(
                db.sm_product_hierarchy.level_id,
                db.sm_product_hierarchy.level_name,
                orderby=db.sm_product_hierarchy.id
            ).first()
            company_id = c_record.level_id if c_record else 'MG01'
            company_name = c_record.level_name if c_record else 'TCPL Products'
            
            b_record = db(
                (db.sm_product_hierarchy.cid == cid) &
                (db.sm_product_hierarchy.level0 == company_id) &
                (db.sm_product_hierarchy.depth == '1')
            ).select(orderby=~db.sm_product_hierarchy.id).first()

            level_id = brand_code_incr(b_record.level_id) if b_record else 'BG01'
            is_leaf = b_record.is_leaf if b_record else '0'
            depth = b_record.depth if b_record else '1'
            image_file = vars.image_path
            image_filename = db.sm_product_hierarchy.image_path.store(image_file.file, image_file.filename)

            db.sm_product_hierarchy.insert(
                cid=cid,
                level_id=level_id,
                level_name=check_special_char(vars.level_name),
                parent_level_id=company_id,
                parent_level_name=company_name,
                level0=company_id,
                level0_name=company_name,
                level1=level_id,
                level1_name=check_special_char(vars.level_name),
                is_leaf=is_leaf,
                depth=depth,
                image_path=image_filename
            )
            session.message = 'Data inserted successfully!'
            redirect(URL('brand', 'index'))
        else:
            session.flash = errors
            redirect(URL('brand', 'add'))
    return locals()

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
    
    response.title='Brand'
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
        redirect(URL(c='brand', f='download_excel',vars=dict(
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
        (db.sm_product_hierarchy.cid==session.cid)&
        (db.sm_product_hierarchy.depth=='1')&
        (db.sm_product_hierarchy.is_leaf=='0')
    )
    
    if (session.btn_filter and session.search_type=='BrandID'):
        searchValue=str(session.search_value).split('|')[0]        
        qset=qset(db.sm_product_hierarchy.level_id==searchValue.upper())
    
    records=qset.select(db.sm_product_hierarchy.ALL,orderby=[~db.sm_product_hierarchy.level_id,db.sm_product_hierarchy.level_name],limitby=limitby)
    totalCount=qset.count() 
    return locals()

def validation_brand_type(form):
    level_name = form.vars.level_name
    if level_name == '' or level_name == None:
        form.errors.level_name='Flavor name can not be empty'
    form.vars.is_leaf=0
    form.vars.depth=2
    form.vars.level_name = check_special_char(level_name) if level_name else ''
    form.vars.level2_name = check_special_char(level_name) if level_name else ''

def brand_type():
    
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
    response.title='Type'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    
    company_id=request.vars.company_id
    company_name=request.vars.company_name
    brand_id=request.vars.brand_id
    brand_name=request.vars.brand_name
    
    if company_id == '' or brand_id == '':
        redirect(URL(c='brand',f='index'))
    
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
        redirect(URL(c='brand', f='download_excel',vars=dict(
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
        
    
        
    type_records = db(
        (db.sm_product_hierarchy.cid == session.cid) & 
        (db.sm_product_hierarchy.depth=='2')
    ).select(
        db.sm_product_hierarchy.level_id,
        orderby=~db.sm_product_hierarchy.id
    )
    
    if type_records:
        max_cg_number = max(int(re.search(r'\d+', item['level_id']).group()) for item in type_records if item['level_id'].startswith('CG'))
        new_cg_number = str(max_cg_number + 1).zfill(2)
        new_level_id = f"CG{new_cg_number}"
    # ===================== Form 
    form = SQLFORM(db.sm_product_hierarchy,
        fields=[ 'level_name'],
        submit_button='Save'
    )

    form.vars.cid = session.cid
    form.vars.level0 = company_id
    form.vars.level0_name = company_name
    form.vars.level1 = brand_id
    form.vars.level1_name = brand_name
    form.vars.parent_level_id = brand_id
    form.vars.parent_level_name = brand_name
    form.vars.level_id = new_level_id
    form.vars.level2 = new_level_id
    
    
    if form.accepts(request.vars, session, onvalidation=validation_brand_type):
        session.flash = 'Data inserted successfully!'
        redirect(URL(c='brand',f='brand_type',vars=dict(company_id=company_id,company_name=company_name,brand_id=brand_id,brand_name=brand_name)))
    # ===================== Form 
    
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_product_hierarchy.cid==session.cid) &
        (db.sm_product_hierarchy.depth=='2') &
        (db.sm_product_hierarchy.is_leaf=='0')
    )
    
    if brand_id:
        qset = qset(db.sm_product_hierarchy.level1 == brand_id)
    
    if (session.btn_filter and session.search_type=='TypeID'):
        searchValue=str(session.search_value).split('|')[0]        
        qset=qset(db.sm_product_hierarchy.level_id==searchValue.upper())
    
    records=qset.select(db.sm_product_hierarchy.ALL,orderby=[~db.sm_product_hierarchy.level_id,db.sm_product_hierarchy.level_name],limitby=limitby)
    totalCount=qset.count() 
    
    return locals()

def validation_brand_type_flavor(form):
    level_name = form.vars.level_name
    if level_name == '' or level_name == None:
        form.errors.level_name='Flavor name can not be empty'
    form.vars.is_leaf=1
    form.vars.depth=3
    form.vars.level_name = check_special_char(level_name) if level_name else ''
    form.vars.level3_name = check_special_char(level_name) if level_name else ''
    

def brand_type_flavor():
    
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
    response.title='Flavor'
    search_type = request.vars.search_type if request.vars.search_type else session.search_type
    search_value = request.vars.search_value if request.vars.search_value else session.search_value
    btn_filter=request.vars.btn_filter if request.vars.btn_filter else session.btn_filter
    btn_all=request.vars.btn_all if request.vars.btn_all else session.btn_all
    btn_download=request.vars.btn_download if request.vars.btn_download else session.btn_download
    
    company_id=request.vars.company_id
    company_name=request.vars.company_name
    brand_id=request.vars.brand_id
    brand_name=request.vars.brand_name
    type_id=request.vars.type_id
    type_name=request.vars.type_name
    
    if company_id == '' or brand_id == '' or type_id == '':
        redirect(URL(c='brand',f='index'))
    
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
        redirect(URL(c='brand', f='download_excel',vars=dict(
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
        
    
        
    flavor_records = db(
        (db.sm_product_hierarchy.cid == session.cid) & 
        (db.sm_product_hierarchy.depth=='3')
    ).select(
        db.sm_product_hierarchy.level_id,
        orderby=~db.sm_product_hierarchy.id
    )
    
    if flavor_records:
        max_fg_number = max(int(re.search(r'\d+', item['level_id']).group()) for item in flavor_records if item['level_id'].startswith('FG'))
        new_fg_number = str(max_fg_number + 1).zfill(2)
        new_level_id = f"FG{new_fg_number}"
    # ===================== Form 
    form = SQLFORM(db.sm_product_hierarchy,
        fields=[ 'level_name'],
        submit_button='Save'
    )

    form.vars.cid = session.cid
    form.vars.level0 = company_id
    form.vars.level0_name = company_name
    form.vars.level1 = brand_id
    form.vars.level1_name = brand_name
    form.vars.level2 = type_id
    form.vars.level2_name = type_name
    form.vars.parent_level_id = type_id
    form.vars.parent_level_name = type_name
    form.vars.level_id = new_level_id
    form.vars.level3 = new_level_id
    
    
    if form.accepts(request.vars, session, onvalidation=validation_brand_type_flavor):
        session.flash = 'Data inserted successfully!'
        redirect(URL(c='brand',f='brand_type_flavor',vars=dict(company_id=company_id,company_name=company_name,brand_id=brand_id,brand_name=brand_name, type_id=type_id, type_name=type_name)))
    # ===================== Form 
    
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_product_hierarchy.cid==session.cid) &
        (db.sm_product_hierarchy.depth=='3') &
        (db.sm_product_hierarchy.is_leaf=='1')
    )
    
    if brand_id and type_id:
        qset = qset(
            (db.sm_product_hierarchy.level1==brand_id) &
            (db.sm_product_hierarchy.level2==type_id)
        )
    
    if (session.btn_filter and session.search_type=='FlavorID'):
        searchValue=str(session.search_value).split('|')[0]        
        qset=qset(db.sm_product_hierarchy.level_id==searchValue.upper())
    
    records=qset.select(db.sm_product_hierarchy.ALL,orderby=[~db.sm_product_hierarchy.level_id,db.sm_product_hierarchy.level_name],limitby=limitby)
    totalCount=qset.count() 
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
        (db.sm_product_hierarchy.cid == session.cid)
    )
    
    if btn_download and search_type == 'BrandID':
        searchValue = str(search_value).split('|')[0].strip()
        qset = qset(db.sm_product_hierarchy.level1 == searchValue.upper())
    if btn_download and search_type == 'TypeID':
        searchValue = str(search_value).split('|')[0].strip()
        qset = qset(db.sm_product_hierarchy.level2 == searchValue.upper())
        
    records = qset.select(
        db.sm_product_hierarchy.level_id,
        db.sm_product_hierarchy.level_name,
        db.sm_product_hierarchy.level0,
        db.sm_product_hierarchy.level0_name,
        db.sm_product_hierarchy.level1,
        db.sm_product_hierarchy.level1_name,
        db.sm_product_hierarchy.level2,
        db.sm_product_hierarchy.level2_name,
        db.sm_product_hierarchy.level3,
        db.sm_product_hierarchy.level3_name,
        db.sm_product_hierarchy.depth,
        db.sm_product_hierarchy.updated_on,
        db.sm_product_hierarchy.updated_by,
        orderby=[db.sm_product_hierarchy.level0,db.sm_product_hierarchy.level1,db.sm_product_hierarchy.level2,db.sm_product_hierarchy.level3]
    )
    
    # return session.btn_filter
    # return db._lastsql
    alias_map = {
        'level0': 'Company Code',
        'level0_name': 'Company Name',
        'level1': 'Brand Code',
        'level1_name': 'Brand Name',
        'level2': 'Type Code',
        'level2_name': 'Type Name',
        'level3': 'Flavor Code',
        'level3_name': 'Flavor Name',
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
    filename = 'product_hierarachy.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=None
    
    return output.read()
