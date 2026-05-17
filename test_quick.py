import sys
sys.path.insert(0, '.')
from skills.thinking import ThinkingSkill

print("Loading ThinkingSkill...")
t = ThinkingSkill()
print("Calling dialog...")
r = t.execute('dialog', {'message': ''})
print(f"State: {r.get('state')}")
print(f"Done: {r.get('done')}")
print(f"Response: {r.get('response', '')[:200]}")
print("\nTest PASSED")