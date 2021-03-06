# -*- coding: utf-8 -*-


    

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
db.define_table('workbook',
Field('path',requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'workbook.path')]),
Field('title',requires=IS_NOT_EMPTY()),
format="%(title)s",
)


db.define_table('chart',
Field('chartName'),
Field('id_workbook',db.workbook),
Field('worksheet'),
Field('file','upload',autodelete=True),
Field('lastupdated','datetime',default=request.now),
format="%(id_workbook)s %(chartName)s",
)

db.define_table('user_chart',
Field('id_user',db.auth_user,readable=False,default=auth.user_id,writable=False),
Field('id_chart','reference chart',readable=False,writable=False),
Field('title', requires=IS_NOT_EMPTY(),label='Default Title'),
Field('description','text',label='Default Description'),
Field('updatehours','integer',default=24),
format="%(title)s",
)

db.define_table('dashboard',
Field('id_user',db.auth_user,readable=False,writable=False,default=auth.user_id),
Field('name', requires=IS_NOT_EMPTY()),
Field('title',label='Display Title',requires=IS_NOT_EMPTY()),
Field('description','text'),
format="%(name)s",
)

db.define_table('dashboard_section',
Field('id_dashboard',db.dashboard,writable=False,readable=False),
Field('title',requires=IS_NOT_EMPTY()),
Field('titlesize','integer',default=12,requires=IS_INT_IN_RANGE(1,200),label='Title Size (PT)'),
Field('bgcolor'),
Field('width','decimal(2,2)',requires=IS_DECIMAL_IN_RANGE(1,100),label='Width(%)',default=50.00),
Field('chartwidth', 'decimal(2,2)',requires=IS_DECIMAL_IN_RANGE(0,100),label='Chart Wdith(%)'),
Field('centre',requires=IS_IN_SET(['True','False']),default='True',label='Centre Charts?'),
format="%(title)s",
)

db.define_table('section_charts',
Field('id_section',db.dashboard_section,ondelete='CASCADE',writable=False,readable=False),
Field('chart','reference chart',writable=False,readable=False),
Field('title'),
Field('description','text'),
Field('width','decimal(2,2)',requires=IS_DECIMAL_IN_RANGE(1,100),label='Width(%)',default=50.00),
Field('position','integer',default=1),
Field('bgcolor'),
)

db.define_table('chart_position',
Field('id_section',db.dashboard_section),
Field('width','integer'),
Field('chart','reference chart'),
)


#Modal Functions
def checkchartindb(chartname):
    if db(db.chart.chartName == chartname).count() > 0:
        return True
    else:
        return False
        
def is_my_chart(chartname):
    count_charts = db(
    (db.user_chart.id_user == auth.user_id) & ##all charts of the user
    (db.chart.chartName == chartname) & ##all charts named 'abc'
    (db.user_chart.id_chart == db.chart.id) ##the actual relation
    ).count()
    if count_charts > 0:
        return True
    else:
        return False
