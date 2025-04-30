from beliefbase import BeliefBase

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
        print("5. Back to the original belief base")
        print("6. Quit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            user_input = input("Enter a logical formula (optionally add priority at end, e.g., 'p | q high'): ")
            formula, priority = parse_input_with_optional_priority(user_input)
            belief_base.add_with_priority(formula, priority)
            print(f"Added belief: {formula} (priority: {priority})")

        elif choice == '2':
            user_input = input("Enter a logical formula (e.g., p | q, ~p, p >> q): ")
            entails = belief_base.resolution(user_input)
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
            print("Not implemented.")

        elif choice == '6':
            print("Exiting. Goodbye!")
            break

        elif choice == '7':
            # Test 1
            #print(belief_base.resolution("r")) #should be true
            #print(belief_base.resolution("~r")) #should be false
            
            # Test 2
            #print(belief_base.resolution("~p | q")) # should be true
            test_contraction_slides10_1(belief_base)
            test_contraction_slides10_2(belief_base)


        else:
            print("Invalid choice. Please try again.")
def parse_input_with_optional_priority(user_input):
    user_input = user_input.strip()
    for priority in ("low", "mid", "high"):
        if user_input.endswith(" " + priority):
            formula = user_input[:-(len(priority)+1)].strip()
            return formula, priority
    return user_input, "low"

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

if __name__ == "__main__":
    main()