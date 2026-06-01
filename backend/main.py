import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = os.environ.get("COMPANY_SLUG", "greenloop_ventures")
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
    name = Column(String)
    description = Column(Text)
    category = Column(String)
    region = Column(String)
    sustainability_rating = Column(Float)
    certifications = Column(Text)
    founded_year = Column(Integer)
    verified = Column(Boolean, default=False)
    contact_email = Column(String)
    website = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProductDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_products"
    id = Column(String, primary_key=True)
    supplier_id = Column(String)
    name = Column(String)
    description = Column(Text)
    category = Column(String)
    price = Column(Float)
    unit = Column(String)
    carbon_footprint = Column(Float)
    carbon_offset_available = Column(Boolean)
    min_order_qty = Column(Integer)
    stock = Column(Integer)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class CertificationDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_certifications"
    id = Column(String, primary_key=True)
    supplier_id = Column(String)
    name = Column(String)
    issuing_body = Column(String)
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    status = Column(String)
    description = Column(Text)

class ReviewDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_reviews"
    id = Column(String, primary_key=True)
    product_id = Column(String)
    user_id = Column(String)
    rating = Column(Integer)
    title = Column(String)
    content = Column(Text)
    verified_purchase = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_orders"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    product_id = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String)
    carbon_offset_contribution = Column(Float)
    payment_method = Column(String)
    shipping_address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserDB(Base):
    __tablename__ = f"{COMPANY_SLUG}_users"
    id = Column(String, primary_key=True)
    username = Column(String)
    email = Column(String)
    company_name = Column(String)
    role = Column(String)
    sustainability_score = Column(Float)
    joined_at = Column(DateTime, default=datetime.utcnow)

if db_engine:
    Base.metadata.create_all(db_engine)

# Mock Data
MOCK_SUPPLIERS = [
    {"id": "sup-001", "name": "EcoMaterials Inc.", "description": "Leading supplier of recycled construction materials and sustainable building solutions.", "category": "construction", "region": "North America", "sustainability_rating": 9.2, "certifications": "ISO 14001, LEED, B Corp", "founded_year": 2008, "verified": True, "contact_email": "info@ecomaterials.com", "website": "www.ecomaterials.com", "created_at": "2023-01-15T08:00:00Z"},
    {"id": "sup-002", "name": "GreenChem Solutions", "description": "B2B supplier of bio-based chemicals and sustainable industrial solvents.", "category": "chemicals", "region": "Europe", "sustainability_rating": 8.7, "certifications": "EU Ecolabel, Cradle to Cradle", "founded_year": 2012, "verified": True, "contact_email": "sales@greenchem.eu", "website": "www.greenchem.eu", "created_at": "2023-02-20T10:30:00Z"},
    {"id": "sup-003", "name": "RenewablePack Co.", "description": "Specialists in 100% biodegradable packaging made from agricultural waste.", "category": "packaging", "region": "Asia Pacific", "sustainability_rating": 9.5, "certifications": "OK Compost, FSC, Carbon Neutral", "founded_year": 2015, "verified": True, "contact_email": "hello@renewablepack.com", "website": "www.renewablepack.com", "created_at": "2023-03-10T14:00:00Z"},
    {"id": "sup-004", "name": "SolarTech Global", "description": "Commercial solar panel manufacturer with integrated recycling program.", "category": "energy", "region": "Global", "sustainability_rating": 8.9, "certifications": "TUV, IEC, Energy Star", "founded_year": 2010, "verified": True, "contact_email": "partners@solartech.com", "website": "www.solartech.com", "created_at": "2023-04-05T09:15:00Z"},
    {"id": "sup-005", "name": "PureWater Systems", "description": "Industrial water purification and recycling systems with zero-liquid discharge.", "category": "water", "region": "Middle East", "sustainability_rating": 9.0, "certifications": "NSF, ISO 9001, WaterSense", "founded_year": 2006, "verified": True, "contact_email": "info@purewater.ae", "website": "www.purewater.ae", "created_at": "2023-05-12T11:45:00Z"},
    {"id": "sup-006", "name": "OrganicFields Agri", "description": "Certified organic agricultural inputs and regenerative farming supplies.", "category": "agriculture", "region": "South America", "sustainability_rating": 9.3, "certifications": "USDA Organic, Rainforest Alliance, Fair Trade", "founded_year": 2018, "verified": True, "contact_email": "orders@organicfields.br", "website": "www.organicfields.br", "created_at": "2023-06-01T07:30:00Z"},
    {"id": "sup-007", "name": "EcoFleet Logistics", "description": "Carbon-neutral logistics provider with electric delivery fleet and route optimization.", "category": "logistics", "region": "Europe", "sustainability_rating": 8.5, "certifications": "ISO 14064, Carbon Trust", "founded_year": 2019, "verified": True, "contact_email": "contact@ecofleet.eu", "website": "www.ecofleet.eu", "created_at": "2023-07-18T15:00:00Z"},
    {"id": "sup-008", "name": "GreenTextiles Ltd.", "description": "Sustainable textile manufacturer using organic cotton and recycled polyester.", "category": "textiles", "region": "South Asia", "sustainability_rating": 8.8, "certifications": "GOTS, OEKO-TEX, Fair Trade", "founded_year": 2014, "verified": True, "contact_email": "trade@greentextiles.in", "website": "www.greentextiles.in", "created_at": "2023-08-22T13:20:00Z"}
]

