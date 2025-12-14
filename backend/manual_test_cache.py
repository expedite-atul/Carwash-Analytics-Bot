
import sys
import os


from app.agent import get_exact_match, add_golden_query, embeddings

def test_caching():
    print("🧪 Starting Semantic Cache Test...")
    
    q1 = "How many active users are there?"
    sql1 = "SELECT count(*) FROM users WHERE active = true;"
    
    # 1. Clean up potential previous run
    # (Optional, purely implementation dependent)
    
    # 2. Add to Cache
    print(f"   Adding: '{q1}'")
    add_golden_query(q1, sql1)
    
    # 3. Test Exact Match
    print("   Testing Exact Match...")
    match = get_exact_match(q1)
    if match == sql1:
        print("   ✅ Exact match found!")
    else:
        print(f"   ❌ Exact match FAILED. Got: {match}")
        
    # 4. Test Semantic Match (slightly different wording)
    q2 = "Total count of active users?"
    print(f"   Testing Semantic Match: '{q2}'")
    match2 = get_exact_match(q2, threshold=0.2) # Relax threshold for this test
    if match2 == sql1:
        print("   ✅ Semantic match found (with relaxed threshold)!")
    else:
        print(f"   ⚠️ Semantic match missed (might be strict threshold). Got: {match2}")
        
    # 5. Test Irrelevant
    q3 = "What is the capital of France?"
    print(f"   Testing Irrelevant: '{q3}'")
    match3 = get_exact_match(q3)
    if match3 is None:
        print("   ✅ Computed correctly as NO MATCH.")
    else:
        print(f"   ❌ False Positive! Got: {match3}")

if __name__ == "__main__":
    try:
        test_caching()
    except Exception as e:
        print(f"💥 Error: {e}")
