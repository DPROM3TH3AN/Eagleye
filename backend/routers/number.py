# backend/routers/numbers.py
from fastapi import APIRouter, HTTPException
from backend.models.schemas import NumberAnalysisRequest, NumberAnalysisResponse
import phonenumbers
from opencage.geocoder import OpenCageGeocode
import os

# Replace with your actual OpenCage API key
OPENCAGEAPI_KEY = os.getenv('OPENCAGEAPI_KEY')

router = APIRouter()

@router.post("/", response_model=NumberAnalysisResponse)
async def analyze_number(data: NumberAnalysisRequest):
    try:
        parsed_number = phonenumbers.parse(data.number, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        analysis_result = {
            "valid": is_valid,
            "formatted": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        }
        if is_valid:
            geocoder = OpenCageGeocode(OPENCAGEAPI_KEY)
            query = analysis_result["formatted"]
            results = geocoder.geocode(query)
            if results and len(results):
                analysis_result["location"] = results[0].get("formatted", "Not found")
            else:
                analysis_result["location"] = "Location not found"
        else:
            analysis_result["location"] = "Invalid number"
        
        return NumberAnalysisResponse(analysis=analysis_result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
