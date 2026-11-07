from app.graph import graph


def main():
    print("Resolve - Customer Support Chatbot")
    print("Type 'exit' to quit.\n")

    config = {
        "configurable": {
            "thread_id": "resolve-session-1"
        }
    }

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            continue

        result = graph.invoke(
            {"messages": [("human", query)]},
            config=config
        )

        print(f"\nResolve: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()