import uuid
from app.graph import graph


def create_session():
    return {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }


def main():
    print("Resolve - Customer Support Chatbot")
    print("Commands: /new = New conversation | exit = Quit\n")

    config = create_session()

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if query.lower() == "/new":
            config = create_session()
            print("\nStarted a new conversation.\n")
            continue

        if not query:
            continue

        result = graph.invoke(
            {"messages": [("human", query)]},
            config=config
        )

        print(f"\nResolve: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()