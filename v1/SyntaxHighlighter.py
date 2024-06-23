import json

def configure_syntax_highlighting(text_editor):
    with open('cpp_syntax_highlighting_rules.json') as f:
        syntax_rules = json.load(f)

    for rule in syntax_rules:
        pattern = rule['pattern']
        color = rule['color']
        tag_name = rule['tag_name']
        text_editor.TextBox.tag_configure(tag_name, foreground=color)

        start_index = '1.0'
        while True:
            start_index = text_editor.TextBox.search(pattern, start_index, stopindex='end')
            if not start_index:
                break
            end_index = f"{start_index}+{len(pattern)}c"
            text_editor.TextBox.tag_add(tag_name, start_index, end_index)
            start_index = end_index
