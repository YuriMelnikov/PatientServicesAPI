from fastapi import FastAPI, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from app.models.service_model import Service 
from db.settingsDB import SettingsDB
from bson import ObjectId

router = APIRouter(prefix='/services', tags=['services'])

settingsDB = SettingsDB()

services_collection = settingsDB.COLLECTION_SERVICES


# Эндпоинт для создания новой услуги
@router.post("/")
async def create_service(service: Service):
    try:
        collection = services_collection
        service_data = {
            "name": service.name,
            "price": service.price,
            "doctor": service.doctor,
            "room_number": service.room_number,
            "description": service.description
        }
        result = await collection.insert_one(service_data)
        inserted_id = str(result.inserted_id)
        return JSONResponse(content={"inserted_id": inserted_id}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Эндпоинт для получения списка всех услуг
@router.get("/")
async def read_services():
    try:
        services = await services_collection.find().to_list(length=None)
        return [
            {
                "_id": str(service["_id"]),
                "name": service.get("name", ""),
                "price": str(service.get("price", "")),
                "doctor": service.get("doctor", ""),
                "room_number": service.get("room_number", ""),
                "description": service.get("description", "")
            }
            for service in services
        ]
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,)

# Эндпоинт для получения информации об одной услуге
@router.get("/{service_id}")
async def read_service(service_id: str):
  try:
    service = await services_collection.find_one({"_id": ObjectId(service_id)})
    if service:
        service["_id"] = str(service["_id"])
        return JSONResponse(content=service, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "Service not found"}, status_code=status.HTTP_404_NOT_FOUND)
  except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Эндпоинт для обновления всех данных
@router.put("/{service_id}")
async def update_all_service(service_id: str, updated_service: Service):
    try:
        service = await services_collection.find_one({"_id": ObjectId(service_id)})
        if service:
            updated_data = {
                "name": updated_service.name,
                "price": updated_service.price,
                "doctor": updated_service.doctor,
                "room_number": updated_service.room_number,
                "description": updated_service.description
            }
            await services_collection.update_one({"_id": ObjectId(service_id)}, {"$set": updated_data})
            return JSONResponse(content={"message": "Service updated successfully"},status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Service not found"},status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Эндпоинт для удаления услуги
@router.delete("/{service_id}")
async def delete_service(service_id: str):
    try:
        result = await services_collection.delete_one({"_id": ObjectId(service_id)})
        if result.deleted_count:
            return JSONResponse(content={"message": "Service deleted successfully"},status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Service not found"},status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
