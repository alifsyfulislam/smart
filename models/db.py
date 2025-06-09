# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    # db = DAL(configuration.get('db.uri'),
    #          pool_size=configuration.get('db.pool_size'),
    #          migrate_enabled=configuration.get('db.migrate'),
    #          check_reserved=['all'])
    pass
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------
    pass

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False, migrate=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# =====================================
signature = db.Table(
    db,
    "signature",
    Field("field1", "string", default="-"),
    Field("field2", "integer", default=0),
    Field("note", "string", default="-"),
    Field("created_on", "datetime", default=date_fixed),
    Field("created_by", default=session.user_id),
    Field("updated_on", "datetime", update=date_fixed),
    Field("updated_by", update=session.user_id),
)
# =====================================

db.define_table("sm_rep",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("rep_id","string",requires=[IS_NOT_EMPTY(), IS_LENGTH(20, error_message="Mmaximum 20 character")],),
    Field("name","string",requires=[IS_NOT_EMPTY(), IS_LENGTH(50, error_message="Maximum 50 character")],),
    Field("name_bn", "string"),
    Field("address", "string"),
    Field("address_bn", "string"),
    Field("mobile_no", "string", default=""),
    Field("alt_mobile_no", "string", default=""),
    Field("email", "string", default=""),
    Field("dob", "date"),
    Field("doj", "date", default=date_fixed),
    Field("nid", "string", default=""),
    Field("tin", "string", default=""),
    Field("password", "password", requires=IS_LENGTH(minsize=3, maxsize=12)),
    Field("image_path", "upload", length=200),
    Field("status", "string", requires=IS_IN_SET(("ACTIVE", "INACTIVE")), default="ACTIVE"),
    Field("sync_code", "string", default=""),
    Field("sync_code_servey", "string", default=""),
    Field("sync_count", "integer", requires=IS_NOT_EMPTY(), default=0),
    Field("first_sync_date", "datetime", default=""),
    Field("last_sync_date", "datetime", default=""),
    Field("monthly_sms_count", "integer", requires=IS_NOT_EMPTY(), default=0),
    Field("monthly_voucher_count", "integer", requires=IS_NOT_EMPTY(), default=0),
    Field("java", "string", requires=IS_IN_SET(("Yes", "No")), default="No"),
    Field("wap", "string", requires=IS_IN_SET(("Yes", "No")), default="No"),
    Field("android", "string", requires=IS_IN_SET(("Yes", "No")), default="No"),
    Field("sms", "string", requires=IS_IN_SET(("Yes", "No")), default="Yes"),
    Field("user_type", "string", default="rep"),
    Field("level_id", "string", default=""),
    Field("designation_id", "string", default=""),
    Field("designation_name", "string", default=""),
    Field("depot_id", "string", default=""),
    Field("depot_name", "string", default=""),
    Field("sync_req_time", "datetime", default=""),  # 10 min gap in 2 sync
    Field("sync_flag", "string", default="0"),
    Field("sync_data", "string", default=""),
    Field("rep_username","string",unique=True),
    signature,
    migrate=False,
)

db.define_table("sm_settings",
    Field("cid", "string", requires=IS_NOT_EMPTY()),
    Field("s_key","string",requires=[IS_NOT_EMPTY(),IS_LENGTH(20, error_message="enter maximum 20 character"),],),
    Field("s_value", "string", default=""),
    signature,
    migrate=False,
)

db.define_table("sm_company_settings",
    Field("cid", "string", requires=IS_NOT_EMPTY()),
    Field("http_pass", "string", default=""),
    Field("subscription_model", "string", default=""),
    Field("clean_Data", "string", default=""),
    Field("keep_history", "string", default=""),
    Field("subscription_date", "date", requires=IS_NOT_EMPTY(), default=present_date),
    Field("status", "string", requires=IS_IN_SET(("ACTIVE", "INACTIVE")), default="ACTIVE"),
    Field("admin_mobile_no", "string", default=""),
    Field("item_list", "text", default=""),
    Field("item_list_mobile", "text", default=""),
    Field("temp_item_list", "text", default=""),
    signature,
    migrate=False,
)

