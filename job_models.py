"""
Job management models for market context generation.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
import uuid


class JobStatus(Enum):
    """Job status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ToolStatus(Enum):
    """Tool execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ToolExecution:
    """Represents a single tool execution within a job."""
    tool_name: str
    status: ToolStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "tool_name": self.tool_name,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "error_message": self.error_message,
            "metadata": self.metadata
        }


@dataclass
class IterationResult:
    """Represents the result of one iteration in the quality loop."""
    iteration_number: int
    start_time: datetime
    end_time: Optional[datetime] = None
    tool_executions: List[ToolExecution] = field(default_factory=list)
    quality_score: Optional[float] = None
    quality_feedback: Optional[str] = None
    commentary_word_count: Optional[int] = None
    missing_data_analysis: Optional[str] = None
    data_collection_prompts: List[str] = field(default_factory=list)
    missing_data_categories: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "iteration_number": self.iteration_number,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "tool_executions": [tool.to_dict() for tool in self.tool_executions],
            "quality_score": self.quality_score,
            "quality_feedback": self.quality_feedback,
            "commentary_word_count": self.commentary_word_count,
            "missing_data_analysis": self.missing_data_analysis,
            "data_collection_prompts": self.data_collection_prompts,
            "missing_data_categories": self.missing_data_categories
        }


@dataclass
class MarketContextJob:
    """Represents a complete market context generation job."""
    job_id: str
    strategy_name: str
    quarter: str
    year: int
    benchmark: str
    custom_instructions: Optional[str] = None
    
    # Job metadata
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: JobStatus = JobStatus.PENDING
    
    # Job results
    iterations: List[IterationResult] = field(default_factory=list)
    final_commentary: Optional[str] = None
    final_quality_score: Optional[float] = None
    error_message: Optional[str] = None
    
    # Progress tracking
    current_iteration: int = 0
    total_iterations: int = 0
    
    @classmethod
    def create_new(cls, strategy_name: str, quarter: str, year: int, 
                   benchmark: str, custom_instructions: Optional[str] = None) -> 'MarketContextJob':
        """Create a new job with a unique ID."""
        return cls(
            job_id=str(uuid.uuid4()),
            strategy_name=strategy_name,
            quarter=quarter,
            year=year,
            benchmark=benchmark,
            custom_instructions=custom_instructions
        )
    
    def start_job(self) -> None:
        """Mark job as started."""
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now()
    
    def complete_job(self, final_commentary: str, final_quality_score: float) -> None:
        """Mark job as completed."""
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now()
        self.final_commentary = final_commentary
        self.final_quality_score = final_quality_score
    
    def fail_job(self, error_message: str) -> None:
        """Mark job as failed."""
        self.status = JobStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error_message
    
    def cancel_job(self) -> None:
        """Mark job as cancelled."""
        self.status = JobStatus.CANCELLED
        self.completed_at = datetime.now()
    
    def add_iteration(self, iteration: IterationResult) -> None:
        """Add an iteration result to the job."""
        self.iterations.append(iteration)
        self.current_iteration = len(self.iterations)
    
    def get_current_iteration(self) -> Optional[IterationResult]:
        """Get the current iteration."""
        if self.iterations:
            return self.iterations[-1]
        return None
    
    def get_progress_percentage(self) -> float:
        """Get job progress as a percentage."""
        if self.status == JobStatus.COMPLETED:
            return 100.0
        elif self.status == JobStatus.FAILED or self.status == JobStatus.CANCELLED:
            return 0.0
        elif self.total_iterations > 0:
            return min(100.0, (self.current_iteration / self.total_iterations) * 100.0)
        else:
            return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "job_id": self.job_id,
            "strategy_name": self.strategy_name,
            "quarter": self.quarter,
            "year": self.year,
            "benchmark": self.benchmark,
            "custom_instructions": self.custom_instructions,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status.value,
            "iterations": [iteration.to_dict() for iteration in self.iterations],
            "final_commentary": self.final_commentary,
            "final_quality_score": self.final_quality_score,
            "error_message": self.error_message,
            "current_iteration": self.current_iteration,
            "total_iterations": self.total_iterations,
            "progress_percentage": self.get_progress_percentage()
        }


class JobManager:
    """Manages multiple market context jobs."""
    
    def __init__(self):
        self.jobs: Dict[str, MarketContextJob] = {}
        self.active_jobs: List[str] = []  # Job IDs currently running
    
    def create_job(self, strategy_name: str, quarter: str, year: int, 
                   benchmark: str, custom_instructions: Optional[str] = None) -> MarketContextJob:
        """Create a new job."""
        job = MarketContextJob.create_new(
            strategy_name=strategy_name,
            quarter=quarter,
            year=year,
            benchmark=benchmark,
            custom_instructions=custom_instructions
        )
        self.jobs[job.job_id] = job
        return job
    
    def get_job(self, job_id: str) -> Optional[MarketContextJob]:
        """Get a job by ID."""
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[MarketContextJob]:
        """Get all jobs."""
        return list(self.jobs.values())
    
    def get_active_jobs(self) -> List[MarketContextJob]:
        """Get all active (running) jobs."""
        return [self.jobs[job_id] for job_id in self.active_jobs if job_id in self.jobs]
    
    def start_job(self, job_id: str) -> bool:
        """Start a job."""
        job = self.get_job(job_id)
        if job and job.status == JobStatus.PENDING:
            job.start_job()
            self.active_jobs.append(job_id)
            return True
        return False
    
    def complete_job(self, job_id: str, final_commentary: str, final_quality_score: float) -> bool:
        """Complete a job."""
        job = self.get_job(job_id)
        if job and job.status == JobStatus.RUNNING:
            job.complete_job(final_commentary, final_quality_score)
            if job_id in self.active_jobs:
                self.active_jobs.remove(job_id)
            return True
        return False
    
    def fail_job(self, job_id: str, error_message: str) -> bool:
        """Fail a job."""
        job = self.get_job(job_id)
        if job and job.status == JobStatus.RUNNING:
            job.fail_job(error_message)
            if job_id in self.active_jobs:
                self.active_jobs.remove(job_id)
            return True
        return False
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job."""
        job = self.get_job(job_id)
        if job and job.status in [JobStatus.PENDING, JobStatus.RUNNING]:
            job.cancel_job()
            if job_id in self.active_jobs:
                self.active_jobs.remove(job_id)
            return True
        return False
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        if job_id in self.jobs:
            if job_id in self.active_jobs:
                self.active_jobs.remove(job_id)
            del self.jobs[job_id]
            return True
        return False
    
    def get_jobs_summary(self) -> Dict[str, Any]:
        """Get summary of all jobs."""
        total_jobs = len(self.jobs)
        active_jobs = len(self.active_jobs)
        completed_jobs = sum(1 for job in self.jobs.values() if job.status == JobStatus.COMPLETED)
        failed_jobs = sum(1 for job in self.jobs.values() if job.status == JobStatus.FAILED)
        pending_jobs = sum(1 for job in self.jobs.values() if job.status == JobStatus.PENDING)
        
        return {
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "completed_jobs": completed_jobs,
            "failed_jobs": failed_jobs,
            "pending_jobs": pending_jobs
        }
