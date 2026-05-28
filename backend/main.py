import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import random

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = os.environ.get("COMPANY_SLUG", "greenloop")
COMPANY_PORT = int(os.environ.get("COMPANY_PORT", 8000))
db_engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    db_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=db_engine)

# Database Models
class SupplierDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_suppliers"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    certification_level = Column(String)
    location = Column(String)
    rating = Column(Float, default=4.0)
    verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProductDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_products"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    supplier_id = Column(String)
    category = Column(String)
    price = Column(Float)
    unit = Column(String)
    carbon_saved = Column(Float)
    stock = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class OffsetDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_offsets"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    price_per_ton = Column(Float)
    available_tons = Column(Integer)
    verification_standard = Column(String)
    project_location = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_orders"
    id = Column(String, primary_key=True)
    buyer_id = Column(String)
    items = Column(Text)
    total = Column(Float)
    status = Column(String)
    carbon_offset_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_users"
    id = Column(String, primary_key=True)
    company_name = Column(String)
    email = Column(String, unique=True)
    industry = Column(String)
    role = Column(String)
    sustainability_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class CertificationDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_certifications"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    issuing_body = Column(String)
    level = Column(String)
    description = Column(Text)
    required_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Mock Data
MOCK_SUPPLIERS = [
    {"id": "SUP-001", "name": "EcoMaterials Inc.", "description": "Sustainable building materials manufacturer", "category": "Construction", "certification_level": "Platinum", "location": "Berlin, Germany", "rating": 4.8, "verified": True, "created_at": "2024-01-15T08:00:00Z"},
    {"id": "SUP-002", "name": "GreenPack Solutions", "description": "Compostable packaging for B2B supply chains", "category": "Packaging", "certification_level": "Gold", "location": "Amsterdam, Netherlands", "rating": 4.6, "verified": True, "created_at": "2024-02-20T10:30:00Z"},
    {"id": "SUP-003", "name": "SunRay Renewables", "description": "Solar panel and renewable energy equipment supplier", "category": "Energy", "certification_level": "Gold", "location": "Barcelona, Spain", "rating": 4.9, "verified": True, "created_at": "2024-01-10T12:00:00Z"},
    {"id": "SUP-004", "name": "PureCycle Organics", "description": "Organic waste management and composting systems", "category": "Waste Management", "certification_level": "Silver", "location": "Copenhagen, Denmark", "rating": 4.3, "verified": True, "created_at": "2024-03-05T09:45:00Z"},
    {"id": "SUP-005", "name": "AquaPure Technologies", "description": "Water purification and conservation solutions", "category": "Water", "certification_level": "Platinum", "location": "Stockholm, Sweden", "rating": 4.7, "verified": True, "created_at": "2024-02-01T14:20:00Z"},
    {"id": "SUP-006", "name": "AgriCycle Bio", "description": "Organic fertilizers and sustainable agriculture inputs", "category": "Agriculture", "certification_level": "Gold", "location": "Lyon, France", "rating": 4.4, "verified": True, "created_at": "2024-01-28T16:10:00Z"},
    {"id": "SUP-007", "name": "EcoTransport Logistics", "description": "Carbon-neutral logistics and freight services", "category": "Transportation", "certification_level": "Platinum", "location": "Hamburg, Germany", "rating": 4.5, "verified": True, "created_at": "2024-03-12T11:30:00Z"},
    {"id": "SUP-008", "name": "GreenTextile Factory", "description": "Organic cotton and recycled fabric manufacturer", "category": "Textiles", "certification_level": "Gold", "location": "Milan, Italy", "rating": 4.2, "verified": True, "created_at": "2024-02-15T13:00:00Z"}
]

