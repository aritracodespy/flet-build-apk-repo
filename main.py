import flet as ft

def main(page: ft.Page):
    page.title = "Simple Text Editor"
    page.padding = 20

    def save_text(e):
        page.client_storage.set("note", text_field.value)

    def load_text():
        try:
            text=page.client_storage.get("note")
            return text
        except:
            return ""

    def clear_text(e):
        page.client_storage.clear()
        text_field.value = ""
        page.update()

    text_field = ft.TextField(
        label="Enter your text here",
        value=load_text(),
        multiline=True,
        border=ft.InputBorder.NONE,
        expand=True
    )

    pb = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(icon=ft.Icons.SAVE,text="Save",on_click=save_text),
            ft.PopupMenuItem(icon=ft.Icons.CLEAR,text="Clear", on_click=clear_text),
        ])

    page.add(text_field,pb)

ft.app(target=main)

