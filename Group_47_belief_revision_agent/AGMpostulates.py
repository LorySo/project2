from beliefbase import BeliefBase
import copy

class TestAGMPostulates:
    
    
    # --- Contraction Postulates ---
    def test_postulate_contraction_succes(self):
        """
        Success: If ϕ /∈ Cn(∅), then ϕ /∈ Cn(B ÷ ϕ) 
        the outcome does not contain ϕ
        """
        base = BeliefBase(initial_beliefs=[
            ("p", 'high'),
            ("p >> q", 'mid'), 
            ("q", 'low')
        ]) 
        phi = "q"
        base.contraction(phi)

        entails_q = base.resolution(base.belief_base, phi)
        assert entails_q is False , "After contraction, q should not be entailed"

        print("Passed: Succes AGM postulate for contraction test")

    def test_postulate_contraction_inclusion(self):
        """
        Inclusion: B ÷ ϕ ⊆ B 
        the outcome is a subset of the original set
        """
        base = BeliefBase(initial_beliefs=[
            ("p", 'high'),
            ("p >> q", 'mid'), 
            ("q", 'low')
        ])
        phi = "q"
        original_beliefs = base.belief_base.copy()
        base.contraction(phi)

        issubset = base.belief_base.issubset(original_beliefs)
        assert issubset is True , "Contracted set is not a subset of original"
        
        print("Passed: Inclusion AGM postulate for contraction test")

    def test_postulate_contraction_vacuity(self):
        """
        Vacuity: If ϕ /∈ Cn(B), then B ÷ ϕ = B
        if the incoming sentence is not in the original set then there is no effect
        """
        base = BeliefBase(initial_beliefs=[
            ("p", 'high'),
            ("p >> q", 'mid'), 
            ("q", 'low')
        ])
        original_beliefs = base.belief_base.copy()
        phi = "r"
        base.contraction(phi)

        assert base.belief_base == original_beliefs , "Base changed when contracting non-entailed belief"

        print("Passed: Vacuity AGM postulate for contraction test")

    # TODO: Extensionality
    def test_postulate_contraction_extensionality(self):
        """
        Extensionality: If ϕ ↔ ψ ∈ Cn(∅), then B ÷ ϕ = B ÷ ψ.
        the outcomes of contracting with equivalent sentences are the same
        """
        initial = [("p", 'high'), ("p >> q", 'mid'), ("q", 'low')]
        base1 = BeliefBase(initial)
        base2 = BeliefBase(initial)

        # Logically equivalent formulas (ϕ ↔ ψ is a tautology)
        phi, psi = "q | r", "r | q" 

        base1.contraction(phi)
        base2.contraction(psi)

        # Check if the contracted bases are logically equivalent
        assert self.logically_equivalent(base1, base2), \
            f"Extensionality violated for contraction: B ÷ {phi} ≠ B ÷ {psi}"
        
        print("Passed: Extensionality AGM postulate for contraction test")


    # --- Contraction Postulates ---
    def test_postulate_revision_succes(self):
        """
        Success: ϕ ∈ B * ϕ
        The new belief is included in the revised set.
        """
        base = BeliefBase(initial_beliefs=[
            ("p", 'high'),
            ("p >> q", 'mid')
        ])
        phi = "q"
        base.revision(phi)

        entails_q = base.resolution(base.belief_base, phi)
        assert entails_q, "After revision, q should be entailed"

        print("Passed: Success AGM postulate for revision test")

    def test_postulate_revision_inclusion(self):
        """
        Inclusion: B * ϕ ⊆ B + ϕ
        The revised set is a subset of the expanded set.
        """
        base = BeliefBase(initial_beliefs=[
            ("p", 'high'),
            ("p >> q", 'mid')
        ])
        phi = "q"

        expanded = copy.deepcopy(base)
        expanded.expansion(phi)

        base.revision(phi)

        assert base.belief_base.issubset(expanded.belief_base) is True, "Revision should be a subset of the expansion"

        print("Passed: Inclusion AGM postulate for revision test")

    # TODO: Add more cases
    def test_postulate_revision_vacuity(self):
        """
        Vacuity: If ¬ϕ /∈ B, then B * ϕ = B + ϕ
        If ϕ is consistent with B, revision is equivalent to expansion.
        """
        initial_beliefs=[
            ("p", 'high'),
            ("p >> q", 'mid')
        ]
        base = BeliefBase(initial_beliefs)
        phi = "q"
        
        # Perform expansion (B + ϕ)
        expanded = BeliefBase(initial_beliefs)
        expanded.expansion(phi)  # Adds q and closes under logical consequence
        
        # Perform revision (B * ϕ)
        base.revision(phi)
        
        # Check if B * ϕ equals B + ϕ
        assert base.belief_base == expanded.belief_base, \
            f"Revision ≠ expansion when ϕ is consistent. Expected {expanded.belief_base}, got {base.belief_base}"
        
        
        print("Passed: Vacuity AGM postulate for revision test")

    def test_postulate_revision_consistency(self):
        """
        Consistency: B * ϕ is consistent if ϕ is consistent
        """
        # Case 1: ϕ is consistent with B
        base = BeliefBase(initial_beliefs=[("p", 'high')])
        phi = "q"  # Consistent with B
        base.revision(phi)
        
        # Check if B * ϕ is consistent (no p ∧ ¬p, q ∧ ¬q, etc.)
        assert not base.resolution(base.belief_base, "False"), \
            "B * ϕ must be consistent when ϕ is consistent"
        
        # Case 2: ϕ contradicts B (tests conflict resolution)
        conflict_base = BeliefBase(initial_beliefs=[("p", 'high'), ("¬p", 'mid')])
        conflict_phi = "p"  # Directly contradicts "¬p" in B
        conflict_base.revision(conflict_phi)
        
        # After revision, B * ϕ should be consistent (e.g., removed "¬p")
        assert not conflict_base.resolution(conflict_base.belief_base, "False"), \
            "B * ϕ must resolve conflicts to maintain consistency"

        print("Passed: Consistency AGM postulate for revision test")

    def test_postulate_revision_extensionality(self):
        """
        Extensionality: If (ϕ ↔ ψ) ∈ Cn(∅), then B * ϕ = B * ψ
        """
        initial = [
            ("p", 'high'),
            ("p >> q", 'mid')  # "p >> q" denotes p → q
        ]
        base1 = BeliefBase(initial)
        base2 = BeliefBase(initial)

        # Logically equivalent formulas (ϕ ↔ ψ)
        phi = "q | r"          # ϕ
        psi = "r | q"          # ψ (equivalent to ϕ)

        # Check if the two formulas are equivalente
        assert set(phi.split()) == set(psi.split())

        base1.revision(phi)
        base2.revision(psi)
        
        assert self.logically_equivalent(base1, base2), \
            f"Extensionality violated: B * {phi} ≠ B * {psi}"

        print("Passed: Extensionality AGM postulate for revision test")

    def logically_equivalent(self, base1, base2):
        """
        Check if two belief bases are logically equivalent
        """
        # Check all beliefs in base1 are entailed by base2
        for belief in base1.belief_base:
            if not base2.resolution(base2.belief_base, belief):
                return False
        
        # Check all beliefs in base2 are entailed by base1
        for belief in base2.belief_base:
            if not base1.resolution(base1.belief_base, belief):
                return False
    
        return True


    def run_all_postulate_test(self):
        print("\n ---- AGM postulates for contraction ----\n")
        self.test_postulate_contraction_succes()
        self.test_postulate_contraction_inclusion()
        self.test_postulate_contraction_vacuity()
        self.test_postulate_contraction_extensionality()

        print("\n ---- AGM postulates for revision ----\n")
        self.test_postulate_revision_succes()
        self.test_postulate_revision_inclusion()
        self.test_postulate_revision_vacuity()
        self.test_postulate_revision_consistency()
        self.test_postulate_revision_extensionality()