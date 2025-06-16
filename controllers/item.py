def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

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
    
    response.title='Item'
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
        redirect(URL(c='item', f='download_excel',vars=dict(
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
        
    items_per_page = int(session.items_per_page)
    limitby=((page*items_per_page),(page+1)*items_per_page)
    
    qset=db()
    qset = qset(
        (db.sm_item.cid==session.cid)
    )
    
    if (session.btn_filter and session.search_type=='BrandID'):
        searchParams=str(session.search_value).strip().split('|') 
        qset=qset(db.sm_item.brand_id==searchParams[0].strip().upper())
        
    if (session.btn_filter and session.search_type=='BrandFlavor'):
        searchParams=str(session.search_value).strip().split('|')     
        qset=qset(
            (db.sm_item.brand_id == searchParams[0].strip().upper()) & 
            (db.sm_item.flavor_id == searchParams[2].strip().upper())
        )
        
    if (session.btn_filter and session.search_type=='BrandWeight'):
        searchParams=str(session.search_value).strip().split('|')  
        qset=qset(
            (db.sm_item.brand_id == searchParams[0].strip().upper()) & 
            (db.sm_item.weight == float(searchParams[2].strip().upper()))
        )
    
    if (session.btn_filter and session.search_type=='FlavorWeight'):
        searchParams=str(session.search_value).strip().split('|') 
        qset=qset(
            (db.sm_item.flavor_id == searchParams[1].strip().upper()) & 
            (db.sm_item.weight == float(searchParams[3].strip().upper()))
        )
        
    if (session.btn_filter and session.search_type=='ItemID'):
        searchParams=str(session.search_value).strip().split('|')      
        qset=qset(db.sm_item.item_id == searchParams[0].strip().upper())
        
    if (session.btn_filter and session.search_type=='ItemType'):
        searchParams=str(session.search_value).strip()     
        qset=qset(db.sm_item.item_category == searchParams.upper())
        
    if (session.btn_filter and session.search_type=='Status'):
        searchParams=str(session.search_value).strip()       
        qset=qset(db.sm_item.status == searchParams.upper())
    
    # return db._lastsql
    records=qset.select(db.sm_item.ALL,orderby=[~db.sm_item.id,db.sm_item.item_id,db.sm_item.name],limitby=limitby)
    totalCount=qset.count() 
    return locals()

def download_excel():
    response.title = 'Item'
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
        (db.sm_item.cid == session.cid)
    )
    
    if (btn_download and search_type=='BrandID'):
        searchParams=str(search_value).strip().split('|') 
        qset=qset(db.sm_item.brand_id==searchParams[0].strip().upper())
        
    if (btn_download and search_type=='BrandFlavor'):
        searchParams=str(search_value).strip().split('|')     
        qset=qset(
            (db.sm_item.brand_id == searchParams[0].strip().upper()) & 
            (db.sm_item.flavor_id == searchParams[2].strip().upper())
        )
        
    if (btn_download and search_type =='BrandWeight'):
        searchParams=str(search_value).strip().split('|')  
        qset=qset(
            (db.sm_item.brand_id == searchParams[0].strip().upper()) & 
            (db.sm_item.weight == float(searchParams[2].strip().upper()))
        )
    
    if (btn_download and search_type =='FlavorWeight'):
        searchParams=str(search_value).strip().split('|') 
        qset=qset(
            (db.sm_item.flavor_id == searchParams[1].strip().upper()) & 
            (db.sm_item.weight == float(searchParams[3].strip().upper()))
        )
        
    if (btn_download and search_type=='ItemID'):
        searchParams=str(search_value).strip().split('|')      
        qset=qset(db.sm_item.item_id == searchParams[0].strip().upper())
        
    if (btn_download and search_type =='ItemType'):
        searchParams=str(search_value).strip()     
        qset=qset(db.sm_item.item_category == searchParams.upper())
        
    if (btn_download and search_type =='Status'):
        searchParams=str(search_value).strip()       
        qset=qset(db.sm_item.status == searchParams.upper())
        
    records = qset.select(
        db.sm_item.ALL,
        orderby=[db.sm_item.item_id,db.sm_item.brand_id,db.sm_item.flavor_id,db.sm_item.weight]
    )
    
    # return session.btn_filter
    # return response.json(records)
    
    alias_map = {
        'item_category': 'Item Type',
        'item_id': 'Item Code',
        'name': 'Item Name',
        'unit_type': 'Unit',
        'pack_size': 'Pack Size',
        'weight': 'Weight',
        'item_carton': 'Item Carton',
        'item_chain': 'Item Chain',
        'total_amt': 'Item Price',
        'brand_id': 'Brand Code',
        'brand_name': 'Brand Name',
        'flavor_id': 'Flavor Code',
        'flavor_name': 'Flavor Name',
        'status': 'Status',
        'updated_by': 'Updated By',
        'updated_on': 'Updated On'
    }
    
    ws.append([
        alias_map['item_category'], 
        alias_map['item_id'], 
        alias_map['name'], 
        alias_map['unit_type'], 
        alias_map['pack_size'], 
        alias_map['weight'], 
        alias_map['item_carton'], 
        alias_map['item_chain'], 
        alias_map['total_amt'], 
        alias_map['brand_id'], 
        alias_map['brand_name'], 
        alias_map['flavor_id'], 
        alias_map['flavor_name'], 
        alias_map['status'], 
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
            row.item_category,
            row.item_id,
            row.name,
            row.unit_type,
            row.pack_size,
            row.weight,
            row.item_carton,
            row.item_chain,
            row.total_amt,
            row.brand_id,
            row.brand_name,
            row.flavor_id,
            row.flavor_name,
            row.status,
            row.updated_by,
            updated_on_str
        ])
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    filename = 'item.xlsx'
    response.headers['Content-Type'] = contenttype('.xlsx')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    session.btn_download=None
    session.search_type=None
    session.search_value=''
    
    return output.read()

def bulk_item():
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
    
    response.title='Item'
    cid = session.cid
    # type_name = 'ITEM_UNIT'
    total_row = 0
    count_inserted = 0
    count_error = 0
    error_str = ''
    btn_upload=request.vars.btn_upload
    item_info = []
    
    if btn_upload:
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        
        for i in range(total_row):
            if i>=10:
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')
            
            if len(coloum_list)!=12:
                error_data=row_data+f'(12 columns need in a row, but given {len(coloum_list)})\n'
                error_str=error_str+error_data
                count_error+=1
                continue
            else:
                item_info = {}
                item_batch_info = {}
                item_depot_stock_info  = []
                
                coloum_list[2] = check_special_char(coloum_list[2])
                
                # Parse item information from the column list
                item_info = {
                    'cid' : cid,
                    'item_category': str(coloum_list[0]).strip(),
                    'item_id': str(coloum_list[1]).strip(),
                    'name': str(coloum_list[2]).strip(),
                    'name_bn': '',
                    'unit_type': str(coloum_list[3]).strip(),
                    'pack_size': str(coloum_list[4]).strip(),
                    'weight': float(coloum_list[5] or 0),
                    'item_carton': int(coloum_list[6] or 0),
                    'ctn_pcs_ratio': int(coloum_list[6] or 0),
                    'item_chain': int(coloum_list[7] or 0),
                    'price': float(coloum_list[8] or 0),
                    'vat_amt': 0,
                    'total_amt': float(coloum_list[8] or 0),
                    'flavor_id': str(coloum_list[9]).strip(),
                    'status': str(coloum_list[11]).strip()
                }
                
                item_batch_info = {
                    'cid' : cid,
                    'item_id': str(coloum_list[1]).strip(),
                    'name': str(coloum_list[2]).strip(),
                    'batch_id' : str(coloum_list[1]).strip().replace("-", "")+'21001231',
                    'expiary_date' : '2100-12-31'
                }

                # Allowed lists
                allowed_categories = ['BONUS', 'REGULAR', 'GIFT']
                allowed_pack_sizes = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA SMALL', 'EXTRA LARGE']
                allowed_units = [u.cat_type_name for u in db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'ITEM_UNIT')).select(db.sm_category_type.cat_type_name)]
                                                            
                flavorRecords = db(
                    (db.sm_product_hierarchy.cid == 'SMART') & 
                    (db.sm_product_hierarchy.depth == 3)
                ).select(
                    db.sm_product_hierarchy.level_id.with_alias('flavor_id'),
                    db.sm_product_hierarchy.level_name.max().with_alias('flavor_name'),
                    db.sm_product_hierarchy.level0.max().with_alias('company_id'),
                    db.sm_product_hierarchy.level1.max().with_alias('brand_id'),
                    db.sm_product_hierarchy.level2.max().with_alias('type_id'),
                    db.sm_product_hierarchy.level0_name.max().with_alias('company_name'),
                    db.sm_product_hierarchy.level1_name.max().with_alias('brand_name'),
                    db.sm_product_hierarchy.level2_name.max().with_alias('type_name'),
                    groupby=db.sm_product_hierarchy.level_id
                )

                # Build allowed flavor IDs
                allowed_flavors = [f['flavor_id'] for f in flavorRecords]

                # Validation and processing
                if (item_info['item_category'] not in allowed_categories) or (item_info['item_category'] == ''):
                    error_data = row_data + '\n(Item category error)\n'
                    error_str += error_data
                    count_error += 1

                elif (item_info['item_id'] == ''):
                    error_data = row_data + '\n(Item id cannot be empty)\n'
                    error_str += error_data
                    count_error += 1

                elif db((db.sm_item.cid == cid) & (db.sm_item.item_id == item_info['item_id'])).select().first():
                    error_data = row_data + '\n(Item id already exists)\n'
                    error_str += error_data
                    count_error += 1

                elif (item_info['unit_type'] not in allowed_units) or (item_info['unit_type'] == ''):
                    error_data = row_data + '\n(Item unit error)\n'
                    error_str += error_data
                    count_error += 1

                elif (item_info['pack_size'] not in allowed_pack_sizes) or (item_info['pack_size'] == ''):
                    error_data = row_data + '\n(Item pack size error)\n'
                    error_str += error_data
                    count_error += 1

                elif (item_info['flavor_id'] not in allowed_flavors) or (item_info['flavor_id'] == ''):
                    error_data = row_data + '\n(Item flavor error)\n'
                    error_str += error_data
                    count_error += 1

                elif (item_info['status'] not in ['ACTIVE', 'INACTIVE']) or (item_info['status'] == ''):
                    error_data = row_data + '\n(Item status error)\n'
                    error_str += error_data
                    count_error += 1

                else:
                    # Find matching flavor info
                    flavor_info = next((f for f in flavorRecords if f['flavor_id'] == item_info['flavor_id']), None)
                    
                    if flavor_info:
                        item_info['flavor_name'] = flavor_info['flavor_name']
                        item_info['company_id'] = flavor_info['company_id']
                        item_info['company_name'] = flavor_info['company_name']
                        item_info['brand_id'] = flavor_info['brand_id']
                        item_info['brand_name'] = flavor_info['brand_name']
                        item_info['type_id'] = flavor_info['type_id']
                        item_info['type_name'] = flavor_info['type_name']
                        item_info['des'] = item_info['name']
                        item_info['category_id'] = flavor_info['brand_id']
                        item_info['category_name'] = flavor_info['brand_name']

                        # Insert the item
                        db.sm_item.insert(**item_info)
                        db.sm_item_batch.insert(**item_batch_info)
                        
                        depotStoreRecords = db(db.sm_depot_store.cid == cid).select(db.sm_depot_store.ALL, orderby = [db.sm_depot_store.depot_id,db.sm_depot_store.store_id])
                        
                        if depotStoreRecords:
                            for dsItem in depotStoreRecords:
                                item_depot_stock_info.append({
                                    'cid' : dsItem['cid'],
                                    'depot_id' : dsItem['depot_id'],
                                    'store_id' : dsItem['store_id'],
                                    'store_name' : dsItem['store_name'],
                                    'item_id' : item_info['item_id'],
                                    'batch_id' : item_batch_info['batch_id'],
                                    'expiary_date' : item_batch_info['expiary_date'],
                                    'quantity' : 0,
                                    'block_qty' : 0,
                                })
                            
                            CHUNK_SIZE = 500
                            for i in range(0, len(item_depot_stock_info), CHUNK_SIZE):
                                chunk = item_depot_stock_info[i:i+CHUNK_SIZE]
                                db.sm_depot_stock_balance.bulk_insert(chunk)
                                db.commit()
                        count_inserted += 1
    return locals()