db.define_table("sm_web_settings",
    Field("cid", "string", requires=IS_NOT_EMPTY()),
    Field("s_key","string",requires=[IS_NOT_EMPTY(),IS_LENGTH(20, error_message="enter maximum 20 character"),],),
    Field("s_value", "integer", default=1),
    signature,
    migrate=False,
)

db.define_table("level_name_settings",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("depth", "integer", requires=IS_NOT_EMPTY()),
    Field("name", "string", default=""),
    Field("starting_code", "string", default=""),
    migrate=False,
)

db.define_table("sm_depot_user",
    Field("cid", "string", requires=IS_NOT_EMPTY()),
    Field("user_id", "string", requires=IS_NOT_EMPTY()),
    Field("depot_id", "string", default=""),
    signature,
    migrate=False,
)

db.define_table("sm_depot",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("sup_depot_id", "string", requires=IS_NOT_EMPTY()),
    Field("sup_depot_name", "string", requires=IS_NOT_EMPTY()),
    Field("depot_id","string",requires=[IS_NOT_EMPTY()]),
    Field("old_depot_id","string", default=''),
    Field("name","string",requires=[IS_NOT_EMPTY(),IS_LENGTH(50, error_message="enter maximum 50 character"),],),
    Field("name_bn","string", default=""),
    Field("short_name", "string", default=""),
    Field("email", "string", default=""),
    Field("contact", "string", default=""),
    Field("depot_category","string", default=''),
    Field("contact_2", "string", default=""),
    Field("address", "string", default=""),
    Field("address_bn", "string", default=""),
    Field("wh_address", "string", default=""),
    Field("wh_address_bn", "string", default=""),
    Field("bin", "string", default=""),
    Field("owner_name", "string", default=""),
    Field("owner_name_bn", "string", default=""),
    Field("tin", "string", default=""),
    Field("town_id", "string", requires=IS_NOT_EMPTY()),
    Field("town_name", "string", default=""),
    Field("latitude", "string", default=""),
    Field("longitude", "string", default=""),
    Field("requisition_sl", "integer", default=0),
    Field("issue_sl", "integer", default=0),
    Field("receive_sl", "integer", default=0),
    Field("damage_sl", "integer", default=0),
    Field("order_sl", "integer", default=0),
    Field("del_sl", "integer", default=0),
    Field("return_sl", "integer", default=0),
    Field("client_payment_sl", "integer",default=0),
    Field("depot_payment_sl", "integer", default=0),
    Field("stock_in_sl", "integer", default=0),  # used for payment to client sl
    Field("dm_pass", "string", default=""),
    Field("sequence_no", "integer", default=0),
    Field("status", "string", requires=IS_IN_SET(("ACTIVE", "INACTIVE")), default="ACTIVE"),
    Field("auto_del_cron_flag","integer", default=0),
    Field("intr_flag","integer", default=1),
    Field("approval_flag","integer", default=0),
    Field("sync_code", "string", default=""),
    Field("sync_count", "integer", requires=IS_NOT_EMPTY(), default=0),
    signature,
    migrate=False,
)

db.define_table("sm_depot_store",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("depot_id", "string", requires=IS_NOT_EMPTY()),
    Field("store_id", "string", requires=IS_NOT_EMPTY()),
    Field("store_name", "string", requires=IS_NOT_EMPTY()),
    Field("store_type", "string", requires=IS_IN_SET(("SALES", "OTHERS")), default="SALES"),  # SALES,OTHERS
    signature,
    migrate=False,
)

db.define_table("sm_depot_stock_balance",
    Field("cid", "string", requires=IS_NOT_EMPTY()),
    Field("depot_id", "string", requires=IS_NOT_EMPTY()),
    Field("store_id", "string", requires=IS_NOT_EMPTY()),  # location id
    Field("store_name", "string", requires=IS_NOT_EMPTY()),  # location name
    Field("item_id", "string", requires=IS_NOT_EMPTY()),
    Field("batch_id", "string", default=""),
    Field("expiary_date", "date"),
    Field("quantity", "integer", requires=IS_NOT_EMPTY(), default=0),
    Field("block_qty", "integer", default=0),
    migrate=False,
)

