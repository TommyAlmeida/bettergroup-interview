from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_company_service
from app.features.companies.schemas import CompanyCreate, CompanyResponse, CompanyWithUsersResponse

from app.features.companies.service import CompanyService
from app.features.users.schemas import UserResponse
from uuid import UUID

router = APIRouter()


@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
    company_service: CompanyService = Depends(get_company_service),
):
    companies = await company_service.get_all_companies()

    return [
        CompanyResponse.model_validate(
            company,
            from_attributes=True
        ) for company in companies
    ]


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: UUID,
    company_service: CompanyService = Depends(get_company_service),
):
    company = await company_service.get_company_by_id(company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return CompanyResponse.model_validate(company, from_attributes=True)


@router.get("/companies/{company_id}/users",
            response_model=CompanyWithUsersResponse)
async def get_company_users(
    company_id: UUID,
    company_service: CompanyService = Depends(get_company_service),
):
    company = await company_service.get_company_by_id(company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    users = await company_service.get_company_users(company_id)

    if not users:
        raise HTTPException(status_code=404,
                            detail="No users found for this company")

    return CompanyWithUsersResponse(
        id=company.id,
        name=company.name,
        domain=company.domain,
        users=[UserResponse.model_validate(user) for user in users]
    )


@router.post("/companies", response_model=CompanyResponse, status_code=201)
async def create_company(
    company_data: CompanyCreate,
    company_service: CompanyService = Depends(get_company_service),
):
    try:
        company = await company_service.create_company(company_data.name, company_data.domain)

        return company
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