MOCK_PRODUCTS = [
    {"id": "PROD-001", "name": "Recycled Steel Beams", "supplier_id": "SUP-001", "category": "Construction", "price": 450.00, "unit": "ton", "carbon_saved": 1.8, "stock": 500, "description": "High-grade recycled steel for commercial construction", "created_at": "2024-01-20T08:00:00Z"},
    {"id": "PROD-002", "name": "Compostable Mailers (1000 pack)", "supplier_id": "SUP-002", "category": "Packaging", "price": 89.00, "unit": "pack", "carbon_saved": 0.3, "stock": 2000, "description": "Plant-based compostable shipping envelopes", "created_at": "2024-02-25T10:30:00Z"},
    {"id": "PROD-003", "name": "Commercial Solar Panel 400W", "supplier_id": "SUP-003", "category": "Energy", "price": 299.00, "unit": "unit", "carbon_saved": 0.5, "stock": 150, "description": "High-efficiency monocrystalline solar panel", "created_at": "2024-01-15T12:00:00Z"},
    {"id": "PROD-004", "name": "Industrial Composter 500L", "supplier_id": "SUP-004", "category": "Waste Management", "price": 2500.00, "unit": "unit", "carbon_saved": 2.1, "stock": 25, "description": "Large-scale composting system for food waste", "created_at": "2024-03-10T09:45:00Z"},
    {"id": "PROD-005", "name": "UV Water Purification System", "supplier_id": "SUP-005", "category": "Water", "price": 1800.00, "unit": "system", "carbon_saved": 0.8, "stock": 40, "description": "Chemical-free water treatment for industrial use", "created_at": "2024-02-05T14:20:00Z"},
    {"id": "PROD-006", "name": "Organic Fertilizer (50kg bag)", "supplier_id": "SUP-006", "category": "Agriculture", "price": 75.00, "unit": "bag", "carbon_saved": 0.2, "stock": 1000, "description": "Certified organic bio-fertilizer from agricultural waste", "created_at": "2024-02-01T16:10:00Z"},
    {"id": "PROD-007", "name": "Carbon-Neutral Freight Service", "supplier_id": "SUP-007", "category": "Transportation", "price": 1200.00, "unit": "shipment", "carbon_saved": 3.5, "stock": 9999, "description": "Full truckload with carbon offset included", "created_at": "2024-03-15T11:30:00Z"},
    {"id": "PROD-008", "name": "Organic Cotton Fabric Roll", "supplier_id": "SUP-008", "category": "Textiles", "price": 45.00, "unit": "meter", "carbon_saved": 0.4, "stock": 5000, "description": "GOTS-certified organic cotton, 100m rolls", "created_at": "2024-02-20T13:00:00Z"}
]

MOCK_OFFSETS = [
    {"id": "OFF-001", "name": "Amazon Rainforest Conservation", "type": "Forest Protection", "price_per_ton": 25.00, "available_tons": 50000, "verification_standard": "VCS", "project_location": "Brazil", "description": "Protecting 10,000 hectares of primary rainforest", "created_at": "2024-01-01T00:00:00Z"},
    {"id": "OFF-002", "name": "Mangrove Reforestation Project", "type": "Reforestation", "price_per_ton": 35.00, "available_tons": 25000, "verification_standard": "Gold Standard", "project_location": "Indonesia", "description": "Restoring coastal mangroves for carbon sequestration", "created_at": "2024-01-15T00:00:00Z"},
    {"id": "OFF-003", "name": "Wind Farm India", "type": "Renewable Energy", "price_per_ton": 15.00, "available_tons": 100000, "verification_standard": "CDM", "project_location": "India", "description": "Wind power replacing coal-fired electricity", "created_at": "2024-02-01T00:00:00Z"},
    {"id": "OFF-004", "name": "Improved Cookstoves Ethiopia", "type": "Energy Efficiency", "price_per_ton": 20.00, "available_tons": 30000, "verification_standard": "VCS", "project_location": "Ethiopia", "description": "Distributing efficient cookstoves to reduce wood consumption", "created_at": "2024-02-15T00:00:00Z"},
    {"id": "OFF-005", "name": "Solar Water Pumping Kenya", "type": "Renewable Energy", "price_per_ton": 18.00, "available_tons": 20000, "verification_standard": "Gold Standard", "project_location": "Kenya", "description": "Solar-powered irrigation replacing diesel pumps", "created_at": "2024-03-01T00:00:00Z"},
    {"id": "OFF-006", "name": "Biochar Production Uganda", "type": "Agricultural Carbon", "price_per_ton": 40.00, "available_tons": 15000, "verification_standard": "Plan Vivo", "project_location": "Uganda", "description": "Converting agricultural waste into carbon-stable biochar", "created_at": "2024-03-10T00:00:00Z"}
]

