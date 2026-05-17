import sys
sys.path.insert(0, '.')

print("Step 1: import SymphonySession")
from agent_symphony_openclaw import SymphonySession, call_openclaw_gateway_rpc

print("Step 2: test Gateway RPC")
result = call_openclaw_gateway_rpc("memory.recall", {"query": "test", "limit": 1})
print(f"  RPC result keys: {list(result.keys())}")
print(f"  success: {result.get('success', 'N/A')}")

print("Step 3: create session")
s = SymphonySession()

print("Step 4: inject_user_memory")
inj = s.inject_user_memory("石榴籽", max_results=3)
print(f"  injected={inj['injected_count']}, success={inj['success']}")

print("Step 5: handle dialog")
r = s.handle("我想搞量化")
print(f"  state={r['state']}, questions={len(r['questions'])}")

print("=== DONE ===")