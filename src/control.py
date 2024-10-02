from pysondb import db

class User():
    def __init__(self):
        self.db = db.getDb("./database/user.json")

    def add_user(self, name, email, pwd, role):
        if self.db.getByQuery({"nama" : name}) or self.db.getByQuery({"email" : email}):
            return 0
        else :
            self.db.add({"nama" : name, "email" : email, "password" : pwd, "role" : role})
            return 1

    def update_user(self, name, email, changedName=None, changedEmail=None, changedRole=None):
        data = self.db.getByQuery({"nama": name, "email": email})

        if not data:
            return 0  # Return 0 if the user doesn't exist

        update_data = {}

        # Collect all fields that need updating
        if changedName:
            update_data["nama"] = changedName

        if changedEmail:
            update_data["email"] = changedEmail

        if changedRole:
            update_data["role"] = changedRole

        # Perform the update only if there is something to change
        if update_data:
            try:
                self.db.updateByQuery({"nama": name, "email": email}, update_data)
                return 1  # Return 1 on success
            except Exception as e:
                print(f"Error updating user: {e}")  # Log the error for debugging
                return 0  # Return 0 on failure

        return 0  # Return 0 if no updates were needed


    def delete_user(self, name, email):
        if self.db.getByQuery({"nama" : name, "email" : email}) :
            self.db.deleteById(self.db.getByQuery({"nama" : name, "email" : email})[0]["id"])
            return 1
        return 0
    
    def get_all_user(self):
        if self.db.getAll():
            return self.db.getAll()
        return 0
    
class Usage():
    def __init__(self):
        self.db = db.getDb("./database/usage.json")

    def add_usage(self, name, email, date, role, status, info):
        if not User().db.getByQuery({"nama" : name, "email" : email}):
            return 2

        try:
            data = self.db.getByQuery({"nama" : name, "date" : date})[0]
        except:
            data = None

        if not data:
            self.db.add({"nama" : name, "email" : email, "date" : date, "role" : role, "status" : status, "info" :  info})
            return 1
        else:
            return 0
    
    def edit_usage(self, name, date, changedStatus=None, changedInfo=None):
        try:
            data = self.db.getByQuery({"nama" : name, "date" : date})[0]
        except:
            data = None

        if data:
            try:
                if data and changedStatus:
                    self.db.updateByQuery({"nama" : name, "date" : date}, {"status" : changedStatus})
                
                if data and changedInfo:
                    self.db.updateByQuery({"nama" : name, "date" : date}, {"info" : changedInfo})
                return 1
            except:
                return 0
        else:
            return 0

    def delete_usage(self, name, date):
        try:
            data = self.db.getByQuery({"nama" : name, "date" : date})[0]
        except:
            data = None

        if data :
            self.db.deleteById(data["id"])
            return 1
        return 0
    
    def get_all_usage(self):
        if self.db.getAll():
            return self.db.getAll()
        return 0
    
class Equipment():
    def __init__(self):
        self.db = db.getDb("./database/equipment.json")

    def refresh(self):
        try:
            data = self.get_all_equipment()
        except:
            data = None

        if data:
            qty = 0
            for i in data:
                i_data = self.db.getByQuery({"nama_equipment" : i["nama_equipment"], "status" : i["status"]})
                if len(i_data) > 1:
                    for x in i_data:
                        qty += x["qty"]
                    
                    print(qty)

                    while self.db.getByQuery({"nama_equipment" : i["nama_equipment"], "status" : i["status"]}):
                        self.delete_equipment(i["nama_equipment"], i["status"])
                        print(self.db.getByQuery({"nama_equipment" : i["nama_equipment"], "status" : i["status"]}))
                    
                    self.add_equipment(i["nama_equipment"], i["status"])
                    self.update_equipment(i["nama_equipment"], i["status"], changedQty=qty)
                    qty = 0
                    

    def add_equipment(self, name, status):
        if self.db.getByQuery({"nama_equipment" : name, "status" : status}):
            self.db.updateById(self.db.getByQuery({"nama_equipment" : name, "status" : status})[0]["id"], {"qty" : self.db.getByQuery({"nama_equipment" : name, "status" : status})[0]["qty"] + 1})
            return self.refresh()
        else :
            self.db.add({"nama_equipment" : name, "qty" : 1, "status" : status})
            self.refresh()
            return 1

    def update_equipment(self, name, status, changedStatus = None, changedQty = None):
        try:
            data = self.db.getByQuery({"nama_equipment" : name, "status" : status})[0]
        except:
            data = None

        if data:
            try:
                if data and changedQty:
                    self.db.updateByQuery({"nama_equipment" : name, "status" : status}, {"qty" : changedQty})
                if data and changedStatus:
                    self.db.updateByQuery({"nama_equipment" : name, "status" : status}, {"status" : changedStatus})
                self.refresh()
            except:
                self.refresh()
                return 0
        else:
            self.refresh()
            return 0

    def delete_equipment(self, name, status):
        try:
            data = self.db.getByQuery({"nama_equipment" : name, "status" : status})[0]
        except:
            data = None

        if data:
            self.db.deleteById(data["id"])
            self.refresh()
            return 1
        return 0
    
    def get_all_equipment(self):
        if self.db.getAll():
            self.refresh()
            return self.db.getAll()
        return 0

# print(Equipment().add_equipment("Compur", "Toll"))
# print(Equipment().get_all_equipment())
# print(Equipment().update_equipment("Compur", "new", changedStatus="Toll", changedQty=5))
# print(Equipment().delete_equipment("Computer", "Toll"))
# print(Usage().add_usage("Ijul", "a@gmail.com", "28/07/2005", "Admin", "Canceled", "For Video"))
# print(Usage().edit_usage("Ijul", "28/07/2005", "tes", "tes"))
# print(Usage().get_all_usage())
# print(Usage().delete_usage("Ijul", "28/07/2005"))
# print(User().add_user("Computer", "new"))
# print(User().get_all_user())
# print(User().update_user("Computer", changedName="Tolol"))
# print(User().delete_user("Tolol"))