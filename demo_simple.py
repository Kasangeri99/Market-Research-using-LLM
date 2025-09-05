#!/usr/bin/env python3
"""
Simple demo of the Market Context Generator
Shows how the system works without requiring API keys.
"""

try:
    from market_context_generator import MarketContextRequest, MarketContextGenerator
except ImportError:
    print("Note: This demo shows the system structure. The main generator requires OpenAI API key.")
    # Define minimal classes for demo
    class MarketContextRequest:
        def __init__(self, strategy_name, quarter, year, benchmark="S&P 500", custom_instructions=None):
            self.strategy_name = strategy_name
            self.quarter = quarter
            self.year = year
            self.benchmark = benchmark
            self.custom_instructions = custom_instructions

def demo_without_api():
    """Demo the system structure without making API calls."""
    
    print("🎯 Simple Market Context Generator - Demo")
    print("=" * 50)
    
    # Create a sample request
    request = MarketContextRequest(
        strategy_name="US Equity Core",
        quarter="Q1",
        year=2024,
        benchmark="S&P 500 Index",
        custom_instructions="Focus on technology sector performance and AI-related market trends"
    )
    
    print(f"📊 Sample Request:")
    print(f"   Strategy: {request.strategy_name}")
    print(f"   Period: {request.quarter} {request.year}")
    print(f"   Benchmark: {request.benchmark}")
    print(f"   Custom Instructions: {request.custom_instructions}")
    
    # Show the prompt that would be generated
    print(f"\n📝 Generated Prompt Preview:")
    print("-" * 30)
    
    # Create a mock generator to show the prompt
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
    
    mock_gen = MockGenerator()
    system_prompt = mock_gen._get_system_prompt()
    user_prompt = mock_gen._create_market_context_prompt(request)
    
    print("System Prompt:")
    print(system_prompt[:200] + "...")
    print(f"\nUser Prompt:")
    print(user_prompt[:300] + "...")
    
    print(f"\n✅ Demo completed successfully!")
    print(f"\n🔑 To use with real API:")
    print(f"   1. Set OPENAI_API_KEY environment variable")
    print(f"   2. Run: python market_context_generator.py")
    print(f"   3. The system will generate actual market context content")

def show_sample_output():
    """Show what a sample output might look like."""
    
    print(f"\n📄 Sample Market Context Output:")
    print("=" * 50)
    
    sample_output = """# Market Context - Q1 2024

## Economic Overview
The first quarter of 2024 was marked by continued economic resilience despite ongoing uncertainty around Federal Reserve policy. The Federal Reserve maintained its benchmark interest rate at 5.25-5.50%, signaling a cautious approach to monetary policy as inflation showed signs of moderation. Core CPI inflation eased to 3.1% year-over-year, down from previous quarters, while the labor market remained robust with unemployment holding steady at 3.8%.

## Market Performance
Equity markets demonstrated strong performance during the quarter, with the S&P 500 Index advancing 10.6% and the technology-heavy NASDAQ Composite gaining 8.4%. Market volatility, as measured by the VIX, remained elevated at an average of 18.2, reflecting ongoing investor sensitivity to economic data and central bank communications.

## Sector Analysis
Technology sector led market performance with a 15.2% gain, driven by continued enthusiasm around artificial intelligence and strong earnings growth from major technology companies. Healthcare sector also performed well, advancing 8.7%, while financials posted modest gains of 3.2%. Energy sector was the notable laggard, declining 2.1% due to concerns about global demand and supply dynamics.

## Global Factors
International markets showed mixed performance, with developed markets generally outperforming emerging markets. Geopolitical tensions in the Middle East and ongoing conflict in Ukraine continued to create market uncertainty, while currency fluctuations impacted international returns for U.S. investors.

## Market Drivers
Key factors influencing market direction included:
• Strong corporate earnings growth across multiple sectors
• Federal Reserve's measured approach to interest rate policy
• Continued innovation and adoption of AI technologies
• Geopolitical developments and their impact on global trade
• Inflation trends and their implications for monetary policy"""
    
    print(sample_output)
    print("=" * 50)

if __name__ == "__main__":
    demo_without_api()
    show_sample_output()
