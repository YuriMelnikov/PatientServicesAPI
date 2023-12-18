import asyncio
from motor.motor_asyncio import AsyncIOMotorClient



class SettingsDB():
    def __init__(self, url='mongodb://localhost:27017', db_name='hospital_db') -> None:

        self.CLIENT = AsyncIOMotorClient(url) 

        self.DB = self.CLIENT[db_name]

        self.COLLECTION_SERVICES = self.DB["services"]
     
        
if __name__ == "__main__":
    pass