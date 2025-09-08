#!/usr/bin/env python3
"""
Demo script for the core agentic market context generation system.
"""
import os
from agent_runner import CoreAgentRunner
from job_models import JobStatus


def main():
    """Demo the core agentic system."""
    print("🤖 Market Context Generator - Core Agentic System Demo")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment")
        print("   Please set your OpenAI API key to run the demo")
        return
    
    # Initialize runner
    runner = CoreAgentRunner()
    
    # Demo 1: Create and run a simple job
    print("\n📝 Demo 1: Creating and running a market context job")
    print("-" * 50)
    
    job1 = runner.create_job(
        strategy_name="US Equity Core",
        quarter="Q1",
        year=2024,
        benchmark="S&P 500",
        custom_instructions="Focus on technology sector performance and interest rate impacts"
    )
    
    print(f"Job created with ID: {job1.job_id}")
    
    # Run the job
    result1 = runner.run_job(job1.job_id)
    
    if result1.success:
        print(f"✅ Job completed successfully!")
        print(f"   Quality Score: {result1.quality_score}/10")
        print(f"   Iterations: {result1.iterations}")
        print(f"   Execution Time: {result1.execution_time:.2f}s")
        print(f"   Commentary Length: {len(result1.final_commentary)} characters")
    else:
        print(f"❌ Job failed: {result1.error_message}")
    
    # Demo 2: Create multiple jobs
    print("\n📝 Demo 2: Creating multiple jobs")
    print("-" * 50)
    
    jobs_data = [
        ("Technology Growth", "Q1", 2024, "NASDAQ", "Focus on AI and cloud computing trends"),
        ("Value Strategy", "Q1", 2024, "Russell 2000", "Emphasize value opportunities and market inefficiencies"),
        ("International Equity", "Q1", 2024, "MSCI EAFE", "Cover global market dynamics and currency impacts")
    ]
    
    created_jobs = []
    for strategy, quarter, year, benchmark, instructions in jobs_data:
        job = runner.create_job(strategy, quarter, year, benchmark, instructions)
        created_jobs.append(job)
    
    print(f"✅ Created {len(created_jobs)} additional jobs")
    
    # Demo 3: Show jobs summary
    print("\n📊 Demo 3: Jobs Summary")
    print("-" * 50)
    
    runner.print_jobs_list()
    
    # Demo 4: Show job details
    print("\n📋 Demo 4: Job Details")
    print("-" * 50)
    
    if created_jobs:
        runner.print_job_details(created_jobs[0].job_id)
    
    # Demo 5: Save results
    print("\n💾 Demo 5: Saving Results")
    print("-" * 50)
    
    for job in [job1] + created_jobs:
        if job.status == JobStatus.COMPLETED:
            runner.save_job_result(job.job_id)
    
    print("\n🎯 Demo completed!")
    print("=" * 60)
    print("Core agentic system is ready for integration with any UI framework.")
    print("Key features:")
    print("  ✅ Job management (create, run, track, delete)")
    print("  ✅ Quality loop with iterative improvement")
    print("  ✅ Real-time status tracking")
    print("  ✅ Result saving and export")
    print("  ✅ Multiple concurrent job support")
    print("  ✅ No UI dependencies - pure agentic functionality")


if __name__ == '__main__':
    main()