MOCK_ORDERS = [
    {"id": "ORD-001", "buyer_id": "USR-001", "items": "PROD-001 x 10, PROD-003 x 5", "total": 5995.00, "status": "completed", "carbon_offset_amount": 20.5, "created_at": "2024-03-20T10:00:00Z"},
    {"id": "ORD-002", "buyer_id": "USR-002", "items": "PROD-002 x 50", "total": 4450.00, "status": "processing", "carbon_offset_amount": 15.0, "created_at": "2024-03-25T14:30:00Z"},
    {"id": "ORD-003", "buyer_id": "USR-003", "items": "OFF-001 x 100, OFF-003 x 50", "total": 3250.00, "status": "pending", "carbon_offset_amount": 150.0, "created_at": "2024-03-28T09:15:00Z"},
    {"id": "ORD-004", "buyer_id": "USR-004", "items": "PROD-004 x 2", "total": 5000.00, "status": "completed", "carbon_offset_amount": 4.2, "created_at": "2024-03-22T11:45:00Z"},
    {"id": "ORD-005", "buyer_id": "USR-005", "items": "PROD-007 x 3", "total": 3600.00, "status": "shipped", "carbon_offset_amount": 10.5, "created_at": "2024-03-27T16:20:00Z"},
    {"id": "ORD-006", "buyer_id": "USR-001", "items": "PROD-005 x 1, PROD-006 x 20", "total": 3300.00, "status": "completed", "carbon_offset_amount": 8.8, "created_at": "2024-03-18T08:30:00Z"},
    {"id": "ORD-007", "buyer_id": "USR-006", "items": "OFF-004 x 200", "total": 4000.00, "status": "pending", "carbon_offset_amount": 200.0, "created_at": "2024-03-29T13:00:00Z"},
    {"id": "ORD-008", "buyer_id": "USR-003", "items": "PROD-008 x 100", "total": 4500.00, "status": "processing", "carbon_offset_amount": 40.0, "created_at": "2024-03-26T10:15:00Z"}
]

MOCK_USERS = [
    {"id": "USR-001", "company_name": "BuildGreen Corp", "email": "contact@buildgreen.com", "industry": "Construction", "role": "buyer", "sustainability_score": 85.5, "created_at": "2024-01-10T08:00:00Z"},
    {"id": "USR-002", "company_name": "EcoChain Logistics", "email": "info@ecochain.com", "industry": "Logistics", "role": "buyer", "sustainability_score": 72.3, "created_at": "2024-01-15T10:30:00Z"},
    {"id": "USR-003", "company_name": "CarbonNeutral Inc", "email": "hello@carbonneutral.com", "industry": "Carbon Trading", "role": "buyer", "sustainability_score": 92.1, "created_at": "2024-02-01T12:00:00Z"},
    {"id": "USR-004", "company_name": "WasteNot Systems", "email": "sales@wastenot.com", "industry": "Waste Management", "role": "supplier", "sustainability_score": 78.9, "created_at": "2024-02-10T09:15:00Z"},
    {"id": "USR-005", "company_name": "SunPower Solutions", "email": "info@sunpower.com", "industry": "Energy", "role": "supplier", "sustainability_score": 88.0, "created_at": "2024-02-20T14:45:00Z"},
    {"id": "USR-006", "company_name": "GreenBuyer Alliance", "email": "members@greenbuyer.org", "industry": "Sustainability", "role": "buyer", "sustainability_score": 95.0, "created_at": "2024-03-01T11:00:00Z"}
]

MOCK_CERTIFICATIONS = [
    {"id": "CERT-001", "name": "B Corp Certification", "issuing_body": "B Lab", "level": "Comprehensive", "description": "Highest standard for verified social and environmental performance", "required_score": 80.0, "created_at": "2024-01-01T00:00:00Z"},
    {"id": "CERT-002", "name": "ISO 14001", "issuing_body": "ISO", "level": "Environmental Management", "description": "International standard for environmental management systems", "required_score": 70.0, "created_at": "2024-01-01T00:00:00Z"},
    {"id": "CERT-003", "name": "Carbon Trust Standard", "issuing_body": "Carbon Trust", "level": "Carbon Reduction", "description": "Achieve year-on-year carbon reduction", "required_score": 75.0, "created_at": "2024-01-01T00:00:00Z"},
    {"id": "CERT-004", "name": "LEED Certification", "issuing_body": "USGBC", "level": "Green Building", "description": "Leadership in Energy and Environmental Design", "required_score": 60.0, "created_at": "2024-01-01T00:00:00Z"},
    {"id": "CERT-005", "name": "Fair Trade Certified", "issuing_body": "Fair Trade International", "level": "Supply Chain", "description": "Ensures fair wages and sustainable practices", "required_score": 65.0, "created_at": "2024-01-01T00:00:00Z"},
    {"id": "CERT-006", "name": "Cradle to Cradle Certified", "issuing_body": "Cradle to Cradle Products Innovation Institute", "level": "Product Design", "description": "Circular economy product certification", "required_score": 55.0, "created_at": "2024-01-01T00:00:00Z"}
]

