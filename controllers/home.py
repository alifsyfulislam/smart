def index():
    
    div_topbar = True
    div_sidebar = True
    div_login_template = False
    
    visited_controller = request.controller
    visited_function = request.function
    
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL(c='auth', f='login'))
        
    response.title = 'Dashboard'
    # session.btn_add_form = ''
    # session.btn_sidebar = ''
    
    return locals()


def sidebar_collapse():
    btn_sidebar = request.vars.btn_sidebar 
    if btn_sidebar:
        if btn_sidebar == 'true':
            btn_sidebar = True
        else:
            btn_sidebar = False
        session.btn_sidebar = btn_sidebar
    # return btn_sidebar
    redirect(request.env.http_web2py_component_location or request.env.http_referer or URL('home', 'index'))
    
    
def form_collapse():
    btn_add_form = request.vars.btn_add_form if request.vars.btn_add_form else 'true'
    session.btn_add_form = btn_add_form
    if btn_add_form:
        if btn_add_form == 'false':
            btn_add_form = 'true'
        else:
            btn_add_form = 'false'
        session.btn_add_form = btn_add_form
    redirect(request.env.http_web2py_component_location or request.env.http_referer or URL('home', 'index'))