def validate_item_form(vars):
    errors = []
    if not vars.item_category:
        errors.append('Category is required.')
    if not vars.item_id:
        errors.append('Code is required.')
    if not vars.name:
        errors.append('Name is required.')
    if not vars.unit_type:
        errors.append('Unit is required.')
    if not vars.pack_size:
        errors.append('Pack size is required.')
    if not vars.status:
        errors.append('Status is required.')
    if not (vars.weight and vars.item_carton and vars.item_chain and vars.price):
        errors.append('Weight or carton or chain or price is required.')
        
    # image = vars.image_path
    # if not hasattr(image, 'filename') or not image.filename:
    #     errors.append('Logo is required.')
    # else:
    #     ext = image.filename.lower()
    #     if not ext.endswith(('.jpg', '.jpeg', '.png', '.gif')):
    #         errors.append('Only JPG, JPEG, PNG, GIF formats are allowed.')
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
    
    response.title='Item'
    cid = session.cid
    btn_save=request.vars.btn_save
    errors = []
    
    
    allowed_units = [u.cat_type_name for u in db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'ITEM_UNIT')).select(db.sm_category_type.cat_type_name)]
    # return str(allowed_units)
    
    flavorRecords = db(
        (db.sm_product_hierarchy.cid == 'SMART') & 
        (db.sm_product_hierarchy.depth == 3)
    ).select(
        db.sm_product_hierarchy.level_id.with_alias('flavor_id'),
        db.sm_product_hierarchy.level_name.max().with_alias('flavor_name'),
        db.sm_product_hierarchy.level0.max().with_alias('company_id'),
        db.sm_product_hierarchy.level1.max().with_alias('brand_id'),
        db.sm_product_hierarchy.level2.max().with_alias('type_id'),
        db.sm_product_hierarchy.level0_name.max().with_alias('company_name'),
        db.sm_product_hierarchy.level1_name.max().with_alias('brand_name'),
        db.sm_product_hierarchy.level2_name.max().with_alias('type_name'),
        groupby=db.sm_product_hierarchy.level_id,
        orderby=~db.sm_product_hierarchy.level_id
    )
    allowed_flavors = [f for f in flavorRecords]
    
    if btn_save:
        vars = request.vars
        cid = session.cid
        errors = validate_item_form(vars)
        # return response.json(vars)
        if not errors:
            image_file = vars.image_path
            image_filename = None

            if image_file is not None and hasattr(image_file, 'file') and image_file.filename:
                image_filename = db.sm_item.image_path.store(image_file.file, image_file.filename)
                
            flavorRecords = next((f for f in allowed_flavors if f.flavor_id == vars.flavor_id.strip()), '')
            
            if flavorRecords:
                company_id      = flavorRecords.company_id
                company_name    = flavorRecords.company_name
                brand_id        = flavorRecords.brand_id
                brand_name      = flavorRecords.brand_name
                type_id         = flavorRecords.type_id
                type_name       = flavorRecords.type_name
                flavor_name     = flavorRecords.flavor_name
            
            new_item = dict(
                cid             = cid,
                item_id         = vars.item_id.strip(),
                name_bn         = vars.name_bn.strip(),
                item_carton     = int(vars.item_carton or 0),
                ctn_pcs_ratio   = int(vars.item_carton or 0),
                name            = vars.name.strip(),
                flavor_id       = vars.flavor_id.strip(),
                unit_type       = vars.unit_type.strip(),
                price           = float(vars.price or 0),
                total_amt       = float(vars.price or 0),
                item_chain      = int(vars.item_chain or 0),
                vat_amt         = float(vars.vat_amt or 0),
                status          = vars.status.strip(),
                item_category   = vars.item_category.strip(),
                invoice_price   = float(vars.invoice_price or 0),
                des             = vars.des.strip(),
                pack_size       = vars.pack_size.strip(),
                mrp             = float(vars.mrp or 0),
                weight          = float(vars.weight or 0),
                old_item_id     = '',
                company_id      = company_id,
                company_name    = company_name,
                brand_id        = brand_id,
                brand_name      = brand_name,
                category_id     = brand_id,
                category_name   = brand_name,
                type_id         = type_id,
                type_name       = type_name,
                flavor_name     = flavor_name
            )
            
            new_batch_item = dict(
                cid             = cid,
                item_id         = vars.item_id.strip(),
                name            = vars.name.strip(),
                batch_id        = vars.item_id.strip().replace("-", "")+'21001231',
                expiary_date    = '2100-12-31'
            )

            if image_filename:
                new_item['image_path'] = image_filename

            inserted_id = db.sm_item.insert(**new_item)
            inserted_batch_id = db.sm_item_batch.insert(**new_batch_item)
            
            item_depot_stock_info = []
            depotStoreRecords = db(db.sm_depot_store.cid == cid).select(db.sm_depot_store.ALL, orderby = [db.sm_depot_store.depot_id,db.sm_depot_store.store_id])
                        
            if depotStoreRecords:
                for dsItem in depotStoreRecords:
                    item_depot_stock_info.append({
                        'cid' : dsItem['cid'],
                        'depot_id' : dsItem['depot_id'],
                        'store_id' : dsItem['store_id'],
                        'store_name' : dsItem['store_name'],
                        'item_id' : vars.item_id.strip(),
                        'batch_id' : vars.name.strip().replace("-", "")+'21001231',
                        'expiary_date' : '2100-12-31',
                        'quantity' : 0,
                        'block_qty' : 0,
                    })
                
                CHUNK_SIZE = 500
                for i in range(0, len(item_depot_stock_info), CHUNK_SIZE):
                    chunk = item_depot_stock_info[i:i+CHUNK_SIZE]
                    db.sm_depot_stock_balance.bulk_insert(chunk)
                    db.commit()

            if inserted_id and inserted_batch_id:
                session.message = 'Item added successfully!'
                redirect(URL('item', 'index'))
            else:
                session.flash = 'Failed to add item!'
                redirect(request.env.http_referer)
        else:
            session.flash = errors
            redirect(request.env.http_referer)
    return locals()

