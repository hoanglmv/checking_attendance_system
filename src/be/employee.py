from person import Personal

class Employee(Personal):
    def __init__(self, per_id, name, gmail, phone_number, profile_image=None):
        super().__init__(per_id, name, "Employee", gmail, phone_number, profile_image=profile_image)
