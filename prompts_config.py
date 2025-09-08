#!/usr/bin/env python3
"""
Prompts Configuration for Market Context Agent
Contains all prompt templates used by the ReAct agent for market context generation.
"""

# ReAct Agent System Prompt
REACT_AGENT_PROMPT = """
You are a professional portfolio manager's assistant specializing in generating Market Context sections for portfolio commentaries.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

QUALITY LOOP REQUIREMENT:
1. First, use market_research to gather market data
2. Then, use commentary_generation to create the initial market context
3. Next, use quality_review to assess and improve the commentary
4. Check the quality score in the quality_review output:
   - If the score is {quality_score_threshold} or higher: Provide the improved commentary as your Final Answer
   - If the score is below {quality_score_threshold}: 
     a) Use data_gatherer with the MISSING_DATA_PROMPTS from quality_review to gather the specific data needed
     b) Use commentary_generation with the improved version and additional data as input
     c) Use quality_review again to assess the new commentary
5. Repeat steps 4a-4c until you achieve a quality score of {quality_score_threshold} or higher
6. If after 3 iterations the score remains below {quality_score_threshold}, accept the best version (highest score achieved) as your Final Answer
7. Maximum iterations: {max_iterations} attempts to reach quality score {quality_score_threshold}+

IMPORTANT: You must continue improving the commentary until the quality_review tool gives a score of {quality_score_threshold} or higher. Only then should you provide the Final Answer.

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

# System Prompt for Market Context Generation
SYSTEM_PROMPT = """You are a professional portfolio manager writing the Market Context section of a quarterly portfolio commentary for institutional clients.

Your task is to write a comprehensive Market Context section that:
- Provides a clear overview of market conditions during the specified period
- Explains key market drivers and economic factors
- Discusses sector performance and market trends
- Uses professional, analytical language suitable for institutional investors
- Focuses on facts and analysis, not speculation
- Maintains a neutral, objective tone

The Market Context should be informative, well-structured, and demonstrate deep market understanding. Keep the commentary relevant to the strategy and the period.
Commentary should be around {word_count} words."""

# Market Context Generation Prompt Template
MARKET_CONTEXT_PROMPT_TEMPLATE = """Generate a Market Context section for the {strategy_name} portfolio commentary for {quarter} {year}.

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
- Aim for around {word_count} words of substantive content

{additional_instructions}"""

# Quality Review Prompt Template
QUALITY_REVIEW_PROMPT_TEMPLATE = """Please review this Market Context section for {strategy_name}:

{commentary}

Evaluate the commentary and provide a quality score, short feedback, and specific prompts for missing data.

IMPORTANT: Be generous with scoring. A well-structured, professional commentary with good market analysis should score 8.5-9.5. Only score below 8.0 if there are significant issues.

Provide your response in the following EXACT format:

QUALITY_SCORE: [Score out of 10]
SHORT_FEEDBACK: [Brief feedback on strengths and areas for improvement - keep it concise]
MISSING_DATA_PROMPTS: [3-5 specific prompts to gather missing data that would improve the commentary]

For MISSING_DATA_PROMPTS, create specific, actionable prompts such as:
- "What was the exact S&P 500 performance percentage for Q1 2024?"
- "What were the specific technology sector performance metrics vs benchmark?"
- "What percentage of S&P 500 companies beat earnings expectations in Q1 2024?"
- "What was the VIX average for Q1 2024?"
- "What were the specific inflation rates for March 2024?"

Example:
QUALITY_SCORE: 8.5
SHORT_FEEDBACK: Good structure and professional tone. Missing specific data points and sector performance details. Needs more quantitative metrics.
MISSING_DATA_PROMPTS: 1) What was the exact S&P 500 performance percentage for Q1 2024? 2) What were the specific technology sector performance metrics vs benchmark? 3) What percentage of S&P 500 companies beat earnings expectations? 4) What was the VIX average for Q1 2024? 5) What were the specific inflation rates for March 2024?"""

# Data Gatherer Prompt Template
DATA_GATHERER_PROMPT_TEMPLATE = """Use the provided prompts to gather the missing data for the market context commentary.

