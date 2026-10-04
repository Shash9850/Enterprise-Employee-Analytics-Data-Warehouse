from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_project_workload()

for project in result[:10]:
    print(project)