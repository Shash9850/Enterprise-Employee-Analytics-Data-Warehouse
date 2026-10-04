from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_attrition_by_tenure()

for tenure_group in result:
    print(tenure_group)