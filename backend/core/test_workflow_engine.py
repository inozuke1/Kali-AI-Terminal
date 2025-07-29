import asyncio
import json
import logging
from datetime import datetime

from core.workflow_engine import AdvancedWorkflowEngine

# Initialize Workflow Engine
workflow_engine = AdvancedWorkflowEngine()

logging.basicConfig(level=logging.INFO)

async def run_test_scenario(request_text, expected_intent):
    """Run a single test scenario to check if the workflow engine produces expected results"""
    context = {}
    print(f"\nRunning test scenario: {request_text}")

    result = await workflow_engine.process_natural_language_request(request_text, context)

    if result['thinking']['extracted_intent'] == expected_intent:
        print(f"\nTest result: SUCCESS\nExtracted Intent: {result['thinking']['extracted_intent']}\n")
    else:
        print(f"\nTest result: FAILURE\nExpected Intent: {expected_intent}, Extracted Intent: {result['thinking']['extracted_intent']}\n")

    return result

async def main():
    """Main test runner function"""
    scenarios = [
        {"request": "Scan ports on example.com", "intent": "reconnaissance"},
        {"request": "Check for vulnerabilities on 192.168.1.1", "intent": "vulnerability_scan"},
        {"request": "Analyze the local network", "intent": "network_analysis"}
    ]

    for scenario in scenarios:
        await run_test_scenario(scenario['request'], scenario['intent'])

if __name__ == "__main__":
    asyncio.run(main())
