#!/usr/bin/env python3
"""
Example usage of the Simple Market Context Generator
Shows different ways to use the system.
"""

import os
from market_context_generator import MarketContextGenerator, MarketContextRequest

def example_basic_usage():
    """Example of basic usage."""
    print("📊 Example 1: Basic Usage")
    print("-" * 30)
    
    # Create request
    request = MarketContextRequest(
        strategy_name="US Equity Core",
        quarter="Q1",
        year=2024
    )
    
    print(f"Request: {request.strategy_name} - {request.quarter} {request.year}")
    
    # Note: This would require API key to actually generate
    if os.getenv("OPENAI_API_KEY"):
        try:
            generator = MarketContextGenerator()
            market_context = generator.generate_market_context(request)
            print(f"Generated {len(market_context)} characters of market context")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Set OPENAI_API_KEY to generate real content")

def example_custom_instructions():
    """Example with custom instructions."""
    print(f"\n📊 Example 2: Custom Instructions")
    print("-" * 30)
    
    request = MarketContextRequest(
        strategy_name="International Growth",
        quarter="Q2",
        year=2024,
        benchmark="MSCI EAFE",
        custom_instructions="Focus on emerging market opportunities, currency impacts, and geopolitical factors affecting international markets"
    )
    
    print(f"Request: {request.strategy_name} - {request.quarter} {request.year}")
    print(f"Custom Instructions: {request.custom_instructions}")

def example_multiple_strategies():
    """Example of generating for multiple strategies."""
    print(f"\n📊 Example 3: Multiple Strategies")
    print("-" * 30)
    
    strategies = [
        ("US Equity Core", "S&P 500", "Focus on technology sector performance"),
        ("International Growth", "MSCI EAFE", "Emphasize emerging market opportunities"),
        ("Fixed Income Core", "Bloomberg US Aggregate", "Highlight interest rate sensitivity")
    ]
    
    for strategy_name, benchmark, instructions in strategies:
        request = MarketContextRequest(
            strategy_name=strategy_name,
            quarter="Q3",
            year=2024,
            benchmark=benchmark,
            custom_instructions=instructions
        )
        print(f"• {request.strategy_name} ({request.benchmark})")

def example_prompt_preview():
    """Show what the prompts look like."""
    print(f"\n📊 Example 4: Prompt Preview")
    print("-" * 30)
    
    # Create a mock generator to show prompts
    class MockGenerator:
        def _get_system_prompt(self):
            return "You are a professional portfolio manager..."
        
        def _create_market_context_prompt(self, request):
            return f"Generate a Market Context section for {request.strategy_name}..."
    
    generator = MockGenerator()
    request = MarketContextRequest(
        strategy_name="US Equity Core",
        quarter="Q1",
        year=2024,
        custom_instructions="Focus on AI and technology trends"
    )
    
    system_prompt = generator._get_system_prompt()
    user_prompt = generator._create_market_context_prompt(request)
    
    print(f"System Prompt Length: {len(system_prompt)} characters")
    print(f"User Prompt Length: {len(user_prompt)} characters")
    print(f"Total Prompt Size: {len(system_prompt) + len(user_prompt)} characters")

def main():
    """Run all examples."""
    print("🎯 Simple Market Context Generator - Usage Examples")
    print("=" * 60)
    
    examples = [
        example_basic_usage,
        example_custom_instructions,
        example_multiple_strategies,
        example_prompt_preview,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"❌ Example failed: {e}")
    
    print(f"\n✅ All examples completed!")
    print(f"\n🔑 To generate real content:")
    print(f"   1. Set OPENAI_API_KEY environment variable")
    print(f"   2. Run: python market_context_generator.py")
    print(f"   3. Or use the generator in your own code")

if __name__ == "__main__":
    main()
