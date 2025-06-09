
from collections import defaultdict
import re

def extract_scheme_number(scheme_id):
    return int(re.search(r'\d+', scheme_id).group())

def calculate_bonus(quantity,item_chain, scheme_slab, scheme_value, scheme_mode):
    bonus = 0
    ordered_chain = quantity
    if scheme_mode == 'Loop':
        bonus = (ordered_chain // scheme_slab) * scheme_value
    elif scheme_mode == 'Repeat':
        bonus = scheme_value if ordered_chain >= scheme_slab else 0
    return bonus

# def update_scheme_apply(cid,depot_id,sl, client_id,cl_category_id, order_date, status, update_table):
def update_scheme_apply():
    
    cid = "SMART"
    cl_category_id = "CH001"
    order_date = str('2025-05-18 15:11:26').strip()[0:10]
    status = "ACTIVE"
    update_table = "INVOICE"
    depot_id = "90000001344"
    sl = "9798"
    client_id = "13441726980498"
    # # client_id = "13131745913189" #gohinjungle
    # # sl = "445"
    # # client_id = "13131731816366" #wholsale
    # # sl = "446"
    # # client_id = "13131707732805" #gohin
    # sl="473"
    # client_id = "13131706724535"
    
    # if depot_id != '13-1313':
        # return True
    
    if update_table == "ORDER":
        sql = """
            SELECT id as order_rid,depot_id,sl, client_id, item_id, quantity, bonus_qty, price,discount,ap_discount, order_date, category_id FROM sm_order WHERE cid = '{cid}' AND depot_id = "{depot_id}" AND sl= "{sl}"
        """.format(
            cid = cid,
            depot_id = depot_id,
            sl=sl
        )
        orderRecords = db.executesql(sql,as_dict=True)
        # return response.json(orderRecords)
        
        if not orderRecords:
            return True
        
        order_list = []
        
        for item in orderRecords:
            order_list.append({
                'order_rid' : str(item["order_rid"]).strip(),
                'order_date' : str(item["order_date"]).strip(),
                'depot_id' : str(item["depot_id"]).strip(),
                'sl' : str(item["sl"]).strip(),
                'channel_id' : str(cl_category_id).strip(),
                'client_id' : str(item["client_id"]).strip(),
                'brand_id' : str(item["category_id"]).strip(),
                'item_id' : str(item["item_id"]).strip(),
                'quantity' : str(item["quantity"]).strip(),
                'bonus_qty' : str(item["bonus_qty"]).strip(),
                'actual_tp' : str(item["price"]).strip(),
                'discount' : str(item["discount"]).strip(),
                'ap_discount' : str(item["ap_discount"]).strip(),
            })
        #end for
        # return response.json(order_list)
    # return response.json(order_list)
    
    if update_table == "INVOICE":
        sql = """
            SELECT id AS order_rid,depot_id,sl, client_id, item_id, quantity, bonus_qty, price,discount, item_discount,DATE(order_datetime) AS order_date, category_id FROM sm_invoice WHERE cid = '{cid}' AND depot_id = "{depot_id}" AND sl= "{sl}"
        """.format(
            cid = cid,
            depot_id = depot_id,
            sl=sl
        )
        # return sql
        orderRecords = db.executesql(sql,as_dict=True)
        # return response.json(orderRecords)
        
        if not orderRecords:
            return True
        
        order_list = []
        
        for item in orderRecords:
            order_list.append({
                'order_rid' : str(item["order_rid"]).strip(),
                'order_date' : str(item["order_date"]).strip(),
                'depot_id' : str(item["depot_id"]).strip(),
                'sl' : str(item["sl"]).strip(),
                'channel_id' : str(cl_category_id).strip(),
                'client_id' : str(item["client_id"]).strip(),
                'brand_id' : str(item["category_id"]).strip(),
                'item_id' : str(item["item_id"]).strip(),
                'quantity' : str(item["quantity"]).strip(),
                'bonus_qty' : str(item["bonus_qty"]).strip(),
                'actual_tp' : str(item["price"]).strip(),
                'discount' : str(item["discount"]).strip(),
                'ap_discount' : str(item["item_discount"]).strip(),
            })
        #end for
        # return response.json(order_list)
    
    ############1.1 Find active scheme list
    
    # return response.json(order_list)
    
    sql = """
        SELECT scheme_id, scheme_name, field2 FROM sm_promo_scheme_head WHERE cid = '{cid}' AND "{order_date}" BETWEEN from_date AND to_date AND status = "{status}"
    """.format(
        cid = cid,
        order_date = str(order_date)[:10],
        status =status
    )
    promoSchemeHead = db.executesql(sql,as_dict=True)
    # return response.json(promoSchemeHead)
    
    if not promoSchemeHead:
        return True
    
    promo_scheme_head = []
    
    for item in promoSchemeHead:
        promo_scheme_head.append({
            "scheme_ref_id" : str(item["field2"]).strip(),
            "scheme_id" : str(item["scheme_id"]).strip(),
            "scheme_name" : str(item["scheme_name"]).strip(),
        })
    # end for
    # return response.json(promoSchemeHead)
    
    ############1.2 Find active scheme list by given depot
    
    promo_code_list_str = ', '.join("'"+str(scheme_id)+"'" for scheme_id in set(pshItem["scheme_id"] for pshItem in promo_scheme_head))
    # return response.json(promo_code_list_str)
    
    sql = """
        SELECT scheme_id, scheme_name, depot_id,field2 FROM sm_promo_scheme_depot WHERE cid = '{cid}' AND scheme_id IN ({promo_code_list_str}) 
        AND depot_id = '{depot_id}'
    """.format(
        cid = cid,
        promo_code_list_str = promo_code_list_str,
        depot_id = depot_id
    )
    # return sql
    promoSchemeDepot = db.executesql(sql,as_dict=True)
    # return response.json(promoSchemeDepot)
    
    if not promoSchemeDepot:
        return True
    
    promo_scheme_depot = []
    for item in promoSchemeDepot:
        if depot_id == str(item["depot_id"]).strip():
            promo_scheme_depot.append({
                "scheme_ref_id" : str(item["field2"]).strip(),
                "scheme_id" : str(item["scheme_id"]).strip(),
                "scheme_name" : str(item["scheme_name"]).strip(),
                "depot_id" : str(item["depot_id"]).strip(),
            })
    #end for
    # return response.json(promo_scheme_depot)
    
    ############1.3 Find active scheme list by given channel
    
    promo_code_list_str = ', '.join("'"+str(scheme_id)+"'" for scheme_id in set(pshItem["scheme_id"] for pshItem in promo_scheme_depot))
    # return response.json(promo_code_list_str)
    
    sql = """
        SELECT scheme_id, scheme_name, channel_id FROM sm_promo_scheme_channel WHERE cid = '{cid}' AND scheme_id IN ({promo_code_list_str}) AND channel_id = '{channel_id}'
    """.format(
        cid = cid,
        promo_code_list_str = promo_code_list_str,
        channel_id = cl_category_id
    )
    # return sql
    promoSchemeChannel = db.executesql(sql,as_dict=True)
    # return response.json(promoSchemeChannel)
    
    if not promoSchemeChannel:
        return True
    
    promo_scheme_channel = []
    for item in promoSchemeChannel:
        if cl_category_id == str(item["channel_id"]).strip():
            promo_scheme_channel.append({
                "scheme_id" : str(item["scheme_id"]).strip(),
                "scheme_name" : str(item["scheme_name"]).strip(),
                "channel_id" : str(item["channel_id"]).strip(),
            })
    #end for
    # return response.json(promo_scheme_channel)
    
    ############1.4 Merged selected depot & channel
    
    merged_depot_channel_scheme = []
    channel_dict = {item["scheme_id"]: item for item in promo_scheme_channel}
    for item in promo_scheme_depot:
        scheme_id = item["scheme_id"]
        if scheme_id in channel_dict:
            merged_depot_channel_scheme.append({
                "scheme_ref_id": item["scheme_ref_id"],
                "scheme_id": item["scheme_id"],
                "scheme_name": item["scheme_name"],
                "depot_id": item["depot_id"],
                "channel_id": channel_dict[scheme_id]["channel_id"]
            })
    # return response.json(merged_depot_channel_scheme)
    
    ############1.5 Find active scheme list by given client
    
    promo_code_list_str = ', '.join("'"+str(scheme_id)+"'" for scheme_id in set(pchItem["scheme_id"] for pchItem in merged_depot_channel_scheme))
    # return promo_code_list_str

    sql = """
        SELECT scheme_id, scheme_name, client_id FROM sm_promo_scheme_client AS scc WHERE cid = '{cid}' AND scheme_id IN ({promo_code_list_str})
        AND client_id = '{client_id}'
    """.format(
        cid = cid,
        promo_code_list_str = promo_code_list_str,
        client_id = client_id
    )
    # return sql
    promoSchemeClient = db.executesql(sql,as_dict=True)
    # return response.json(promoSchemeClient)
    
    promo_scheme_client = []
    for item in promoSchemeClient:
        promo_scheme_client.append({
            "scheme_id" : str(item["scheme_id"]).strip(),
            "scheme_name" : str(item["scheme_name"]).strip(),
            "client_id" : str(item["client_id"]).strip(),
        })
    #end for
    # return response.json(promo_scheme_client)
    
    merged_depot_channel_scheme_by_unmatched = []
    if len(promo_scheme_client) == 0:
        sql = """
            SELECT scheme_id, scheme_name, COUNT(DISTINCT(client_id)) AS client_id FROM sm_promo_scheme_client WHERE cid = '{cid}' AND scheme_id IN ({promo_code_list_str})
            GROUP BY scheme_id, scheme_name
        """.format(
            cid = cid,
            promo_code_list_str = promo_code_list_str
        )
        # return sql
        promoSchemeClient1 = db.executesql(sql,as_dict=True)
        # return response.json(promoSchemeClient1)
        
        promo_scheme_client_0 = []
        if len(promoSchemeClient1) > 0:
            for item1 in promoSchemeClient1:
                promo_scheme_client_0.append({
                    "scheme_id" : str(item1["scheme_id"]).strip(),
                    "scheme_name" : str(item1["scheme_name"]).strip(),
                    "client_id" : str(item1["client_id"]).strip(),
                })
                # return response.json(promo_scheme_client_0)
                
                scheme_ids_list2 = {item['scheme_id'] for item in promo_scheme_client_0}
                merged_depot_channel_scheme_by_unmatched = [item for item in merged_depot_channel_scheme if item['scheme_id'] not in scheme_ids_list2]
                # return response.json(merged_depot_channel_scheme_by_unmatched)
        else:
            merged_depot_channel_scheme_by_unmatched = merged_depot_channel_scheme
    else:
        merged_depot_channel_scheme_by_unmatched = merged_depot_channel_scheme
    # return response.json(merged_depot_channel_scheme_by_unmatched)
    
    ############1.6 client grouping by scheme
    
    if len(merged_depot_channel_scheme_by_unmatched) == 0:
        return True
    
    for item in merged_depot_channel_scheme_by_unmatched:
        item["client_id"] = client_id
        item["client_count"] = "1"
        
    # return response.json(merged_depot_channel_scheme_by_unmatched)
    
    ############1.7 Cross join selcted depot & channel & client
    promo_code_list_str = ', '.join("'"+str(scheme_id)+"'" for scheme_id in set(pchItem["scheme_id"] for pchItem in merged_depot_channel_scheme_by_unmatched))
    # return promo_code_list_str

    merged_depot_channel_client_scheme = []
    merged_depot_channel_client_scheme = merged_depot_channel_scheme_by_unmatched
    # return response.json(merged_depot_channel_client_scheme)
    
    ############1.8 Find active scheme list by given depot, channel ,client & brand
    
    promo_code_list_str = ', '.join("'"+str(scheme_id)+"'" for scheme_id in set(pchItem["scheme_id"] for pchItem in merged_depot_channel_client_scheme))
    # return promo_code_list_str
    
    sql = """
        SELECT scheme_id, scheme_name, brand_id, weight, actual_tp, discount FROM sm_promo_scheme_brand WHERE cid = '{cid}' AND scheme_id IN ({promo_code_list_str})
    """.format(
        cid = cid,
        promo_code_list_str = promo_code_list_str
    )
    # return sql
    promoSchemeBrand = db.executesql(sql,as_dict=True)
    # return response.json(promoSchemeBrand)
    
    if not promoSchemeBrand:
        return True
    
    promo_scheme_brand = []
    for item in promoSchemeBrand:
        promo_scheme_brand.append({
            "scheme_id" : str(item["scheme_id"]).strip(),
            "scheme_name" : str(item["scheme_name"]).strip(),
            "brand_id" : str(item["brand_id"]).strip(),
            "weight" : str(item["weight"]).strip(),
            "actual_tp" : str(item["actual_tp"]).strip(),
            "discount" : str(item["discount"]).strip(),
            "flat_tp" : str(float(item["actual_tp"])-float(item["discount"])).strip(),
        })
    #end for
    # return response.json(promo_scheme_brand)
    
    ############1.9 Cross join selcted depot & channel & client & brand
    
    merged_depot_channel_client_brand_scheme = []
    brand_dict = {
        f"{item['scheme_id']}_{item['brand_id']}_{item['weight'].replace('.', '_')}"
        : item
        for item in promo_scheme_brand
    }
    for item in merged_depot_channel_client_scheme:
        scheme_id = item["scheme_id"]
        for key, brand_info in brand_dict.items():
            if key.startswith(f"{scheme_id}_"):
                merged_depot_channel_client_brand_scheme.append({
                    "scheme_ref_id": item["scheme_ref_id"],
                    "scheme_id": item["scheme_id"],
                    "scheme_name": item["scheme_name"],
                    "depot_id": item["depot_id"],
                    "channel_id": item["channel_id"],
                    "client_id": item["client_id"],
                    "client_count": item["client_count"],
                    "brand_id": brand_info["brand_id"],
                    "weight": brand_info["weight"],
                    "actual_tp": brand_info["actual_tp"],
                    "discount": brand_info["discount"],
                    "flat_tp": brand_info["flat_tp"],
                })
    # return response.json(merged_depot_channel_client_brand_scheme)
    
    ############2.0 Find active scheme list by given depot, channel ,client & brand, item and filtered by ordered item
    
    ord_item_uniq_list = list(set([ordItem["item_id"] for ordItem in order_list]))
    # return response.json(ord_item_uniq_list)
    
    promo_code_list_str = ', '.join("'"+str(scheme_id)+"'" for scheme_id in set(pchItem["scheme_id"] for pchItem in merged_depot_channel_client_scheme))
    # return promo_code_list_str
    
    sql = """
        SELECT scheme_id, scheme_name, item_id FROM sm_promo_scheme_item WHERE cid = '{cid}' AND scheme_id IN ({promo_code_list_str})
    """.format(
        cid = cid,
        promo_code_list_str = promo_code_list_str
    )
    # return sql
    promoSchemeItem = db.executesql(sql,as_dict=True)
    # return response.json(promoSchemeItem)
    
    if not promoSchemeItem:
        return True
    
    promo_scheme_item = []
    for item in promoSchemeItem:
        promo_scheme_item.append({
            "scheme_id" : str(item["scheme_id"]).strip(),
            "scheme_name" : str(item["scheme_name"]).strip(),
            "item_id" : str(item["item_id"]).strip(),
        })
    #end for
    # return response.json(promo_scheme_item)
    
    ############2.1 Cross join selcted depot & channel & client & brand & ordered item 
    
    # promo_scheme_item_1 = [entry for entry in promo_scheme_item if entry["item_id"] in ord_item_uniq_list]
    # return response.json(promo_scheme_item_1)
    
    ordered_item_list_str = ', '.join("'"+str(item_id)+"'" for item_id in set(ordItem["item_id"] for ordItem in order_list))
    # return response.json(ordered_item_list_str)
    
    # =============> get ordered item_brand_record
    sql = """
        SELECT item_id, category_id, weight, item_chain, item_carton FROM sm_item WHERE cid = '{cid}' AND item_id IN ({ordered_item_list_str})
    """.format(
        cid = cid,
        ordered_item_list_str = ordered_item_list_str,
        channel_id = cl_category_id
    )
    itemRecords = db.executesql(sql,as_dict=True)
    # return response.json(itemRecords)
    
    item_list = []
    
    for item in itemRecords:
        item_list.append({
            "item_id" : str(item["item_id"]).strip(),
            "brand_id" : str(item["category_id"]).strip(),
            "weight" : str(item["weight"]).strip(),
            "item_chain" : str(item["item_chain"]).strip(),
            "item_carton" : str(item["item_carton"]).strip(),
        })
    #end for
    # return response.json(item_list)
    # =============> get ordered item_brand_record
    
    # =============> get promo item filtered by order
    item_lookup = {item["item_id"]: item for item in item_list}
    promo_scheme_item_1 = []
    for scheme in promo_scheme_item:
        item_id = scheme["item_id"]
        if item_id in item_lookup:
            merged_entry = {**scheme, **item_lookup[item_id]}
            promo_scheme_item_1.append(merged_entry)
    # return response.json(promo_scheme_item_1)
    # =============> get promo item filtered by order
    
    
    # promo_item_lookup = {
    #     (item["scheme_id"], item["brand_id"], item["weight"]): item
    #     for item in promo_scheme_item_1
    # }
    promo_item_lookup = {}
    for item in promo_scheme_item_1:
        key = (item["scheme_id"], item["brand_id"], item["weight"])
        if key not in promo_item_lookup:
            promo_item_lookup[key] = []
        promo_item_lookup[key].append(item)
    # return str(promo_item_lookup)

    # merged_depot_channel_client_brand_item_scheme = []
    # for scheme in merged_depot_channel_client_brand_scheme:
    #     key = (scheme["scheme_id"], scheme["brand_id"], scheme["weight"], scheme["item_id"])
    #     if key in promo_item_lookup:
    #         merged_depot_channel_client_brand_item_scheme.append({**scheme, **promo_item_lookup[key]})
    
    merged_depot_channel_client_brand_item_scheme = []
    for scheme in merged_depot_channel_client_brand_scheme:
        key = (scheme["scheme_id"], scheme["brand_id"], scheme["weight"])
        if key in promo_item_lookup:
            for item in promo_item_lookup[key]:
                if item["scheme_id"] == scheme["scheme_id"] and  item["brand_id"] == scheme["brand_id"] and  item["weight"] == scheme["weight"]:
                    merged_depot_channel_client_brand_item_scheme.append({**scheme, **item})
    
    # return response.json(order_list)
    # return response.json(merged_depot_channel_client_brand_item_scheme)
    
    merged_brand_item_weight_lookup = {
        (item["brand_id"], item["item_id"]): item
        for item in merged_depot_channel_client_brand_item_scheme
    }

    # Merge
    merged_depot_channel_client_brand_item_with_order_scheme = []
    for order in order_list:
        key = (order["brand_id"], order["item_id"])
        merged_order = order.copy()
        if key in merged_brand_item_weight_lookup:
            merged_order.update(merged_brand_item_weight_lookup[key])
        merged_depot_channel_client_brand_item_with_order_scheme.append(merged_order)
    # return response.json(merged_depot_channel_client_brand_item_with_order_scheme)
    
    ############2.2 Find active scheme list by given depot, channel ,client & brand, item, slab and filtered by ordered item
    
    promo_code_list_str = ', '.join("'"+str(scheme_id)+"'" for scheme_id in set(pchItem["scheme_id"] for pchItem in merged_depot_channel_client_scheme))
    # return promo_code_list_str

    sql = """
        SELECT scheme_id, scheme_name, scheme_type, scheme_slab, scheme_value, note FROM sm_promo_scheme_slab WHERE cid = '{cid}' AND scheme_id IN ({promo_code_list_str})
    """.format(
        cid = cid,
        promo_code_list_str = promo_code_list_str
    )
    # return sql
    promoSchemeSlab = db.executesql(sql,as_dict=True)
    # return response.json(promoSchemeSlab)
    
    if not promoSchemeSlab:
        return True
    
    promo_scheme_slab = []
    for item in promoSchemeSlab:
        promo_scheme_slab.append({
            "scheme_id" : str(item["scheme_id"]).strip(),
            "scheme_name" : str(item["scheme_name"]).strip(),
            "scheme_type" : str(item["scheme_type"]).strip(),
            "scheme_slab" : str(item["scheme_slab"]).strip(),
            "scheme_value" : str(item["scheme_value"]).strip(),
            "scheme_mode" : str(item["note"]).strip(),
        })
    #end for
    # return response.json(promo_scheme_slab)
    
    ############2.3 Cross join selcted depot & channel & client & brand & ordered item & slab
    
    merged_depot_channel_client_brand_item_scheme_slab = []
    for item1 in merged_depot_channel_client_brand_item_scheme:
        for item2 in promo_scheme_slab:
            if item1["scheme_id"] == item2["scheme_id"]:
                merged = {
                    **item1,
                    **item2
                }
                merged_depot_channel_client_brand_item_scheme_slab.append(merged)
    # return response.json(merged_depot_channel_client_brand_item_scheme_slab)
    # return response.json(len(merged_depot_channel_client_brand_item_scheme_slab))
    
    ############2.4 Ordered item & item table
    
    ordered_item_list_str = ', '.join("'"+str(item_id)+"'" for item_id in set(ordItem["item_id"] for ordItem in order_list))
    # return response.json(ordered_item_list_str)
    
    
    for item in itemRecords:
        item_list.append({
            "item_id" : str(item["item_id"]).strip(),
            "brand_id" : str(item["category_id"]).strip(),
            "weight" : str(item["weight"]).strip(),
            "item_chain" : str(item["item_chain"]).strip(),
            "item_carton" : str(item["item_carton"]).strip(),
        })
    #end for
    # return response.json(item_list)
    
    item_dict = {item['item_id']: item for item in item_list}
    merged_order_item_list = [
        {**item1, **item_dict.get(item1['item_id'], {})}
        for item1 in order_list
    ]
    # return response.json(merged_order_item_list)
    # return response.json(merged_depot_channel_client_brand_item_scheme_slab)
    
    ############2.5 Applying conditon and find the latest promo
    
    for item in merged_order_item_list:
        brand = item["brand_id"]
        item_id = item["item_id"]
        channel_id = item["channel_id"]
        client_id = item["client_id"]
        weight = float(item["weight"])
        quantity = float(item["quantity"])
        item_chain = float(item["item_chain"])
        order_chain = quantity
        
        # step 1: find the available schemes
        # matching_shemes = [
        #     slab for slab in merged_depot_channel_client_brand_item_scheme_slab
        #     if slab["brand_id"] == brand and float(slab["weight"]) == float(weight) 
        #     and item_id in [x.strip().strip("'") for x in slab["item_id"].split(',')]
        #     and (client_id in [x.strip().strip("'") for x in slab["client_id"].split(',')] or slab["client_id"].strip() == "ALL")
        # ]
        matching_shemes = [
            slab for slab in merged_depot_channel_client_brand_item_scheme_slab
            if slab["brand_id"] == brand and float(slab["weight"]) == weight
            and slab["channel_id"] == channel_id and slab["client_id"] == client_id
            and slab["item_id"] == item_id
        ]
        # return response.json(matching_shemes)
        
        # step 2: get schemes max ref id
        max_ref_id = list(set([int(item['scheme_ref_id']) for item in matching_shemes]))
        # return response.json(max_ref_id)
        
        max_row_id = 0
        if max_ref_id:
            max_row_id = max(max_ref_id)
            
        # Step 3: Filter items with that max_ref_id from the available schemes
        matching_max_slabs = [item for item in matching_shemes if int(item['scheme_ref_id']) == max_row_id]
        # return response.json(matching_max_slabs)
        
        # step 4: Find best matching slab
        selected_slab = None
        for slab in sorted(matching_max_slabs, key=lambda s: int(s["scheme_slab"])):
            if int(slab["scheme_slab"]) <= order_chain:
                selected_slab = slab
            else:
                break
        # return response.json(selected_slab)
            
        # step 5: Attach scheme details to the item
        if selected_slab:
            item["scheme_id"] = selected_slab["scheme_id"]
            item["scheme_name"] = selected_slab["scheme_name"]
            item["scheme_type"] = selected_slab["scheme_type"]
            item["scheme_slab"] = selected_slab["scheme_slab"]
            item["scheme_value"] = selected_slab["scheme_value"]
            item["scheme_mode"] = selected_slab["scheme_mode"]
            item["scheme_actual_tp"] = selected_slab["actual_tp"]
        else:
            item["scheme_id"] = ""
            item["scheme_name"] = ""
            item["scheme_type"] = ""
            item["scheme_slab"] = ""
            item["scheme_value"] = ""
            item["scheme_mode"] = ""
            item["scheme_actual_tp"] = ""
    # return response.json(merged_order_item_list)
    
    final_order_applied_scheme = []
    
    for fiItem in merged_order_item_list:
        # return response.json(fiItem)
        fiItem["discount"] = "0"
        fiItem["bonus_qty"] = "0"
        if fiItem["scheme_id"] != "":
            scheme_type = fiItem["scheme_type"]
            scheme_mode = fiItem["scheme_mode"]
            scheme_slab = int(fiItem["scheme_slab"])
            scheme_value = float(fiItem["scheme_value"])
            scheme_actual_tp = float(fiItem.get("scheme_actual_tp", 0))
            quantity = int(fiItem.get("quantity", 0))
            bonus_qty = int(fiItem.get("bonus_qty", 0))
            item_chain = int(fiItem.get("item_chain", 0))
            
            fiItem["ap_discount"] = "0"
            
            if scheme_type == "Percentage":
                fiItem["actual_tp"] = str(round(scheme_actual_tp,2))
                fiItem["discount"] = str(round(((quantity) * (scheme_actual_tp*(scheme_value/100))),2))
                
            elif scheme_type == "Value":
                fiItem["actual_tp"] = str(round(scheme_actual_tp,2))
                fiItem["discount"] = str(round((quantity*scheme_actual_tp),2) - round(((quantity*scheme_actual_tp)-scheme_value),2))
                
            elif scheme_type == "Product Bonus":
                fiItem["bonus_qty"] = str(calculate_bonus(quantity, item_chain, scheme_slab, scheme_value, scheme_mode))
            
        final_order_applied_scheme.append({
            'order_rid' : fiItem["order_rid"],
            'depot_id' : fiItem["depot_id"],
            'sl' : fiItem["sl"],
            'item_id' : fiItem["item_id"],
            'quantity' : fiItem["quantity"],
            'weight' : fiItem["weight"],
            'bonus_qty' : fiItem["bonus_qty"],
            'actual_tp' : fiItem["actual_tp"],
            'discount' : fiItem["discount"],
            'ap_discount' : fiItem["ap_discount"],
            'note' : fiItem["scheme_id"]+"|"+fiItem["scheme_type"]+"|"+fiItem["scheme_slab"]+"|"+fiItem["scheme_value"]+"|"+fiItem["scheme_mode"]
        })
        return response.json(final_order_applied_scheme)
        
        if update_table == "ORDER":
            for last in final_order_applied_scheme:
                # last['ap_discount'] = "0" if float(last['discount']) > 0 else last['ap_discount']
                sql = """
                    UPDATE sm_order SET bonus_qty = '{bonus_qty}', price = '{actual_tp}',ap_discount='{ap_discount}',discount='{discount}', market_name = '{note}' WHERE id = '{order_rid}'
                """.format(
                    bonus_qty = last['bonus_qty'],
                    actual_tp = last['actual_tp'],
                    note = last['note'],
                    order_rid = last['order_rid'],
                    discount = last['discount'],
                    ap_discount = last['ap_discount'],
                )
                # return sql
                db.executesql(sql)
                
            sql = """
                UPDATE sm_order_head SET market_name = '{note}' WHERE cid = '{cid}' AND depot_id = '{depot_id}' AND sl='{sl}'
            """.format(
                cid = cid,
                depot_id = depot_id,
                sl = sl,
                note = 'Scheme Check'
            )
            db.executesql(sql)
            
        if update_table == "INVOICE":
            for last in final_order_applied_scheme:
                # last['ap_discount'] = "0" if float(last['discount']) > 0 else last['ap_discount']
                sql = """
                    UPDATE sm_invoice SET bonus_qty = '{bonus_qty}',actual_tp='{actual_tp}', price = '{actual_tp}',item_discount='{ap_discount}',discount='{discount}', special_rsm_code = '{note}' WHERE id = '{order_rid}'
                """.format(
                    bonus_qty = last['bonus_qty'],
                    actual_tp = last['actual_tp'],
                    note = last['note'],
                    order_rid = last['order_rid'],
                    discount = last['discount'],
                    ap_discount = last['ap_discount'],
                )
                # return sql
                db.executesql(sql)
                
            sql = """
                UPDATE sm_invoice_head SET special_rsm_code = '{note}' WHERE cid = '{cid}' AND depot_id = '{depot_id}' AND sl='{sl}'
            """.format(
                cid = cid,
                depot_id = depot_id,
                sl = sl,
                note = 'Scheme Check'
            )
            db.executesql(sql)
            
    return response.json(final_order_applied_scheme)
    return True
pass