from sympy.logic.boolalg import to_cnf, And, Or
from sympy import sympify
from itertools import combinations

class BeliefBase:
    """Representation of the belief base"""
    belief_base = set()

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

        print(kb)
        while True:
            new_clauses = set()
            
            for ci, cj in combinations(kb, 2):
                print(ci, cj)
                resolvents = self.resolve(ci, cj)
                print(resolvents)
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


def main():
    belief_base = BeliefBase()

    print("=== Belief Revision Agent ===")

    while True:
        print("\nOptions:")
        print("1. Add a new belief")
        print("2. Show current belief base")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            print(f"Added belief: ")

        elif choice == '2':
            print("\nCurrent Belief Base:")
            print(belief_base.belief_base)

        elif choice == '3':
            print("Exiting. Goodbye!")
            break

        elif choice == '4':
            # Test 1
            #print(belief_base.resolution("r")) #should be true
            #print(belief_base.resolution("~r")) #should be false
            
            # Test 2
            print(belief_base.resolution("~p | q")) # should be true


        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()