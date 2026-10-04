from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_project_attention_indicators()

for project in result[:15]:
    print(project)