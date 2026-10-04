from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_employee_history("E075722")

for version in result:
    print(version)








    