MOCK_PRODUCTS = [
    {"id": "prod-001", "supplier_id": "sup-001", "name": "EcoConcrete Blocks", "description": "Recycled aggregate concrete blocks for sustainable construction.", "category": "construction materials", "price": 45.00, "unit": "per pallet", "carbon_footprint": 12.5, "carbon_offset_available": True, "min_order_qty": 10, "stock": 5000, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c5b", "created_at": "2023-09-01T08:00:00Z"},
    {"id": "prod-002", "supplier_id": "sup-002", "name": "BioSolvent Cleaner", "description": "Non-toxic industrial cleaner derived from plant-based solvents.", "category": "industrial chemicals", "price": 28.50, "unit": "per gallon", "carbon_footprint": 3.2, "carbon_offset_available": True, "min_order_qty": 50, "stock": 10000, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c5c", "created_at": "2023-09-05T09:00:00Z"},
    {"id": "prod-003", "supplier_id": "sup-003", "name": "Biodegradable Mailer", "description": "Compostable shipping mailers made from cornstarch and PBAT.", "category": "packaging", "price": 0.75, "unit": "per unit", "carbon_footprint": 0.8, "carbon_offset_available": False, "min_order_qty": 500, "stock": 50000, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c5d", "created_at": "2023-09-10T10:00:00Z"},
    {"id": "prod-004", "supplier_id": "sup-004", "name": "Solar Panel 400W", "description": "High-efficiency monocrystalline solar panel with 25-year warranty.", "category": "solar energy", "price": 285.00, "unit": "per panel", "carbon_footprint": 45.0, "carbon_offset_available": True, "min_order_qty": 20, "stock": 2000, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c5e", "created_at": "2023-09-15T11:00:00Z"},
    {"id": "prod-005", "supplier_id": "sup-005", "name": "Industrial RO System", "description": "Reverse osmosis water purification system for manufacturing facilities.", "category": "water treatment", "price": 12500.00, "unit": "per system", "carbon_footprint": 200.0, "carbon_offset_available": True, "min_order_qty": 1, "stock": 50, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c5f", "created_at": "2023-09-20T12:00:00Z"},
    {"id": "prod-006", "supplier_id": "sup-006", "name": "Organic Fertilizer 50lb", "description": "Certified organic slow-release fertilizer for commercial agriculture.", "category": "agriculture inputs", "price": 35.00, "unit": "per bag", "carbon_footprint": 5.5, "carbon_offset_available": True, "min_order_qty": 100, "stock": 20000, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c60", "created_at": "2023-09-25T13:00:00Z"},
    {"id": "prod-007", "supplier_id": "sup-007", "name": "Carbon-Neutral Shipping", "description": "Full truckload logistics with carbon offset certificates included.", "category": "logistics services", "price": 2500.00, "unit": "per shipment", "carbon_footprint": 150.0, "carbon_offset_available": True, "min_order_qty": 1, "stock": 500, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c61", "created_at": "2023-10-01T14:00:00Z"},
    {"id": "prod-008", "supplier_id": "sup-008", "name": "Organic Cotton Fabric", "description": "GOTS-certified organic cotton fabric for sustainable apparel production.", "category": "textiles", "price": 12.00, "unit": "per yard", "carbon_footprint": 2.5, "carbon_offset_available": True, "min_order_qty": 100, "stock": 100000, "image_url": "https://images.unsplash.com/photo-1581092797707-5b7b1c5b5c62", "created_at": "2023-10-05T15:00:00Z"}
]

MOCK_CERTIFICATIONS = [
    {"id": "cert-001", "supplier_id": "sup-001", "name": "ISO 14001:2015", "issuing_body": "International Organization for Standardization", "issue_date": "2022-03-15", "expiry_date": "2025-03-15", "status": "active", "description": "Environmental management systems certification."},
    {"id": "cert-002", "supplier_id": "sup-001", "name": "LEED v4.1", "issuing_body": "U.S. Green Building Council", "issue_date": "2023-01-10", "expiry_date": "2026-01-10", "status": "active", "description": "Leadership in Energy and Environmental Design."},
    {"id": "cert-003", "supplier_id": "sup-001", "name": "B Corp Certification", "issuing_body": "B Lab", "issue_date": "2021-06-20", "expiry_date": "2024-06-20", "status": "active", "description": "Certified B Corporation meeting highest social and environmental standards."},
    {"id": "cert-004", "supplier_id": "sup-002", "name": "EU Ecolabel", "issuing_body": "European Commission", "issue_date": "2023-04-01", "expiry_date": "2026-04-01", "status": "active", "description": "EU product environmental excellence label."},
    {"id": "cert-005", "supplier_id": "sup-002", "name": "Cradle to Cradle Certified", "issuing_body": "Cradle to Cradle Products Innovation Institute", "issue_date": "2022-08-15", "expiry_date": "2025-08-15", "status": "active", "description": "Product circularity and sustainability certification."},
    {"id": "cert-006", "supplier_id": "sup-003", "name": "OK Compost INDUSTRIAL", "issuing_body": "TÜV Austria", "issue_date": "2023-02-28", "expiry_date": "2025-02-28", "status": "active", "description": "Certification for industrial compostability."},
    {"id": "cert-007", "supplier_id": "sup-003", "name": "FSC Certified", "issuing_body": "Forest Stewardship Council", "issue_date": "2022-11-01", "expiry_date": "2027-11-01", "status": "active", "description": "Responsible forestry certification."},
    {"id": "cert-008", "supplier_id": "sup-003", "name": "Carbon Neutral Certified", "issuing_body": "Carbon Trust", "issue_date": "2023-06-10", "expiry_date": "2024-06-10", "status": "active", "description": "Carbon neutrality certification for products and operations."}
]

MOCK_REVIEWS = [
    {"id": "rev-001", "product_id": "prod-001", "user_id": "user-001", "rating": 5, "title": "Excellent quality and sustainable", "content": "Used their EcoConcrete blocks for our new office building. Great quality and the carbon offset program was a bonus.", "verified_purchase": True, "created_at": "2023-10-10T10:00:00Z"},
    {"id": "rev-002", "product_id": "prod-003", "user_id": "user-002", "rating": 4, "title": "Great eco-friendly packaging", "content": "Switched to these mailers for our shipping. Customers love the compostable aspect. Minor issue with tear strength.", "verified_purchase": True, "created_at": "2023-10-12T14:30:00Z"},
    {"id": "rev-003", "product_id": "prod-002", "user_id": "user-003", "rating": 5, "title": "Best green solvent we've tried", "content": "Replaced our traditional solvents with BioSolvent. Works just as well with zero VOC emissions.", "verified_purchase": True, "created_at": "2023-10-15T09:45:00Z"},
    {"id": "rev-004", "product_id": "prod-004", "user_id": "user-004", "rating": 4, "title": "Good panels, excellent support", "content": "Installation was smooth. Generating great output. Slightly higher price point but worth it for the recycling program.", "verified_purchase": True, "created_at": "2023-10-18T11:20:00Z"},
    {"id": "rev-005", "product_id": "prod-006", "user_id": "user-005", "rating": 5, "title": "Amazing results for our farm", "content": "Our crop yields increased 20% while reducing synthetic fertilizer use. Highly recommend.", "verified_purchase": True, "created_at": "2023-10-20T16:00:00Z"},
    {"id": "rev-006", "product_id": "prod-005", "user_id": "user-006", "rating": 5, "title": "Zero-liquid discharge works perfectly", "content": "Installed in our factory. Recycles 95% of water. Payback period was less than 2 years.", "verified_purchase": True, "created_at": "2023-10-22T08:30:00Z"},
    {"id": "rev-007", "product_id": "prod-008", "user_id": "user-007", "rating": 4, "title": "Quality organic fabric", "content": "Consistent quality across batches. Colors hold well. Would love more variety in organic blends.", "verified_purchase": True, "created_at": "2023-10-25T13:15:00Z"},
    {"id": "rev-008", "product_id": "prod-007", "user_id": "user-008", "rating": 5, "title": "Fully carbon-neutral shipping", "content": "Their offset certificates are verified and transparent. Great partnership for our sustainability goals.", "verified_purchase": True, "created_at": "2023-10-28T10:45:00Z"}
]

MOCK_ORDERS = [
    {"id": "ord-001", "user_id": "user-001", "product_id": "prod-001", "quantity": 200, "total_price": 9000.00, "status": "delivered", "carbon_offset_contribution": 2500.00, "payment_method": "credit_card", "shipping_address": "123 Main Street, New York, NY 10001", "created_at": "2023-09-20T08:00:00Z"},
    {"id": "ord-002", "user_id": "user-002", "product_id": "prod-003", "quantity": 5000, "total_price": 3750.00, "status": "shipped", "carbon_offset_contribution": 4000.00, "payment_method": "bank_transfer", "shipping_address": "456 Innovation Drive, San Francisco, CA 94105", "created_at": "2023-09-25T10:30:00Z"},
    {"id": "ord-003", "user_id": "user-003", "product_id": "prod-002", "quantity": 500, "total_price": 14250.00, "status": "processing", "carbon_offset_contribution": 1600.00, "payment_method": "invoice", "shipping_address": "789 Eco Lane, Portland, OR 97201", "created_at": "2023-10-01T14:00:00Z"},
    {"id": "ord-004", "user_id": "user-004", "product_id": "prod-004", "quantity": 100, "total_price": 28500.00, "status": "confirmed", "carbon_offset_contribution": 4500.00, "payment_method": "credit_card", "shipping_address": "321 Green Street, Austin, TX 78701", "created_at": "2023-10-05T09:00:00Z"},
    {"id": "ord-005", "user_id": "user-005", "product_id": "prod-006", "quantity": 1000, "total_price": 35000.00, "status": "delivered", "carbon_offset_contribution": 5500.00, "payment_method": "bank_transfer", "shipping_address": "654 Harvest Road, Des Moines, IA 50309", "created_at": "2023-10-08T11:15:00Z"},
    {"id": "ord-006", "user_id": "user-006", "product_id": "prod-005", "quantity": 1, "total_price": 12500.00, "status": "processing", "carbon_offset_contribution": 2000.00, "payment_method": "invoice", "shipping_address": "987 Industrial Blvd, Chicago, IL 60601", "created_at": "2023-10-12T16:45:00Z"},
    {"id": "ord-007", "user_id": "user-007", "product_id": "prod-008", "quantity": 10000, "total_price": 120000.00, "status": "confirmed", "carbon_offset_contribution": 25000.00, "payment_method": "wire_transfer", "shipping_address": "147 Textile Way, Los Angeles, CA 90001", "created_at": "2023-10-15T08:30:00Z"},
    {"id": "ord-008", "user_id": "user-008", "product_id": "prod-007", "quantity": 5, "total_price": 12500.00, "status": "shipped", "carbon_offset_contribution": 7500.00, "payment_method": "credit_card", "shipping_address": "258 Logistics Park, Atlanta, GA 30301", "created_at": "2023-10-18T13:00:00Z"}
]

MOCK_USERS = [
    {"id": "user-001", "username": "ecobuilder", "email": "john@ecoconstruction.com", "company_name": "EcoBuild Corp", "role": "buyer", "sustainability_score": 85.0, "joined_at": "2023-01-10T08:00:00Z"},
    {"id": "user-002", "username": "greenpack", "email": "sarah@greenpackaging.com", "company_name": "GreenPackaging Solutions", "role": "buyer", "sustainability_score": 78.5, "joined_at": "2023-02-15T10:00:00Z"},
    {"id": "user-003", "username": "chemeco", "email": "mike@ecochemicals.com", "company_name": "EcoChemical Industries", "role": "buyer", "sustainability_score": 92.0, "joined_at": "2023-03-20T09:30:00Z"},
    {"id": "user-004", "username": "solarpro", "email": "emma@solarpro.com", "company_name": "SolarPro Installations", "role": "buyer", "sustainability_score": 88.5, "joined_at": "2023-04-10T14:00:00Z"},
    {"id": "user-005", "username": "agrigrow", "email": "carlos@agrigrow.com", "company_name": "AgriGrow Farms", "role": "buyer", "sustainability_score": 76.0, "joined_at": "2023-05-05T11:00:00Z"},
    {"id": "user-006", "username": "watertech", "email": "lena@watertech.com", "company_name": "WaterTech Industries", "role": "buyer", "sustainability_score": 91.5, "joined_at": "2023-06-01T16:00:00Z"},
    {"id": "user-007", "username": "textilegrn", "email": "priya@greentextiles.in", "company_name": "GreenTextiles Ltd.", "role": "supplier", "sustainability_score": 95.0, "joined_at": "2023-01-01T08:00:00Z"},
    {"id": "user-008", "username": "logistech", "email": "tom@ecofleet.eu", "company_name": "EcoFleet Logistics", "role": "supplier", "sustainability_score": 82.0, "joined_at": "2023-02-01T10:00:00Z"}
]

# Pydantic Models
class SupplierCreate(BaseModel):
    name: str
    description: str
    category: str
    region: str
    sustainability_rating: float
    certifications: str
    founded_year: int
    verified: bool = False
    contact_email: str
    website: str

class ProductCreate(BaseModel):
    supplier_id: str
    name: str
    description: str
    category: str
    price: float
    unit: str
    carbon_footprint: float
    carbon_offset_available: bool
    min_order_qty: int
    stock: int
    image_url: str

class OrderCreate(BaseModel):
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    payment_method: str
    shipping_address: str

app = FastAPI(title="GreenLoop Connect", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    if db_engine:
        Base.metadata.create_all(db_engine)

@app.get("/health")
def health():
    return {"status": "ok", "app": "GreenLoop Connect", "version": "1.0.0"}

@app.get("/api/info")
def info():
    return {
        "name": "GreenLoop Ventures",
        "app": "GreenLoop Connect",
        "tagline": "Connecting Businesses for a Sustainable Future",
        "description": "A sustainability-focused B2B marketplace connecting buyers with certified green suppliers and carbon-offset products.",
        "founded": 2021,
        "team_size": 120,
        "headquarters": "San Francisco, CA",
        "mission": "Accelerating the transition to a circular economy by making sustainable procurement accessible and transparent.",
        "verified_suppliers": 850,
        "products_listed": 15000,
        "carbon_offset_delivered": 250000,
        "certifications_accepted": 15,
        "regions_served": 45,
        "industries_covered": ["construction", "packaging", "chemicals", "energy", "water", "agriculture", "logistics", "textiles"]
    }

@app.get("/api/metrics")
def metrics():
    return {
        "total_suppliers": 850,
        "active_suppliers": 720,
        "total_products": 15000,
        "total_orders": 12500,
        "total_revenue": 58000000,
        "avg_sustainability_rating": 8.7,
        "carbon_offset_contribution_kg": 250000,
        "verified_suppliers_percentage": 84.7,
        "monthly_active_users": 3400,
        "order_fulfillment_rate": 96.5,
        "avg_order_value": 4640.00,
        "return_rate": 2.3,
        "top_categories": ["packaging", "construction materials", "energy", "agriculture inputs"],
        "growth_rate": 18.5
    }

# Supplier endpoints
@app.get("/api/suppliers")
def get_suppliers(category: str = None, region: str = None, verified: bool = None):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(SupplierDB)
        if category:
            query = query.filter(SupplierDB.category == category)
        if region:
            query = query.filter(SupplierDB.region == region)
        if verified is not None:
            query = query.filter(SupplierDB.verified == verified)
        suppliers = query.all()
        db.close()
        return [{"id": s.id, "name": s.name, "description": s.description, "category": s.category, "region": s.region, "sustainability_rating": s.sustainability_rating, "certifications": s.certifications, "founded_year": s.founded_year, "verified": s.verified, "contact_email": s.contact_email, "website": s.website, "created_at": s.created_at.isoformat()} for s in suppliers]
    else:
        results = MOCK_SUPPLIERS
        if category:
            results = [s for s in results if s["category"] == category]
        if region:
            results = [s for s in results if s["region"] == region]
        if verified is not None:
            results = [s for s in results if s["verified"] == verified]
        return results

@app.get("/api/suppliers/{supplier_id}")
def get_supplier(supplier_id: str):
    if SessionLocal:
        db = SessionLocal()
        s = db.query(SupplierDB).filter(SupplierDB.id == supplier_id).first()
        db.close()
        if not s:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return {"id": s.id, "name": s.name, "description": s.description, "category": s.category, "region": s.region, "sustainability_rating": s.sustainability_rating, "certifications": s.certifications, "founded_year": s.founded_year, "verified": s.verified, "contact_email": s.contact_email, "website": s.website, "created_at": s.created_at.isoformat()}
    else:
        for s in MOCK_SUPPLIERS:
            if s["id"] == supplier_id:
                return s
        raise HTTPException(status_code=404, detail="Supplier not found")

@app.post("/api/suppliers")
def create_supplier(supplier: SupplierCreate):
    supplier_id = f"sup-{uuid.uuid4().hex[:8]}"
    if SessionLocal:
        db = SessionLocal()
        new_supplier = SupplierDB(
            id=supplier_id,
            name=supplier.name,
            description=supplier.description,
            category=supplier.category,
            region=supplier.region,
            sustainability_rating=supplier.sustainability_rating,
            certifications=supplier.certifications,
            founded_year=supplier.founded_year,
            verified=supplier.verified,
            contact_email=supplier.contact_email,
            website=supplier.website,
            created_at=datetime.utcnow()
        )
        db.add(new_supplier)
        db.commit()
        db.refresh(new_supplier)
        db.close()
        return {"id": new_supplier.id, "name": new_supplier.name, "description": new_supplier.description, "category": new_supplier.category, "region": new_supplier.region, "sustainability_rating": new_supplier.sustainability_rating, "certifications": new_supplier.certifications, "founded_year": new_supplier.founded_year, "verified": new_supplier.verified, "contact_email": new_supplier.contact_email, "website": new_supplier.website, "created_at": new_supplier.created_at.isoformat()}
    else:
        new_supplier = {
            "id": supplier_id,
            "name": supplier.name,
            "description": supplier.description,
            "category": supplier.category,
            "region": supplier.region,
            "sustainability_rating": supplier.sustainability_rating,
            "certifications": supplier.certifications,
            "founded_year": supplier.founded_year,
            "verified": supplier.verified,
            "contact_email": supplier.contact_email,
            "website": supplier.website,
            "created_at": datetime.utcnow().isoformat()
        }
        MOCK_SUPPLIERS.append(new_supplier)
        return new_supplier

# Product endpoints
@app.get("/api/listings")
def get_listings(category: str = None, supplier_id: str = None, min_rating: float = None, carbon_offset: bool = None):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(ProductDB)
        if category:
            query = query.filter(ProductDB.category == category)
        if supplier_id:
            query = query.filter(ProductDB.supplier_id == supplier_id)
        if carbon_offset is not None:
            query = query.filter(ProductDB.carbon_offset_available == carbon_offset)
        products = query.all()
        db.close()
        results = []
        for p in products:
            supplier = None
            if SessionLocal:
                s = db.query(SupplierDB).filter(SupplierDB.id == p.supplier_id).first()
                if s:
                    supplier = {"id": s.id, "name": s.name, "sustainability_rating": s.sustainability_rating}
            else:
                for s in MOCK_SUPPLIERS:
                    if s["id"] == p.supplier_id:
                        supplier = {"id": s["id"], "name": s["name"], "sustainability_rating": s["sustainability_rating"]}
            results.append({
                "id": p.id,
                "supplier_id": p.supplier_id,
                "supplier": supplier,
                "name": p.name,
                "description": p.description,
                "category": p.category,
                "price": p.price,
                "unit": p.unit,
                "carbon_footprint": p.carbon_footprint,
                "carbon_offset_available": p.carbon_offset_available,
                "min_order_qty": p.min_order_qty,
                "stock": p.stock,
                "image_url": p.image_url,
                "created_at": p.created_at.isoformat()
            })
        return results
    else:
        results = MOCK_PRODUCTS
        if category:
            results = [p for p in results if p["category"] == category]
        if supplier_id:
            results = [p for p in results if p["supplier_id"] == supplier_id]
        if min_rating is not None:
            supplier_ids_with_