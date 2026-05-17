#!/usr/bin/env python
"""
AgentSymphony CLI - 交互式入口

用法：
  python agent_symphony_cli.py "你的需求"
  python agent_symphony_cli.py -i        # 交互模式
  python agent_symphony_cli.py --test   # 测试对话模式
"""

import sys
import os

# 添加父目录到路径
SYMPHONY_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SYMPHONY_PATH)

from agent_symphony.skills.thinking import ThinkingSkill
from agent_symphony.skills.memory import MemorySkill
from agent_symphony.skills.search import SearchSkill
from agent_symphony.shared import SharedContext


class SymphonyRunner:
    """交响乐运行器 - 用于测试 dialog 模式"""
    
    def __init__(self):
        self.context = SharedContext()
        self.thinking = ThinkingSkill()
        self.memory = MemorySkill()
        self.search = SearchSkill()
        
        # 链接技能
        self.thinking.link_skill("memory", self.memory)
        self.thinking.link_skill("search", self.search)
        
        # 标记为用户直接调用
        self.context.set_caller("user", "cli")
    
    def run_once(self, message: str, answers: dict = None, skill_results: dict = None) -> dict:
        """运行一次对话"""
        return self.thinking.execute("dialog", {
            "message": message or "",
            "answers": answers or {},
            "skill_results": skill_results or {}
        })
    
    def run_interactive(self):
        """交互模式"""
        print("=" * 50)
        print("🎵 AgentSymphony 交响乐 - 指挥模式")
        print("=" * 50)
        print()
        print("输入 'q' 退出，输入 'restart' 重新开始")
        print()
        
        done = False
        
        while not done:
            # 获取用户输入
            user_input = input("\n👤 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("\n👋 再见！")
                break
            
            if user_input.lower() == 'restart':
                # 重新开始
                self.context = SharedContext()
                self.thinking = ThinkingSkill()
                self.thinking.link_skill("memory", self.memory)
                self.thinking.link_skill("search", self.search)
                print("\n🔄 已重新开始\n")
                # 重新触发开场
                result = self.run_once("")
                print(f"\n🎵 指挥: {result.get('response', '')}")
                continue
            
            # 运行对话
            result = self.run_once(user_input)
            
            # 打印回复
            response = result.get("response", "")
            print(f"\n🎵 指挥: {response}")
            
            # 处理技能申请
            skill_requests = result.get("skill_requests", [])
            if skill_requests:
                print(f"\n📋 技能申请: {len(skill_requests)} 个")
                for req in skill_requests:
                    skill = req.get("skill", "?")
                    action = req.get("action", "?")
                    print(f"  - {skill}.{action}")
                
                # 模拟执行（简化版）
                # 实际使用时 OpenClaw 会执行这些
                results = {}
                for req in skill_requests:
                    skill = req.get("skill")
                    # 这里简化处理，不真正执行
                    results[skill] = {"success": True, "data": {}}
                
                # 回调结果
                result = self.run_once("", skill_results=results)
                if result.get("response"):
                    print(f"\n🎵 指挥: {result.get('response', '')}")
            
            # 检查是否完成
            done = result.get("done", False)
            if done:
                print("\n✅ 交响乐会话结束")
        
        print("\n" + "=" * 50)


def test_dialog_mode():
    """测试对话模式"""
    print("=" * 50)
    print("🎵 测试对话模式")
    print("=" * 50)
    
    runner = SymphonyRunner()
    
    # 测试1: 开场
    print("\n\n【测试1: 开场】")
    result = runner.run_once("")
    print(f"指挥: {result.get('response', '')}")
    print(f"状态: {result.get('state', '?')}, 完成: {result.get('done', '?')}")
    
    # 测试2: 提出需求
    print("\n\n【测试2: 提出需求】")
    result = runner.run_once("我想搞量化交易")
    print(f"指挥: {result.get('response', '')}")
    print(f"状态: {result.get('state', '?')}, 完成: {result.get('done', '?')}")
    
    # 如果需要澄清
    if result.get("questions"):
        print(f"\n问题: {len(result['questions'])} 个")
        for q in result["questions"][:2]:
            print(f"  - {q.get('question', '')}")
    
    # 测试3: 回答问题
    print("\n\n【测试3: 回答问题】")
    result = runner.run_once("完全新手，想实盘赚钱")
    print(f"指挥: {result.get('response', '')}")
    print(f"状态: {result.get('state', '?')}, 完成: {result.get('done', '?')}")
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")


def main():
    args = sys.argv[1:]
    
    if "--test" in args or "-t" in args:
        test_dialog_mode()
    elif "-i" in args or "--interactive" in args:
        runner = SymphonyRunner()
        runner.run_interactive()
    elif len(args) == 0:
        print("AgentSymphony CLI")
        print()
        print("用法:")
        print("  python agent_symphony_cli.py -i          # 交互模式")
        print("  python agent_symphony_cli.py --test     # 测试对话模式")
        print("  python agent_symphony_cli.py \"你的需求\"   # 单次对话")
    else:
        requirement = " ".join(args)
        runner = SymphonyRunner()
        result = runner.run_once(requirement)
        print(f"\n🎵 指挥: {result.get('response', '')}")


if __name__ == "__main__":
    main()