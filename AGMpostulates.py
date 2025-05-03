from beliefbase import BeliefBase

class TestAGMPostulates:

    def test_postulate_succes_contraction(self):
        """
        Success: If ϕ /∈ Cn(∅), then ϕ /∈ Cn(B ÷ ϕ) the outcome does not contain ϕ
        """
        base = BeliefBase(initial_beliefs=[
            ("p", 'high'),
            ("p >> q", 'mid'), 
            ("q", 'low')
        ]) 
        phi = "q"
        base.contraction(phi)
        entails_q = base.resolution(base.belief_base, phi)
        assert entails_q is False
        print("Passed: Succes AGM postulate for contraction test")

    

    def run_all_postulate_test(self):
        self.test_postulate_succes_contraction()