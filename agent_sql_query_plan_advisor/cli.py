"""CLI for agent-sql-query-plan-advisor."""
import sys
import argparse
from .advisor import SQLQueryAdvisor

def main():
    parser = argparse.ArgumentParser(description="Agent SQL Query Plan Advisor CLI")
    parser.add_argument("--demo", action="store_true", help="Analyze sample SQL query")
    args = parser.parse_args()

    if args.demo:
        advisor = SQLQueryAdvisor()
        query = "SELECT * FROM orders WHERE customer_id = 99 AND status = 'active' ORDER BY created_at DESC"
        res = advisor.analyze_query(query)
        print(f"Full Scan Risk: {res.has_full_scan_risk}")
        print(f"Filters: {res.identified_filters}")
        print(f"Recommended DDL: {res.recommended_index_ddl}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