db.define_table("sm_login_device",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("user_id","string",default="",requires=[IS_NOT_EMPTY(), IS_LENGTH(20, error_message="Mmaximum 20 character")],),
    Field("device_name","string",default="",requires=[IS_NOT_EMPTY(), IS_LENGTH(50, error_message="Mmaximum 50 character")],),
    Field("user_agent", "string", default=""),
    Field("sync_code", "string", default=""),
    Field("request_ip", "string", default=""),
    Field("status","string",requires=IS_IN_SET(("Submitted", "Activated", "Blocked")),default="Submitted",),
    Field("created_on", "datetime", default=date_fixed),
    Field("updated_on", "datetime", update=date_fixed),
    Field("updated_by", update=session.user_id),
    migrate=False,
)


db.define_table("sm_level",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("level_id","string",requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T("must be alphanumeric ( a-z, A-Z, 0-9 )!")),IS_LENGTH(20, error_message="Maximum 20 character"),],),
    Field("level_name","string",requires=[IS_NOT_EMPTY(), IS_LENGTH(50, error_message="Maximum 50 character")],),
    Field("parent_level_id","string",default="0",requires=[IS_NOT_EMPTY(), IS_LENGTH(50, error_message="Maximum 50 character")],),
    Field("parent_level_name", "string", default=""),
    Field("is_leaf", "string", requires=IS_NOT_EMPTY(), default="0"),  # 0 for group & 1 for final
    Field("area_id_list", "string", default=""),
    Field("special_territory_code", "string", default=""),
    Field("depot_id","string",default="-",requires=[IS_NOT_EMPTY(), IS_LENGTH(20, error_message="Maximum 20 character")],),
    Field("depot_name", "string", default=""),
    Field("depth", "integer", default=0),
    Field("level0", "string", default=""),
    Field("level0_name", "string", default=""),
    Field("level1", "string", default=""),
    Field("level1_name", "string", default=""),
    Field("level2", "string", default=""),
    Field("level2_name", "string", default=""),
    Field("level3", "string", default=""),
    Field("level3_name", "string", default=""),
    Field("level4", "string", default=""),
    Field("level4_name", "string", default=""),
    Field("level5", "string", default=""),
    Field("level5_name", "string", default=""),
    Field("level6", "string", default=""),
    Field("level6_name", "string", default=""),
    Field("level7", "string", default=""),
    Field("level7_name", "string", default=""),
    Field("level8", "string", default=""),
    Field("level8_name", "string", default=""),
    Field("territory_des", "string", default=""),
    signature,
    migrate=False,
)

db.define_table("sm_supervisor_level",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("sup_id", "string", requires=IS_NOT_EMPTY()),
    Field("sup_name", "string", default=""),
    Field("level_id", "string", requires=IS_NOT_EMPTY()),
    Field("level_name", "string", default=""),
    Field("level_depth_no", "integer", default=0),
    signature,
    migrate=False,
)

db.define_table("sm_login_log",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("user_id","string",default="",requires=[IS_NOT_EMPTY(), IS_LENGTH(20, error_message="Mmaximum 20 character")],),
    Field("device_name","string",default="",requires=[IS_NOT_EMPTY(), IS_LENGTH(50, error_message="Mmaximum 50 character")],),
    Field("user_agent", "string", default=""),
    Field("request_ip", "string", default=""),
    Field("sync_code", "string", default=""),
    Field("login_time", "datetime", default=date_fixed),
    Field("logout_time", "datetime"),
    migrate=False,
)


db.define_table("sm_product_hierarchy",
    Field("cid", "string", default=session.cid),
    Field("level_id","string"),
    Field("level_name","string"),
    Field("parent_level_id","string",default="0"),
    Field("parent_level_name", "string", default=""),
    Field("level0", "string", default=""),
    Field("level0_name", "string", default=""),
    Field("level1", "string", default=""),
    Field("level1_name", "string", default=""),
    Field("level2", "string", default=""),
    Field("level2_name", "string", default=""),
    Field("level3", "string", default=""),
    Field("level3_name", "string", default=""),
    Field("is_leaf", "string", requires=IS_NOT_EMPTY(), default="0"),
    Field("depth", "integer", default=0),
    Field("image_path", "upload", length=200),
    signature,
    migrate=False
)

