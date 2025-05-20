class HistoryManager:
    def __init__(self):
        self.entries = []

    def record(self, flavor, operation, arguments, result):
        """ Store a new operation entry in memory. """
        if flavor not in ("STACK", "INDEPENDENT"):
            raise ValueError(f"Invalid flavor: {flavor}")

        entry = {
            "flavor": flavor,
            "operation": operation,
            "arguments": arguments,
            "result": result
        }
        self.entries.append(entry)

    def get(self, flavor=None):
        """ Get history entries by flavor. """
        if flavor is None:
            stack_entries = [entry for entry in self.entries if entry["flavor"] == "STACK"]
            independent_entries = [entry for entry in self.entries if entry["flavor"] == "INDEPENDENT"]
            return stack_entries + independent_entries

        if flavor not in ("STACK", "INDEPENDENT"):
            raise ValueError("Flavor must be either STACK or INDEPENDENT")

        return [entry for entry in self.entries if entry["flavor"] == flavor]