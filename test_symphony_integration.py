"""
Test full symphony dialog - multi-turn
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_symphony_openclaw import SymphonySession

session = SymphonySession()

# Turn 1: User starts with requirement
print("=== Turn 1 ===")
result1 = session.handle("我想做量化交易")
print(f"State: {result1['state']}")
print(f"Response: {result1['response']}")
print()

# Turn 2: User responds to clarifying question
print("=== Turn 2 ===")
result2 = session.handle("没任何基础，新手")
print(f"State: {result2['state']}")
print(f"Response: {result2['response']}")
