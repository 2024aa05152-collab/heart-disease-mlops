"""
CPU and System Resource Metrics for Heart Disease Prediction API
Monitors CPU utilization, memory usage, and system performance
"""

from prometheus_client import Gauge, Counter
import psutil
import threading
import time
from typing import Optional


# ============================================================================
# CPU Metrics
# ============================================================================

# CPU utilization gauge (percentage)
cpu_utilization = Gauge(
    'heart_api_cpu_utilization_percent',
    'Current CPU utilization percentage',
    ['cpu_type']  # 'overall', 'per_core'
)

# CPU usage per core
cpu_per_core = Gauge(
    'heart_api_cpu_per_core_percent',
    'CPU utilization per core',
    ['core']
)

# ============================================================================
# Memory Metrics
# ============================================================================

# Memory usage gauge (bytes)
memory_usage_bytes = Gauge(
    'heart_api_memory_usage_bytes',
    'Current memory usage in bytes',
    ['memory_type']  # 'rss', 'vms', 'percent'
)

# Memory percent gauge
memory_percent = Gauge(
    'heart_api_memory_percent',
    'Current memory usage as percentage of total'
)

# ============================================================================
# Process Metrics
# ============================================================================

# Number of threads
thread_count = Gauge(
    'heart_api_thread_count',
    'Current number of threads in the process'
)

# Number of open file descriptors
open_files = Gauge(
    'heart_api_open_files',
    'Number of open file descriptors'
)

# Process CPU time
process_cpu_seconds = Gauge(
    'heart_api_process_cpu_seconds_total',
    'Total CPU time spent in the process',
    ['mode']  # 'user', 'system'
)

# ============================================================================
# System Metrics
# ============================================================================

# System CPU utilization
system_cpu_utilization = Gauge(
    'heart_api_system_cpu_utilization_percent',
    'System-wide CPU utilization',
    ['mode']  # 'user', 'system', 'idle'
)

# System memory usage
system_memory_usage = Gauge(
    'heart_api_system_memory_usage_bytes',
    'System memory usage',
    ['memory_type']  # 'total', 'available', 'used', 'free'
)

# System memory percent
system_memory_percent = Gauge(
    'heart_api_system_memory_percent',
    'System memory usage as percentage'
)

# Disk usage
disk_usage = Gauge(
    'heart_api_disk_usage_bytes',
    'Disk usage in bytes',
    ['disk_type']  # 'total', 'used', 'free'
)

# Disk percent
disk_percent = Gauge(
    'heart_api_disk_percent',
    'Disk usage as percentage'
)

# ============================================================================
# Monitoring Thread
# ============================================================================

class CPUMetricsCollector:
    """
    Background thread that periodically collects CPU and system metrics
    """
    
    def __init__(self, interval: int = 5):
        """
        Initialize the CPU metrics collector
        
        Args:
            interval: Collection interval in seconds (default: 5)
        """
        self.interval = interval
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.process = psutil.Process()
    
    def start(self):
        """Start the metrics collection thread"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._collect_metrics, daemon=True)
        self.thread.start()
        print("CPU metrics collector started")
    
    def stop(self):
        """Stop the metrics collection thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("CPU metrics collector stopped")
    
    def _collect_metrics(self):
        """Main metrics collection loop"""
        while self.running:
            try:
                self._collect_cpu_metrics()
                self._collect_memory_metrics()
                self._collect_process_metrics()
                self._collect_system_metrics()
                self._collect_disk_metrics()
            except Exception as e:
                print(f"Error collecting metrics: {e}")
            
            time.sleep(self.interval)
    
    def _collect_cpu_metrics(self):
        """Collect CPU utilization metrics"""
        try:
            # Overall CPU usage
            overall_cpu = psutil.cpu_percent(interval=0.1)
            cpu_utilization.labels(cpu_type='overall').set(overall_cpu)
            
            # Per-core CPU usage
            per_core = psutil.cpu_percent(interval=0.1, percpu=True)
            for i, usage in enumerate(per_core):
                cpu_per_core.labels(core=str(i)).set(usage)
        except Exception as e:
            print(f"Error collecting CPU metrics: {e}")
    
    def _collect_memory_metrics(self):
        """Collect memory usage metrics"""
        try:
            # Process memory
            mem_info = self.process.memory_info()
            memory_usage_bytes.labels(memory_type='rss').set(mem_info.rss)
            memory_usage_bytes.labels(memory_type='vms').set(mem_info.vms)
            
            # Process memory percent
            mem_percent = self.process.memory_percent()
            memory_percent.set(mem_percent)
            memory_usage_bytes.labels(memory_type='percent').set(mem_percent)
        except Exception as e:
            print(f"Error collecting memory metrics: {e}")
    
    def _collect_process_metrics(self):
        """Collect process-related metrics"""
        try:
            # Thread count
            thread_count.set(self.process.num_threads())
            
            # Open files
            try:
                open_files.set(len(self.process.open_files()))
            except (psutil.AccessDenied, AttributeError):
                pass  # May not be available on all systems
            
            # CPU times
            cpu_times = self.process.cpu_times()
            process_cpu_seconds.labels(mode='user').set(cpu_times.user)
            process_cpu_seconds.labels(mode='system').set(cpu_times.system)
        except Exception as e:
            print(f"Error collecting process metrics: {e}")
    
    def _collect_system_metrics(self):
        """Collect system-wide metrics"""
        try:
            # System CPU usage
            cpu_times = psutil.cpu_times_percent(interval=0.1)
            system_cpu_utilization.labels(mode='user').set(cpu_times.user)
            system_cpu_utilization.labels(mode='system').set(cpu_times.system)
            system_cpu_utilization.labels(mode='idle').set(cpu_times.idle)
            
            # System memory
            vm = psutil.virtual_memory()
            system_memory_usage.labels(memory_type='total').set(vm.total)
            system_memory_usage.labels(memory_type='available').set(vm.available)
            system_memory_usage.labels(memory_type='used').set(vm.used)
            system_memory_usage.labels(memory_type='free').set(vm.free)
            system_memory_percent.set(vm.percent)
        except Exception as e:
            print(f"Error collecting system metrics: {e}")
    
    def _collect_disk_metrics(self):
        """Collect disk usage metrics"""
        try:
            disk = psutil.disk_usage('/')
            disk_usage.labels(disk_type='total').set(disk.total)
            disk_usage.labels(disk_type='used').set(disk.used)
            disk_usage.labels(disk_type='free').set(disk.free)
            disk_percent.set(disk.percent)
        except Exception as e:
            print(f"Error collecting disk metrics: {e}")


# Global collector instance
_collector: Optional[CPUMetricsCollector] = None


def start_cpu_metrics_collection(interval: int = 5):
    """
    Start collecting CPU and system metrics
    
    Args:
        interval: Collection interval in seconds
    """
    global _collector
    if _collector is None:
        _collector = CPUMetricsCollector(interval=interval)
    _collector.start()


def stop_cpu_metrics_collection():
    """Stop collecting CPU and system metrics"""
    global _collector # noqa: F824
    if _collector is not None:
        _collector.stop()
