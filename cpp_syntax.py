import json

syntax_rules = [
    {"pattern": "#[^\n]*", "color": "gray", "tag_name": "comment"},
    {"pattern": "\\b(if|else|for|while|break|continue|return)\\b", "color": "blue", "tag_name": "keyword"},
    {"pattern": "\\b(int|float|double|char|void)\\b", "color": "purple", "tag_name": "type"},
    {"pattern": "\\b(true|false)\\b", "color": "green", "tag_name": "boolean"},
    {"pattern": "\\b[0-9]+\\b", "color": "orange", "tag_name": "number"},
    {"pattern": "\".*?\"", "color": "red", "tag_name": "string"}
]

with open('cpp_syntax_highlighting_rules.json', 'w') as f:
    json.dump(syntax_rules, f, indent=2)
