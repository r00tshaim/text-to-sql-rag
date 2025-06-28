from agent.agent import build_agent
from agent.utils import create_ecommerce_db
import os



if __name__ == "__main__":
    app = build_agent()
    while True:
        user_input = input('> ')
        if not user_input.split():
            continue
        result = app.invoke({"question": user_input, "attempts": 0})
        print("\n🤖Response:", result["query_result"])