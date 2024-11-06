from bson import Int64, ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

import settings


class MongoDB:

    def set_collection(self, collection: str):
        self.__collection = collection

    __client = AsyncIOMotorClient(settings.DB)
    __collection = settings.COLLECTION
    __database = settings.DATABASE

    async def get_prof_by_type(self, filter_user, limit: int | None = 0, skip: int | None = 0):
        collection = self.__client.get_database(self.__database).get_collection(self.__collection)

        pipeline = [
            {'$match': {'type': filter_user}},
            {'$group': {'_id': 'docs', 'prof': {"$addToSet": {"code": "$code", "prof": "$prof"}}}},
            {'$set': {'prof': {'$setIntersection': ['$prof']}}},
            {'$set': {'prof': {'$sortArray': {'input': '$prof', 'sortBy': 1}}}},
            {'$project': {'_id': 0, 'prof': {'$slice': ['$prof', skip, limit]}}}
        ]
        res = await collection.aggregate(pipeline).next()
        return res.get("prof")

    async def get_college_by_code(self, code):
        return await (self.__client.get_database(self.__database).get_collection(self.__collection).find({"code": code})
                      .to_list(1000))

    async def get_prof_count_by_type(self, type_filter: str):
        pipeline = [{'$match': {'type': type_filter}},
                    {'$group': {'_id': 'count', 'prof': {'$addToSet': '$prof'}}},
                    {'$project': {'_id': 0, 'count': {"$size": "$prof"}}}]
        count = self.__client.get_database(self.__database).get_collection(self.__collection).aggregate(pipeline).next()
        return await count

    async def get_college_by_type(self, filter_user, limit: int | None = 0, skip: int | None = 0):
        collection = self.__client.get_database(self.__database).get_collection(self.__collection)

        pipeline = [
            {'$match': {'type': filter_user}},
            {'$group': {'_id': 'docs',
                        'college': {'$addToSet': {'hash_college': '$hash_college', 'college': '$college'}}}},
            {'$set': {'college': {'$setIntersection': ['$college']}}},
            {'$set': {'college': {'$sortArray': {'input': '$college', 'sortBy': 1}}}},
            {'$project': {'_id': 0, 'college': {'$slice': ['$college', skip, limit]}}}
        ]
        res = await collection.aggregate(pipeline).next()
        return res.get("college")

    async def get_college_by_prof(self, hash_college: str):
        return await self.__client.get_database(self.__database).get_collection(self.__collection).find(
            {"hash_college": hash_college}).to_list(1000)

    async def get_college_count_by_type(self, type_filter: str):
        pipeline = [{'$match': {'type': type_filter}},
                    {'$group': {'_id': 'count', 'college': {'$addToSet': '$college'}}},
                    {'$project': {'_id': 0, 'count': {"$size": "$college"}}}]
        count = self.__client.get_database(self.__database).get_collection(self.__collection).aggregate(pipeline).next()
        return await count

    async def get_prof_by_college(self, type_filter, request_hash):
        pipeline = [
            {'$match': {'type': type_filter, 'hash_college': Int64(request_hash)}},
            {'$group': {'_id': {'college': '$college', 'link': '$link', 'socnet': '$socnet'},
                        'profs': {'$addToSet': {'code': '$code', 'prof': '$prof'}}}},
            {'$set': {'profs': {'$setIntersection': ['$profs']}}},
            {'$set': {'profs': {'$sortArray': {'input': '$profs', 'sortBy': 1}}}},
            {'$project': {'profs': {'$slice': ['$profs', 0, 20]}}}
        ]
        prof_list = (self.__client.get_database(self.__database).get_collection(self.__collection).aggregate(pipeline)
                     .next())
        return await prof_list

    async def get_faq_question_list(self, limit, skip):
        co = await (self.__client.get_database(self.__database).get_collection(self.__collection)
                    .aggregate([{"$skip": skip}, {"$limit": limit}, {"$project": {"answer": 0}}])
                    .to_list(1000))
        return co


    async def get_faq_count(self):
        return await (self.__client.get_database(self.__database).get_collection(self.__collection)
                      .estimated_document_count())

    async def get_faq_question(self, _id: str):
        return await (self.__client.get_database(self.__database).get_collection(self.__collection)
                      .find_one({"_id": ObjectId(_id)}))

    async def get_type_desc(self, type: str):
        return await (self.__client.get_database(self.__database).getcollection(self.__collection)
                      .find_one({"type": type}))

    async def get_prof_desc(self, code: str):
        return await (self.__client.get_database(self.__database).getcollection(self.__collection)
                      .find_one({"code": code}))