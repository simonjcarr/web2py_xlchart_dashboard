# coding: utf8
# try something like
def component(text):
    return text
    
def index(): 
    return auth.wiki()
    
@auth.requires_login()
def manage_dashboard():
    query = db.dashboard.id_user == auth.user_id
    constraints = {'dashboard':query}
    links = [
    lambda row: A(T('Manage Charts'),_href=URL(c='dashboard',f='view_dashboard',vars={'dbid':row.id}))
    ]
    grid = SQLFORM.smartgrid(db.dashboard,constraints=constraints,links=links)
    return dict(grid = grid)
    
def view_dashboard():
    pass
    
def get_chart(id):
    return id
