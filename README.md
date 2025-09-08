# Market Context Generator - ReAct Agent System

A sophisticated ReAct agent system for generating high-quality Market Context sections of portfolio commentaries using OpenAI's GPT models with iterative quality improvement.

## a. Setup & Execution Steps

### Prerequisites
- Python 3.9+
- OpenAI API key

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd NeubergerBermanProject

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Quick Start
```bash
# Run the core agent system
python agent_runner.py --strategy "US Equity Core" --quarter Q1 --year 2024

# Or use the Python API
python -c "
from agent_runner import CoreAgentRunner
runner = CoreAgentRunner()
job = runner.create_job('US Equity Core', 'Q1', 2024)
result = runner.run_job(job.job_id)
print(f'Quality Score: {result.quality_score}/10')
"
```

### Core Files
- `market_context_agent.py` - ReAct agent with quality loop
- `agent_runner.py` - Main system interface
- `job_models.py` - Job management and tracking
- `prompts_config.py` - All prompts and configuration

## b. The Problem You Focused On and Why

### Primary Problem
**Automated Generation of High-Quality Market Context Sections** for portfolio commentaries that meet institutional standards.


### Specific Challenges Addressed
- **Quality Control**: Ensuring output meets 9.0+ quality threshold
- **Iterative Improvement**: Automatically refining content based on feedback
- **Structured Data Flow**: Managing market research → commentary → quality review → data gathering
- **Error Handling**: Graceful handling of API failures and max iteration limits
- **Best Result Selection**: Always returning the highest quality commentary available

## c. Architectural and Design Decisions

### ReAct Agent Architecture
**Decision**: Implemented ReAct (Reasoning + Acting) framework using LangChain
**Rationale**: 
- Enables multi-step reasoning and tool usage
- Provides transparency in decision-making process
- Allows iterative improvement through quality loops
- Supports specialized tools for different tasks

### Quality Loop Design
**Decision**: Implemented iterative quality improvement with structured data flow
**Components**:
1. **Market Research Tool**: Gathers market data for specific periods
2. **Commentary Generation Tool**: Creates initial market context
3. **Quality Review Tool**: Scores and provides feedback (3 keys: score, feedback, prompts)
4. **Data Gatherer Tool**: Collects missing data for improvement

**Flow**: Research → Generate → Review → Gather Data → Regenerate → Review (until quality ≥ 9.0)

### Structured Data Format
**Decision**: Used structured key-value format for all tool outputs
**Benefits**:
- Easier parsing and processing
- Clear separation of concerns
- Simplified error handling
- Better debugging and monitoring

### Fallback Strategy
**Decision**: Implemented comprehensive fallback logic for max iterations
**Logic**:
1. Return best iteration commentary (highest quality score)
2. If best iteration empty, return last iteration commentary
3. Only return error if no commentary available

### Job Management System 
(TBDeveloped)
**Decision**: Built comprehensive job tracking and management
**Features**:
- Job lifecycle management (Created → Pending → Running → Completed/Failed)
- Iteration tracking with quality scores and feedback
- Result export and persistence
- Concurrent job support

## d. Key Assumptions and Trade-offs

### Assumptions
1. **API Reliability**: OpenAI API will be available and responsive
2. **Quality Threshold**: 9.0+ quality score indicates institutional-grade content
3. **Market Data**: Simulated market data is sufficient for demonstration
4. **User Requirements**: Users prefer quality over speed
5. **Content Structure**: Standard market context format is appropriate for all strategies

### Trade-offs Made

#### Quality vs Speed
- **Chosen**: Quality (iterative improvement until 9.0+ score)
- **Trade-off**: Longer execution time (30-120s vs 2-5s for simple approach)
- **Rationale**: Institutional requirements prioritize quality over speed

#### Complexity vs Simplicity
- **Chosen**: ReAct agent complexity for enhanced capabilities
- **Trade-off**: More complex codebase and debugging
- **Rationale**: Multi-step reasoning provides better results and transparency

#### Structured vs Natural Language
- **Chosen**: Structured key-value format for tool outputs
- **Trade-off**: Less natural but more reliable parsing
- **Rationale**: Better error handling and system reliability

#### Max Iterations vs Infinite Loops
- **Chosen**: 10 max iterations with best result selection
- **Trade-off**: May not reach quality threshold in some cases
- **Rationale**: Prevents infinite loops and ensures completion

## e. What You Would Add with More Time

### 0. Unit testing
- **Tools** if each tool has been active
- **Data flow** test if the data exchanged between the tools is non-empty
- **Stress testing** handling edge cases, test for hallucination 

### 1. Real-time Market Data Integration
Currently data collection is from simulated data, that is hardcoded. 
- **Bloomberg API** integration for live market data
- **FRED API** for economic indicators
- **Real-time sector performance** data
- **Historical data** for trend analysis

### 2. Advanced Quality Metrics
- **Fact-checking** against real market data
- **Consistency validation** across multiple sources
- **Sentiment analysis** for tone appropriateness
- **Readability scoring** for institutional standards

### 3. Multi-Agent Coordination
- **Specialist agents** for different market sectors
- **Coordinator agent** for overall strategy
- **Quality assurance agent** for final validation
- **Research agent** for deep market analysis

### 4. Enhanced User Experience
- **Web UI** with real-time progress tracking
- **Batch processing** for multiple strategies
- **Template customization** for different fund types
- **Export options** (PDF, Word, HTML)



The architecture is designed for extensibility, making it straightforward to add the enhancements listed above as requirements evolve.

## AI Technologies Used

This system leverages several cutting-edge AI technologies:

- **OpenAI GPT-4**: Primary language model for content generation, reasoning, and quality assessment
- **LangChain**: Agent orchestration framework that enables the ReAct pattern implementation
- **ReAct Pattern**: Reasoning + Acting framework that allows the AI to think through problems step-by-step and use specialized tools


The combination of these technologies enables sophisticated multi-step reasoning, iterative quality improvement, and robust error handling while maintaining high-quality institutional-grade output.