Missing Data Prompts:
{missing_data_prompts}

Quality Feedback:
{quality_feedback}

Current Commentary:
{current_commentary}

Strategy Details:
- Strategy: {strategy_name}
- Quarter: {quarter}
- Year: {year}
- Benchmark: {benchmark}

Using the provided prompts, gather the specific data needed to improve the commentary quality. Execute each prompt and collect the relevant information.

Provide your response in the following EXACT format:

DATA_GATHERING_RESULTS:
1. [Result from first prompt]
2. [Result from second prompt]
3. [Result from third prompt]
4. [Result from fourth prompt]
5. [Result from fifth prompt]

Example:
DATA_GATHERING_RESULTS:
1. S&P 500 performance for Q1 2024: +8.3%
2. Technology sector performance vs S&P 500: +12.1% (outperformed by 3.8%)
3. S&P 500 companies beating earnings expectations: 75%
4. VIX average for Q1 2024: 18.5
5. Inflation rate for March 2024: 3.2% year-over-year"""


# Agent Input Prompt Template
AGENT_INPUT_PROMPT_TEMPLATE = """Generate a Market Context section for the {strategy_name} portfolio commentary for {quarter} {year}.

Strategy Details:
- Strategy: {strategy_name}
- Benchmark: {benchmark}
- Period: {quarter} {year}
- Custom Instructions: {custom_instructions}

Please use the available tools to research market conditions and generate a comprehensive Market Context section. Make sure to provide the complete Market Context as your final answer."""

# Market Research Tool Response Template
MARKET_RESEARCH_RESPONSE_TEMPLATE = """Market Research Summary for {quarter} {year}:
            
Key Market Indicators:
- S&P 500: Strong performance with technology sector leading
- Federal Reserve: Maintained interest rates at current levels
- Inflation: Continued moderation trend
- Employment: Robust labor market conditions
- Geopolitical: Ongoing tensions affecting market sentiment

Sector Performance:
- Technology: Leading sector performance
- Healthcare: Solid gains
- Financials: Moderate performance
- Energy: Mixed results due to supply concerns

Market Drivers:
- Corporate earnings growth
- Federal Reserve policy
- Geopolitical developments
- AI and technology innovation"""

# Tool Descriptions
TOOL_DESCRIPTIONS = {
    "market_research": "Research market conditions for a specific quarter and year. Input should be in format: 'quarter year' (e.g., 'Q1 2024')",
    "commentary_generation": "Generate Market Context section for portfolio commentary. Input should contain strategy details and market research data.",
    "quality_review": "Review and improve generated market context for quality and accuracy. Input should contain the commentary to review.",
    "data_gatherer": "Use provided prompts to gather missing data for commentary improvement. Input should contain missing data prompts, quality feedback, and current commentary."
}

# Error Messages
ERROR_MESSAGES = {
    "api_key_required": "OpenAI API key is required. Set OPENAI_API_KEY environment variable.",
    "commentary_generation_error": "Error generating commentary: {error}",
    "quality_review_error": "Error in quality review: {error}",
    "data_gatherer_error": "Error analyzing missing data requirements: {error}",
    "agent_stopped": "Error: Agent stopped before completing the task. Please try again with a simpler request.",
    "no_output": "Error: No output generated by the agent.",
    "general_error": "Error generating market context: {error}"
}

# Default Values
DEFAULT_VALUES = {
    "strategy_name": "US Equity Core",
    "quarter": "Q1",
    "year": "2024",
    "benchmark": "S&P 500",
    "custom_instructions": "",
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_iterations": 10, 
    "quality_score_threshold": 9.0,
    "word_count": 400,
}
