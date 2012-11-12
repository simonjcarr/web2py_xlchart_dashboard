# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
  
    if auth.is_logged_in():
        redirect(URL('dashboard','manage_dashboard'))
    else:
        return dict()

def add_workbook():
    grid = SQLFORM.smartgrid(db.workbook)
    return locals()

def add_chart():
    grid = SQLFORM.smartgrid(db.chart)
    return locals()

def register_chart_part1():
    grid = SQLFORM.smartgrid(db.workbook,links = [lambda row: A(T('List charts in this workbook'),_href=URL("default","list_workbook_charts",vars={'wbid':row.id})),] )
    return dict(workbookGrid = grid)
    
def list_workbook_charts():
    import os
    wbid = request.vars['wbid']
    rsPath = db(db.workbook.id == wbid).select(db.workbook.path)
    wbPath = rsPath[0].path
    ChartDetails = get_chart(wbPath)
    chartfiles = []
    DivCount = 0
    for ChartDetail in ChartDetails['chartdetail']: 
        DivCount += 1
        div_name = "div" + str(DivCount)
        #div_name = ChartDetail['sheetname'].replace(' ','_') + '_' + ChartDetail['chartname'].replace(' ','_')  
        if checkchartindb(ChartDetail['chartname']):
            chartimage = IMG(_src=URL(ChartDetails['webfolder'],str(ChartDetail['imagename'])),_width="200",_height="200")
        else:
            chartimage = A(IMG(_src=URL(ChartDetails['webfolder'],str(ChartDetail['imagename'])),_width="200",_height="200"),callback = URL(f='registerchart',vars={'wbid':wbid,'sheetname':ChartDetail['sheetname'],'chartname':ChartDetail['chartname'],'imagename':ChartDetail['imagename'],'webfolder':ChartDetails['webfolder']}), target=div_name)
        chartfiles.append(dict(chartname = ChartDetail['chartname'], divname = div_name,chartimage = chartimage, chartfolder = ChartDetails['webfolder'] ))
    #for root, dirs, files in os.walk(ChartDetails['osfolder']):
    #    for file in files:
    #        chartfiles.append(IMG(_src=URL(ChartDetails['webfolder'],file),_width="200",_height="200"))
    return dict(chartfiles=chartfiles)

def get_chart(workbookPath, imageName="XLChart"):
    import os, time
    wbPath, wbFile = os.path.split(workbookPath)
    import pythoncom
    pythoncom.CoInitialize()
    from pyxlchart import Pyxlchart
    
    ChartObj = Pyxlchart()
    ChartObj.WorkbookDirectory = wbPath
    ChartObj.WorkbookFilename = wbFile
    ChartObj.ImageFilename = imageName
    timeDir = str(time.time())
    os.makedirs(os.path.join(request.folder, 'static\\images\\temp', timeDir))
    exportFolder = os.path.join(request.folder, 'static\\images\\temp', timeDir)
    ChartObj.ExportPath =  exportFolder
    ChartObj.ReplaceWhiteSpaceChar = '_'
    ChartDetailList = ChartObj.start_export()
    ChartDetails = dict(chartdetail = ChartDetailList, webfolder = os.path.join('static/images/temp/',timeDir),osfolder = exportFolder)
    return ChartDetails

def registerchart():
    import os
    if db(db.chart.chartName==request.vars['chartname']).count() == 0:
        imagepath = os.path.join(request.folder,request.vars['webfolder'],request.vars['imagename'])
        stream = open(imagepath,'rb')
        chartid = db.chart.insert(chartName=request.vars['chartname'],id_workbook=request.vars['wbid'],worksheet=request.vars['sheetname'],file=stream)
        
        return "Chart registered with id " + str(chartid)
    else:
        return "Chart already registered"


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())
def refresh_charts():
    import datetime
    charts = db(db.user_chart).select()
    for chart in charts:
       a = chart.id_chart.lastupdated
       try:
           b = datetime.datetime(a.year,a.month,a.day,a.hour,a.minute,a.second)
           print chart.id_chart.lastupdated, b + datetime.timedelta(hours=5)
       except:
           pass

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
