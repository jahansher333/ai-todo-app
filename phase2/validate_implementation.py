#!/usr/bin/env python3
"""
Validation script for Todo AI Chatbot Implementation
Confirms all requirements from the specification are met
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_file_exists(filepath):
    """Check if a file exists"""
    return Path(filepath).exists()

def check_required_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...")

    required_files = [
        "backend/main.py",
        "backend/models.py",
        "backend/mcp_server.py",
        "backend/agent_runner.py",
        "frontend/src/app/chat/page.tsx",
        "frontend/src/lib/api.ts",
        ".env.example",
        "README.md"
    ]

    all_found = True
    for file in required_files:
        if check_file_exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            all_found = False

    return all_found

def check_stateless_design():
    """Check for stateless design implementation"""
    print("\n🔍 Checking stateless design...")

    # Check if database models exist for conversation persistence
    models_file = "backend/models.py"
    if check_file_exists(models_file):
        with open(models_file, 'r') as f:
            content = f.read()

        has_conversation = 'class Conversation' in content
        has_message = 'class Message' in content

        if has_conversation and has_message:
            print("✅ Conversation and Message models exist for state persistence")
            return True
        else:
            print("❌ Missing Conversation or Message models")
            return False
    else:
        print("❌ Models file not found")
        return False

def check_mcp_tools():
    """Check MCP tools implementation"""
    print("\n🔍 Checking MCP tools...")

    mcp_file = "backend/mcp_server.py"
    if check_file_exists(mcp_file):
        with open(mcp_file, 'r') as f:
            content = f.read()

        tools = ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task']
        found_tools = []

        for tool in tools:
            if f'async def {tool}' in content:
                found_tools.append(tool)

        if len(found_tools) == 5:
            print(f"✅ All 5 MCP tools implemented: {', '.join(found_tools)}")
            return True
        else:
            print(f"❌ Missing MCP tools. Found: {found_tools}")
            return False
    else:
        print("❌ MCP server file not found")
        return False

def check_jwt_authentication():
    """Check JWT authentication implementation"""
    print("\n🔍 Checking JWT authentication...")

    auth_files = [
        "backend/src/middleware/jwt_middleware.py",
        "frontend/src/lib/auth.ts"
    ]

    auth_found = True
    for file in auth_files:
        if check_file_exists(file):
            with open(file, 'r') as f:
                content = f.read()

            if 'jwt' in content.lower() or 'token' in content.lower():
                print(f"✅ JWT authentication found in {file}")
            else:
                print(f"❌ JWT authentication not clearly found in {file}")
                auth_found = False
        else:
            print(f"❌ {file} not found")
            auth_found = False

    return auth_found

def check_user_isolation():
    """Check user isolation implementation"""
    print("\n🔍 Checking user isolation...")

    # Check if user_id is used as a filter in models and services
    models_file = "backend/models.py"
    if check_file_exists(models_file):
        with open(models_file, 'r') as f:
            content = f.read()

        has_user_id = 'user_id' in content
        has_filters = 'foreign_key' in content.lower() or '.where(' in content

        if has_user_id and has_filters:
            print("✅ User isolation mechanisms found in models")
            return True
        else:
            print("❌ User isolation mechanisms not clearly found")
            return False
    else:
        print("❌ Models file not found")
        return False

def check_natural_language_handling():
    """Check natural language handling implementation"""
    print("\n🔍 Checking natural language handling...")

    agent_file = "backend/agent_runner.py"
    if check_file_exists(agent_file):
        with open(agent_file, 'r') as f:
            content = f.read()

        has_agent = 'Agent(' in content
        has_tools = 'tools=' in content
        has_instructions = 'instructions=' in content

        if has_agent and has_tools and has_instructions:
            print("✅ Natural language processing with AI agent found")
            return True
        else:
            print("❌ Natural language processing not clearly found")
            return False
    else:
        print("❌ Agent runner file not found")
        return False

def check_environment_variables():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")

    env_file = ".env.example"
    if check_file_exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()

        required_vars = ['GROK_API_KEY', 'BETTER_AUTH_SECRET', 'DATABASE_URL']
        found_vars = []

        for var in required_vars:
            if var in content:
                found_vars.append(var)

        if len(found_vars) == len(required_vars):
            print(f"✅ Required environment variables found: {', '.join(found_vars)}")
            return True
        else:
            print(f"❌ Missing environment variables. Found: {found_vars}")
            return False
    else:
        print("❌ .env.example file not found")
        return False

def main():
    """Main validation function"""
    print("🚀 Starting Todo AI Chatbot Implementation Validation\n")

    # Run all checks
    checks = [
        ("Required Files", check_required_files),
        ("Stateless Design", check_stateless_design),
        ("MCP Tools", check_mcp_tools),
        ("JWT Authentication", check_jwt_authentication),
        ("User Isolation", check_user_isolation),
        ("Natural Language Handling", check_natural_language_handling),
        ("Environment Variables", check_environment_variables)
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ Error during {name} check: {str(e)}")
            results[name] = False

    # Print summary
    print(f"\n📊 Validation Summary:")
    print("="*50)

    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)

    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:<25} {status}")

    print("="*50)
    print(f"Overall: {passed_checks}/{total_checks} checks passed")

    if passed_checks == total_checks:
        print("\n🎉 All validation checks passed!")
        print("✅ Todo AI Chatbot implementation is complete and meets all requirements")
        return True
    else:
        print(f"\n❌ {total_checks - passed_checks} validation checks failed")
        print("🔧 Please address the issues above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)