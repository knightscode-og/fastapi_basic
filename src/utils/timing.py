"""Request timing instrumentation for performance monitoring.

Provides decorators and utilities for measuring and logging endpoint
response times to track performance metrics like p95 and p99 latencies.
"""

import functools
import logging
import time
from typing import Any, Callable, Coroutine, TypeVar

logger = logging.getLogger(__name__)

# Type variable for function decorators
F = TypeVar("F", bound=Callable[..., Any])


class LatencyTracker:
    """Tracks latency metrics for endpoint performance monitoring.
    
    Maintains running statistics for request/response times including
    min, max, mean, and percentile calculations for performance analysis.
    
    Attributes:
        endpoint_name: Descriptive name for the endpoint being tracked
        measurements: List of response times in milliseconds
    """

    def __init__(self, endpoint_name: str) -> None:
        """Initialize latency tracker for an endpoint.
        
        Args:
            endpoint_name: Human-readable name for the endpoint (e.g., "GET /tabs")
        """
        self.endpoint_name = endpoint_name
        self.measurements: list[float] = []

    def record(self, latency_ms: float) -> None:
        """Record a single latency measurement.
        
        Args:
            latency_ms: Response time in milliseconds
        """
        self.measurements.append(latency_ms)

    def percentile(self, p: float) -> float:
        """Calculate percentile of recorded latencies.
        
        Args:
            p: Percentile value (0-100), e.g., 95 for p95
        
        Returns:
            Latency in milliseconds at the requested percentile.
            Returns 0.0 if no measurements recorded.
        """
        if not self.measurements:
            return 0.0
        sorted_measurements = sorted(self.measurements)
        index = int((len(sorted_measurements) - 1) * (p / 100.0))
        return sorted_measurements[min(index, len(sorted_measurements) - 1)]

    def stats(self) -> dict[str, float]:
        """Get summary statistics for all recorded measurements.
        
        Returns:
            Dictionary with keys: count, min, max, mean, p50, p95, p99
        """
        if not self.measurements:
            return {
                "count": 0,
                "min": 0.0,
                "max": 0.0,
                "mean": 0.0,
                "p50": 0.0,
                "p95": 0.0,
                "p99": 0.0,
            }

        count = len(self.measurements)
        min_latency = min(self.measurements)
        max_latency = max(self.measurements)
        mean_latency = sum(self.measurements) / count

        return {
            "count": float(count),
            "min": min_latency,
            "max": max_latency,
            "mean": mean_latency,
            "p50": self.percentile(50),
            "p95": self.percentile(95),
            "p99": self.percentile(99),
        }


# Global registry of latency trackers per endpoint
_endpoint_trackers: dict[str, LatencyTracker] = {}


def get_tracker(endpoint_name: str) -> LatencyTracker:
    """Get or create a latency tracker for an endpoint.
    
    Args:
        endpoint_name: Name of the endpoint to track
    
    Returns:
        LatencyTracker instance for the endpoint
    """
    if endpoint_name not in _endpoint_trackers:
        _endpoint_trackers[endpoint_name] = LatencyTracker(endpoint_name)
    return _endpoint_trackers[endpoint_name]


def measure_latency(endpoint_name: str) -> Callable[[Callable[..., Coroutine[Any, Any, Any]]], Callable[..., Coroutine[Any, Any, Any]]]:
    """Decorator to measure and log endpoint response latency.
    
    Wraps async endpoint functions to record request/response time.
    Logs latency in milliseconds at DEBUG level.
    After every 10 requests, logs p95 and p99 percentiles at INFO level.
    
    Usage:
        @measure_latency("GET /api/v1/tabs")
        async def get_all_tabs() -> TabsListResponse:
            ...
    
    Args:
        endpoint_name: Human-readable endpoint name (e.g., "GET /api/v1/tabs")
    
    Returns:
        Decorated async function that measures latency
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
        @functools.wraps(func)
        async def wrapper(
            *args: Any, **kwargs: Any
        ) -> Any:
            tracker = get_tracker(endpoint_name)

            # Start timer
            start_time = time.time()

            try:
                # Execute endpoint function
                result = await func(*args, **kwargs)
                return result
            finally:
                # Record latency
                elapsed_seconds = time.time() - start_time
                elapsed_ms = elapsed_seconds * 1000

                tracker.record(elapsed_ms)

                # Log individual request latency at DEBUG level
                logger.debug(
                    "%s latency: %.2fms",
                    endpoint_name,
                    elapsed_ms,
                )

                # Log percentiles at INFO level every 10 requests
                if tracker.measurements and len(tracker.measurements) % 10 == 0:
                    stats = tracker.stats()
                    logger.info(
                        "%s statistics (n=%d): p95=%.2fms, p99=%.2fms, mean=%.2fms",
                        endpoint_name,
                        int(stats["count"]),
                        stats["p95"],
                        stats["p99"],
                        stats["mean"],
                    )

        return wrapper

    return decorator


def get_all_stats() -> dict[str, dict[str, float]]:
    """Get summary statistics for all tracked endpoints.
    
    Returns:
        Dictionary mapping endpoint names to their statistics dictionaries
    """
    return {
        name: tracker.stats()
        for name, tracker in _endpoint_trackers.items()
    }
