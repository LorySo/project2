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
            user_input = input("Enter a logical formula (e.g., p | q, ~p, p >> q): ")
            belief_base.add(user_input)

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
            print("4")

        elif choice == '6':
            print("Exiting. Goodbye!")
            break

        #elif choice == '4':
            # Test 1
            #print(belief_base.resolution("r")) #should be true
            #print(belief_base.resolution("~r")) #should be false
            
            # Test 2
         #   print(belief_base.resolution("~p | q")) # should be true


        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()