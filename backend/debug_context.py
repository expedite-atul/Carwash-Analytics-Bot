from app.agent import process_user_question
import asyncio

async def test_context():
    # 1. First Turn: "Show active vehicles"
    print("\n--- Turn 1 (No Context) ---")
    res1 = await process_user_question("How many active vehicles do we have?")
    print(f"SQL 1: {res1.get('sql')}")
    
    # 2. Second Turn: "Filter THAT by make Tesla"
    # We manually simulate the history string that would come from the DB
    history = "User: How many active vehicles do we have?\nAI: SELECT count(*) FROM vehicle WHERE active = 1;"
    
    print("\n--- Turn 2 (With Context) ---")
    print(f"Injecting History:\n{history}")
    res2 = await process_user_question("Filter that to only show Teslas", chat_history=history)
    print(f"SQL 2: {res2.get('sql')}")

    if "Tesla" in res2.get('sql', '') or "tesla" in res2.get('sql', ''):
        print("\nSUCCESS: Context used!")
    else:
        print("\nFAIL: Context ignored.")

if __name__ == "__main__":
    asyncio.run(test_context())
