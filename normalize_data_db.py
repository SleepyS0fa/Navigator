import asyncio
import re

from motor.motor_asyncio import AsyncIOMotorClient

import settings

DATABASE = "navigator"
COLLECTION = "prof_list"
db = __client = AsyncIOMotorClient(settings.DB)


async def start():
    await change_data()


async def change_data():
    # await change_prof_name_and_code()
    # await hash_college_name()
    await change_name_college()


async def change_name_college():
    all_data = await db.get_database(DATABASE).get_collection(COLLECTION).find().to_list(1000)
    pref = ["ГБПОУ ВО ", "БПОУ ВО ", "АНО ПО ", "АНО ", "АН ПОО ", "ГАПОУ ВО ", "АНОО ВО", ]
    for item in all_data:
        for i_pref in pref:
            if i_pref in item["college"]:
                item["college"] = item["college"].replace(i_pref, "")
                await db.get_database(DATABASE).get_collection(COLLECTION).replace_one({"_id": item["_id"]}, item)
                print("replace")


async def change_prof_name_and_code(self):
    all_data = await db.get_database(DATABASE).get_collection(COLLECTION).find().to_list(1000)
    regex = r"(?:(?:\d{2}\.?){2}\d{2})|\d{5}"

    for item in all_data:
        prof = item.get("prof")
        code = re.match(pattern=regex, string=prof)
        if not code:
            await (db.get_database(DATABASE).get_collection(COLLECTION)
                   .delete_one({"_id": item.get("_id")}))
            return
        code = code.group(0)
        prof = prof.replace(f"{code} ", "")
        print(prof + " | " + code)
        new_doc = {"_id": item.get("_id"), "type": item.get("type"), "prof": prof, "code": code,
                   "college": item.get("college")}
        if item.get("link"):
            new_doc["link"] = item.get("link")
        if item.get("socnet"):
            new_doc["socnet"] = item.get("socnet")

        await db.get_database(DATABASE).get_collection(COLLECTION).replace_one(
            {"_id": item.get("_id")}, new_doc)


async def hash_college_name(self):
    all_data = await db.get_database(DATABASE).get_collection(COLLECTION).find().to_list(
        1000)
    for item in all_data:
        item["hash_college"] = hash(item["college"])
        await db.get_database(DATABASE).get_collection(COLLECTION).replace_one(
            {"_id": item["_id"]}, item)


asyncio.run(start())
