





import requests
import urllib.parse, random, string



#logout
def logout():  
    loginRows=db((db.sm_login_log.cid==session.cid) & (db.sm_login_log.user_id==session.user_id)).select(db.sm_login_log.id,orderby=~db.sm_login_log.id,limitby=(0,1))
    if loginRows:
        loginRows[0].update_record(logout_time=present_datetime)
    session.clear()
    redirect(URL(c='auth', f='login'))

#login
def login():
    # ================ IF Session =================
    if (session.get('cid')):
        redirect(URL(c='home', f='index'))
        return
    # ================ IF Session =================
    
    # ================ Request ====================
    cid = str(request.vars.cid).strip().upper() if request.vars.cid else ""
    uid = str(request.vars.uid).strip().upper() if request.vars.uid else ""
    password = str(request.vars.password).strip() if request.vars.password else ""
    sync_code = str(request.vars.loginSyncCode).strip() if request.vars.loginSyncCode else ""
    user_agent = str(request.vars.userAgentKey).strip() if request.vars.userAgentKey else ""
    btnlogin = str(request.vars.btnlogin).strip() if request.vars.btnlogin else ""
    # ================ Request ===================
    
    # ================ HTML ======================
    div_topbar = False
    div_sidebar = False
    div_login_template = True
    # ================ HTML ======================
    response.title = 'Login'
    
    if btnlogin:
        if uid == "":
            response.flash = "Invalid user id"   
        elif password == "":
            response.flash = "Invalid password" 
        else:
            redirect(URL(c='auth', f='check_user', vars=dict(cid=cid, uid=uid, password=password,sync_code=sync_code, user_agent=user_agent)))
            
    return locals()


