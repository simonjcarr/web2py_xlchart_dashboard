# coding: utf8
# try something like
def index(): 
    return dict(message="hello from charts.py")

@auth.requires_login()    
def user_charts():
    mycharts = db(db.user_chart.id_user == auth.user_id).select()
    allcharts = db(db.chart).select()
    return dict(mycharts = mycharts,allcharts = allcharts)

@auth.requires_login()
def subscribe_form():
    
    form = SQLFORM(db.user_chart,fields=['title','description'],hidden=dict(id_chart=request.vars['id_chart'][0]))
    form.element('textarea')['_rows']=5
    form.element('textarea')['_cols']=50
    form.vars.id_chart = request.vars['id_chart'][1]
    
    if form.process().accepted:
        response.flash = 'Chart Registered'
        redirect(URL('charts', 'user_charts'),client_side=True)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'Please complete the form to register the chart.'
    return form

def unsubscribe():
    db(db.user_chart.id == request.vars['id_chart']).delete()
    redirect(URL('user_charts'))
    
def download():
    return response.download(request, db)
