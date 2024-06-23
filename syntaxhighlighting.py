class SyntaxHighlightingText(Text):
    def __init__(self, master=None, **kw):
        Text.__init__(self, master, **kw)
        self.syntax_rules = []  # This will be populated with syntax highlighting rules from JSON
        self.apply_syntax_highlighting()

    def apply_syntax_highlighting(self):
        for rule in self.syntax_rules:
            self.tag_configure(rule["tag_name"], foreground=rule["color"])
            self.highlight_pattern(rule["pattern"], rule["tag_name"])

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=True):
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd", "searchLimit", count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def configure_syntax_highlighting(self):
        # Load syntax highlighting rules from a JSON file
        with open('syntax_highlighting_rules.json') as f:
            self.syntax_rules = json.load(f)

        # Apply syntax highlighting using the loaded rules
        self.apply_syntax_highlighting()
