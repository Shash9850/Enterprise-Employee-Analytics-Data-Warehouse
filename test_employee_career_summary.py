from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_employee_career_summary("E075722")

print(result)