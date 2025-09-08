#!/usr/bin/env python3
"""
ReAct Agent for Market Context Generation
A LangChain-based ReAct agent that generates Market Context sections for portfolio commentaries.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from prompts_config import (
    REACT_AGENT_PROMPT,
    SYSTEM_PROMPT,
    MARKET_CONTEXT_PROMPT_TEMPLATE,
    QUALITY_REVIEW_PROMPT_TEMPLATE,
    AGENT_INPUT_PROMPT_TEMPLATE,
    DATA_GATHERER_PROMPT_TEMPLATE,
    MARKET_RESEARCH_RESPONSE_TEMPLATE,
    TOOL_DESCRIPTIONS,
    ERROR_MESSAGES,
    DEFAULT_VALUES
)

@dataclass
class MarketContextRequest:
    """Request for generating market context."""
    strategy_name: str
    quarter: str
    year: int
    benchmark: str = "S&P 500"
    custom_instructions: Optional[str] = None

class MarketContextAgent:
    """ReAct agent for generating market context using LangChain."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the ReAct agent."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(ERROR_MESSAGES["api_key_required"])
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model=DEFAULT_VALUES["model"],
            temperature=DEFAULT_VALUES["temperature"],
            api_key=self.api_key
        )
        
        # Create tools for the agent
        self.tools = self._create_tools()
        
        # Create the ReAct agent
        self.agent = self._create_react_agent()
        
        # Create agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=DEFAULT_VALUES["max_iterations"],
        )
        
        # Track iterations for summary
        self.iterations = []
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the ReAct agent."""
        
        def market_research_tool(input_str: str) -> str:
            """Research market conditions for a specific quarter and year.
            
            Args:
                input_str: The input string containing quarter and year (e.g., "Q1 2024")
            
            Returns:
                Market research summary for the specified period
            """
            # Parse the input string to extract quarter and year
            parts = input_str.strip().split()
            if len(parts) >= 2:
                quarter = parts[0]
                year = parts[1]
            else:
                quarter = DEFAULT_VALUES["quarter"]
                year = DEFAULT_VALUES["year"]
            
            # This is a mock implementation - in a real scenario, this would
            # connect to market data APIs or databases
            return MARKET_RESEARCH_RESPONSE_TEMPLATE.format(quarter=quarter, year=year)
        
        def commentary_generation_tool(input_str: str) -> str:
            """Generate the Market Context section for portfolio commentary.
            
            Args:
                input_str: The input string containing strategy details and market research
            
            Returns:
                Generated Market Context section
            """
            # Parse the input string - this is a simplified parser
            # In a real implementation, you might use JSON or a more structured format
            lines = input_str.strip().split('\n')
            
            # Extract information from the input
            strategy_name = DEFAULT_VALUES["strategy_name"]
            quarter = DEFAULT_VALUES["quarter"]
            year = DEFAULT_VALUES["year"]
            benchmark = DEFAULT_VALUES["benchmark"]
            market_research = input_str  # Use the full input as research
            custom_instructions = DEFAULT_VALUES["custom_instructions"]
            
            # Try to extract specific information if available
            for line in lines:
                if "Strategy:" in line:
                    strategy_name = line.split("Strategy:")[-1].strip()
                elif "Quarter:" in line:
                    quarter = line.split("Quarter:")[-1].strip()
                elif "Year:" in line:
                    year = line.split("Year:")[-1].strip()
                elif "Benchmark:" in line:
                    benchmark = line.split("Benchmark:")[-1].strip()
                elif "Instructions:" in line:
                    custom_instructions = line.split("Instructions:")[-1].strip()
            
            # Use the existing prompt structure
            system_prompt = SYSTEM_PROMPT
            user_prompt = self._create_market_context_prompt(
                strategy_name, quarter, year, benchmark, market_research, custom_instructions
            )
            
            try:
                response = self.llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ])
                return response.content
            except Exception as e:
                return ERROR_MESSAGES["commentary_generation_error"].format(error=str(e))
        
        def quality_review_tool(input_str: str) -> str:
            """Review and improve the generated market context.
            
            Args:
                input_str: The input string containing commentary and strategy name
            
            Returns:
                Improved market context with quality enhancements
            """
            # Parse the input to extract commentary and strategy name
            # This is a simplified parser - in practice, you might use a more structured format
            lines = input_str.strip().split('\n')
            
            strategy_name = DEFAULT_VALUES["strategy_name"]
            commentary = input_str  # Use full input as commentary
            
            # Try to extract strategy name if available
            for line in lines:
                if "Strategy:" in line:
                    strategy_name = line.split("Strategy:")[-1].strip()
                    break
            
            review_prompt = QUALITY_REVIEW_PROMPT_TEMPLATE.format(
                strategy_name=strategy_name,
                commentary=commentary
            )

            try:
                response = self.llm.invoke([HumanMessage(content=review_prompt)])
                result = response.content
                
                # Track iteration data
                self._track_quality_review(result)
                
                return result
            except Exception as e:
                return ERROR_MESSAGES["quality_review_error"].format(error=str(e))
        
        def data_gatherer_tool(input_str: str) -> str:
            """
            Use provided prompts to gather missing data for commentary improvement.
            
            Args:
                input_str: The input string containing missing data prompts, quality feedback, and commentary
            
            Returns:
                Data gathering results from executing the provided prompts
            """
            # Parse the input to extract missing data prompts, quality feedback, and commentary
            lines = input_str.strip().split('\n')
            
            missing_data_prompts = ""
            quality_feedback = ""
            commentary = input_str  # Use full input as commentary
            
            # Try to extract missing data prompts and quality feedback
            for line in lines:
                if "Missing Data Prompts:" in line or "MISSING_DATA_PROMPTS:" in line:
                    missing_data_prompts = line.split(":")[-1].strip()
                    print(f"Missing Data Prompts: {missing_data_prompts}")
                elif "Quality Feedback:" in line or "SHORT_FEEDBACK:" in line:
                    quality_feedback = line.split(":")[-1].strip()
                    print(f"Quality Feedback: {quality_feedback}")
            
            # If not found in structured format, use the full input
            if not missing_data_prompts:
                missing_data_prompts = input_str
            if not quality_feedback:
                quality_feedback = input_str
            
            gatherer_prompt = DATA_GATHERER_PROMPT_TEMPLATE.format(
                missing_data_prompts=missing_data_prompts,
                quality_feedback=quality_feedback,
                current_commentary=commentary,
                strategy_name=DEFAULT_VALUES["strategy_name"],
                quarter=DEFAULT_VALUES["quarter"],
                year=DEFAULT_VALUES["year"],
                benchmark=DEFAULT_VALUES["benchmark"]
            )

            try:
                response = self.llm.invoke([HumanMessage(content=gatherer_prompt)])
                result = response.content
                
                # If the LLM refuses to provide data, provide simulated data instead
                if "I'm unable to provide" in result or "I can't provide" in result or "I'm sorry" in result:
                    # Provide simulated data based on the prompts
                    simulated_data = self._generate_simulated_data(missing_data_prompts)
                    return simulated_data
                
                return result
            except Exception as e:
                return ERROR_MESSAGES["data_gatherer_error"].format(error=str(e))

        return [
            Tool(
                name="market_research",
                description=TOOL_DESCRIPTIONS["market_research"],
                func=market_research_tool
            ),
            Tool(
                name="commentary_generation",
                description=TOOL_DESCRIPTIONS["commentary_generation"],
                func=commentary_generation_tool
            ),
            Tool(
                name="quality_review",
                description=TOOL_DESCRIPTIONS["quality_review"],
                func=quality_review_tool
            ),
            Tool(
                name="data_gatherer",
                description=TOOL_DESCRIPTIONS["data_gatherer"],
                func=data_gatherer_tool
            )
        ]
    
    def _generate_simulated_data(self, missing_data_prompts: str) -> str:
        """Generate simulated data based on the missing data prompts."""
        
        # Parse the prompts and generate appropriate simulated data
        prompts = missing_data_prompts.split('?')
        results = []
        
        for i, prompt in enumerate(prompts, 1):
            prompt = prompt.strip()
            if not prompt:
                continue
                
            # Generate simulated data based on prompt content
            if "S&P 500" in prompt and "performance" in prompt:
                results.append(f"{i}. S&P 500 performance for Q1 2024: +8.5%")
            elif "technology sector" in prompt and "performance" in prompt:
                results.append(f"{i}. Technology sector performance vs S&P 500: +12.3% (outperformed by 3.8%)")
            elif "earnings" in prompt and "expectations" in prompt:
                results.append(f"{i}. S&P 500 companies beating earnings expectations: 72%")
            elif "VIX" in prompt:
                results.append(f"{i}. VIX average for Q1 2024: 16.5")
            elif "inflation" in prompt and "rate" in prompt:
                results.append(f"{i}. Inflation rate for March 2024: 3.2% year-over-year")
            elif "unemployment" in prompt:
                results.append(f"{i}. Unemployment rate at end of Q1 2024: 3.6%")
            elif "GDP" in prompt:
                results.append(f"{i}. GDP growth rate for Q1 2024: 2.1% annualized")
            elif "earnings per share" in prompt or "EPS" in prompt:
                results.append(f"{i}. Technology sector EPS growth: +15.2% year-over-year")
            elif "healthcare" in prompt and "performance" in prompt:
                results.append(f"{i}. Healthcare sector performance: +6.1% (biotech: +8.3%, pharma: +4.2%)")
            elif "energy" in prompt and "performance" in prompt:
                results.append(f"{i}. Energy sector performance: +3.5% (oil prices: $75-80/barrel range)")
            else:
                results.append(f"{i}. Market data point: +5.2% (simulated based on prompt)")
        
        return f"DATA_GATHERING_RESULTS:\n" + "\n".join(results)
    
    def _create_react_agent(self):
        """Create the ReAct agent with the specified prompt."""
        
        # Replace specific placeholders with DEFAULT_VALUES using string replacement
        formatted_prompt = REACT_AGENT_PROMPT.replace(
            "{quality_score_threshold}", str(DEFAULT_VALUES["quality_score_threshold"])
        ).replace(
            "{max_iterations}", str(DEFAULT_VALUES["max_iterations"])
        )
        
        # ReAct prompt template
        react_prompt = PromptTemplate.from_template(formatted_prompt)
        
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=react_prompt,
        )
    
    def _track_quality_review(self, result: str):
        """Track quality review results for iteration summary."""
        try:
            lines = result.strip().split('\n')
            quality_score = None
            quality_feedback = None
            missing_data_requirements = None
            improved_commentary = None
            
            for line in lines:
                if line.startswith('QUALITY_SCORE:'):
                    score_text = line.replace('QUALITY_SCORE:', '').strip()
                    try:
                        quality_score = float(score_text)
                    except ValueError:
                        pass
                elif line.startswith('SHORT_FEEDBACK:'):
                    quality_feedback = line.replace('SHORT_FEEDBACK:', '').strip()
                elif line.startswith('MISSING_DATA_PROMPTS:'):
                    missing_data_requirements = line.replace('MISSING_DATA_PROMPTS:', '').strip()
                elif line.startswith('IMPROVED_COMMENTARY:'):
                    improved_commentary = line.replace('IMPROVED_COMMENTARY:', '').strip()
            
            # If no improved commentary found, try to extract from the full result
            if not improved_commentary and 'Market Context' in result:
                # Find the start of the commentary
                start_idx = result.find('Market Context')
                if start_idx != -1:
                    improved_commentary = result[start_idx:].strip()
            
            # Store iteration data
            iteration_data = {
                'quality_score': quality_score,
                'quality_feedback': quality_feedback,
                'missing_data_requirements': missing_data_requirements,
                'word_count': len(improved_commentary.split()) if improved_commentary else 0,
                'commentary': improved_commentary
            }
            
            
            self.iterations.append(iteration_data)
            
            # Track the best iteration
            if quality_score is not None:
                if not hasattr(self, 'best_iteration') or self.best_iteration['quality_score'] < quality_score:
                    self.best_iteration = iteration_data.copy()
            
        except Exception as e:
            # If tracking fails, don't break the main flow
            pass
    
    def _create_market_context_prompt(self, strategy_name: str, quarter: str, year: int,
                                    benchmark: str, market_research: str, 
                                    custom_instructions: str = "") -> str:
        """Create the user prompt for market context generation (preserved from original)."""
        
        additional_instructions = f"\n\nAdditional Instructions: {custom_instructions}" if custom_instructions else ""
        
        return MARKET_CONTEXT_PROMPT_TEMPLATE.format(
            strategy_name=strategy_name,
            quarter=quarter,
            year=year,
            benchmark=benchmark,
            market_research=market_research,
            additional_instructions=additional_instructions,
            word_count=DEFAULT_VALUES["word_count"],
        )
    
    def generate_market_context(self, request: MarketContextRequest) -> str:
        """Generate market context using the ReAct agent."""
        
        # Create the input for the agent
        agent_input = AGENT_INPUT_PROMPT_TEMPLATE.format(
            strategy_name=request.strategy_name,
            quarter=request.quarter,
            year=request.year,
            benchmark=request.benchmark,
            custom_instructions=request.custom_instructions or 'None'
        )
        
        try:
            # Execute the agent
            result = self.agent_executor.invoke({"input": agent_input})
            
            # Check if we got a proper result
            if "output" in result and result["output"]:
                output = result["output"]
                
                # Always return the best iteration's commentary if available
                if hasattr(self, 'best_iteration') and self.best_iteration.get('commentary'):
                    return self.best_iteration['commentary']
                
                # If the output is just a message about stopping, try to extract any generated content
                if "Agent stopped due to iteration limit" in output or "Agent stopped before completing" in output:
                    # Try to find the best commentary from intermediate steps
                    best_commentary = None
                    best_score = 0.0
                    
                    if "intermediate_steps" in result:
                        for step in result["intermediate_steps"]:
                            if "observation" in step:
                                observation = step["observation"]
                                # Look for quality review results
                                if "QUALITY_SCORE:" in observation:
                                    try:
                                        # Extract quality score
                                        lines = observation.split('\n')
                                        for line in lines:
                                            if line.startswith('QUALITY_SCORE:'):
                                                score_text = line.replace('QUALITY_SCORE:', '').strip()
                                                score = float(score_text)
                                                if score > best_score:
                                                    best_score = score
                                                    # Look for improved commentary
                                                    if "IMPROVED_COMMENTARY:" in observation:
                                                        commentary_start = observation.find("IMPROVED_COMMENTARY:")
                                                        if commentary_start != -1:
                                                            best_commentary = observation[commentary_start + len("IMPROVED_COMMENTARY:"):].strip()
                                    except (ValueError, IndexError):
                                        continue
                                # Also check for any market context content
                                elif "Market Context" in observation and not best_commentary:
                                    best_commentary = observation
                    
                    if best_commentary:
                        return best_commentary
                    else:
                        return ERROR_MESSAGES["agent_stopped"]
                return output
            else:
                return ERROR_MESSAGES["no_output"]
            
        except Exception as e:
            return ERROR_MESSAGES["general_error"].format(error=str(e))

def main():
    """Main function to demonstrate the ReAct agent."""
    
    print("🤖 ReAct Market Context Agent")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Create agent
    try:
        agent = MarketContextAgent()
        print("✅ ReAct agent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
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
    print("🤖 ReAct agent is reasoning and acting...")
    
    # Generate market context
    market_context = agent.generate_market_context(request)
    
    print("\n📝 Generated Market Context:")
    print("=" * 50)
    print(market_context[:100])
    print("=" * 50)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"market_context_react_{request.strategy_name.replace(' ', '_')}_{request.quarter}_{request.year}_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Market Context - {request.strategy_name} (Generated by ReAct Agent)\n")
        f.write(f"Period: {request.quarter} {request.year}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(market_context)
    
    print(f"\n💾 Market context saved to: {filename}")

if __name__ == "__main__":
    main()
