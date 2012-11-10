# coding: utf8
# try something like
def component(text):
    return text
    
def index(): 
    return auth.wiki()
    
@auth.requires_login()
def manage_dashboard():
    dash_data = db(db.dashboard.id_user == auth.user_id).select(db.dashboard.ALL)
    return dict(dash_data = dash_data)

@auth.requires_login()   
def view_dashboard():
    dashboard = db.dashboard(request.vars['dbid'])
    sections = db(db.dashboard_section.id_dashboard == request.vars['dbid']).select(db.dashboard_section.ALL)
    return dict(sections = sections,dashboard_title = dashboard.title)
    
def get_chart(id):
    return id

@auth.requires_login()    
def add_dashboard():
    form = SQLFORM(db.dashboard,Fields=('name','title','description'))
    if form.process().accepted:
        response.flash = "Dashboard Created"
        redirect(URL('manage_dashboard'))
    elif form.errors:
        response.flash = "There were errors in the form"
    else:
        response.flash = "Please complete the form."
    return dict(form = form)

@auth.requires_login()
def add_section():
    form = SQLFORM(db.dashboard_section,Fields=('title'),hidden=dict(id_dashboard=request.vars['dbid']))
    form.vars.id_dashboard = request.vars['dbid']
    if form.process().accepted:
        response.flash = "Section Created"
        redirect(URL('manage_dashboard'))
    elif form.errors:
        response.flash = "There were errors in the form"
    else:
        response.flash = "Please complete the form."
    return dict(form = form)

@auth.requires_login()
def delete_section():
    form = FORM.confirm('Yes Delete',{"No, DON'T Delete":URL('manage_dashboard')})
    if form.accepted:
        response.flash = "Form Accepted"
        db(db.dashboard_section.id == request.vars['sid']).delete()
        redirect(URL('manage_dashboard'),client_side=True)
    return form

@auth.requires_login()
def select_charts():
    chartlist = ""
    for charts in db(db.user_chart.id_user == auth.user_id).select(db.user_chart.ALL):
       
        chartlist += str(A(IMG(_src=URL('download',args=charts.id_chart.file),_class='select_chart'),_href=URL('add_chart_to_section',vars={'sid':request.vars['sid'],'cid':charts.id_chart.id})))
    
    return chartlist

@auth.requires_login()    
def add_chart_to_section():
    sid = request.vars['sid']
    cid = request.vars['cid']
    if db.section_charts.insert(id_section = sid, chart = cid):
        response.flash = "Chart Added to section"
    else:
        response.flash = "Error: Unable to add chart to section"
    redirect(URL('manage_dashboard'))
@auth.requires_login() 
def delete_chart():
    form = FORM.confirm('Yes Delete',{"No, DON'T Delete":URL('manage_dashboard')})
    if form.accepted:
        response.flash = "Form Accepted"
        db(db.section_charts.id == request.vars['sid']).delete()
        redirect(URL('manage_dashboard'),client_side=True)
    return form

@auth.requires_login() 
def edit_section():
    sid = request.vars['sid']
    section = db.dashboard_section(sid)
    form = SQLFORM(db.dashboard_section,section)
    if form.process().accepted:
        response.flash = "Section updated"
        redirect(URL('manage_dashboard'),client_side=True)
    elif form.errors:
        response.flash = "There were errors in the form"
    else:
        response.flash = "Use the form to edit this section"
    return form
               
@auth.requires_login()        
def download():
    return response.download(request, db)
