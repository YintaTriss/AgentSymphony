"""
Test new flow: thinking selects experts directly, spawns jury subprocess
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.thinking.skill import ThinkingSkill

# Mock SharedContext for testing
class MockContext:
    def __init__(self):
        self._data = {}
        self.llm = None

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def call_llm(self, prompt, system=None, max_tokens=512):
        return "[LLM mock]"

# Create thinking skill
os.environ['OPENCLAW_WORKSPACE'] = os.path.dirname(os.path.abspath(__file__))
thinking = ThinkingSkill()

# Override context with mock
thinking._context = MockContext()

# Test 1: Expert selection
print("=== Test 1: Expert Selection ===")
selected = thinking._select_perspectives_for("clarifying", "build a chrome extension that translates web pages")
print(f"Selected experts: {selected}")

# Test 2: Full clarifying flow
print("\n=== Test 2: Clarifying Flow ===")
thinking._context = MockContext()
result1 = thinking._clarify_requirement("I want to build a chrome extension that translates web pages")
print(f"Round 1 response: {result1['response'][:100]}")
print(f"State: {result1['state']}")
print(f"Jury status: {result1.get('jury_status', 'N/A')}")

# Check jury result path
result_file = thinking._get_jury_result_path()
print(f"Jury result file: {result_file}")
print(f"File exists: {os.path.exists(result_file)}")
