class BeliefBase:
    def __init__(self):
        self.beliefs = []  # list of (formula, priority) tuples

    def add(self, formula, priority=1):
        """Add a belief with a priority."""
        if formula not in [f for f, _ in self.beliefs]:
            self.beliefs.append((formula, priority))
            self.beliefs.sort(key=lambda x: -x[1])  # sort by priority descending
        else:
            print(f"Belief '{formula}' already exists.")

    def remove(self, formula):
        """Remove a belief."""
        self.beliefs = [b for b in self.beliefs if b[0] != formula]

    def list_beliefs(self):
        """Return the list of beliefs in order of priority."""
        return self.beliefs

    def contains(self, formula):
        """Check if a belief is in the base."""
        return any(b[0] == formula for b in self.beliefs)

    def get_formulas(self):
        """Return just the formulas."""
        return [f for f, _ in self.beliefs]

    def __str__(self):
        return '\n'.join([f"{f} (priority {p})" for f, p in self.beliefs])