# check_user
def check_user():
    cid = str(request.vars.cid).strip().upper() if request.vars.cid else ''
    uid = str(request.vars.uid).strip().upper() if request.vars.uid else ''
    password = str(request.vars.password).strip() if request.vars.password else ''
    loginSyncCode=str(request.vars.sync_code).strip()   if request.vars.sync_code else ''  
    user_agent=str(request.vars.user_agent).strip() if request.vars.user_agent else ''
    request_ip=str(request.client).strip() if request.vars.client else ''
    
    if (request_ip=='' or request_ip==None):
        request_ip='127.0.0.1'
    
    if (cid == '' or uid == '' or password == ''):
        redirect(URL(c='auth', f='login'))
        
    access_module = 'RetailerMapping'
    my_uname = 'ADMIN'
    my_user_type = 'Admin'
    limitby=(0,1)
    session.clear()
    
    supRows=db(
        (db.sm_rep.cid==cid) & 
        ((db.sm_rep.rep_id==uid) | (db.sm_rep.field1==uid)) &
        (db.sm_rep.password==password)  & 
        (db.sm_rep.user_type=='sup') & 
        (db.sm_rep.status=='ACTIVE')
    ).select(
        db.sm_rep.ALL,
        limitby=limitby
    )
    
    if not supRows:
        mac_address = 'a'
        hdd_address = 'b'
        
        ip_address = request_ip
        http_pass = 'abC321'
        
        userText = str(cid).strip() + '<url>' + str(uid).strip() + '<url>' + str(password).strip() + '<url>' + str(mac_address) + '<url>' + str(hdd_address).strip() + '<url>' + str(ip_address).strip() + '<url>' + str(http_pass).strip() + '<url>' + str(access_module).strip()
        
        request_text = urllib.parse.quote(userText)     
        url = 'https://mreporting.transcombd.com/cpanel/login_permission/check_login?login_data=' + request_text
        
        try:
            response = requests.get(url, timeout=10)
            result = response.text
        except:
            session.flash = 'Connection Time out. Please try again after few minutes.'
            redirect(URL(c='auth', f='login'))
        
        # return str(result)
        #"STARTsuccess<fd>SMART<fd>ADMIN<fd>Admin<fd>6<fd>0<fd>0<fd>rm_analysis_view,rm_client_cat_manage,rm_client_manage,rm_client_payment_manage,rm_depot_belt_manage,rm_depot_manage,rm_depot_market_manage,rm_depot_payment_manage,rm_depot_setting_manage,rm_depot_type_manage,rm_depot_user_manage,rm_device_manage,rm_doctor_manage,rm_doctor_visit_manage,rm_doctor_visit_plan_manage,rm_ff_target_manage,rm_invoice_manage,rm_item_batch_manage,rm_item_cat_unit_manage,rm_item_manage,rm_merchandizing_manage,rm_reparea_manage,rm_report_process_manage,rm_rep_manage,rm_requisition_view,rm_stock_damage_view,rm_stock_issue_view,rm_stock_receive_view,rm_stock_transfer_view,rm_sup_manage,rm_tpcp_rules_manage,rm_user_log_view,rm_utility_manage,rm_visit_manage,rm_visit_plan_manage,rm_workingarea_manage,rm_campaign_manage,rm_campaign_view,rm_delivery_man_manage,rm_stock_transfer_manage,rm_stock_damage_manage,rm_stock_issue_manage,rm_stock_receive_manage,rm_stock_trans_dispute_manage,rm_tour_plan_manage,rm_tour_plan_view<fd>SMART<compfdsep>123<compfdsep>smart@yahoo.com<compfdsep><compfdsep>dhaka<compfdsep>bangladesh<compfdsep>1212<compfdsep><fd>NO<fd>None<fd>None<fd>Please pay your bill for continued system access. Otherwise service will be discontinued from NoneEND"
        
        if (str(result).find('START') == (-1) or str(result).find('END') == (-1)):
            session.flash = 'Communication error'
            redirect(URL(c='auth', f='login'))
        else:
            myDecReslutStr = str(result)[5:-3]
            
            separator = '<fd>'
            urlList = myDecReslutStr.split(separator, myDecReslutStr.count(separator))
            
            if len(urlList) == 2:
                myDecReslutStr = urlList[0]
            
    else:
        cid = cid
        uid = uid
        my_uname = supRows[0].rep_username
        my_user_type = 'Supervisor' if supRows[0].user_type == 'sup' else supRows[0].user_type
        
        moduleTaskStr='rm_depot_view,rm_tour_plan_view,rm_tour_plan_manage,rm_item_view,rm_reparea_view,rm_stock_trans_dispute_view,rm_stock_issue_view,rm_stock_transfer_view,rm_stock_receive_view,rm_client_manage,rm_client_view,rm_supervisor_utility,rm_national_view,rm_analysis_view,rm_invoice_view,rm_invoice_manage,rm_visit_manage,rm_visit_list_view,rm_stock_damage_view,rm_visit_plan_view,rm_rep_view'
        
        c_name='SMART'; phone='123';  email_add=''; street=''; city='Dhaka'; country='Bangladesh'; zip_code='1212'; logo='welcome/static/images/smart.png'
        companyStr=c_name+'<compfdsep>'+phone+'<compfdsep>'+email_add+'<compfdsep>'+street+'<compfdsep>'+city+'<compfdsep>'+country+'<compfdsep>'+zip_code+'<compfdsep>'+logo
        
        myDecReslutStr='success<fd>'+cid+'<fd>'+uid+'<fd>'+my_user_type+'<fd>6<fd>9<fd>5<fd>%s<fd>%s<fd>NO' %(moduleTaskStr,companyStr)
    
    if myDecReslutStr == 'failed':
        session.flash = 'Invaild autthorization'
        redirect(URL(c='auth', f='login'))
        
    separator = '<fd>'
    sepCount = myDecReslutStr.count(separator)        
    urlList = myDecReslutStr.split(separator, sepCount)
    
    if len(urlList) < 10:
        session.flash = 'Process error'
        redirect(URL(c='auth', f='login'))
    
    
    myRes = urlList[0]
    my_cid = urlList[1]
    my_uid = urlList[2]
    my_type = urlList[3]
    my_gmt = urlList[4]
    my_fromTime = urlList[5]
    my_toTime = urlList[6]
    my_task = urlList[7]
    my_companyStr = urlList[8]
    my_deviceCheck = urlList[9]
    
    if myRes != 'success':
        session.flash = 'Login failed'
        redirect(URL(c='auth', f='login'))
    
    session.cid = my_cid
    session.user_id = my_uid
    session.user_name = my_uname
    session.user_type = my_user_type
    session.user_type = my_type
    session.gmt = int(my_gmt)
    session.from_time = my_fromTime
    session.to_time = my_toTime
    session.task_listStr = my_task
    session.module_id = access_module
    session.companyStr = my_companyStr                
    session.levleDepth='0'
    session.login_synCode=loginSyncCode
    session.userPassword=password
    session.user_agent=user_agent
    session.prefix_invoice='SMART'
    
    
    compSettingsRows = db(
        (db.sm_company_settings.cid == session.cid) & 
        (db.sm_company_settings.status == 'ACTIVE')
    ).select(
        db.sm_company_settings.ALL, limitby=(0, 1)
    )
        
    if not compSettingsRows:
        session.flash = 'Need Company Settings'
        redirect(URL(c='auth', f='login'))
        
    sysItemPerPageRows = db(db.sm_settings.cid == session.cid).select()
    
    item = 0
    depot = 0
    primary_sales = 0
    working_area = 0
    field_force = 0
    client = 0
    secondary_sales = 0
    report = 0
    utility_settings = 0
    target = 0
    office = 0
    doctor = 0
    ppm = 0
        
    if not sysItemPerPageRows:
        session.flash = 'Need to check system record'
        redirect(URL(c='auth', f='login'))
        
    for records in sysItemPerPageRows:
        s_key = records.s_key
        value = records.s_value
        if (s_key == 'ITEM_PER_PAGE'):
            itemPerPage = int(value)
            session.items_per_page = itemPerPage
        elif (s_key == 'AUTO_RECEIVE'):
            autoReceive = value
            session.auto_receive = str(autoReceive).strip().upper()
        elif (s_key == 'SHOW_LEVEL_FOR_DEPOT'):
            showLevelForDepot = value
            session.showLevelForDepot = str(showLevelForDepot).strip().upper()
        elif (s_key == 'ERROR_PROCESS'):
            session.error_process_flag = str(value).strip().upper()
        elif (s_key == 'LEVEL_DEPTH'):
            session.levleDepth = str(value).strip()
        elif (s_key == 'LEDGER_CREATE'):
            session.ledgerCreate = str(value).strip().upper()
        elif (s_key == 'DEVICE_CHECK'):
            session.deviceCheck = str(value).strip().upper()
        elif (s_key == 'STOCK_CRON'):
            session.stockCreate = str(value).strip().upper()
        elif (s_key == 'MARKET_DAY'):
            session.market_day_check = str(value).strip().upper()
                
    records_websettings = db(
        (db.sm_web_settings.cid == session.cid) & 
        (db.sm_web_settings.s_value == 1)
    ).select(
        db.sm_web_settings.s_key, 
        db.sm_web_settings.s_value
    )
        
    for records in records_websettings:
        s_key = records.s_key
        value = records.s_value
        if (s_key == 'item'):
            item = int(value)
        elif (s_key == 'depot'):
            depot = int(value)
        elif (s_key == 'primary_sales'):
            primary_sales = int(value)
        elif (s_key == 'working_area'):
            working_area = int(value)
        elif (s_key == 'field_force'):
            field_force = int(value)
        elif (s_key == 'client'):
            client = int(value)
        elif (s_key == 'secondary_sales'):
            secondary_sales = int(value)
        elif (s_key == 'report'):
            report = int(value)
        elif (s_key == 'utility_settings'):
            utility_settings = int(value)
        elif (s_key == 'target'):
            target = int(value)
        elif (s_key == 'office'):
            office = int(value)
        elif (s_key == 'doctor'):
            doctor = int(value)
        elif (s_key == 'visit'):
            visit = int(value)
        elif (s_key == 'ppm'):
            ppm = int(value)
                
    session.setting_item = item
    session.setting_depot = depot
    session.primary_sales = primary_sales
    session.setting_working_area = working_area
    session.field_force = field_force
    session.setting_client = client
    session.secondary_sales = secondary_sales
    session.setting_report = report
    session.utility_settings = utility_settings
    session.setting_target = target
    session.setting_office = office
    session.setting_doctor = doctor
    session.visit = visit
    session.ppm = ppm
    
    level0Name = ''
    level1Name = ''
    level2Name = ''
    level3Name = ''
    
    records_levelsettings = db(
        (db.level_name_settings.cid == session.cid)
    ).select(
        db.level_name_settings.ALL, 
        orderby=db.level_name_settings.depth
    )
    for records_level in records_levelsettings:
        levelDepth = str(records_level.depth)
        levelName = str(records_level.name)
        if levelDepth == '0':
            level0Name = levelName
        elif levelDepth == '1':
            level1Name = levelName
        elif levelDepth == '2':
            level2Name = levelName
        elif levelDepth == '3':
            level3Name = levelName
        
    
    session.level0Name = level0Name
    session.level1Name = level1Name
    session.level2Name = level2Name
    session.level3Name = level3Name
    
    
    depot_id = ''
    user_depot_name = ''
    depot_category=''
    user_depot_address=''
    depot_short_name=''
    
    if (session.user_type == 'Depot'):
        records_depot = db(
            (db.sm_depot_user.cid == session.cid) & 
            (db.sm_depot_user.user_id == session.user_id)
        ).select(
            db.sm_depot_user.depot_id, 
            limitby=limitby
        ).first()
        
        if not records_depot:
            session.flash = 'Distributor not assigned, needed to assign !'
            redirect(URL(c='auth', f='login'))
        
        depot_id = records_depot.depot_id
        
        depotRows = db(
            (db.sm_depot.cid == session.cid) & 
            (db.sm_depot.depot_id == depot_id)
        ).select(
            db.sm_depot.name,
            db.sm_depot.field1,
            db.sm_depot.short_name, 
            limitby=limitby
        )
        
        if depotRows:
            user_depot_name = depotRows[0].name
            depot_category = ''
            user_depot_address=depotRows[0].field1
            depot_short_name=depotRows[0].short_name
            
        session.depot_id = depot_id
        session.user_depot_name = user_depot_name
        session.user_depot_category = depot_category
        session.user_depot_address = user_depot_address
        session.depot_short_name = depot_short_name
    
    device_name = 'N/A'
    if my_deviceCheck=='YES':   #& (db.sm_login_device.user_id==session.user_id)
        deviceRows=db(
            (db.sm_login_device.cid==session.cid) & 
            (db.sm_login_device.sync_code==session.login_synCode) & 
            (db.sm_login_device.status=='Activated')
        ).select(
            db.sm_login_device.ALL,
            limitby=limitby
        )
        
        if not deviceRows:
            session.flash = 'Unauthorized Device.Please contact with administrator !'
            redirect(URL(c='auth', f='login'))

        device_name=deviceRows[0].device_name
    
    db.sm_login_log.insert(cid=session.cid,user_id=session.user_id,device_name=device_name,user_agent=user_agent,request_ip=request_ip,sync_code=session.login_synCode)
    
    appName = str(request.application)
    session.appName=appName
    
    
    
    
    
    #====================================================================================
    
    
    #workingA
    records =  []
    territoryList = []
    townList =  []
    routeList =  []
    beatList =  []
    distributorList =  []
    level_idList=[]
    marketList=[]
    all_rows = []
    
    if session.user_type == 'Depot':
        
        records = db(
            (db.sm_level.cid == session.cid) & 
            (db.sm_level.depot_id == session.depot_id)
        ).select(
            db.sm_level.ALL
        )
        
        # level_idList.append(level_id)
        for rec in records:
            all_rows.append(rec)
        
    if session.user_type == 'Supervisor':
        supLevelRows=db(
            (db.sm_supervisor_level.cid==cid) & 
            (db.sm_supervisor_level.sup_id==uid)
        ).select(
            db.sm_supervisor_level.level_id,
            db.sm_supervisor_level.level_depth_no
        )
        
        if len(supLevelRows) > 0:
            
            for supRow in supLevelRows:
                level_id=supRow.level_id
                depthNo=supRow.level_depth_no
                level_idList.append(level_id)
                level = 'level' + str(depthNo)
                records = db(
                    (db.sm_level.cid == cid) & 
                    (db.sm_level.is_leaf == 1) & 
                    (db.sm_level[level] == level_id)
                ).select(
                    db.sm_level.ALL, 
                    orderby=db.sm_level.level_id
                )
                
                for rec in records:
                    all_rows.append(rec)
        
    if len(all_rows) > 0:
        
        territoryList = [item.level0 for item in all_rows]
        territoryList = list(set(territoryList))
        marketList = [item.level_id for item in all_rows]
        
        townList = [item.level1 for item in all_rows]
        townList = list(set(townList))
        
        routeList = [item.level2 for item in all_rows]
        routeList = list(set(routeList))
        
        beatList = [item.level3 for item in all_rows]
        beatList = list(set(beatList))
        
        distributorList = [item.depot_id for item in all_rows]
        distributorList = list(set(distributorList))
        
        session.marketList=marketList
        session.level_idList=territoryList
        session.territoryList=territoryList
        session.townList=townList
        session.routeList=routeList
        session.beatList=beatList
        session.distributorList=distributorList
        
    #====================================================================================
    redirect(URL(c='home', f='index'))
    pass

