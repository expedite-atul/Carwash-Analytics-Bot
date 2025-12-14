from app.agent import execute_approved_sql
import json
import logging

# Configure logging to see SQL
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def test(name, sql):
    print(f"\n--- {name} ---")
    print(f"SQL: {sql}")
    try:
        res = execute_approved_sql(sql)
        print(json.dumps({
            "status": res.get("status"), 
            "type": res.get("type"), 
            "chartType": res.get("chartType"),
            "data_keys": list(res.get("data", {}).keys())
        }, indent=2))

        if res.get("type") == "table" and len(res.get("data", {}).get("rows", [])) > 0:
            row = res["data"]["rows"][0]
            print(f"DEBUG ROW TYPES: {[type(v) for v in row.values()]}")
        
        if res.get("type") == "chart":
             print(f"SUCCESS: Detected as {res['chartType']}")
        else:
             print(f"FAIL: Detected as {res.get('type')}")
             
    except Exception as e:
        print(f"ERROR: {e}")

# Pie Chart Test (Small categorical)
test("Pie Candidate", "SELECT status, count(*) FROM membership_account GROUP BY status")

# Line Chart Test (Date series)
test("Line Candidate", "SELECT created_at::date, count(*) FROM \"customer\" GROUP BY created_at::date ORDER BY created_at::date LIMIT 5")

# Bar Chart Test (Categorical)
test("Bar Candidate", "SELECT name, billing_amount FROM membership_account LIMIT 5")
