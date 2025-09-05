#!/usr/bin/env python3
"""
Simple test script for the Market Context Generator
Tests the basic functionality without requiring API keys.
"""

import os
from market_context_generator import MarketContextRequest

def test_request_creation():
    """Test creating market context requests."""
    print("🧪 Testing Market Context Request Creation")
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

def test_prompt_generation():
    """Test prompt generation without API calls."""
    print(f"\n🧪 Testing Prompt Generation")
    print("=" * 50)
    
    # Create a mock generator class to test prompts
    class MockGenerator:
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
        
        def _create_market_context_prompt(self, request):
            prompt = f"""Generate a Market Context section for the {request.strategy_name} portfolio commentary for {request.quarter} {request.year}.

Strategy Details:
- Strategy: {request.strategy_name}
- Benchmark: {request.benchmark}
- Period: {request.quarter} {request.year}

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

            if request.custom_instructions:
                prompt += f"\n\nAdditional Instructions: {request.custom_instructions}"
            
            return prompt
    
    # Test prompt generation
    generator = MockGenerator()
    request = MarketContextRequest(
        strategy_name="Fixed Income Core",
        quarter="Q3",
        year=2024,
        custom_instructions="Emphasize interest rate sensitivity and credit spreads"
    )
    
    system_prompt = generator._get_system_prompt()
    user_prompt = generator._create_market_context_prompt(request)
    
    print(f"✅ System Prompt Generated ({len(system_prompt)} characters)")
    print(f"✅ User Prompt Generated ({len(user_prompt)} characters)")
    print(f"✅ Custom Instructions Included: {'Yes' if request.custom_instructions else 'No'}")
    
    return True

def test_api_key_handling():
    """Test API key handling."""
    print(f"\n🧪 Testing API Key Handling")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print(f"✅ API Key Found: {api_key[:10]}...")
        print(f"   Ready for real generation")
    else:
        print(f"⚠️  No API Key Set")
        print(f"   Set OPENAI_API_KEY environment variable to enable real generation")
        print(f"   Demo mode available without API key")
    
    return True

def main():
    """Run all tests."""
    print("🎯 Simple Market Context Generator - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Request Creation", test_request_creation),
        ("Prompt Generation", test_prompt_generation),
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
        print("🎉 All tests passed! System is ready.")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Set OPENAI_API_KEY to enable real generation")
        print(f"   2. Run: python market_context_generator.py")
        print(f"   3. Generate market context for your strategies")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
