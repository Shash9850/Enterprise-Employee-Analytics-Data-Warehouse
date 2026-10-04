from managers.analytics_manager import AnalyticsManager


manager = AnalyticsManager()

data = manager.get_top_employees_by_department()

for row in data:
    print(row)