def edit():
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
    
    
    # =============================== Valid
    rid = request.vars.rid
    rmode = request.vars.rmode
    if rid == '' or rid == None or rmode == '' or rmode == None:
        session.flash='Not Allowed without Params!'
        redirect (URL('item','index'))
    # =============================== Valid
    
    response.title='Item'
    cid = session.cid
    btn_save=request.vars.btn_save
    errors = []
    
    
    allowed_units = [u.cat_type_name for u in db((db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == 'ITEM_UNIT')).select(db.sm_category_type.cat_type_name)]
    # return str(allowed_units)
    
    flavorRecords = db(
        (db.sm_product_hierarchy.cid == 'SMART') & 
        (db.sm_product_hierarchy.depth == 3)
    ).select(
        db.sm_product_hierarchy.level_id.with_alias('flavor_id'),
        db.sm_product_hierarchy.level_name.max().with_alias('flavor_name'),
        db.sm_product_hierarchy.level0.max().with_alias('company_id'),
        db.sm_product_hierarchy.level1.max().with_alias('brand_id'),
        db.sm_product_hierarchy.level2.max().with_alias('type_id'),
        db.sm_product_hierarchy.level0_name.max().with_alias('company_name'),
        db.sm_product_hierarchy.level1_name.max().with_alias('brand_name'),
        db.sm_product_hierarchy.level2_name.max().with_alias('type_name'),
        groupby=db.sm_product_hierarchy.level_id,
        orderby=~db.sm_product_hierarchy.level_id
    )
    allowed_flavors = [f for f in flavorRecords]
    
    record = db(db.sm_item.id == rid).select().first()
    
    if btn_save:
        vars = request.vars
        cid = session.cid
        errors = validate_item_form(vars)

        if not errors:
            item_id = vars.item_id.strip()
            image_file = vars.image_path
            image_filename = None

            if image_file is not None and hasattr(image_file, 'file') and image_file.filename:
                image_filename = db.sm_item.image_path.store(image_file.file, image_file.filename)
                
            flavorRecords = next((f for f in allowed_flavors if f.flavor_id == vars.flavor_id.strip()), '')
            
            if flavorRecords:
                company_id      = flavorRecords.company_id
                company_name    = flavorRecords.company_name
                brand_id        = flavorRecords.brand_id
                brand_name      = flavorRecords.brand_name
                type_id         = flavorRecords.type_id
                type_name       = flavorRecords.type_name
                flavor_name     = flavorRecords.flavor_name
            
            update_fields = dict(
                cid             = cid,
                name_bn         = vars.name_bn.strip(),
                item_carton     = int(vars.item_carton or 0),
                ctn_pcs_ratio   = int(vars.item_carton or 0),
                name            = vars.name.strip(),
                flavor_id       = vars.flavor_id.strip(),
                unit_type       = vars.unit_type.strip(),
                price           = float(vars.price or 0),
                total_amt       = float(vars.price or 0),
                item_chain      = int(vars.item_chain or 0),
                vat_amt         = float(vars.vat_amt or 0),
                status          = vars.status.strip(),
                item_category   = vars.item_category.strip(),
                invoice_price   = float(vars.invoice_price or 0),
                des             = vars.des.strip(),
                pack_size       = vars.pack_size.strip(),
                mrp             = float(vars.mrp or 0),
                weight          = float(vars.weight or 0),
                old_item_id     = '',
                company_id      = company_id,
                company_name    = company_name,
                brand_id        = brand_id,
                brand_name      = brand_name,
                category_id     = brand_id,
                category_name   = brand_name,
                type_id         = type_id,
                type_name       = type_name,
                flavor_name     = flavor_name
            )
            
            if image_filename:
                update_fields['image_path'] = image_filename
                
            update_flag = db(
                (db.sm_item.cid == session.cid) &
                (db.sm_item.item_id == item_id)
            ).update(**update_fields)
            
            if update_flag:
                session.message = 'Data updated successfully!'
                redirect(URL('item', 'index'))
            else:
                session.flash = 'Update failed!'
                redirect(request.env.http_referer)
        else:
            session.flash = errors
            redirect(request.env.http_referer)
    return locals()

