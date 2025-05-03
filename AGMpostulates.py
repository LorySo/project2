from beliefbase import BeliefBase

class TestAGMPostulates:

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

    # TODO: Inclusion postulate 
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


    # TODO: Vacuity postulate
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

    # TODO: Succes postulate
    #def test_postulate_revision_succes():

    # TODO: Inclusion postulate 
    #def test_postulate_revision_inclusion():

    # TODO: Vacuity postulate
    #def test_postulate_revision_vacuity():

    # TODO: Consistency
    #def test_postulate_revision_consistency():

    # TODO: Extensionality
    #def test_postulate_revision_extensionality():

    def run_all_postulate_test(self):
        self.test_postulate_contraction_succes()
        self.test_postulate_contraction_inclusion()
        self.test_postulate_contraction_vacuity()