app = FastAPI(title="GreenLoop Exchange", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SupplierCreate(BaseModel):
    name: str
    description: str = ""
    category: str = ""
    certification_level: str = "Standard"
    location: str = ""
    rating: float = 4.0
    verified: bool = True

class ProductCreate(BaseModel):
    name: str
    supplier_id: str
    category: str = ""
    price: float = 0.0
    unit: str = "unit"
    carbon_saved: float = 0.0
    stock: int = 0
    description: str = ""

class OffsetCreate(BaseModel):
    name: str
    type: str = ""
    price_per_ton: float = 0.0
    available_tons: int = 0
    verification_standard: str = ""
    project_location: str = ""
    description: str = ""

class OrderCreate(BaseModel):
    buyer_id: str
    items: str = ""
    total: float = 0.0
    status: str = "pending"
    carbon_offset_amount: float = 0.0

class UserCreate(BaseModel):
    company_name: str
    email: str
    industry: str = ""
    role: str = "buyer"
    sustainability_score: float = 0.0

class CertificationCreate(BaseModel):
    name: str
    issuing_body: str = ""
    level: str = "Standard"
    description: str = ""
    required_score: float = 0.0

@app.on_event("startup")
async def startup():
    global db_engine, SessionLocal
    if db_engine:
        Base.metadata.create_all(db_engine)

@app.get("/health")
async def health():
    return {"status": "ok", "app": "GreenLoop Exchange", "version": "1.0.0"}

@app.get("/api/info")
async def info():
    return {
        "name": "GreenLoop Exchange",
        "tagline": "Connecting B2B buyers with certified green suppliers and carbon-offset products",
        "description": "A sustainability-focused marketplace for verified green products and carbon offsets",
        "founded": "2024",
        "company": "GreenLoop Ventures",
        "team_size": 47,
        "headquarters": "Berlin, Germany",
        "certified_suppliers": 250,
        "products_listed": 1200,
        "carbon_offset_total_tons": 50000,
        "industry": "Sustainability / Green Technology"
    }

@app.get("/api/metrics")
async def metrics():
    return {
        "total_suppliers": 250,
        "total_products": 1200,
        "total_offsets_available": 240000,
        "total_orders": 1800,
        "total_users": 650,
        "carbon_saved_this_year": 15000,
        "co2_offset_tons_sold": 35000,
        "average_order_value": 4200.00,
        "supplier_verification_rate": 85.5,
        "monthly_active_users": 320,
        "platform_growth_percent": 28.3,
        "certifications_issued": 45
    }

# Supplier endpoints
@app.get("/api/suppliers")
async def get_suppliers(category: str = Query(None), verified: bool = Query(None)):
    if SessionLocal:
        session = SessionLocal()
        try:
            query = session.query(SupplierDB)
            if category:
                query = query.filter(SupplierDB.category == category)
            if verified is not None:
                query = query.filter(SupplierDB.verified == verified)
            results = query.all()
            suppliers = [{"id": s.id, "name": s.name, "description": s.description, "category": s.category, "certification_level": s.certification_level, "location": s.location, "rating": s.rating, "verified": s.verified, "created_at": str(s.created_at)} for s in results]
            return suppliers
        finally:
            session.close()
    else:
        results = MOCK_SUPPLIERS
        if category:
            results = [s for s in results if s["category"] == category]
        if verified is not None:
            results = [s for s in results if s["verified"] == verified]
        return results

@app.get("/api/suppliers/{supplier_id}")
async def get_supplier(supplier_id: str):
    if SessionLocal:
        session = SessionLocal()
        try:
            s = session.query(SupplierDB).filter(SupplierDB.id == supplier_id).first()
            if not s:
                raise HTTPException(status_code=404, detail="Supplier not found")
            return {"id": s.id, "name": s.name, "description": s.description, "category": s.category, "certification_level": s.certification_level, "location": s.location, "rating": s.rating, "verified": s.verified, "created_at": str(s.created_at)}
        finally:
            session.close()
    else:
        for s in MOCK_SUPPLIERS:
            if s["id"] == supplier_id:
                return s
        raise HTTPException(status_code=404, detail="Supplier not found")

@app.post("/api/suppliers")
async def create_supplier(supplier: SupplierCreate):
    new_id = f"SUP-{len(MOCK_SUPPLIERS) + 1:03d}"
    if SessionLocal:
        session = SessionLocal()
        try:
            db_item = SupplierDB(id=new_id, name=supplier.name, description=supplier.description, category=supplier.category, certification_level=supplier.certification_level, location=supplier.location, rating=supplier.rating, verified=supplier.verified, created_at=datetime.utcnow())
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return {"id": db_item.id, "name": db_item.name, "description": db_item.description, "category": db_item.category, "certification_level": db_item.certification_level, "location": db_item.location, "rating": db_item.rating, "verified": db_item.verified, "created_at": str(db_item.created_at)}
        finally:
            session.close()
    else:
        new_supplier = {"id": new_id, "name": supplier.name, "description": supplier.description, "category": supplier.category, "certification_level": supplier.certification_level, "location": supplier.location, "rating": supplier.rating, "verified": supplier.verified, "created_at": datetime.utcnow().isoformat()}
        MOCK_SUPPLIERS.append(new_supplier)
        return new_supplier

# Product endpoints
@app.get("/api/products")
async def get_products(category: str = Query(None), supplier_id: str = Query(None), min_price: float = Query(None), max_price: float = Query(None)):
    if SessionLocal:
        session = SessionLocal()
        try:
            query = session.query(ProductDB)
            if category:
                query = query.filter(ProductDB.category == category)
            if supplier_id:
                query = query.filter(ProductDB.supplier_id == supplier_id)
            if min_price is not None:
                query = query.filter(ProductDB.price >= min_price)
            if max_price is not None:
                query = query.filter(ProductDB.price <= max_price)
            results = query.all()
            products = [{"id": p.id, "name": p.name, "supplier_id": p.supplier_id, "category": p.category, "price": p.price, "unit": p.unit, "carbon_saved": p.carbon_saved, "stock": p.stock, "description": p.description, "created_at": str(p.created_at)} for p in results]
            return products
        finally:
            session.close()
    else:
        results = MOCK_PRODUCTS
        if category:
            results = [p for p in results if p["category"] == category]
        if supplier_id:
            results = [p for p in results if p["supplier_id"] == supplier_id]
        if min_price is not None:
            results = [p for p in results if p["price"] >= min_price]
        if max_price is not None:
            results = [p for p in results if p["price"] <= max_price]
        return results

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    if SessionLocal:
        session = SessionLocal()
        try:
            p = session.query(ProductDB).filter(ProductDB.id == product_id).first()
            if not p:
                raise HTTPException(status_code=404, detail="Product not found")
            return {"id": p.id, "name": p.name, "supplier_id": p.supplier_id, "category": p.category, "price": p.price, "unit": p.unit, "carbon_saved": p.carbon_saved, "stock": p.stock, "description": p.description, "created_at": str(p.created_at)}
        finally:
            session.close()
    else:
        for p in MOCK_PRODUCTS:
            if p["id"] == product_id:
                return p
        raise HTTPException(status_code=404, detail="Product not found")

@app.post("/api/products")
async def create_product(product: ProductCreate):
    new_id = f"PROD-{len(MOCK_PRODUCTS) + 1:03d}"
    if SessionLocal:
        session = SessionLocal()
        try:
            db_item = ProductDB(id=new_id, name=product.name, supplier_id=product.supplier_id, category=product.category, price=product.price, unit=product.unit, carbon_saved=product.carbon_saved, stock=product.stock, description=product.description, created_at=datetime.utcnow())
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return {"id": db_item.id, "name": db_item.name, "supplier_id": db_item.supplier_id, "category": db_item.category, "price": db_item.price, "unit": db_item.unit, "carbon_saved": db_item.carbon_saved, "stock": db_item.stock, "description": db_item.description, "created_at": str(db_item.created_at)}
        finally:
            session.close()
    else:
        new_product = {"id": new_id, "name": product.name, "supplier_id": product.supplier_id, "category": product.category, "price": product.price, "unit": product.unit, "carbon_saved": product.carbon_saved, "stock": product.stock, "description": product.description, "created_at": datetime.utcnow().isoformat()}
        MOCK_PRODUCTS.append(new_product)
        return new_product

# Offset endpoints
@app.get("/api/offsets")
async def get_offsets(offset_type: str = Query(None, alias="type"), min_price: float = Query(None), max_price: float = Query(None)):
    if SessionLocal:
        session = SessionLocal()
        try:
            query = session.query(OffsetDB)
            if offset_type:
                query = query.filter(OffsetDB.type == offset_type)
            if min_price is not None:
                query = query.filter(OffsetDB.price_per_ton >= min_price)
            if max_price is not None:
                query = query.filter(OffsetDB.price_per_ton <= max_price)
            results = query.all()
            offsets = [{"id": o.id, "name": o.name, "type": o.type, "price_per_ton": o.price_per_ton, "available_tons": o.available_tons, "verification_standard": o.verification_standard, "project_location": o.project_location, "description": o.description, "created_at": str(o.created_at)} for o in results]
            return offsets
        finally:
            session.close()
    else:
        results = MOCK_OFFSETS
        if offset_type:
            results = [o for o in results if o["type"] == offset_type]
        if min_price is not None:
            results = [o for o in results if o["price_per_ton"] >= min_price]
        if max_price is not None:
            results = [o for o in results if o["price_per_ton"] <= max_price]
        return results

@app.get("/api/offsets/{offset_id}")
async def get_offset(offset_id: str):
    if SessionLocal:
        session = SessionLocal()
        try:
            o = session.query(OffsetDB).filter(OffsetDB.id == offset_id).first()
            if not o:
                raise HTTPException(status_code=404, detail="Offset not found")
            return {"id": o.id, "name": o.name, "type": o.type, "price_per_ton": o.price_per_ton, "available_tons": o.available_tons, "verification_standard": o.verification_standard, "project_location": o.project_location, "description": o.description, "created_at": str(o.created_at)}
        finally:
            session.close()
    else:
        for o in MOCK_OFFSETS:
            if o["id"] == offset_id:
                return o
        raise HTTPException(status_code=404, detail="Offset not found")

@app.post("/api/offsets")
async def create_offset(offset: OffsetCreate):
    new_id = f"OFF-{len(MOCK_OFFSETS) + 1:03d}"
    if SessionLocal:
        session = SessionLocal()
        try:
            db_item = OffsetDB(id=new_id, name=offset.name, type=offset.type, price_per_ton=offset.price_per_ton, available_tons=offset.available_tons, verification_standard=offset.verification_standard, project_location=offset.project_location, description=offset.description, created_at=datetime.utcnow())
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return {"id": db_item.id, "name": db_item.name, "type": db_item.type, "price_per_ton": db_item.price_per_ton, "available_tons": db_item.available_tons, "verification_standard": db_item.verification_standard, "project_location": db_item.project_location, "description": db_item.description, "created_at": str(db_item.created_at)}
        finally:
            session.close()
    else:
        new_offset = {"id": new_id, "name": offset.name, "type": offset.type, "price_per_ton": offset.price_per_ton, "available_tons": offset.available_tons, "verification_standard": offset.verification_standard, "project_location": offset.project_location, "description": offset.description, "created_at": datetime.utcnow().isoformat()}
        MOCK_OFFSETS.append(new_offset)
        return new_offset

# Order endpoints
@app.get("/api/orders")
async def get_orders(status: str = Query(None), buyer_id: str = Query(None)):
    if SessionLocal:
        session = SessionLocal()
        try:
            query = session.query(OrderDB)
            if status:
                query = query.filter(OrderDB.status == status)
            if buyer_id:
                query = query.filter(OrderDB.buyer_id == buyer_id)
            results = query.all()
            orders = [{"id": o.id, "buyer_id": o.buyer_id, "items": o.items, "total": o.total, "status": o.status, "carbon_offset_amount": o.carbon_offset_amount, "created_at": str(o.created_at)} for o in results]
            return orders
        finally:
            session.close()
    else:
        results = MOCK_ORDERS
        if status:
            results = [o for o in results if o["status"] == status]
        if buyer_id:
            results = [o for o in results if o["buyer_id"] == buyer_id]
        return results

@app.get("/api/orders/{order_id}")
async def get_order(order_id: str):
    if SessionLocal:
        session = SessionLocal()
        try:
            o = session.query(OrderDB).filter(OrderDB.id == order_id).first()
            if not o:
                raise HTTPException(status_code=404, detail="Order not found")
            return {"id": o.id, "buyer_id": o.buyer_id, "items": o.items, "total": o.total, "status": o.status, "carbon_offset_amount": o.carbon_offset_amount, "created_at": str(o.created_at)}
        finally:
            session.close()
    else:
        for o in MOCK_ORDERS:
            if o["id"] == order_id:
                return o
        raise HTTPException(status_code=404