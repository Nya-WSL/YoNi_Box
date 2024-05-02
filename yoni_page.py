import os
import hashlib
import yoni_db
from uuid import uuid4
from router import Router
from nicegui import ui, app
from datetime import datetime
from main import version

def messages():
    with ui.row():
        ui.button('Quit', on_click=lambda: (app.storage.user.clear(), ui.open('/'))).classes('bg-transparent')
        ui.button('Back', on_click=lambda: ui.open('/')).classes('bg-transparent')
        show_module = ui.switch(text="紧凑模式", value=False, on_change=lambda: ui.open("/messages")).bind_value(app.storage.user, "show_module")
        show_module.set_visibility(False)
    if not os.path.exists('yoni_box.db'):
        yoni_db.create()
        message_list = []
    else:
        message_list = yoni_db.check_message()

    if message_list == []:
        ui.query('body').style('background: url("static/bg1.png") 0px 0px/cover')
        with ui.card().classes('absolute-center bg-transparent'):
            ui.badge('目前没人投稿...', outline=True, color="", text_color='#735798').classes('text-xl')
    else:
        ui.query('body').style('background: url("static/bg.png") 0px 0px/cover')
        for i in message_list:
            message = str(i["message"]).replace("\n", "\n\n").replace("\\n", "\n\n")
            with ui.expansion(i["user"]).classes('w-full'):
                if show_module.value:
                    ui.textarea(value=message).classes('text-xl w-full').props('outlined readonly bg-color="green-1"')
                else:
                    ui.chat_message(message, avatar='static/YoNi.jpg').props('bg-color="green-1"').classes('text-h6')
            ui.separator()
    # app.on_disconnect(app.storage.user.clear())

def login():
    def try_login() -> None:
        if yoni_db.check_user(username.value)[1] == hashlib.sha256(str(password.value).encode('utf-8')).hexdigest():
            app.storage.user.update({'user': username.value, 'authenticated': True})
            ui.open(app.storage.user.get('referrer_path', '/messages'))
        else:
            ui.notify('错误的账号密码！', color='negative')

    ui.query('body').style('background: url("static/bg1.png") 0px 0px/cover')
    with ui.card().classes('absolute-center'):
        ui.badge('YoNi的棉花糖登记处', outline=True, color='', text_color='#735798').classes('text-xl')
        username = ui.input('来访人').on('keydown.enter', try_login)
        password = ui.input('密码', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        with ui.row():
            ui.button('登记', on_click=try_login)
            ui.button('返回', on_click=lambda: ui.open("/"))

def main():
    router = Router()
    page_id = str(uuid4())

    @router.add('/')
    def page():
        ui.badge(f'YoNi的棉花糖投放处v{version}', outline=True, text_color="#735798", color="").classes('text-2xl absolute top-1/3 left-1/2 translate-x-[-50%]')

    @router.add('/nicegui/')
    def page():
        ui.badge(f'YoNi的棉花糖投放处v{version}', outline=True, text_color="#735798", color="").classes('text-2xl absolute top-1/3 left-1/2 translate-x-[-50%]')

    @router.add(f'/{page_id}')
    def index():
        send_button.set_visibility(False)
        login_button.set_visibility(False)

        def send():
            if text.value == '':
                ui.notify('虚假的提问是会被岚子诅咒的！', type="negative", position="top")
                return
            if not os.path.exists('yoni_box.db'):
                yoni_db.create()
            if author.value == "":
                yoni_db.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(text.value)}字", text.value)
            else:
                yoni_db.write(f"{author.value} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {len(text.value)}字", text.value)
            ui.notify('岚子会保佑你的...', type="positive", position="top")
            text.set_value('')

        def back():
            with ui.dialog() as dialog, ui.card():
                ui.label('提问内容将不会被保存，确定要返回吗？')
                with ui.row().classes('w-full'):
                    ui.button('确定', on_click=lambda: ui.open('/'), color='#735798').classes("text-white")
                    ui.button('取消', on_click=dialog.close, color='#735798').classes("text-white")
            if not text.value == "":
                dialog.open()
            else:
                ui.open('/')

        def check():
            count = 1500
            if len(text.value) > int(count):
                with ui.dialog() as dialog, ui.card():
                    ui.label(f'字数大于{count}字（包括标点符号和换行）！确定要投稿吗？').classes('text-red')
                    with ui.row().classes('w-full'):
                        ui.button('确定', on_click=lambda :send(), color='#735798').classes("text-white").on(type='click', handler=dialog.close)
                        ui.button('取消', on_click=dialog.close, color='#735798').classes("text-white")
                dialog.open()
            else:
                send()

        def change():
            count.classes('text-white')
            count.set_text(f'{len(text.value)}/1500')
            if len(text.value) > 1500:
                count.classes('text-red')

        with ui.row().classes('w-full no-wrap'):
            author = ui.input(label="称呼(非必填)").props('input-class=mx-3').classes("absolute-center translate-x-[-50%] translate-y-[-200%]")
            text = ui.textarea(placeholder='提问内容', on_change=lambda: change()).props('rounded outlined input-class=mx-3"').classes('flex-grow')
            # ui.button('提问', on_click=lambda: call(), color='#735798').classes("absolute top-1/2 left-1/2 translate-x-[-50%] text-white")
            with ui.row().classes("absolute-center text-white"):
                ui.button('提问', on_click=lambda: check(), color='#735798').classes("text-white")
                ui.button('返回', on_click=lambda: back(), color='#735798').classes("text-white")
        count = ui.label('YoNi的棉花糖投放处').classes('text-xs self-end mr-8 p-2').style('color: rgb(115 87 152)')

    ui.query('body').style('background: url("static/bg1.png") 0px 0px/cover')
    with ui.row():
        send_button = ui.button('向YoNi提问', on_click=lambda: router.open(index), color="#735798").classes("absolute top-1/2 left-1/2 translate-x-[-50%] text-white")
        login_button = ui.button('YoNi的棉花糖登记处', on_click=lambda: ui.open('/login'), color="#735798").classes("absolute top-1/2 left-1/2 translate-x-[-50%] translate-y-[200%] text-white")
        with ui.badge(outline=True, color="", text_color="#735798").classes("absolute top-2/3 left-1/2 translate-x-[-50%]"):
            ui.html('<center>注意事项<br>提问页面阅后即焚<br>刷新或关闭后页面将立即销毁<br>如非必要请勿在提问界面撰写投稿<br>您应该在撰写完毕后直接复制过来<br>如需多次提问，可在提问后继续投稿</center>').classes('text-xl')
            # ui.badge("提问页面阅后即焚", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[110%]")
            # ui.badge("刷新或关闭后页面将立即销毁", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[220%]")
            # ui.badge("如需多次提问，可在提问后继续提问", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[330%]")
            # ui.badge("请勿提问违法、违规、禁播内容", color="lightpink", text_color="white").classes("text-xl absolute top-2/3 left-1/2 translate-x-[-50%] translate-y-[440%]")
        
        ui.button("装修日志", on_click=lambda: ui.open('/update'), color="#735798").classes("text-white bg-transparent")

    # 不可删除
    router.frame().classes('w-full')