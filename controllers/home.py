def index():
    
    div_topbar = True
    div_sidebar = True
    div_login_template = False
    
    visited_controller = request.controller
    visited_function = request.function
    
    if (session.cid == '' or session.user_id == '' or session.cid == None or session.user_id == None):
        redirect(URL(c='auth', f='login'))
        
    response.title = 'Dashboard'
    
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
