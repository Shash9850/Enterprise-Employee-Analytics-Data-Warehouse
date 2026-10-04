from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_employee_allocation()

for employee in result[:10]:
    print(employee)