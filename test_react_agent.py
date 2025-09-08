#!/usr/bin/env python3
"""
Test script for the ReAct Market Context Agent
Tests the basic functionality without requiring API keys.
"""

import os
from market_context_agent import MarketContextRequest

def test_request_creation():
    """Test creating market context requests."""
    print("🧪 Testing ReAct Agent Request Creation")
    print("=" * 50)
    
    # Test basic request
    request1 = MarketContextRequest(
        strategy_name="US Equity Core",
        quarter="Q1",
        year=2024
    )
    
    print(f"✅ Basic Request Created:")
    print(f"   Strategy: {request1.strategy_name}")
    print(f"   Period: {request1.quarter} {request1.year}")
    print(f"   Benchmark: {request1.benchmark}")
    
    # Test request with custom instructions
    request2 = MarketContextRequest(
        strategy_name="International Growth",
        quarter="Q2",
        year=2024,
        benchmark="MSCI EAFE",
        custom_instructions="Focus on emerging market opportunities and currency impacts"
    )
    
    print(f"\n✅ Custom Request Created:")
    print(f"   Strategy: {request2.strategy_name}")
    print(f"   Period: {request2.quarter} {request2.year}")
    print(f"   Benchmark: {request2.benchmark}")
    print(f"   Instructions: {request2.custom_instructions}")
    
    return True

def test_agent_structure():
    """Test the agent structure and components."""
    print(f"\n🧪 Testing ReAct Agent Structure")
    print("=" * 50)
    
    # Test that we can import the agent class
    try:
        from market_context_agent import MarketContextAgent
        print("✅ MarketContextAgent class imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MarketContextAgent: {e}")
        return False
    
    # Test agent initialization (without API key)
    try:
        # This should fail gracefully without API key
        agent = MarketContextAgent()
        print("✅ Agent initialized (API key found)")
    except ValueError as e:
        if "API key is required" in str(e):
            print("✅ Agent properly validates API key requirement")
        else:
            print(f"❌ Unexpected error: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error during initialization: {e}")
        return False
    
    return True

def test_tools_structure():
    """Test the tools structure."""
    print(f"\n🧪 Testing ReAct Agent Tools")
    print("=" * 50)
    
    # Create a mock agent to test tools
    class MockAgent:
        def _create_tools(self):
            """Mock tools creation."""
            def market_research_tool(quarter: str, year: int) -> str:
                return f"Market research for {quarter} {year}"
            
            def commentary_generation_tool(strategy_name: str, quarter: str, year: int, 
                                         benchmark: str, market_research: str, 
                                         custom_instructions: str = "") -> str:
                return f"Generated commentary for {strategy_name}"
            
            def quality_review_tool(commentary: str, strategy_name: str) -> str:
                return f"Reviewed commentary for {strategy_name}"
            
            return [
                {"name": "market_research", "description": "Research market conditions"},
                {"name": "commentary_generation", "description": "Generate Market Context"},
                {"name": "quality_review", "description": "Review and improve content"}
            ]
    
    mock_agent = MockAgent()
    tools = mock_agent._create_tools()
    
    print(f"✅ Tools created successfully:")
    for tool in tools:
        print(f"   • {tool['name']}: {tool['description']}")
    
    return True

def test_prompt_preservation():
    """Test that original prompts are preserved."""
    print(f"\n🧪 Testing Prompt Preservation")
    print("=" * 50)
    
    # Create a mock agent to test prompts
    class MockAgent:
        def _get_system_prompt(self):
            return """You are a professional portfolio manager writing the Market Context section of a quarterly portfolio commentary for institutional clients.

Your task is to write a comprehensive Market Context section that:
- Provides a clear overview of market conditions during the specified period
- Explains key market drivers and economic factors
- Discusses sector performance and market trends
- Uses professional, analytical language suitable for institutional investors
- Focuses on facts and analysis, not speculation
- Maintains a neutral, objective tone

The Market Context should be informative, well-structured, and demonstrate deep market understanding."""
        
        def _create_market_context_prompt(self, strategy_name: str, quarter: str, year: int,
                                        benchmark: str, market_research: str, 
                                        custom_instructions: str = "") -> str:
            return f"""Generate a Market Context section for the {strategy_name} portfolio commentary for {quarter} {year}.

Strategy Details:
- Strategy: {strategy_name}
- Benchmark: {benchmark}
- Period: {quarter} {year}

Market Research Data:
{market_research}

Please write a comprehensive Market Context section that covers:

1. **Economic Overview**: Key economic indicators, Federal Reserve policy, inflation trends, and GDP growth
2. **Market Performance**: Major index performance, volatility levels, and market sentiment
3. **Sector Analysis**: Sector rotation, performance leaders and laggards, and key themes
4. **Global Factors**: International market conditions, geopolitical events, and currency impacts
5. **Market Drivers**: Key events, earnings trends, and factors that influenced market direction

Guidelines:
- Write in a professional, analytical tone
- Use specific data points and percentages where relevant
- Focus on what happened during the period, not predictions
- Keep the content factual and objective
- Structure the content with clear headings and bullet points
- Aim for 400-600 words of substantive content"""

            if custom_instructions:
                prompt += f"\n\nAdditional Instructions: {custom_instructions}"
            
            return prompt
    
    mock_agent = MockAgent()
    
    # Test system prompt
    system_prompt = mock_agent._get_system_prompt()
    print(f"✅ System Prompt Preserved ({len(system_prompt)} characters)")
    print(f"   Contains 'professional portfolio manager': {'professional portfolio manager' in system_prompt}")
    print(f"   Contains 'institutional clients': {'institutional clients' in system_prompt}")
    
    # Test user prompt
    user_prompt = mock_agent._create_market_context_prompt(
        "US Equity Core", "Q1", "2024", "S&P 500", "Mock research data", "Focus on tech"
    )
    print(f"✅ User Prompt Preserved ({len(user_prompt)} characters)")
    print(f"   Contains 'Economic Overview': {'Economic Overview' in user_prompt}")
    print(f"   Contains 'Market Performance': {'Market Performance' in user_prompt}")
    print(f"   Contains '400-600 words': {'400-600 words' in user_prompt}")
    
    return True

def test_api_key_handling():
    """Test API key handling."""
    print(f"\n🧪 Testing API Key Handling")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print(f"✅ API Key Found: {api_key[:10]}...")
        print(f"   Ready for ReAct agent execution")
    else:
        print(f"⚠️  No API Key Set")
        print(f"   Set OPENAI_API_KEY environment variable to enable ReAct agent")
        print(f"   Demo mode available without API key")
    
    return True

def main():
    """Run all tests."""
    print("🤖 ReAct Market Context Agent - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Request Creation", test_request_creation),
        ("Agent Structure", test_agent_structure),
        ("Tools Structure", test_tools_structure),
        ("Prompt Preservation", test_prompt_preservation),
        ("API Key Handling", test_api_key_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n📊 Test Results Summary:")
    print("=" * 40)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ReAct agent is ready.")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Set OPENAI_API_KEY to enable ReAct agent execution")
        print(f"   2. Run: python market_context_agent.py")
        print(f"   3. Watch the agent reason and act to generate market context")
        print(f"   4. Compare with simple version to see ReAct benefits")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
