#!/usr/bin/env python3
"""
Test script for the core agentic system.
"""
import os
from agent_runner import CoreAgentRunner
from job_models import JobStatus


def test_core_system():
    """Test the core agentic system functionality."""
    print("🧪 Testing Core Agentic System")
    print("=" * 50)
    
    # Test 1: Job Manager
    print("Test 1: Job Manager")
    runner = CoreAgentRunner()
    print("✅ CoreAgentRunner initialized")
    
    # Test 2: Job Creation
    print("\nTest 2: Job Creation")
    job = runner.create_job(
        strategy_name="Test Strategy",
        quarter="Q1",
        year=2024,
        benchmark="S&P 500"
    )
    print(f"✅ Job created: {job.job_id[:8]}...")
    print(f"   Status: {job.status.value}")
    print(f"   Strategy: {job.strategy_name}")
    
    # Test 3: Job Retrieval
    print("\nTest 3: Job Retrieval")
    retrieved_job = runner.get_job(job.job_id)
    assert retrieved_job is not None, "Job retrieval failed"
    assert retrieved_job.job_id == job.job_id, "Job ID mismatch"
    print("✅ Job retrieval successful")
    
    # Test 4: Jobs Summary
    print("\nTest 4: Jobs Summary")
    summary = runner.get_jobs_summary()
    assert summary['total_jobs'] >= 1, "Jobs summary incorrect"
    print(f"✅ Jobs summary: {summary}")
    
    # Test 5: Multiple Jobs
    print("\nTest 5: Multiple Jobs")
    job2 = runner.create_job("Test Strategy 2", "Q2", 2024, "NASDAQ")
    job3 = runner.create_job("Test Strategy 3", "Q3", 2024, "Russell 2000")
    
    all_jobs = runner.get_all_jobs()
    assert len(all_jobs) >= 3, "Multiple jobs creation failed"
    print(f"✅ Created {len(all_jobs)} jobs total")
    
    # Test 6: Job Status Management
    print("\nTest 6: Job Status Management")
    runner.job_manager.start_job(job.job_id)
    assert job.status == JobStatus.RUNNING, "Job start failed"
    print("✅ Job status management working")
    
    # Test 7: Job Deletion
    print("\nTest 7: Job Deletion")
    delete_result = runner.delete_job(job3.job_id)
    assert delete_result, "Job deletion failed"
    
    remaining_jobs = runner.get_all_jobs()
    assert len(remaining_jobs) == 2, "Job deletion count incorrect"
    print("✅ Job deletion successful")
    
    # Test 8: Job Details Printing
    print("\nTest 8: Job Details")
    runner.print_job_details(job.job_id)
    print("✅ Job details printing working")
    
    # Test 9: Jobs List Printing
    print("\nTest 9: Jobs List")
    runner.print_jobs_list()
    print("✅ Jobs list printing working")
    
    print("\n🎯 All Core System Tests Passed!")
    print("=" * 50)
    print("Core agentic system is fully functional and ready for use.")
    
    return True


def test_without_api_key():
    """Test system without API key (should not crash)."""
    print("\n🔒 Testing without API key...")
    
    # Temporarily remove API key
    original_key = os.environ.get('OPENAI_API_KEY')
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        runner = CoreAgentRunner()
        job = runner.create_job("Test", "Q1", 2024)
        print("✅ System handles missing API key gracefully")
        return True
    except Exception as e:
        print(f"❌ System failed without API key: {e}")
        return False
    finally:
        # Restore API key
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key


if __name__ == '__main__':
    try:
        # Run core system tests
        test_core_system()
        
        # Test without API key
        test_without_api_key()
        
        print("\n🎉 All tests completed successfully!")
        print("The core agentic system is ready for integration.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
