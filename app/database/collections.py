from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient


class Collections:
    @staticmethod
    def get_collection(
            connection: AsyncIOMotorClient,
            db_name: str,
            collection_name: str,
    ) -> AsyncIOMotorCollection:
        return connection[db_name][collection_name]
