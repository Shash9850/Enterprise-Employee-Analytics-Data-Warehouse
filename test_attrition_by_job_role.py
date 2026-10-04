from managers.analytics_manager import AnalyticsManager


analytics_manager = AnalyticsManager()

result = analytics_manager.get_attrition_by_job_role()

for job_role in result:
    print(job_role)