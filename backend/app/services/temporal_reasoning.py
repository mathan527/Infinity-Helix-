"""
Temporal Reasoning Engine - The Agent's Temporal Cognition Module

This module enables the AI agent to reason OVER TIME, not just across documents.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHITECTURAL PHILOSOPHY: Why Temporal Reasoning Matters
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Traditional RAG Systems:
- Query: "What is my glucose level?"
- Answer: "Your glucose is 180 mg/dL" 
- Problem: NO temporal context. Is this improving? Worsening? First time?

Temporal Reasoning System:
- Query: "What is my glucose level?"
- Answer: "Your glucose is 180 mg/dL. This is +15 mg/dL since last month (was 165).
          Risk level increased from 'borderline' to 'concerning'. This is the 3rd 
          consecutive increase. Recommend medication review."
- Power: CONTEXT + TREND + RISK PROGRESSION

This is the difference between a document search engine and a medical intelligence agent.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ChangeDirection(str, Enum):
    """Direction of change"""
    INCREASED = "increased"
    DECREASED = "decreased"
    STABLE = "stable"
    NEW = "new"
    RESOLVED = "resolved"


class RiskProgression(str, Enum):
    """How risk level changed"""
    IMPROVED = "improved"
    WORSENED = "worsened"
    STABLE = "stable"
    NEW_RISK = "new_risk"
    RESOLVED_RISK = "resolved_risk"


@dataclass
class TemporalMetric:
    """Represents a metric with temporal context"""
    metric_name: str
    current_value: float
    previous_value: Optional[float]
    change: Optional[float]
    percent_change: Optional[float]
    direction: ChangeDirection
    first_observed: str  # ISO timestamp
    last_observed: str  # ISO timestamp
    measurement_count: int
    trend: str  # "improving", "worsening", "stable"
    risk_level_current: str
    risk_level_previous: Optional[str]
    risk_progression: RiskProgression


@dataclass
class TemporalInsight:
    """A temporal insight with full context"""
    insight_type: str  # "risk_increase", "trend_detected", "new_finding", etc.
    priority: int  # 0-1000
    title: str
    description: str
    evidence: List[str]  # Supporting evidence from temporal analysis
    temporal_context: str  # Human-readable temporal explanation
    recommendation: Optional[str]
    confidence: float  # 0.0 - 1.0
    timestamp: str


class TemporalReasoningEngine:
    """
    Temporal Reasoning Engine - Enables agent to reason over time
    
    Core Capabilities:
    1. Detect metric changes and trends
    2. Assess risk progression (improving vs worsening)
    3. Generate temporal insights ("what changed and why")
    4. Provide temporal recommendations
    5. Calculate temporal confidence scores
    """
    
    def __init__(self):
        # Clinical thresholds for various metrics
        self.metric_thresholds = self._load_clinical_thresholds()
        
        # Significance thresholds for change detection
        self.significance_thresholds = {
            'glucose_fasting': 10,  # mg/dL
            'glucose_random': 20,
            'hba1c': 0.5,  # percentage points
            'blood_pressure_systolic': 10,  # mmHg
            'blood_pressure_diastolic': 5,
            'cholesterol_total': 20,  # mg/dL
            'ldl': 15,
            'hdl': 5,
            'triglycerides': 30
        }
    
    def _load_clinical_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Load clinical reference ranges and risk thresholds"""
        return {
            'glucose_fasting': {
                'normal': (70, 99),
                'prediabetic': (100, 125),
                'diabetic': (126, 999),
                'unit': 'mg/dL'
            },
            'glucose_random': {
                'normal': (70, 140),
                'concerning': (141, 199),
                'diabetic': (200, 999),
                'unit': 'mg/dL'
            },
            'hba1c': {
                'normal': (0, 5.6),
                'prediabetic': (5.7, 6.4),
                'diabetic': (6.5, 99),
                'unit': '%'
            },
            'blood_pressure_systolic': {
                'normal': (90, 120),
                'elevated': (121, 129),
                'stage1_hypertension': (130, 139),
                'stage2_hypertension': (140, 179),
                'crisis': (180, 999),
                'unit': 'mmHg'
            },
            'blood_pressure_diastolic': {
                'normal': (60, 80),
                'elevated': (80, 84),
                'stage1_hypertension': (85, 89),
                'stage2_hypertension': (90, 119),
                'crisis': (120, 999),
                'unit': 'mmHg'
            },
            'cholesterol_total': {
                'desirable': (0, 199),
                'borderline': (200, 239),
                'high': (240, 999),
                'unit': 'mg/dL'
            },
            'ldl': {
                'optimal': (0, 99),
                'near_optimal': (100, 129),
                'borderline': (130, 159),
                'high': (160, 189),
                'very_high': (190, 999),
                'unit': 'mg/dL'
            }
        }
    
    def analyze_temporal_context(self,
                                 current_document: Dict[str, Any],
                                 historical_documents: List[Dict[str, Any]],
                                 temporal_trends: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core temporal reasoning function
        
        Takes current + historical data and produces temporal insights.
        
        Returns:
            - temporal_metrics: Enriched metrics with temporal context
            - detected_changes: Significant changes detected
            - risk_progressions: How risks evolved
            - temporal_insights: Actionable insights with temporal reasoning
            - temporal_summary: Human-readable summary
        """
        
        # Extract current metrics
        current_metrics = current_document.get('metrics', {})
        current_timestamp = current_document.get('timestamp', datetime.now().isoformat())
        
        # Build temporal metrics
        temporal_metrics = []
        for metric_name, current_value in current_metrics.items():
            temporal_metric = self._build_temporal_metric(
                metric_name=metric_name,
                current_value=current_value,
                current_timestamp=current_timestamp,
                historical_documents=historical_documents,
                temporal_trends=temporal_trends
            )
            if temporal_metric:
                temporal_metrics.append(temporal_metric)
        
        # Detect significant changes
        detected_changes = self._detect_significant_changes(temporal_metrics)
        
        # Assess risk progressions
        risk_progressions = self._assess_risk_progressions(temporal_metrics)
        
        # Generate temporal insights
        temporal_insights = self._generate_temporal_insights(
            temporal_metrics=temporal_metrics,
            detected_changes=detected_changes,
            risk_progressions=risk_progressions,
            current_document=current_document,
            historical_documents=historical_documents
        )
        
        # Create temporal summary
        temporal_summary = self._create_temporal_summary(
            temporal_metrics=temporal_metrics,
            detected_changes=detected_changes,
            risk_progressions=risk_progressions,
            temporal_insights=temporal_insights
        )
        
        return {
            'temporal_metrics': [self._metric_to_dict(m) for m in temporal_metrics],
            'detected_changes': detected_changes,
            'risk_progressions': risk_progressions,
            'temporal_insights': [self._insight_to_dict(i) for i in temporal_insights],
            'temporal_summary': temporal_summary,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _build_temporal_metric(self,
                               metric_name: str,
                               current_value: Any,
                               current_timestamp: str,
                               historical_documents: List[Dict[str, Any]],
                               temporal_trends: Dict[str, Any]) -> Optional[TemporalMetric]:
        """Build a temporal metric with full context"""
        
        # Try to extract numeric value
        current_numeric = self._extract_numeric(current_value)
        if current_numeric is None:
            return None
        
        # Find historical values
        historical_values = []
        for doc in sorted(historical_documents, key=lambda x: x.get('timestamp', '')):
            metrics = doc.get('metrics', {})
            if metric_name in metrics:
                hist_value = self._extract_numeric(metrics[metric_name])
                if hist_value is not None:
                    historical_values.append({
                        'value': hist_value,
                        'timestamp': doc.get('timestamp')
                    })
        
        # Determine previous value
        previous_value = historical_values[-1]['value'] if historical_values else None
        previous_timestamp = historical_values[-1]['timestamp'] if historical_values else None
        
        # Calculate change
        change = None
        percent_change = None
        direction = ChangeDirection.NEW
        
        if previous_value is not None:
            change = current_numeric - previous_value
            if previous_value != 0:
                percent_change = (change / previous_value) * 100
            
            if abs(change) < 0.01:
                direction = ChangeDirection.STABLE
            elif change > 0:
                direction = ChangeDirection.INCREASED
            else:
                direction = ChangeDirection.DECREASED
        
        # Determine trend
        trend = self._determine_trend(historical_values + [{'value': current_numeric, 'timestamp': current_timestamp}])
        
        # Assess risk levels
        risk_level_current = self._assess_risk_level(metric_name, current_numeric)
        risk_level_previous = self._assess_risk_level(metric_name, previous_value) if previous_value else None
        
        # Determine risk progression
        risk_progression = self._determine_risk_progression(risk_level_current, risk_level_previous)
        
        # Get first observation
        first_observed = historical_values[0]['timestamp'] if historical_values else current_timestamp
        
        return TemporalMetric(
            metric_name=metric_name,
            current_value=current_numeric,
            previous_value=previous_value,
            change=change,
            percent_change=percent_change,
            direction=direction,
            first_observed=first_observed,
            last_observed=current_timestamp,
            measurement_count=len(historical_values) + 1,
            trend=trend,
            risk_level_current=risk_level_current,
            risk_level_previous=risk_level_previous,
            risk_progression=risk_progression
        )
    
    def _determine_trend(self, values: List[Dict]) -> str:
        """Determine overall trend from value history"""
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple linear trend
        numeric_values = [v['value'] for v in values]
        
        # Count increases vs decreases
        increases = 0
        decreases = 0
        
        for i in range(1, len(numeric_values)):
            if numeric_values[i] > numeric_values[i-1]:
                increases += 1
            elif numeric_values[i] < numeric_values[i-1]:
                decreases += 1
        
        if increases > decreases * 1.5:
            return "worsening" if self._is_higher_worse(values[0].get('value')) else "improving"
        elif decreases > increases * 1.5:
            return "improving" if self._is_higher_worse(values[0].get('value')) else "worsening"
        else:
            return "stable"
    
    def _is_higher_worse(self, value: float) -> bool:
        """Determine if higher values are worse for this metric"""
        # For most metrics, higher is worse (glucose, BP, cholesterol)
        # Exceptions: HDL (higher is better)
        return True
    
    def _assess_risk_level(self, metric_name: str, value: Optional[float]) -> str:
        """Assess risk level for a metric value"""
        if value is None:
            return "unknown"
        
        # Normalize metric name
        metric_key = metric_name.lower().replace(' ', '_')
        
        if metric_key not in self.metric_thresholds:
            return "unknown"
        
        thresholds = self.metric_thresholds[metric_key]
        
        # Check each threshold range
        for risk_level, (min_val, max_val) in thresholds.items():
            if risk_level == 'unit':
                continue
            if min_val <= value <= max_val:
                return risk_level
        
        return "unknown"
    
    def _determine_risk_progression(self, 
                                   current_risk: str,
                                   previous_risk: Optional[str]) -> RiskProgression:
        """Determine how risk level changed"""
        if previous_risk is None:
            return RiskProgression.NEW_RISK if current_risk != "normal" else RiskProgression.STABLE
        
        # Define risk severity order
        risk_severity = {
            'normal': 0,
            'desirable': 0,
            'optimal': 0,
            'elevated': 1,
            'borderline': 1,
            'prediabetic': 2,
            'concerning': 2,
            'high': 3,
            'stage1_hypertension': 3,
            'diabetic': 4,
            'stage2_hypertension': 4,
            'very_high': 5,
            'crisis': 6
        }
        
        current_severity = risk_severity.get(current_risk, 0)
        previous_severity = risk_severity.get(previous_risk, 0)
        
        if current_severity > previous_severity:
            return RiskProgression.WORSENED
        elif current_severity < previous_severity:
            return RiskProgression.IMPROVED
        else:
            return RiskProgression.STABLE
    
    def _detect_significant_changes(self, temporal_metrics: List[TemporalMetric]) -> List[Dict[str, Any]]:
        """Detect significant changes that warrant attention"""
        significant_changes = []
        
        for metric in temporal_metrics:
            if metric.change is None:
                continue
            
            # Check if change is significant
            metric_key = metric.metric_name.lower().replace(' ', '_')
            threshold = self.significance_thresholds.get(metric_key, 5)  # Default threshold
            
            if abs(metric.change) >= threshold:
                significant_changes.append({
                    'metric_name': metric.metric_name,
                    'change': round(metric.change, 2),
                    'percent_change': round(metric.percent_change, 1) if metric.percent_change else None,
                    'direction': metric.direction.value,
                    'previous_value': round(metric.previous_value, 2) if metric.previous_value else None,
                    'current_value': round(metric.current_value, 2),
                    'significance': 'high' if abs(metric.change) >= threshold * 2 else 'moderate',
                    'risk_progression': metric.risk_progression.value
                })
        
        return significant_changes
    
    def _assess_risk_progressions(self, temporal_metrics: List[TemporalMetric]) -> Dict[str, Any]:
        """Assess overall risk progression"""
        progressions = {
            'improved_count': 0,
            'worsened_count': 0,
            'stable_count': 0,
            'new_risks_count': 0,
            'resolved_risks_count': 0,
            'details': []
        }
        
        for metric in temporal_metrics:
            if metric.risk_progression == RiskProgression.IMPROVED:
                progressions['improved_count'] += 1
            elif metric.risk_progression == RiskProgression.WORSENED:
                progressions['worsened_count'] += 1
            elif metric.risk_progression == RiskProgression.STABLE:
                progressions['stable_count'] += 1
            elif metric.risk_progression == RiskProgression.NEW_RISK:
                progressions['new_risks_count'] += 1
            elif metric.risk_progression == RiskProgression.RESOLVED_RISK:
                progressions['resolved_risks_count'] += 1
            
            if metric.risk_progression != RiskProgression.STABLE:
                progressions['details'].append({
                    'metric': metric.metric_name,
                    'progression': metric.risk_progression.value,
                    'current_risk': metric.risk_level_current,
                    'previous_risk': metric.risk_level_previous
                })
        
        # Overall assessment
        if progressions['worsened_count'] > progressions['improved_count']:
            progressions['overall_trend'] = 'worsening'
        elif progressions['improved_count'] > progressions['worsened_count']:
            progressions['overall_trend'] = 'improving'
        else:
            progressions['overall_trend'] = 'stable'
        
        return progressions
    
    def _generate_temporal_insights(self,
                                   temporal_metrics: List[TemporalMetric],
                                   detected_changes: List[Dict[str, Any]],
                                   risk_progressions: Dict[str, Any],
                                   current_document: Dict[str, Any],
                                   historical_documents: List[Dict[str, Any]]) -> List[TemporalInsight]:
        """Generate actionable temporal insights"""
        insights = []
        
        # Insight 1: Significant metric changes
        for change in detected_changes:
            if change['significance'] == 'high':
                insight = TemporalInsight(
                    insight_type='significant_change',
                    priority=800,
                    title=f"{change['metric_name']} {change['direction']}",
                    description=f"{change['metric_name']} {change['direction']} from {change['previous_value']} to {change['current_value']} ({change['change']:+.1f}, {change['percent_change']:+.1f}%)",
                    evidence=[
                        f"Previous measurement: {change['previous_value']}",
                        f"Current measurement: {change['current_value']}",
                        f"Change magnitude: {abs(change['change']):.1f}",
                        f"Risk progression: {change['risk_progression']}"
                    ],
                    temporal_context=f"This represents a significant change since the last measurement. The {change['direction']} trend is {change['risk_progression']}.",
                    recommendation=f"Monitor {change['metric_name']} closely. Consider consulting with healthcare provider about this change.",
                    confidence=0.85,
                    timestamp=datetime.now().isoformat()
                )
                insights.append(insight)
        
        # Insight 2: Risk progressions
        if risk_progressions['worsened_count'] > 0:
            worsened_metrics = [d['metric'] for d in risk_progressions['details'] if d['progression'] == 'worsened']
            insight = TemporalInsight(
                insight_type='risk_increase',
                priority=900,
                title=f"Risk Increased: {', '.join(worsened_metrics)}",
                description=f"{risk_progressions['worsened_count']} metric(s) showed worsening risk levels compared to previous measurements.",
                evidence=[f"{d['metric']}: {d['previous_risk']} → {d['current_risk']}" for d in risk_progressions['details'] if d['progression'] == 'worsened'],
                temporal_context="Risk levels have deteriorated since the last assessment. This requires attention.",
                recommendation="Schedule a follow-up appointment to discuss these changes and review treatment plan.",
                confidence=0.9,
                timestamp=datetime.now().isoformat()
            )
            insights.append(insight)
        
        # Insight 3: Improvements
        if risk_progressions['improved_count'] > 0:
            improved_metrics = [d['metric'] for d in risk_progressions['details'] if d['progression'] == 'improved']
            insight = TemporalInsight(
                insight_type='improvement',
                priority=600,
                title=f"Improvement Detected: {', '.join(improved_metrics)}",
                description=f"{risk_progressions['improved_count']} metric(s) showed improvement compared to previous measurements.",
                evidence=[f"{d['metric']}: {d['previous_risk']} → {d['current_risk']}" for d in risk_progressions['details'] if d['progression'] == 'improved'],
                temporal_context="Positive progress observed. Current interventions appear effective.",
                recommendation="Continue current treatment plan. Maintain lifestyle modifications.",
                confidence=0.85,
                timestamp=datetime.now().isoformat()
            )
            insights.append(insight)
        
        # Insight 4: Trends
        for metric in temporal_metrics:
            if metric.trend in ['worsening', 'improving'] and metric.measurement_count >= 3:
                insight = TemporalInsight(
                    insight_type='trend_detected',
                    priority=700,
                    title=f"Trend: {metric.metric_name} is {metric.trend}",
                    description=f"{metric.metric_name} shows a {metric.trend} trend over {metric.measurement_count} measurements.",
                    evidence=[
                        f"Measurements: {metric.measurement_count}",
                        f"Current value: {metric.current_value:.1f}",
                        f"Overall direction: {metric.trend}",
                        f"Current risk level: {metric.risk_level_current}"
                    ],
                    temporal_context=f"This trend has been consistent across multiple measurements from {metric.first_observed} to {metric.last_observed}.",
                    recommendation=f"Monitor this trend. {'Consider intervention if trend continues.' if metric.trend == 'worsening' else 'Current approach is effective.'}",
                    confidence=0.8,
                    timestamp=datetime.now().isoformat()
                )
                insights.append(insight)
        
        # Sort by priority
        insights.sort(key=lambda x: x.priority, reverse=True)
        
        return insights
    
    def _create_temporal_summary(self,
                                temporal_metrics: List[TemporalMetric],
                                detected_changes: List[Dict[str, Any]],
                                risk_progressions: Dict[str, Any],
                                temporal_insights: List[TemporalInsight]) -> str:
        """Create human-readable temporal summary"""
        
        summary_parts = []
        
        # Overall trend
        overall_trend = risk_progressions.get('overall_trend', 'stable')
        if overall_trend == 'worsening':
            summary_parts.append("⚠️ **Overall Health Trend: Concerning**")
            summary_parts.append(f"Your health metrics show signs of deterioration. {risk_progressions['worsened_count']} metric(s) have worsened since your last assessment.")
        elif overall_trend == 'improving':
            summary_parts.append("✅ **Overall Health Trend: Improving**")
            summary_parts.append(f"Positive progress detected! {risk_progressions['improved_count']} metric(s) have improved since your last assessment.")
        else:
            summary_parts.append("📊 **Overall Health Trend: Stable**")
            summary_parts.append("Your health metrics remain relatively stable compared to previous measurements.")
        
        # Significant changes
        if detected_changes:
            summary_parts.append(f"\n**Significant Changes Detected: {len(detected_changes)}**")
            for change in detected_changes[:3]:  # Top 3
                summary_parts.append(f"- {change['metric_name']}: {change['direction']} by {abs(change['change']):.1f} ({change['percent_change']:+.1f}%)")
        
        # Key insights
        if temporal_insights:
            summary_parts.append(f"\n**Key Temporal Insights:**")
            for insight in temporal_insights[:3]:  # Top 3
                summary_parts.append(f"- {insight.title}: {insight.description[:100]}...")
        
        # Time context
        if temporal_metrics:
            summary_parts.append(f"\n**Analysis Period:** {len(temporal_metrics)} metrics tracked over time")
        
        return "\n".join(summary_parts)
    
    def _extract_numeric(self, value: Any) -> Optional[float]:
        """Extract numeric value"""
        try:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                clean = value.replace('mg/dL', '').replace('mmHg', '').replace('%', '').strip()
                return float(clean)
        except:
            pass
        return None
    
    def _metric_to_dict(self, metric: TemporalMetric) -> Dict[str, Any]:
        """Convert TemporalMetric to dictionary"""
        return {
            'metric_name': metric.metric_name,
            'current_value': round(metric.current_value, 2),
            'previous_value': round(metric.previous_value, 2) if metric.previous_value else None,
            'change': round(metric.change, 2) if metric.change else None,
            'percent_change': round(metric.percent_change, 2) if metric.percent_change else None,
            'direction': metric.direction.value,
            'first_observed': metric.first_observed,
            'last_observed': metric.last_observed,
            'measurement_count': metric.measurement_count,
            'trend': metric.trend,
            'risk_level_current': metric.risk_level_current,
            'risk_level_previous': metric.risk_level_previous,
            'risk_progression': metric.risk_progression.value
        }
    
    def _insight_to_dict(self, insight: TemporalInsight) -> Dict[str, Any]:
        """Convert TemporalInsight to dictionary"""
        return {
            'insight_type': insight.insight_type,
            'priority': insight.priority,
            'title': insight.title,
            'description': insight.description,
            'evidence': insight.evidence,
            'temporal_context': insight.temporal_context,
            'recommendation': insight.recommendation,
            'confidence': insight.confidence,
            'timestamp': insight.timestamp
        }
