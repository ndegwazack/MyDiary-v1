class DiaryEntries(object):
    def __init__(self, Id = 1):
        self.Id = Id

    def get_all(self, Id):
        self.Id = Id
        return self.Id

    def put(self, Id):
        self.Id = Id
        return self.Id

    def get_one(self, Id):
        self.Id = Id
        return self.Id

    def post(self, newId):
        self.Id += newId
        return self.Id

    def delete(self, Id):
        self.Id -= Id
        return self.Id
