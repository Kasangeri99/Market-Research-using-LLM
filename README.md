# Simple Market Context Generator

A straightforward prompt engineering solution for generating Market Context sections of portfolio commentaries using OpenAI's GPT models.

## 🎯 Purpose

This tool automates the creation of Market Context sections for portfolio commentaries, focusing on:
- Economic overview and market conditions
- Sector performance analysis
- Key market drivers and trends
- Professional, institutional-grade writing

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Run Demo (No API Key Required)
```bash
python demo_simple.py
```

### 4. Generate Market Context
```bash
python market_context_generator.py
```

## 📁 Files

- **`market_context_generator.py`**: Main generator with OpenAI integration
- **`demo_simple.py`**: Demo script showing how the system works
- **`requirements.txt`**: Python dependencies
- **`README.md`**: This file

## 🔧 Usage

### Basic Usage
```python
from market_context_generator import MarketContextGenerator, MarketContextRequest

# Initialize generator
generator = MarketContextGenerator()

# Create request
request = MarketContextRequest(
    strategy_name="US Equity Core",
    quarter="Q1",
    year=2024,
    benchmark="S&P 500 Index",
    custom_instructions="Focus on technology sector performance"
)

# Generate market context
market_context = generator.generate_market_context(request)
print(market_context)
```

### Customization

The generator supports:
- **Strategy Name**: Name of the investment strategy
- **Quarter/Year**: Time period for the commentary
- **Benchmark**: Reference benchmark for the strategy
- **Custom Instructions**: Additional guidance for content generation

## 📊 Output Format

The generated Market Context includes:
1. **Economic Overview**: Key economic indicators and policy
2. **Market Performance**: Index performance and volatility
3. **Sector Analysis**: Sector rotation and performance
4. **Global Factors**: International market conditions
5. **Market Drivers**: Key events and trends

## 🎨 Prompt Engineering Features

- **Professional Tone**: Institutional-grade writing style
- **Structured Content**: Clear headings and bullet points
- **Factual Focus**: Emphasis on what happened, not predictions
- **Customizable**: Strategy-specific instructions supported
- **Consistent Format**: Standardized output structure

## 🔮 Future Enhancements

This simple solution can be enhanced with:
- **ReAct Framework**: Reasoning and acting capabilities
- **Real-time Data**: Integration with market data APIs
- **Multi-strategy Support**: Batch processing capabilities
- **Template System**: Customizable output formats
- **Quality Validation**: Automated fact-checking

## 📝 Example Output

```
# Market Context - Q1 2024

## Economic Overview
The first quarter of 2024 was marked by continued economic resilience...

## Market Performance
Equity markets demonstrated strong performance during the quarter...

## Sector Analysis
Technology sector led market performance with a 15.2% gain...
```

## 🛠️ Development

To extend this solution:
1. Modify prompts in `_create_market_context_prompt()`
2. Adjust system prompt in `_get_system_prompt()`
3. Add new request parameters as needed
4. Enhance output formatting

## 📄 License

This project is for educational and demonstration purposes.
