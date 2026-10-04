from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_attrition_risk_indicators()

for risk_group in result:
    print(risk_group)