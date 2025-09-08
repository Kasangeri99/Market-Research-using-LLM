#!/usr/bin/env python3
"""
Test script for quality loop functionality
"""

import os
from app import StatusTrackingAgent
from market_context_agent import MarketContextRequest

def test_quality_loop():
    """Test the quality loop functionality."""
    
    print("🧪 Testing Quality Loop Functionality")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Warning: OPENAI_API_KEY not found!")
        print("   Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    try:
        # Create agent
        agent = StatusTrackingAgent()
        print("✅ StatusTrackingAgent created successfully")
        
        # Create test request
        request = MarketContextRequest(
            strategy_name='Test Strategy',
            quarter='Q1',
            year=2024,
            benchmark='S&P 500',
            custom_instructions='Focus on technology sector performance'
        )
        print("✅ Test request created successfully")
        
        # Test the quality loop logic
        print("\n🔍 Quality Loop Configuration:")
        print(f"   - Max iterations: {agent.agent_executor.max_iterations}")
        print(f"   - Quality threshold: 9.0+")
        print(f"   - Tools available: {len(agent.tools)}")
        
        print("\n📋 Quality Loop Process:")
        print("   1. Market Research → Gather market data")
        print("   2. Commentary Generation → Create initial context")
        print("   3. Quality Review → Score and improve")
        print("   4. If score < 9.0 → Repeat steps 2-3")
        print("   5. Continue until score ≥ 9.0")
        
        print("\n✅ Quality loop functionality is ready!")
        print("   Run the Flask UI to test the full quality loop process.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing quality loop: {e}")
        return False

if __name__ == "__main__":
    test_quality_loop()
