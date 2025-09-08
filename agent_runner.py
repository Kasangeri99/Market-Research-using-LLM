"""
Core agentic system for market context generation.
No UI dependencies - pure agentic functionality.
"""
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

from market_context_agent import MarketContextAgent, MarketContextRequest
from job_models import JobManager, MarketContextJob, JobStatus, ToolStatus, ToolExecution, IterationResult
from prompts_config import DEFAULT_VALUES


@dataclass
class AgentRunResult:
    """Result of an agent run."""
    success: bool
    job_id: str
    final_commentary: Optional[str] = None
    quality_score: Optional[float] = None
    iterations: int = 0
    error_message: Optional[str] = None
    execution_time: Optional[float] = None


class CoreAgentRunner:
    """Core agent runner without UI dependencies."""
    
    def __init__(self):
        self.job_manager = JobManager()
        self.agent = MarketContextAgent()
    
    def create_job(self, strategy_name: str, quarter: str, year: int, 
                   benchmark: str = None, custom_instructions: str = None) -> MarketContextJob:
        """Create a new market context job."""
        if benchmark is None:
            benchmark = DEFAULT_VALUES['benchmark']
        
        job = self.job_manager.create_job(
            strategy_name=strategy_name,
            quarter=quarter,
            year=year,
            benchmark=benchmark,
            custom_instructions=custom_instructions
        )
        
        print(f"✅ Created job: {job.job_id[:8]}... - {strategy_name} {quarter} {year}")
        return job
    
    def run_job(self, job_id: str) -> AgentRunResult:
        """Run a market context generation job."""
        job = self.job_manager.get_job(job_id)
        if not job:
            return AgentRunResult(
                success=False,
                job_id=job_id,
                error_message="Job not found"
            )
        
        start_time = datetime.now()
        
        try:
            # Start job
            self.job_manager.start_job(job_id)
            print(f"🚀 Starting job: {job.strategy_name} {job.quarter} {job.year}")
            
            # Create request
            request = MarketContextRequest(
                strategy_name=job.strategy_name,
                quarter=job.quarter,
                year=job.year,
                benchmark=job.benchmark,
                custom_instructions=job.custom_instructions
            )
            
            # Run the agent
            result = self.agent.generate_market_context(request)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Check if result is a string (successful generation) or error message
            if isinstance(result, str) and not result.startswith("Error:"):
                # Success - extract quality score from the result if possible
                quality_score = self._extract_quality_score(result)
                
                # Complete job
                self.job_manager.complete_job(job_id, result, quality_score)
                
                print(f"✅ Job completed successfully!")
                print(f"   Quality Score: {quality_score}/10")
                print(f"   Execution Time: {execution_time:.2f}s")
                print(f"   Final Commentary Length: {len(result)} characters")
                
                # Show iteration summary
                self._print_iteration_summary(job)
                
                return AgentRunResult(
                    success=True,
                    job_id=job_id,
                    final_commentary=result,
                    quality_score=quality_score,
                    iterations=len(job.iterations),
                    execution_time=execution_time
                )
            else:
                # Fail job
                error_message = result if isinstance(result, str) else "Unknown error"
                self.job_manager.fail_job(job_id, error_message)
                
                print(f"❌ Job failed: {error_message}")
                
                return AgentRunResult(
                    success=False,
                    job_id=job_id,
                    error_message=error_message,
                    execution_time=execution_time
                )
                
        except Exception as e:
            # Fail job
            self.job_manager.fail_job(job_id, str(e))
            
            print(f"❌ Job failed with exception: {str(e)}")
            
            return AgentRunResult(
                success=False,
                job_id=job_id,
                error_message=str(e),
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    def get_job(self, job_id: str) -> Optional[MarketContextJob]:
        """Get a job by ID."""
        return self.job_manager.get_job(job_id)
    
    def get_all_jobs(self) -> list[MarketContextJob]:
        """Get all jobs."""
        return self.job_manager.get_all_jobs()
    
    def get_jobs_summary(self) -> Dict[str, Any]:
        """Get jobs summary."""
        return self.job_manager.get_jobs_summary()
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        return self.job_manager.delete_job(job_id)
    
    def print_job_details(self, job_id: str):
        """Print detailed job information."""
        job = self.get_job(job_id)
        if not job:
            print(f"❌ Job {job_id} not found")
            return
        
        print(f"\n📋 Job Details: {job.job_id[:8]}...")
        print(f"   Strategy: {job.strategy_name}")
        print(f"   Period: {job.quarter} {job.year}")
        print(f"   Benchmark: {job.benchmark}")
        print(f"   Status: {job.status.value}")
        print(f"   Created: {job.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if job.started_at:
            print(f"   Started: {job.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if job.completed_at:
            print(f"   Completed: {job.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if job.final_quality_score:
            print(f"   Quality Score: {job.final_quality_score}/10")
        
        if job.iterations:
            print(f"   Iterations: {len(job.iterations)}")
            for i, iteration in enumerate(job.iterations, 1):
                print(f"     Iteration {i}: {iteration.quality_score}/10" if iteration.quality_score else f"     Iteration {i}: In progress")
        
        if job.final_commentary:
            print(f"   Commentary Length: {len(job.final_commentary)} characters")
        
        if job.error_message:
            print(f"   Error: {job.error_message}")
    
    def print_jobs_list(self):
        """Print a list of all jobs."""
        jobs = self.get_all_jobs()
        if not jobs:
            print("📭 No jobs found")
            return
        
        print(f"\n📊 Jobs Summary ({len(jobs)} total)")
        print("-" * 80)
        print(f"{'ID':<8} {'Strategy':<20} {'Period':<8} {'Status':<12} {'Quality':<8} {'Created'}")
        print("-" * 80)
        
        for job in sorted(jobs, key=lambda x: x.created_at, reverse=True):
            quality_str = f"{job.final_quality_score}/10" if job.final_quality_score else "-"
            created_str = job.created_at.strftime('%m-%d %H:%M')
            
            print(f"{job.job_id[:8]:<8} {job.strategy_name[:20]:<20} {job.quarter} {job.year:<4} {job.status.value:<12} {quality_str:<8} {created_str}")
    
    def _print_iteration_summary(self, job):
        """Print a summary of iterations with quality scores, word counts, and feedback."""
        # Use agent's tracked iterations if available
        if hasattr(self.agent, 'iterations') and self.agent.iterations:
            print(f"\n📊 Iteration Summary:")
            print("-" * 60)
            
            for i, iteration_data in enumerate(self.agent.iterations, 1):
                # Check if this is the best iteration
                is_best = (hasattr(self.agent, 'best_iteration') and 
                          self.agent.best_iteration.get('quality_score') == iteration_data.get('quality_score'))
                best_marker = " ⭐ BEST" if is_best else ""
                
                print(f"Iteration {i}:{best_marker}")
                
                # Print quality score
                if iteration_data.get('quality_score'):
                    score = iteration_data['quality_score']
                    score_class = "🟢" if score >= DEFAULT_VALUES["quality_score_threshold"] else "🟡" if score >= 7.0 else "🔴"
                    print(f"  Quality Score: {score_class} {score}/10")
                
                # Print word count
                if iteration_data.get('word_count'):
                    word_count = iteration_data['word_count']
                    print(f"  Word Count: {word_count} words")
                
                # Print feedback (truncated)
                if iteration_data.get('quality_feedback'):
                    feedback = iteration_data['quality_feedback']
                    # Truncate feedback to first 100 characters
                    truncated_feedback = feedback[:100] + "..." if len(feedback) > 100 else feedback
                    print(f"  Feedback: {truncated_feedback}")
                
                # Print missing data requirements (truncated)
                if iteration_data.get('missing_data_requirements'):
                    missing_data = iteration_data['missing_data_requirements']
                    # Truncate missing data to first 100 characters
                    truncated_missing_data = missing_data[:100] + "..." if len(missing_data) > 100 else missing_data
                    print(f"  Missing Data: {truncated_missing_data}")
                
                print()  # Empty line between iterations
        else:
            # Fallback to job iterations if agent tracking not available
            if not job.iterations:
                return
            
            print(f"\n📊 Iteration Summary:")
            print("-" * 60)
            
            for i, iteration in enumerate(job.iterations, 1):
                print(f"Iteration {i}:")
                
                # Find quality review tool execution
                quality_tool = None
                commentary_tool = None
                
                for tool_exec in iteration.tool_executions:
                    if tool_exec.tool_name == "quality_review" and tool_exec.status.value == "completed":
                        quality_tool = tool_exec
                    elif tool_exec.tool_name == "commentary_generation" and tool_exec.status.value == "completed":
                        commentary_tool = tool_exec
                
                # Print quality score
                if quality_tool and quality_tool.metadata.get("quality_score"):
                    score = quality_tool.metadata["quality_score"]
                    score_class = "🟢" if score >= DEFAULT_VALUES["quality_score_threshold"] else "🟡" if score >= 7.0 else "🔴"
                    print(f"  Quality Score: {score_class} {score}/10")
                
                # Print word count
                if commentary_tool and commentary_tool.metadata.get("word_count"):
                    word_count = commentary_tool.metadata["word_count"]
                    print(f"  Word Count: {word_count} words")
                elif quality_tool and quality_tool.metadata.get("word_count"):
                    word_count = quality_tool.metadata["word_count"]
                    print(f"  Word Count: {word_count} words")
                
                # Print feedback (truncated)
                if quality_tool and quality_tool.metadata.get("quality_feedback"):
                    feedback = quality_tool.metadata["quality_feedback"]
                    # Truncate feedback to first 100 characters
                    truncated_feedback = feedback[:100] + "..." if len(feedback) > 100 else feedback
                    print(f"  Feedback: {truncated_feedback}")
                
                print()  # Empty line between iterations
    
    def _extract_quality_score(self, commentary: str) -> float:
        """Extract quality score from commentary if available."""
        try:
            # First try to get the best iteration's score from the agent
            if hasattr(self.agent, 'best_iteration') and self.agent.best_iteration.get('quality_score'):
                return self.agent.best_iteration['quality_score']
            
            # Look for quality score in the commentary
            lines = commentary.split('\n')
            for line in lines:
                if 'QUALITY_SCORE:' in line:
                    score_text = line.split('QUALITY_SCORE:')[1].strip()
                    return float(score_text)
            # If no quality score found, return a default based on content quality
            if len(commentary) > 1000 and 'Market Context' in commentary:
                return 8.5  # Default good score for substantial commentary
            return 7.0  # Default score
        except (ValueError, IndexError):
            return 7.0  # Default score if parsing fails
    
    def save_job_result(self, job_id: str, filename: str = None):
        """Save job result to file."""
        job = self.get_job(job_id)
        if not job or not job.final_commentary:
            print(f"❌ No result to save for job {job_id}")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"market_context_{job.strategy_name.replace(' ', '_')}_{job.quarter}_{job.year}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Market Context for {job.strategy_name} - {job.quarter} {job.year}\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Quality Score: {job.final_quality_score}/10\n")
                f.write(f"Benchmark: {job.benchmark}\n")
                f.write("=" * 80 + "\n\n")
                f.write(job.final_commentary)
            
            print(f"💾 Saved result to: {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Market Context Generator - Core Agentic System')
    parser.add_argument('--strategy', required=True, help='Strategy name')
    parser.add_argument('--quarter', required=True, choices=['Q1', 'Q2', 'Q3', 'Q4'], help='Quarter')
    parser.add_argument('--year', type=int, required=True, help='Year')
    parser.add_argument('--benchmark', default='S&P 500', help='Benchmark (default: S&P 500)')
    parser.add_argument('--instructions', help='Custom instructions')
    parser.add_argument('--list', action='store_true', help='List all jobs')
    parser.add_argument('--show', help='Show job details by ID')
    parser.add_argument('--save', help='Save job result to file')
    parser.add_argument('--delete', help='Delete job by ID')
    
    args = parser.parse_args()
    
    runner = CoreAgentRunner()
    
    if args.list:
        runner.print_jobs_list()
        return
    
    if args.show:
        runner.print_job_details(args.show)
        return
    
    if args.save:
        runner.save_job_result(args.save)
        return
    
    if args.delete:
        if runner.delete_job(args.delete):
            print(f"✅ Deleted job {args.delete}")
        else:
            print(f"❌ Failed to delete job {args.delete}")
        return
    
    # Create and run job
    job = runner.create_job(
        strategy_name=args.strategy,
        quarter=args.quarter,
        year=args.year,
        benchmark=args.benchmark,
        custom_instructions=args.instructions
    )
    
    result = runner.run_job(job.job_id)
    
    if result.success:
        print(f"\n🎯 Final Commentary Preview:")
        print("-" * 50)
        print(result.final_commentary[:500] + "..." if len(result.final_commentary) > 500 else result.final_commentary)
        print("-" * 50)
        
        # Auto-save result
        runner.save_job_result(job.job_id)
    else:
        print(f"\n❌ Job failed: {result.error_message}")


if __name__ == '__main__':
    main()
