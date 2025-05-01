from sympy.logic.boolalg import to_cnf, And, Or
from sympy import sympify
from itertools import combinations

class BeliefBase:
    """Representation of the belief base"""
    belief_base = set()
    low_prio = set()
    mid_prio = set()
    high_prio = set()

    def __init__(self):
        # Test 1
        #self.belief_base.add("p | q")
        #self.belief_base.add("~p | r")
        #self.belief_base.add("~q | r")

        # Test 2
        self.belief_base.add("p >> (q & r)")

        #self.belief_base.add("q")
        #self.belief_base.add(sympify("p"))
        #self.belief_base.add("p >> (q & w) >> p")
        #self.belief_base.add("~(p|q)")
        #self.belief_base.add(self.negate_literal("q"))
        #self.belief_base.add(self.negate_literal("~p"))

    def clear(self):
        self.belief_base.clear()
        self.low_prio.clear()
        self.mid_prio.clear()
        self.high_prio.clear()

    def add(self, input):
        self.belief_base.add(input)

    def add_with_priority(self, belief, priority='low'):
        """Add a belief with specified priority"""
        if priority == 'low':
            self.low_prio.add(belief)
        elif priority == 'mid':
            self.mid_prio.add(belief)
        elif priority == 'high':
            self.high_prio.add(belief)
        else:
            raise ValueError("Priority must be 'low', 'mid', or 'high'")
        self.belief_base = self.concatenate_priorities()

    def get_belief_base(self):
        return self.belief_base

    def kb_to_cnf(self, kb):
        """Converts all clauses in a knowledge base to CNF format."""
        cnf = set()
        for clause in kb:
            cnf.add(to_cnf(clause))
        return cnf

    def negate_literal(self, lit):
        """Negates a literal"""
        return ~lit if not isinstance(lit, str) else sympify(f'~{lit}')

    def split(self, operand, formula):
        """Splits a formula on the given operand (And/Or) and returns a set of subformulas."""
        if isinstance(formula, operand):
                return set(formula.args)
        else:
            return {formula}

    def resolve(self, c1, c2):
        """
        Resolve two clauses (c1, c2) and return the resolvant.
        c1, c2: sets of literals.
        """
        resolvents = set()
        c1_literals = self.split(Or, c1)
        c2_literals = self.split(Or, c2)

        for i in c1_literals:
            for j in c2_literals:
                if i == ~j:
                    # Remove the complementary literals and combine the rest
                    resolvent = (c1_literals - {i}) | (c2_literals - {j})

                    if not resolvent:  # Empty set means contradiction found
                        return set()
                    
                    # Convert back to Or if multiple literals
                    resolvent_expr = Or(*resolvent) if len(resolvent) > 1 else next(iter(resolvent))
                    resolvents.add(resolvent_expr)
        
        # If no resolutions, return the original clauses
        if not resolvents:
            return {c1, c2} 
        
        return resolvents

    def resolution(self, beliefs, query):
        """
        Returns True if KB entails query, False otherwise.
        """
        # Convert KB to CNF and flatten
        kb = self.kb_to_cnf(beliefs)
        kb_flat = set()
        
        for clause in kb:
            kb_flat.update(self.split(And, clause))

        # Negate the query and add to KB
        negated_query = to_cnf(f"~({query})", simplify=True)
        for clause in self.split(And, negated_query):
            kb_flat.add(clause)
        
        kb = list(kb_flat)

        while True:
            new_clauses = set()
            
            for ci, cj in combinations(kb, 2):
                resolvents = self.resolve(ci, cj)
                # two clauses resolve to yield the empty clause
                if resolvents == set():
                    return True
                
                # only add if it's not already present
                for resolvent in resolvents:
                    if resolvent not in kb and resolvent not in new_clauses:
                        new_clauses.add(resolvent)

            # there are no new clauses that can be added   
            if not new_clauses:
                return False
            kb.extend(new_clauses)

    def concatenate_priorities(self):
        return self.low_prio | self.mid_prio | self.high_prio

    def all_subsets(set):
        return [set(c) for r in range(1, len(set)+1) for c in combinations(set, r)]

    # TODO: add remainder sets and partial meet contraction
    def contraction(self, phi):
        """
        Contraction: B ÷ ϕ; ϕ is removed from B giving a new belief set B'.
        Contract the belief base by phi, using priority order: low, mid, high.
        Partial meet contraction
            1. Generate remainder sets
            2. Apply selection function on the remainders
            3. Intersect selected remainders to get contracted base
        """
        print(self.belief_base)
        # First check if phi is even entailed by the belief base
        if not self.resolution(self.belief_base, phi):
            print(f"{phi} is not entailed by anything in the Belief Base, no contraction needed.")
            return
        
        # Save original state
        original_state = {
            'low': set(self.low_prio),
            'mid': set(self.mid_prio),
            'high': set(self.high_prio)
        }

        # 1. Generate remainder sets
        remainder_sets = self._compute_remainder_sets(phi)
        if not remainder_sets:
            print("Contraction impossible.")
            return

        # 2. Apply selection function on the remainders
        selected_remainders = self._selection_function(remainder_sets)

        # 3. Intersect selected remainders to get contracted base
        new_belief_base = set.intersection(*selected_remainders)
        self._update_belief_base(new_belief_base)
        print("Contracted the belief base.")
        print("The new belief base: ", self.belief_base)

    def _compute_remainder_sets(self, phi):
        """
        Compute all remainder sets of the belief base.
        A⊥ϕ: set of inclusion-maximal subsets of A that do not imply ϕ
        """
        remainder_sets = []
        beliefs = list(self.belief_base)

        for r in range(len(beliefs), 0, -1):
            for subset in combinations(beliefs, r):
                subset = set(subset)
                if not self.resolution(subset, phi):
                    # Check if this subset is maximal
                    to_remove = []

                    for existing in remainder_sets:
                        if subset.issubset(existing):
                            to_remove.append(existing)
                    for remove in to_remove:
                        remainder_sets.remove(remove)

                    remainder_sets.append(subset)
        return remainder_sets


    def _selection_function(self, remainder_sets):
        """
        Select remainders based on priority (high-priority beliefs preferred).
        """
        if not remainder_sets:
            return []

        scored_remainders = []
        for remainder in remainder_sets:
            # weighted priority point low > mid > high
            prio_point = (
                10 * len(remainder & self.low_prio) + 
                5 * len(remainder & self.mid_prio) + 
                1 * len(remainder & self.high_prio)
            )

            # normalize by length
            score = prio_point / len(remainder) if remainder else 0
            scored_remainders.append((score, remainder))
                
        if not any(score for score, _ in scored_remainders):
            return remainder_sets

        # select the ones with the max score
        max_score = max(score for score, _ in scored_remainders)
        return [r for score, r in scored_remainders if score == max_score]

    def _update_belief_base(self, new_beliefs):
        """
        Update the actual belief sets with temporary sets.
        """
        self.belief_base = new_beliefs
        self.low_prio = self.low_prio & new_beliefs
        self.mid_prio = self.mid_prio & new_beliefs
        self.high_prio = self.high_prio & new_beliefs





    # TODO: Expansion: B + ϕ; ϕ is added to B giving a new belief set B'
    # def expansion
    def expansion(self, phi):
        """
        Expand the belief base by adding phi.
        No consistency check or priority is used.
        """
        self.belief_base.add(phi)
        print(f"Expanded belief base with: {phi}")
    #Clem: I don't know if it has to be more complex?


    # TODO: Revision: B ∗ ϕ; ϕ is added and other things are removed, 
    # so that the resulting new belief set B'is consistent.
    # Levi indentity: B ∗ ϕ := (B ÷ ¬ϕ) + ϕ
    # def revision
    def revision(self, phi):
        """
        Revises the belief base by phi using Levi Identity:
        B * phi := (B ÷ ¬phi) + phi
        """
        print(f"\n--- Revision with: {phi} ---")
    
        # Step 1: Contract the belief base by ¬phi
        neg_phi = self.negate_literal(sympify(phi))
        print(f"Contracting by: {neg_phi}")
        self.contraction(neg_phi)

        # Step 2: Expand with phi
        self.expansion(phi)
