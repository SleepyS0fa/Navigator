import asyncio
import re

from motor.motor_asyncio import AsyncIOMotorClient

import settings

DATABASE = "navigator"
COLLECTION = "prof_list"
db = __client = AsyncIOMotorClient(settings.DB)


async def start():
    await set_desc()


async def change_data():
    await change_name_college()


async def set_desc():
    tempdata = await db.get_database(DATABASE).get_collection("temp").find().to_list(1000)
    for item in tempdata:
        code = re.match("(\d{2}\.\d{2}\.\d{2}|\d{5}) ", item.get("prof"))
        print(item["prof"])
        if code is None:
            continue
        item["prof"] = item["prof"].replace(code.group(0), "")
        await db.get_database(DATABASE).get_collection("temp").replace_one({"_id": item.get("_id")}, item)


    all_data = await db.get_database(DATABASE).get_collection(COLLECTION).find().to_list(1000)
    for item in all_data:
        prof_name = item["prof"]
        obj_desc = await db.get_database(DATABASE).get_collection("temp").find_one({"prof": prof_name})
        if obj_desc is None:
            print("notFound")
            continue

        print(obj_desc.keys())
        item["type_desc"] = obj_desc["type_desc"]
        item["desc"] = obj_desc["desc"]
        print("replace: " + item["type"])
        await db.get_database(DATABASE).get_collection(COLLECTION).replace_one({"_id": item["_id"]}, item)


async def change_name_college():
    all_data = await db.get_database(DATABASE).get_collection(COLLECTION).find().to_list(1000)
    pref = ["ГБПОУ ВО ", "БПОУ ВО ", "АНО ПО ", "АНО ", "АН ПОО ", "ГАПОУ ВО ", "АНОО ВО", ]
    for item in all_data:
        for i_pref in pref:
            if i_pref in item["college"]:
                item["college"] = item["college"].replace(i_pref, "")
                await db.get_database(DATABASE).get_collection(COLLECTION).replace_one({"_id": item["_id"]}, item)
                print("replace")


async def change_prof_name_and_code():
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
