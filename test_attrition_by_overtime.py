from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_attrition_by_overtime()

for overtime_group in result:
    print(overtime_group)