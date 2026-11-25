"""Command-line interface for the food recommendation RAG application."""

from src.rag_pipeline import rag_pipeline

def main():

    print(f"="*50)
    print("  FOOD RECOMMENDATION SYSTEM  ")
    print(f"="*50)

    while True:
        query=input("\nWhat food are you looking for? (or type 'exit'): ").strip()

        if not query:
            print("Please Enter a valid food request.")
            continue

        if query.lower()=="exit":
            print("Thank you for using the Food Recommendation Assistant!")
            break 

        cuisine=input("Preferred cuisine (press Enter to skip): ").strip() or None

        calories_input = input(
            "Maximum calories (press Enter to skip): "
        ).strip()

        max_calories=None

        if calories_input:
            try:
                max_calories=float(calories_input)

                if max_calories < 0 :
                    print("Calories cannot be negative. ")
                    continue

            except ValueError:
                print("Please enter a valid calorie number.")
                continue


        dietary_input = input(
            "Dietary preference (vegetarian/non_vegetarian, "
            "press Enter to skip): "
        ).strip().lower()

        dietary_type = None

        if dietary_input:
            if dietary_input not in ["vegetarian", "non_vegetarian"]:
                print("Please enter vegetarian or non_vegetarian.")
                continue

            dietary_type = dietary_input


        try:
            answer=rag_pipeline(
                query=query,
                cuisine=cuisine,
                max_calories=max_calories,
                dietary_type=dietary_type,
            )

            print("\n---------- RECOMMENDATIONS ----------")
            print(answer)
            print("-------------------------------------")

        except Exception as error:
            print(f"\nSomething went wrong:{error}")

if __name__=="__main__":
    main()

