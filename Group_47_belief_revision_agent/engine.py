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
        print("4. Initialiaze with dummy data")
        print("5. Clear current belief base")
        print("6. Running all AGM postulates tests")
        print("7. Quit")

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
                print("Belief Base is empty.")

        elif choice == '4':
            belief_base.add_with_priority('p | q', 'low')
            belief_base.add_with_priority('p & q', 'mid')
            belief_base.add_with_priority('(p & q) >> r', 'mid')

        elif choice == '5':
            print("\nClearing the current Belief Base:")
            belief_base.clear()

        elif choice == '6':
            postulates = TestAGMPostulates()
            postulates.run_all_postulate_test()

        elif choice == '7':
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


if __name__ == "__main__":
    main()