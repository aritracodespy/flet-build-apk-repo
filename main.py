import flet as ft
import json

def main(page: ft.Page):
    page.title = "Quick Notes"
    #page.scroll = "adaptive"

    tabs = ft.Tabs(tabs=[], expand=1)
    note_counter = 0

    def get_note_keys():
        data = page.client_storage.get("note_keys")
        return json.loads(data) if data else []

    def save_note_keys(keys):
        page.client_storage.set("note_keys", json.dumps(keys))

    def load_saved_notes():
        nonlocal note_counter
        note_keys = get_note_keys()
        for key in note_keys:
            note_text = page.client_storage.get(key)
            index = int(key.split("_")[1])
            note_counter = max(note_counter, index + 1)
            create_note_tab(index, note_text)

    def create_note_tab(index, initial_text=""):
        text_field = ft.TextField(value=initial_text,hint_text="Enter your note...", multiline=True, expand=True, border_width=0)
        
        


        def save_note(e):
            key = f"note_{index}"
            page.client_storage.set(key, text_field.value)
            keys = get_note_keys()
            if key not in keys:
                keys.append(key)
                save_note_keys(keys)
            page.snack_bar = ft.SnackBar(ft.Text("Note saved!"))
            page.snack_bar.open = True
            page.update()

        def clear_note(e):
            page.close(dlg_clear)
            text_field.value = ""
            page.update()

        def delete_note(e):
            page.close(dlg_delete)
            key = f"note_{index}"
            tab_to_delete = None
            for tab in tabs.tabs:
                if tab.text == f"Note {index + 1}":
                    tab_to_delete = tab
                    break
            if tab_to_delete:
                tabs.tabs.remove(tab_to_delete)
                page.client_storage.remove(key)
                keys = get_note_keys()
                if key in keys:
                    keys.remove(key)
                    save_note_keys(keys)
                page.update()




        dlg_clear = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to clear note?"),
            actions=[
                ft.TextButton("Yes", on_click=clear_note),
                ft.TextButton("No", on_click=lambda e: page.close(dlg_clear)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            
        )

        dlg_delete = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this tab?"),
            actions=[
                ft.TextButton("Yes", on_click=delete_note),
                ft.TextButton("No", on_click=lambda e: page.close(dlg_delete)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            
        )
        tab_content = ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(icon=ft.Icons.SAVE,on_click=save_note),
                        ft.IconButton(icon=ft.Icons.CLEAR,on_click=lambda e: page.open(dlg_clear)),
                        ft.IconButton(icon=ft.Icons.DELETE,icon_color=ft.Colors.RED_300,on_click=lambda e: page.open(dlg_delete))
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                text_field
            ],
            expand=True,
        )

        new_tab = ft.Tab(
            text=f"Note {index + 1}",
            content=tab_content
        )

        tabs.tabs.append(new_tab)
        tabs.selected_index = len(tabs.tabs) - 1
        page.update()

    def add_tab(e):
        used_indices = sorted(
            [int(k.split("_")[1]) for k in get_note_keys()]
        )

        # Find the smallest available index (e.g., fill in deleted slots)
        index = 0
        while index in used_indices:
            index += 1

        create_note_tab(index)
    

    add_button = ft.ElevatedButton("Quick Note", on_click=add_tab)

    page.add(ft.Column([add_button, tabs], expand = True))
    load_saved_notes()

ft.app(target=main)
