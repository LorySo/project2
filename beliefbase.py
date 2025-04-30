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
        self.resolution("p")

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

    def resolution(self, query):
        """
        Returns True if KB entails query, False otherwise.
        """
        # Convert KB to CNF and flatten
        kb = self.kb_to_cnf(self.belief_base)
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

    # TODO: Contraction: B ÷ ϕ; ϕ is removed from B giving a new belief set B'
    def contraction(self, phi):
        """
        Contract the belief base by phi, using priority order: low, mid, high.
        """
        print(self.belief_base)
        # First check if phi is even entailed by the belief base
        if not self.resolution(phi):
            print(f"{phi} is not entailed by anything in the Belief Base, no contraction needed.")
            return
        
        # Save original state
        original_state = {
            'low': set(self.low_prio),
            'mid': set(self.mid_prio),
            'high': set(self.high_prio)
        }

        # Try removing from low-priority beliefs only
        if self._try_remove_and_check(phi, ['low']):
            return True

        # Try removing from low + mid (still avoiding high-priority)
        if self._try_remove_and_check(phi, ['low', 'mid']):
            return True

        # Only remove high-priority if absolutely necessary
        if self._try_remove_and_check(phi, ['low', 'mid', 'high']):
            return True

        print("Contraction failed - cannot remove all beliefs.")
        self._restore_state(original_state)
        return False

    def _try_remove_and_check(self, phi, priorities):
        """
        Try removing beliefs from specified priorities and check 
        if phi is no longer entailed.
        """
        beliefs = []
        for p in priorities:
            beliefs.extend(getattr(self, f"{p}_prio"))

        for k in range(1, len(beliefs) + 1):
            for to_remove in combinations(beliefs, k):
                # Temporarily remove beliefs
                temp_sets = self._create_temp_sets_without_beliefs(to_remove)
                self._update_belief_base(temp_sets)

                print("tried to remove: ", to_remove, " in the priorities: ", priorities)
                print("belief base", self.belief_base)

                print(f"Resolution with {phi}: {self.resolution(phi)}")
                # Check if contraction succeeded
                if not self.resolution(phi):
                    print(f"Contracted by removing: {to_remove}")
                    return True

                # Restore if failed
                self._restore_state(temp_sets)

        return False

    def _create_temp_sets_without_beliefs(self, to_remove):
        """
        Create temporary copies of belief sets with specified beliefs removed.
        """
        temp_sets = {
            'low': set(self.low_prio),
            'mid': set(self.mid_prio),
            'high': set(self.high_prio)
        }
        for belief in to_remove:
            for p in ['low', 'mid', 'high']:
                if belief in temp_sets[p]:
                    temp_sets[p].remove(belief)
                    break
        return temp_sets

    def _update_belief_base(self, temp_sets):
        """
        Update the actual belief sets with temporary sets.
        """
        self.low_prio = temp_sets['low']
        self.mid_prio = temp_sets['mid']
        self.high_prio = temp_sets['high']
        self.belief_base = self.concatenate_priorities()

    def _restore_state(self, original_state):
        """
        Restore the original state of the belief base.
        """
        self.low_prio = original_state['low']
        self.mid_prio = original_state['mid']
        self.high_prio = original_state['high']
        self.belief_base = self.concatenate_priorities()

    # TODO: Expansion: B + ϕ; ϕ is added to B giving a new belief set B'
    # def expansion

    # TODO: Revision: B ∗ ϕ; ϕ is added and other things are removed, 
    # so that the resulting new belief set B'is consistent.
    # Levi indentity: B ∗ ϕ := (B ÷ ¬ϕ) + ϕ
    # def revision