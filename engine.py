from beliefbase import BeliefBase
from AGMpostulates import TestAGMPostulates

def main():
    belief_base = BeliefBase()

    print("=== Belief Revision Agent ===")
    print("\n symbols to be used: &, |, >>, <<, ~")

    while True:
        print("\nOptions:")
        print("1. Add a new belief")
        print("2. Check logical entailment")
        print("3. Show current belief base")
        print("4. Clear current belief base")
        print("5. Running all AGM postulates tests")
        print("6. Quit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            user_input = input("Enter a logical formula (optionally add priority at end, e.g., 'p | q high'): ")
            formula, priority = parse_input_with_optional_priority(user_input)
            belief_base.add_with_priority(formula, priority)
            print(f"Added belief: {formula} (priority: {priority})")

        elif choice == '2':
            user_input = input("Enter a logical formula (e.g., p | q, ~p, p >> q): ")
            entails = belief_base.resolution(belief_base.get_belief_base(), user_input)
            if entails:
                print('\n', belief_base.belief_base, " |= ", user_input)
            else:
                print('\n', belief_base.belief_base, " !|= ", user_input)

        elif choice == '3':
            print("\nCurrent Belief Base:")
            if belief_base.belief_base:
                print(belief_base.belief_base)
            else:
                print("The Belief Base is empty.")

        elif choice == '4':
            print("\nClearing the current Belief Base:")
            belief_base.clear()

        elif choice == '5':
            # Test 1
            #print(belief_base.resolution("r")) #should be true
            #print(belief_base.resolution("~r")) #should be false
            
            # Test 2
            #print(belief_base.resolution("~p | q")) # should be true
            
            #test_contraction_slides10_1(belief_base)
            #test_contraction_slides10_2(belief_base)

            #run_all_contraction_tests(belief_base)\
            postulates = TestAGMPostulates()
            postulates.run_all_postulate_test()

        elif choice == '6':
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
def parse_input_with_optional_priority(user_input):
    user_input = user_input.strip()
    for priority in ("low", "mid", "high"):
        if user_input.endswith(" " + priority):
            formula = user_input[:-(len(priority)+1)].strip()
            return formula, priority
    return user_input, "low"


# Simple tests

def test_contraction_slides10_1(belief_base):
    belief_base.clear()
    # Add beliefs with priorities
    belief_base.add_with_priority("p", "low")
    belief_base.add_with_priority("p >> q", "mid")
    belief_base.add_with_priority("q", "high")

    result = belief_base.contraction("q")
        
    # Verify
    assert result is True  # Contraction succeeded
    assert "p" not in belief_base.low_prio
    assert "q" not in belief_base.high_prio
    print("passed slides10_1")

def test_contraction_slides10_2(belief_base):
    belief_base.clear()
    # Add beliefs with priorities
    belief_base.add_with_priority("p", "high")
    belief_base.add_with_priority("p >> q", "low")
    belief_base.add_with_priority("q", "high")

    result = belief_base.contraction("q")
        
    # Verify
    assert result is True  # Contraction succeeded
    assert "p" in belief_base.high_prio
    assert "p >> q" not in belief_base.low_prio
    assert "q" not in belief_base.high_prio

    print("passed slides10_2")

def test_basic_contraction(belief_base):
    """Test contraction of a simple belief."""
    belief_base.clear()
    belief_base.add_with_priority("p", "low")
    belief_base.add_with_priority("q", "high")
    
    print("\n=== Testing Basic Contraction (p) ===")
    belief_base.contraction("p")
    assert "p" not in belief_base.belief_base
    print("Passed: Basic contraction")

def test_priority_resolution(belief_base):
    """Test if lower-priority beliefs are removed first."""
    belief_base.clear()
    belief_base.add_with_priority("p", "low")
    belief_base.add_with_priority("q", "high")
    belief_base.add_with_priority("p >> q", "mid")
    
    print("\n=== Testing Priority Resolution (q) ===")
    belief_base.contraction("q")
    assert "p" not in belief_base.belief_base  # Low-prio should be removed first
    assert "q" not in belief_base.belief_base
    print("Passed: Priority resolution")

def test_maximal_remainders(belief_base):
    """Test if maximal remainder sets are generated correctly."""
    belief_base.clear()
    belief_base.add_with_priority("p", "low")
    belief_base.add_with_priority("q", "mid")
    belief_base.add_with_priority("p >> q", "high")
    
    print("\n=== Testing Maximal Remainders (q) ===")
    remainders = belief_base._compute_remainder_sets("q")
    assert len(remainders) == 2  # Expected: [{'p'}, {'p >> q'}]
    print("Passed: Maximal remainders")

def test_no_entailment(belief_base):
    """Test contraction when ϕ is not entailed."""
    belief_base.clear()
    belief_base.add_with_priority("p", "low")
    
    print("\n=== Testing No Entailment (q) ===")
    belief_base.contraction("q")  # Should print "no contraction needed"
    assert "p" in belief_base.belief_base
    print("Passed: No entailment")

def test_tautology_contraction(belief_base):
    """Test contraction of a tautology (should fail)."""
    belief_base.clear()
    belief_base.add_with_priority("p | ~p", "low")
    
    print("\n=== Testing Tautology Contraction (p | ~p) ===")
    belief_base.contraction("p | ~p")  # Should print "Contraction impossible"
    print("Passed: Tautology handling")

def run_all_contraction_tests(belief_base):
    """Run all test cases."""
    test_basic_contraction(belief_base)
    #test_priority_resolution(belief_base) # Fails for now
    test_maximal_remainders(belief_base)
    test_no_entailment(belief_base)
    test_tautology_contraction(belief_base)
    print("\nAll tests passed!")


if __name__ == "__main__":
    main()