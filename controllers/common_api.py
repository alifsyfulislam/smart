def get_brand():
    cid = session.cid
    search = request.vars.search or ''
    
    if cid == '' or cid == None:
        return
    query = (db.sm_product_hierarchy.cid == cid) & (db.sm_product_hierarchy.depth == '1')
    if search:
        query &= (
            (db.sm_product_hierarchy.level_name.contains(search)) |
            (db.sm_product_hierarchy.level_id.contains(search))
        )
    rows = db(query).select(
        db.sm_product_hierarchy.level_id,
        db.sm_product_hierarchy.level_name,
        orderby=~db.sm_product_hierarchy.level_id
    )
    return ','.join(f"{row.level_id}|{row.level_name}" for row in rows)

def get_item():
    cid = session.cid
    parameter = request.vars.parameter or ''
    search = str(request.vars.search) or ''
    
    if cid == '' or cid == None or parameter == '' or parameter == None:
        return
    
    query = ''
    rows = ''
    data = ''
    query = (db.sm_item.cid == cid)
    
    if parameter == 'BrandID':
        query &= (
            (
                (db.sm_item.brand_id.contains(search)) |
                (db.sm_item.brand_name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_item.brand_id,
            db.sm_item.brand_name,
            groupby=[db.sm_item.brand_id],
            orderby=~db.sm_item.brand_id
        )
        data =  ','.join(f"{row.brand_id} | {row.brand_name}" for row in rows)
        
    if parameter == 'BrandFlavor':
        query &= (
            (
                (db.sm_item.brand_id.contains(search)) |
                (db.sm_item.brand_name.contains(search)) |
                (db.sm_item.flavor_id.contains(search)) |
                (db.sm_item.flavor_name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_item.brand_id,
            db.sm_item.brand_name,
            db.sm_item.flavor_id,
            db.sm_item.flavor_name,
            groupby=[db.sm_item.brand_id, db.sm_item.brand_name, db.sm_item.flavor_id, db.sm_item.flavor_name],
            orderby=[~db.sm_item.brand_id, ~db.sm_item.flavor_id]
        )
        data =  ','.join(f"{row.brand_id} | {row.brand_name} | {row.flavor_id} | {row.flavor_name}" for row in rows)
        
    if parameter == 'BrandWeight':
        query &= (
            (
                (db.sm_item.brand_id.contains(search)) |
                (db.sm_item.brand_name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_item.brand_id,
            db.sm_item.brand_name,
            db.sm_item.weight,
            groupby=[db.sm_item.brand_id, db.sm_item.brand_name, db.sm_item.weight],
            orderby=~db.sm_item.brand_id
        )
        data =  ','.join(f"{row.brand_id} | {row.brand_name} | {row.weight}" for row in rows)
        
    if parameter == 'FlavorWeight':
        query &= (
            (
                (db.sm_item.flavor_id.contains(search)) |
                (db.sm_item.flavor_name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_item.brand_name,
            db.sm_item.flavor_id,
            db.sm_item.flavor_name,
            db.sm_item.weight,
            groupby=[db.sm_item.brand_name,db.sm_item.flavor_id, db.sm_item.flavor_name, db.sm_item.weight],
            orderby=~db.sm_item.flavor_id
        )
        data =  ','.join(f"{row.brand_name} | {row.flavor_id} | {row.flavor_name} | {row.weight}" for row in rows)
        
    if parameter == 'ItemID':
        query &= (
            (
                (db.sm_item.item_id.contains(search)) |
                (db.sm_item.name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_item.item_id,
            db.sm_item.name,
            groupby=db.sm_item.item_id,
            orderby=~db.sm_item.item_id
        )
        data =  ','.join(f"{row.item_id} | {row.name}" for row in rows)
        
    if parameter == 'ItemType':
        query &= (
            (db.sm_item.item_category.contains(search))
        )
        rows = db(query).select(
            db.sm_item.item_category,
            groupby=db.sm_item.item_category,
            orderby=~db.sm_item.item_category
        )
        data =  ','.join(f"{row.item_category}" for row in rows)
    
    if parameter == 'Status':
        query &= (
            (db.sm_item.status.contains(search))
        )
        rows = db(query).select(
            db.sm_item.status,
            groupby=db.sm_item.status,
            orderby=~db.sm_item.status
        )
        data =  ','.join(f"{row.status}" for row in rows)
    return data

def get_brand_type():
    cid = session.cid
    brand_id = request.vars.brand_id or ''
    search = request.vars.search or ''
    
    if cid == '' or cid == None or brand_id == '' or brand_id == None:
        return
    query = (db.sm_product_hierarchy.cid == cid) & (db.sm_product_hierarchy.depth == '2') & (db.sm_product_hierarchy.level1.contains(brand_id))
    if search:
        query &= (
            (db.sm_product_hierarchy.level_name.contains(search)) |
            (db.sm_product_hierarchy.level_id.contains(search))
        )
    rows = db(query).select(
        db.sm_product_hierarchy.level_id,
        db.sm_product_hierarchy.level_name,
        orderby=~db.sm_product_hierarchy.level_id
    )
    return ','.join(f"{row.level_id}|{row.level_name}" for row in rows)


def get_brand_type_flavor():
    cid = session.cid
    brand_id = request.vars.brand_id or ''
    type_id = request.vars.type_id or ''
    search = request.vars.search or ''
    
    if cid == '' or cid == None or brand_id == '' or brand_id == None:
        return
    query = (db.sm_product_hierarchy.cid == cid) & (db.sm_product_hierarchy.depth == '3') & (db.sm_product_hierarchy.level1.contains(brand_id)) & (db.sm_product_hierarchy.level2.contains(type_id))
    if search:
        query &= (
            (db.sm_product_hierarchy.level_name.contains(search)) |
            (db.sm_product_hierarchy.level_id.contains(search))
        )
    rows = db(query).select(
        db.sm_product_hierarchy.level_id,
        db.sm_product_hierarchy.level_name,
        orderby=~db.sm_product_hierarchy.level_id
    )
    return ','.join(f"{row.level_id}|{row.level_name}" for row in rows)

def get_unit():
    cid = session.cid
    type_name = request.vars.type_name or ''
    search = request.vars.search or ''
    
    if cid == '' or cid == None:
        return
    query = (db.sm_category_type.cid == cid) & (db.sm_category_type.type_name == type_name)
    if search:
        query &= (
            (db.sm_category_type.cat_type_id.contains(search)) |
            (db.sm_category_type.cat_type_name.contains(search))
        )
    rows = db(query).select(
        db.sm_category_type.cat_type_id,
        db.sm_category_type.cat_type_name,
        orderby=~db.sm_category_type.cat_type_id
    )
    return ','.join(f"{row.cat_type_id}|{row.cat_type_name}" for row in rows)

def get_branch():
    cid = session.cid
    parameter = request.vars.parameter or ''
    search = str(request.vars.search) or ''
    
    if cid == '' or cid == None or parameter == '' or parameter == None:
        return
    
    query = ''
    rows = ''
    data = ''
    query = (db.sm_sup_depot.cid == cid)
    
    if parameter == 'BranchID':
        query &= (
            (
                (db.sm_sup_depot.sup_depot_id.contains(search)) |
                (db.sm_sup_depot.name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_sup_depot.sup_depot_id,
            db.sm_sup_depot.name,
            groupby=[db.sm_sup_depot.sup_depot_id],
            orderby=~db.sm_sup_depot.sup_depot_id
        )
        data =  ','.join(f"{row.sup_depot_id} | {row.name}" for row in rows)
        
    if parameter == 'Status':
        query &= (
            (db.sm_sup_depot.status.contains(search))
        )
        rows = db(query).select(
            db.sm_sup_depot.status,
            groupby=db.sm_sup_depot.status,
            orderby=~db.sm_sup_depot.status
        )
        data =  ','.join(f"{row.status}" for row in rows)
    return data

def get_depot():
    cid = session.cid
    parameter = request.vars.parameter or ''
    search = str(request.vars.search) or ''
    
    if cid == '' or cid == None or parameter == '' or parameter == None:
        return
    
    query = ''
    rows = ''
    data = ''
    query = (db.sm_depot.cid == cid)
    
    if parameter == 'DepotID':
        query &= (
            (
                (db.sm_depot.depot_id.contains(search)) |
                (db.sm_depot.name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_depot.depot_id,
            db.sm_depot.name,
            groupby=[db.sm_depot.depot_id],
            orderby=~db.sm_depot.depot_id
        )
        data =  ','.join(f"{row.depot_id} | {row.name}" for row in rows)
        
    if parameter == 'TownID':
        query &= (
            (
                (db.sm_depot.town_id.contains(search)) |
                (db.sm_depot.town_name.contains(search))
            )
        )
        rows = db(query).select(
            db.sm_depot.town_id,
            db.sm_depot.town_name,
            groupby=[db.sm_depot.town_id],
            orderby=~db.sm_depot.town_id
        )
        data =  ','.join(f"{row.town_id} | {row.town_name}" for row in rows)
        
    if parameter == 'OperateBy':
        rows = ['0 | PSR','1 | Distributor','2 | Operator']
        rows = [row for row in rows if search.lower() in row.lower()]
        data = ', '.join(f"{row}" for row in rows)
        
    if parameter == 'OperateFlag':
        rows = ['0 | Open','1 | Block']
        rows = [row for row in rows if search.lower() in row.lower()]
        data = ', '.join(f"{row}" for row in rows)
        
    if parameter == 'Status':
        query &= (
            (db.sm_sup_depot.status.contains(search))
        )
        rows = db(query).select(
            db.sm_depot.status,
            groupby=db.sm_depot.status,
            orderby=~db.sm_depot.status
        )
        data =  ','.join(f"{row.status}" for row in rows)
    return data




