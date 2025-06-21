"""
Learning Module for PDF Comparison Agent.
Stores and learns from comparison patterns to improve accuracy and performance.
"""

import json
import logging
import time
from typing import Dict, Any, List, Optional
from collections import defaultdict, Counter
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class LearningModule:
    """Learning module for pattern recognition and optimization."""
    
    def __init__(self, storage_path: str = "models/learning_data.json"):
        self.storage_path = Path(storage_path)
        self.patterns = {}
        self.statistics = {}
        self.frequent_changes = defaultdict(int)
        self.performance_metrics = {}
        self.logger = logging.getLogger(__name__)
        
        # Ensure storage directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_data()
        
    def _load_data(self):
        """Load learning data from storage."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.patterns = data.get('patterns', {})
                    self.statistics = data.get('statistics', {})
                    self.frequent_changes = defaultdict(int, data.get('frequent_changes', {}))
                    self.performance_metrics = data.get('performance_metrics', {})
                    
                self.logger.info(f"Loaded learning data from {self.storage_path}")
            else:
                self.logger.info("No existing learning data found, starting fresh")
                
        except Exception as e:
            self.logger.error(f"Error loading learning data: {str(e)}")
            # Initialize with empty data
            self.patterns = {}
            self.statistics = {}
            self.frequent_changes = defaultdict(int)
            self.performance_metrics = {}
            
    def _save_data(self):
        """Save learning data to storage."""
        try:
            data = {
                'patterns': self.patterns,
                'statistics': self.statistics,
                'frequent_changes': dict(self.frequent_changes),
                'performance_metrics': self.performance_metrics,
                'last_updated': time.time()
            }
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            self.logger.debug(f"Learning data saved to {self.storage_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving learning data: {str(e)}")
            
    def update_patterns(self, comparison_data: Dict[str, Any]):
        """Update patterns based on comparison results."""
        
        try:
            # Extract pattern key
            pattern_key = self._extract_pattern_key(comparison_data)
            
            # Update pattern frequency
            if pattern_key not in self.patterns:
                self.patterns[pattern_key] = {
                    'count': 0,
                    'first_seen': time.time(),
                    'last_seen': time.time(),
                    'examples': [],
                    'metadata': comparison_data
                }
            else:
                self.patterns[pattern_key]['count'] += 1
                self.patterns[pattern_key]['last_seen'] = time.time()
                
            # Store example (limit to last 10)
            examples = self.patterns[pattern_key]['examples']
            examples.append({
                'timestamp': time.time(),
                'data': comparison_data
            })
            
            # Keep only last 10 examples
            if len(examples) > 10:
                examples.pop(0)
                
            # Update frequent changes
            self._update_frequent_changes(comparison_data)
            
            # Save data
            self._save_data()
            
        except Exception as e:
            self.logger.error(f"Error updating patterns: {str(e)}")
            
    def _extract_pattern_key(self, data: Dict[str, Any]) -> str:
        """Extract a pattern key from comparison data."""
        
        # Extract key characteristics
        change_types = []
        severities = []
        
        if 'differences' in data:
            differences = data['differences']
            
            # Extract change types
            for diff in differences:
                if isinstance(diff, dict):
                    change_type = diff.get('type', 'unknown')
                    severity = diff.get('severity', 'unknown')
                    change_types.append(change_type)
                    severities.append(severity)
                    
        # Create pattern key
        change_type_str = '_'.join(sorted(set(change_types))) if change_types else 'no_changes'
        severity_str = '_'.join(sorted(set(severities))) if severities else 'no_severity'
        
        return f"{change_type_str}_{severity_str}"
        
    def _update_frequent_changes(self, comparison_data: Dict[str, Any]):
        """Update frequent changes tracking."""
        
        if 'differences' in comparison_data:
            differences = comparison_data['differences']
            
            for diff in differences:
                if isinstance(diff, dict):
                    # Create change signature
                    change_type = diff.get('type', 'unknown')
                    operation = diff.get('operation', 'unknown')
                    change_signature = f"{change_type}_{operation}"
                    
                    self.frequent_changes[change_signature] += 1
                    
    def get_frequent_patterns(self, min_frequency: int = 3) -> Dict[str, Any]:
        """Get patterns that occur frequently."""
        
        frequent = {}
        for pattern_key, pattern_data in self.patterns.items():
            if pattern_data['count'] >= min_frequency:
                frequent[pattern_key] = pattern_data
                
        return frequent
        
    def get_frequent_changes(self, min_frequency: int = 2) -> Dict[str, int]:
        """Get frequently occurring changes."""
        
        return {
            k: v for k, v in self.frequent_changes.items() 
            if v >= min_frequency
        }
        
    def update_statistics(self, metric: str, value: Any):
        """Update statistics."""
        
        if metric not in self.statistics:
            self.statistics[metric] = []
            
        self.statistics[metric].append({
            'value': value,
            'timestamp': time.time()
        })
        
        # Keep only last 1000 entries
        if len(self.statistics[metric]) > 1000:
            self.statistics[metric] = self.statistics[metric][-1000:]
            
        self._save_data()
        
    def get_statistics_summary(self) -> Dict[str, Any]:
        """Get a summary of statistics."""
        
        summary = {}
        
        for metric, values in self.statistics.items():
            if values:
                numeric_values = [v['value'] for v in values if isinstance(v['value'], (int, float))]
                
                if numeric_values:
                    summary[metric] = {
                        'count': len(numeric_values),
                        'mean': sum(numeric_values) / len(numeric_values),
                        'min': min(numeric_values),
                        'max': max(numeric_values),
                        'latest': values[-1]['value']
                    }
                else:
                    summary[metric] = {
                        'count': len(values),
                        'latest': values[-1]['value']
                    }
                    
        return summary
        
    def update_performance_metrics(self, operation: str, duration: float, success: bool):
        """Update performance metrics."""
        
        if operation not in self.performance_metrics:
            self.performance_metrics[operation] = {
                'total_operations': 0,
                'successful_operations': 0,
                'failed_operations': 0,
                'total_duration': 0.0,
                'avg_duration': 0.0,
                'min_duration': float('inf'),
                'max_duration': 0.0
            }
            
        metrics = self.performance_metrics[operation]
        metrics['total_operations'] += 1
        metrics['total_duration'] += duration
        
        if success:
            metrics['successful_operations'] += 1
        else:
            metrics['failed_operations'] += 1
            
        # Update averages and extremes
        metrics['avg_duration'] = metrics['total_duration'] / metrics['total_operations']
        metrics['min_duration'] = min(metrics['min_duration'], duration)
        metrics['max_duration'] = max(metrics['max_duration'], duration)
        
        self._save_data()
        
    def get_performance_insights(self) -> Dict[str, Any]:
        """Get performance insights and recommendations."""
        
        insights = {
            'slowest_operations': [],
            'most_failed_operations': [],
            'recommendations': []
        }
        
        # Find slowest operations
        operations_by_duration = []
        for operation, metrics in self.performance_metrics.items():
            if metrics['total_operations'] > 0:
                operations_by_duration.append({
                    'operation': operation,
                    'avg_duration': metrics['avg_duration'],
                    'total_operations': metrics['total_operations']
                })
                
        operations_by_duration.sort(key=lambda x: x['avg_duration'], reverse=True)
        insights['slowest_operations'] = operations_by_duration[:5]
        
        # Find operations with most failures
        operations_by_failures = []
        for operation, metrics in self.performance_metrics.items():
            if metrics['total_operations'] > 0:
                failure_rate = metrics['failed_operations'] / metrics['total_operations']
                operations_by_failures.append({
                    'operation': operation,
                    'failure_rate': failure_rate,
                    'failed_operations': metrics['failed_operations'],
                    'total_operations': metrics['total_operations']
                })
                
        operations_by_failures.sort(key=lambda x: x['failure_rate'], reverse=True)
        insights['most_failed_operations'] = operations_by_failures[:5]
        
        # Generate recommendations
        recommendations = []
        
        # Check for slow operations
        for op in insights['slowest_operations'][:3]:
            if op['avg_duration'] > 10.0:  # More than 10 seconds
                recommendations.append(f"Consider optimizing {op['operation']} (avg: {op['avg_duration']:.2f}s)")
                
        # Check for high failure rates
        for op in insights['most_failed_operations'][:3]:
            if op['failure_rate'] > 0.1:  # More than 10% failure rate
                recommendations.append(f"Investigate failures in {op['operation']} ({op['failure_rate']:.1%} failure rate)")
                
        # Check for frequent patterns
        frequent_patterns = self.get_frequent_patterns(min_frequency=5)
        if frequent_patterns:
            recommendations.append(f"Found {len(frequent_patterns)} frequent patterns - consider caching or optimization")
            
        insights['recommendations'] = recommendations
        
        return insights
        
    def predict_comparison_time(self, file_count: int, avg_file_size_mb: float) -> float:
        """Predict comparison time based on historical data."""
        
        if 'comparison_duration' not in self.statistics:
            return 30.0  # Default estimate
            
        durations = [v['value'] for v in self.statistics['comparison_duration'] 
                    if isinstance(v['value'], (int, float))]
        
        if not durations:
            return 30.0
            
        # Calculate average duration per file
        avg_duration_per_file = sum(durations) / len(durations)
        
        # Estimate based on file count and size
        estimated_time = avg_duration_per_file * file_count
        
        # Adjust for file size (larger files take longer)
        size_factor = min(2.0, max(0.5, avg_file_size_mb / 5.0))  # Normalize to 5MB baseline
        estimated_time *= size_factor
        
        return estimated_time
        
    def get_optimization_suggestions(self) -> List[str]:
        """Get optimization suggestions based on learning data."""
        
        suggestions = []
        
        # Check performance metrics
        insights = self.get_performance_insights()
        
        # Add performance-based suggestions
        for recommendation in insights['recommendations']:
            suggestions.append(recommendation)
            
        # Check for frequent patterns that could be cached
        frequent_patterns = self.get_frequent_patterns(min_frequency=3)
        if len(frequent_patterns) > 5:
            suggestions.append("Consider implementing pattern caching for frequently occurring changes")
            
        # Check for common failure patterns
        if 'validation_errors' in self.statistics:
            error_count = len(self.statistics['validation_errors'])
            if error_count > 10:
                suggestions.append("High number of validation errors - review file validation logic")
                
        # Check for memory usage patterns
        if 'memory_usage_mb' in self.statistics:
            memory_values = [v['value'] for v in self.statistics['memory_usage_mb'] 
                           if isinstance(v['value'], (int, float))]
            if memory_values:
                avg_memory = sum(memory_values) / len(memory_values)
                if avg_memory > 1000:  # More than 1GB
                    suggestions.append("High memory usage detected - consider implementing memory optimization")
                    
        return suggestions
        
    def clear_old_data(self, days_to_keep: int = 30):
        """Clear old learning data to prevent storage bloat."""
        
        cutoff_time = time.time() - (days_to_keep * 24 * 3600)
        
        # Clear old statistics
        for metric in list(self.statistics.keys()):
            self.statistics[metric] = [
                v for v in self.statistics[metric] 
                if v['timestamp'] > cutoff_time
            ]
            
            # Remove empty metrics
            if not self.statistics[metric]:
                del self.statistics[metric]
                
        # Clear old patterns (keep only recent examples)
        for pattern_key in list(self.patterns.keys()):
            pattern = self.patterns[pattern_key]
            pattern['examples'] = [
                ex for ex in pattern['examples'] 
                if ex['timestamp'] > cutoff_time
            ]
            
            # Remove patterns with no recent examples
            if not pattern['examples'] and pattern['last_seen'] < cutoff_time:
                del self.patterns[pattern_key]
                
        self._save_data()
        self.logger.info(f"Cleared learning data older than {days_to_keep} days")
        
    def export_learning_data(self, export_path: str):
        """Export learning data for analysis."""
        
        export_data = {
            'patterns': self.patterns,
            'statistics': self.statistics,
            'frequent_changes': dict(self.frequent_changes),
            'performance_metrics': self.performance_metrics,
            'export_timestamp': time.time()
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        self.logger.info(f"Learning data exported to {export_path}")
        
    def import_learning_data(self, import_path: str):
        """Import learning data from file."""
        
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
                
            # Merge data
            self.patterns.update(import_data.get('patterns', {}))
            self.statistics.update(import_data.get('statistics', {}))
            
            # Merge frequent changes
            for change, count in import_data.get('frequent_changes', {}).items():
                self.frequent_changes[change] += count
                
            # Merge performance metrics
            for operation, metrics in import_data.get('performance_metrics', {}).items():
                if operation not in self.performance_metrics:
                    self.performance_metrics[operation] = metrics
                else:
                    # Merge metrics
                    existing = self.performance_metrics[operation]
                    existing['total_operations'] += metrics.get('total_operations', 0)
                    existing['successful_operations'] += metrics.get('successful_operations', 0)
                    existing['failed_operations'] += metrics.get('failed_operations', 0)
                    existing['total_duration'] += metrics.get('total_duration', 0)
                    
                    # Recalculate averages
                    if existing['total_operations'] > 0:
                        existing['avg_duration'] = existing['total_duration'] / existing['total_operations']
                        
            self._save_data()
            self.logger.info(f"Learning data imported from {import_path}")
            
        except Exception as e:
            self.logger.error(f"Error importing learning data: {str(e)}")
            raise 