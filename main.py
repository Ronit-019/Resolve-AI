from app.graph import graph


def main():
    print("Resolve - Customer Support Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            continue

        result = graph.invoke({
            "user_input": query,
            "response": ""
        })

        print(f"\nResolve: {result['response']}\n")


if __name__ == "__main__":
    main()