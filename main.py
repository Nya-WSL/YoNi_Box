import function
import yoni_page
import update_page
from nicegui import ui, app
from typing import Optional
from fastapi.responses import RedirectResponse

# messages: List[Tuple[str, str, str, str]] = []
version = "1.2.7.2"
app.add_static_files('/static', 'static')

@ui.page('/login', title="YoNi的棉花糖登记处")
def page() -> Optional[RedirectResponse]:
    if app.storage.user.get('authenticated'):
        return RedirectResponse('/messages')
    else:
        yoni_page.login()

@ui.page('/messages', title="YoNi的棉花糖")
def page():
    if not app.storage.user.get('authenticated'):
        return RedirectResponse('/login')
    else:
        yoni_page.messages()

@ui.page('/update', title="YoNi的棉花糖装修日志")
def page():
    update_page.page()

@ui.page('/')
# @ui.page('/{_:path}')
def page():
    yoni_page.main()

if __name__ == '__mp_main__':
    function.init()

ui.run(title="YoNi的棉花糖", favicon="static/icon.png", host="0.0.0.0", port=11452, language="zh-CN", show=False, storage_secret='YourSecretKey')