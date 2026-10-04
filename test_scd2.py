from managers.scd2_manager import SCD2Manager

manager = SCD2Manager()

result = manager.update_employee_department(
    "SCD20001",
    2
)

print("SCD2 update result:", result)