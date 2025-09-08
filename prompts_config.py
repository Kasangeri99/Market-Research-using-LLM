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
     b) Use commentary_generation with the improved version and response from data_gatherer as input
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
MARKET_CONTEXT_PROMPT_TEMPLATE = """Generate a Market Context section for {strategy_name} - {quarter} {year}.

Market Research: {market_research}
The quality checker has provided the following feedback: {feedback}
and the following additional data: {additional_data}
Using the above feedback and additional data, improve or generate a new Market Context.

Write a professional Market Context covering:
1. Economic Overview (Fed policy, inflation, GDP)
2. Market Performance (index performance, volatility)
3. Sector Analysis (leaders/laggards, themes)
4. Key Market Drivers (events, earnings)

Target: ~{word_count} words, professional tone, specific data points.

{additional_instructions}
Provide structured response:
COMMENTARY: [Market Context section]
"""

# Quality Review Prompt Template
QUALITY_REVIEW_PROMPT_TEMPLATE = """Review this Market Context for {strategy_name}:

{commentary}

Provide structured response:
QUALITY_SCORE: [Score 1-10]
FEEDBACK: [Brief feedback on strengths/improvements]
MORE_PROMPTS: [3-5 specific data prompts to improve commentary]

Be generous with scoring (8.5-9.5 for good analysis)."""

# Data Gatherer Prompt Template
DATA_GATHERER_PROMPT_TEMPLATE = """Gather data for {strategy_name} - {quarter} {year}.

Prompts: {missing_data_prompts}
Feedback: {quality_feedback}

Provide response:
DATA_RESPONSE: [Gathered data results]"""


# Agent Input Prompt Template
AGENT_INPUT_PROMPT_TEMPLATE = """Generate a Market Context section for the {strategy_name} portfolio commentary for {quarter} {year}.

Strategy Details:
- Strategy: {strategy_name}
- Benchmark: {benchmark}
- Period: {quarter} {year}
- Custom Instructions: {custom_instructions}

Please use the available tools to research market conditions and generate a comprehensive Market Context section. Make sure to provide the complete Market Context as your final answer."""

# Market Research Tool Response Template
MARKET_RESEARCH_RESPONSE_TEMPLATE = """MARKET_RESEARCH: S&P 500 strong performance, tech sector leading, Fed rates maintained, inflation moderating, robust employment, geopolitical tensions affecting sentiment. Technology leading, healthcare solid, financials moderate, energy mixed. Key drivers: earnings growth, Fed policy, geopolitical events, AI innovation."""

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
    "max_iterations": 5, 
    "quality_score_threshold": 10.0,
    "word_count": 200,
}
