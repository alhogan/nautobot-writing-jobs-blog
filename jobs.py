"""Blog Example Jobs."""

# Nautobot Job imports (Job class, input vars, etc)
from nautobot.apps.jobs import Job, ObjectVar, MultiObjectVar, register_jobs

# Nautobot Core imports (models, helper functions, etc)
from nautobot.dcim.models import Location, Device, Interface
from nautobot.extras.models import Role

# Python packages (json, pandas,4 netmiko, etc)

# Job Grouping Name
name = "Example Jobs"


# Nautobot Job Class Definition
class MyExampleJob(Job):
    # Input Variables
    location = ObjectVar(
        model=Location,
        query_params={
            "content_type": "dcim.device",
        },
    )
    roles = MultiObjectVar(
        model=Role,
        query_params={
            "content_types": "dcim.device",
        },
    )

    # Job Class Metadata
    class Meta:
        description = "My first nautobot job"
        # Add other job settings here

    # Required Job.run() method
    def run(self, location, roles):
        # Job logic
        devices = Device.objects.filter(location=location, role__in=roles)
        self.logger.info("%d Devices", devices.count())
        interfaces = Interface.objects.filter(device__in=devices)
        total_intf = interfaces.count()
        used_intf = interfaces.filter(
            status__name__in=["Active", "Failed", "Maintenance"]
        ).count()
        unused_intf = interfaces.filter(
            status__name__in=["Decommissioning", "Planned"]
        ).count()
        self.logger.info(
            f"The current interface capacity of {location.name} is: Total = {total_intf}, Used = {used_intf}({int(round(used_intf/total_intf, 2)*100)}%), Unused = {unused_intf}({int(round(unused_intf/total_intf, 2)*100)}%)"
        )


register_jobs(MyExampleJob)