db.define_table("sm_category_type",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("type_name", "string", requires=IS_NOT_EMPTY()),
    Field("cat_type_id","string",requires=[IS_NOT_EMPTY(),IS_LENGTH(50, error_message="enter maximum 50 character"),],),
    Field("cat_type_name","string",requires=[IS_NOT_EMPTY(),IS_LENGTH(100, error_message="enter maximum 100 character"),],),
    signature,
    migrate=False,
)

db.define_table("sm_item",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("item_id", "string", requires=[IS_NOT_EMPTY(), IS_LENGTH(20, error_message="enter maximum 20 character")]),
    Field("old_item_id", "string",default=''),
    Field("detail_name","string",default=''),
    Field("name", "string", requires=[IS_NOT_EMPTY(), IS_LENGTH(100, error_message="enter maximum 100 character")]),
    Field("name_bn", "string", requires=[IS_LENGTH(100, error_message="enter maximum 100 character")]),
    Field("short_name", "string", default=''),
    Field("des", "string", requires=[IS_NOT_EMPTY(), IS_LENGTH(100, error_message="enter maximum 100 character")], default="-"),
    Field("image_path", "upload", length=200,requires=IS_EMPTY_OR(IS_IMAGE(extensions=('jpeg', 'jpg', 'png', 'gif')))),
    Field("pack_size", "string", requires=IS_IN_SET(("SMALL", "LARGE", "MEDIUM")), default="SMALL"),
    Field("unit_type", "string", requires=IS_NOT_EMPTY()),
    Field("category_id", "string", default=""),
    Field("category_name", "string",default=""),
    Field("category_id_sp", "string", requires=IS_NOT_EMPTY()),
    Field("company_id", "string", default=""),
    Field("company_name", "string", default=""),
    Field("brand_id", "string", default=""),
    Field("brand_name", "string", default=""),
    Field("type_id", "string", default=""),
    Field("type_name", "string", default=""),
    Field("flavor_id", "string", default=""),
    Field("flavor_name", "string", default=""),
    Field("ctn_pcs_ratio", "integer", default=1),
    Field("manufacturer", "string", requires=[IS_NOT_EMPTY(), IS_LENGTH(50, error_message="enter maximum 50 character")], default="-"),
    Field("item_carton", "integer", requires=IS_INT_IN_RANGE(1, 9999999, error_message="too small or large number")),
    Field("item_chain", "integer", default=1, requires=IS_INT_IN_RANGE(1, 100, error_message="too small or large number")),
    Field("sequence_no", "integer", default=1),
    Field("stock_cover_days", "integer",default=7, requires=[IS_NOT_EMPTY()]),
    Field("invoice_price", "double", requires=[IS_NOT_EMPTY(), IS_FLOAT_IN_RANGE(0, 999999, dot=".", error_message="too small or too large!")]),
    Field("price", "double", default=0, requires=[IS_NOT_EMPTY(), IS_FLOAT_IN_RANGE(0, 999999, dot=".", error_message="too small or too large!")]),
    Field("dist_price", "double", default=0, requires=[IS_NOT_EMPTY(), IS_FLOAT_IN_RANGE(0, 999999, dot=".", error_message="too small or too large!")]),
    Field("vat_amt", "double", default=0, requires=[IS_NOT_EMPTY(), IS_FLOAT_IN_RANGE(0, 999999, dot=".", error_message="too small or too large!")]),
    Field("total_amt", "double", default=0),
    Field("mrp", "double", default=0),
    Field("weight", "double",default = 0, requires=[IS_NOT_EMPTY(),IS_FLOAT_IN_RANGE(0, 999999, dot=".", error_message="too small or too large!")]),
    Field("intr_flag", "integer", default=1),
    Field("status", "string", requires=IS_IN_SET(("ACTIVE", "INACTIVE")), default="ACTIVE"),
    Field("item_category", "string", requires=IS_IN_SET(("BONUS","GIFT","OTHERS","REGULAR")), default="REGULAR"),
    signature,
    migrate=False,
)

db.define_table("sm_item_batch",
    Field("cid", "string", requires=IS_NOT_EMPTY(), default=session.cid),
    Field("item_id", "string", requires=IS_NOT_EMPTY()),
    Field("name", "string", default=""),
    Field("batch_id", "string", requires=IS_NOT_EMPTY()),
    Field("expiary_date", "date", requires=IS_NOT_EMPTY()),
    signature,
    migrate=False,
)
