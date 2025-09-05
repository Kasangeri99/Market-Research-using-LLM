#!/usr/bin/env python3
"""
Simple Market Context Generator for Portfolio Commentaries
A straightforward prompt engineering approach to generate Market Context sections.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from openai import OpenAI
OPENAI_AVAILABLE = True
# try:
#     from openai import OpenAI
#     OPENAI_AVAILABLE = True
# except ImportError:
#     OPENAI_AVAILABLE = False
#     print("Warning: OpenAI not available. Install with: pip install openai")

@dataclass
class MarketContextRequest:
    """Request for generating market context."""
    strategy_name: str
    quarter: str
    year: int
    benchmark: str = "S&P 500"
    custom_instructions: Optional[str] = None

class MarketContextGenerator:
    """Simple market context generator using prompt engineering."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the generator."""
        # if not OPENAI_AVAILABLE:
        #     raise ImportError("OpenAI library not available. Install with: pip install openai")
            
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Cost-effective model
    
    def generate_market_context(self, request: MarketContextRequest) -> str:
        """Generate market context for the given request."""
        
        # Create the prompt
        prompt = self._create_market_context_prompt(request)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating market context: {str(e)}"
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for market context generation."""
        return """You are a professional portfolio manager writing the Market Context section of a quarterly portfolio commentary for institutional clients.

Your task is to write a comprehensive Market Context section that:
- Provides a clear overview of market conditions during the specified period
- Explains key market drivers and economic factors
- Discusses sector performance and market trends
- Uses professional, analytical language suitable for institutional investors
- Focuses on facts and analysis, not speculation
- Maintains a neutral, objective tone

The Market Context should be informative, well-structured, and demonstrate deep market understanding."""
    
    def _create_market_context_prompt(self, request: MarketContextRequest) -> str:
        """Create the user prompt for market context generation."""
        
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

def main():
    """Main function to demonstrate the market context generator."""
    
    print("🎯 Simple Market Context Generator")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Create generator
    try:
        generator = MarketContextGenerator()
        print("✅ Generator initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return
    
    # Example request
    request = MarketContextRequest(
        strategy_name="US Equity Core",
        quarter="Q1",
        year=2024,
        benchmark="S&P 500 Index",
        custom_instructions="Focus on technology sector performance and AI-related market trends"
    )
    
    print(f"\n📊 Generating Market Context for {request.strategy_name} - {request.quarter} {request.year}")
    print("⏳ Please wait...")
    
    # Generate market context
    market_context = generator.generate_market_context(request)
    
    print("\n📝 Generated Market Context:")
    print("=" * 50)
    print(market_context)
    print("=" * 50)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"market_context_{request.strategy_name.replace(' ', '_')}_{request.quarter}_{request.year}_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Market Context - {request.strategy_name}\n")
        f.write(f"Period: {request.quarter} {request.year}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(market_context)
    
    print(f"\n💾 Market context saved to: {filename}")

if __name__ == "__main__":
    main()
