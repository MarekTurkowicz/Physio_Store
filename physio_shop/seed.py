"""
Seed script — populates the database with realistic physiotherapy product data.
Run: python seed.py
"""

import asyncio
import sys
from decimal import Decimal

from app.core.security import hash_password
from app.database import async_session_factory, engine
from app.models import Base, Category, Order, OrderItem, Product, User


# ──────────────────────────────────────────────
# Seed data
# ──────────────────────────────────────────────

CATEGORIES = [
    {
        "name": "Taśmy i gumy do ćwiczeń",
        "slug": "tasmy-i-gumy-do-cwiczen",
        "description": "Taśmy oporowe, gumy i minibandy do rehabilitacji i treningu.",
    },
    {
        "name": "Piłki i wałki do masażu",
        "slug": "pilki-i-walki-do-masazu",
        "description": "Roller, piłki lacrosse, wałki wibracyjne — automasaż i rozluźnianie mięśniowo-powięziowe.",
    },
    {
        "name": "Elektrostymulatory",
        "slug": "elektrostymulatory",
        "description": "Urządzenia TENS, EMS i kombinowane do elektrostymulacji mięśni.",
    },
    {
        "name": "Ortezy i stabilizatory",
        "slug": "ortezy-i-stabilizatory",
        "description": "Ortezy stawowe, stabilizatory, opaski uciskowe do rehabilitacji pourazowej.",
    },
    {
        "name": "Poduszki i kliny rehabilitacyjne",
        "slug": "poduszki-i-kliny-rehabilitacyjne",
        "description": "Kliny pozycjonujące, poduszki ortopedyczne, siedziska rehabilitacyjne.",
    },
    {
        "name": "Akcesoria do terapii manualnej",
        "slug": "akcesoria-do-terapii-manualnej",
        "description": "Kinesiology tape, bańki próżniowe, narzędzia IASTM i akcesoria fizjoterapeutyczne.",
    },
]

PRODUCTS = [
    # Taśmy i gumy (category index 0)
    {
        "name": "Taśma TheraBand CLX zielona (mocny opór)",
        "description": "Taśma oporowa z pętlami do rehabilitacji kończyn górnych i dolnych. Latex-free, 2.2m.",
        "price": Decimal("89.99"),
        "stock_quantity": 50,
        "sku": "TB-CLX-GREEN",
        "category_idx": 0,
    },
    {
        "name": "Guma oporowa MoVes Band 5.5m niebieska",
        "description": "Taśma do ćwiczeń fizjoterapeutycznych, opór średni. Idealna do ćwiczeń stabilizacyjnych.",
        "price": Decimal("45.00"),
        "stock_quantity": 80,
        "sku": "MV-BAND-BLUE",
        "category_idx": 0,
    },
    {
        "name": "MiniBand zestaw 3 szt. (lekki/średni/mocny)",
        "description": "Zestaw gum oporowych do treningu pośladków, bioder i kolan. 3 poziomy oporu.",
        "price": Decimal("39.90"),
        "stock_quantity": 120,
        "sku": "MB-SET-3",
        "category_idx": 0,
    },
    # Piłki i wałki (category index 1)
    {
        "name": "Wałek do masażu roller EVA 45cm",
        "description": "Wałek piankowy do automasażu i rozluźniania mięśniowo-powięziowego. Twardy rdzeń EVA.",
        "price": Decimal("59.99"),
        "stock_quantity": 60,
        "sku": "RLR-EVA-45",
        "category_idx": 1,
    },
    {
        "name": "Piłka lacrosse do trigger pointów",
        "description": "Twardość piłki pozwala precyzyjnie rozluźnić punkty spustowe. Średnica 6.3cm.",
        "price": Decimal("24.90"),
        "stock_quantity": 100,
        "sku": "BALL-LAX-63",
        "category_idx": 1,
    },
    {
        "name": "Roller wibracyjny Vibra Pro 4-biegowy",
        "description": "Wałek wibracyjny z 4 poziomami intensywności. Bateria litowa, 2h pracy ciągłej.",
        "price": Decimal("249.00"),
        "stock_quantity": 20,
        "sku": "VBR-PRO-4",
        "category_idx": 1,
    },
    {
        "name": "Duo-Ball podwójna piłka do masażu kręgosłupa",
        "description": "Podwójna piłka do masażu mięśni przykręgosłupowych. Silikonowa, antypoślizgowa.",
        "price": Decimal("34.50"),
        "stock_quantity": 70,
        "sku": "DBALL-SPINE",
        "category_idx": 1,
    },
    # Elektrostymulatory (category index 2)
    {
        "name": "TENS/EMS Beurer EM 49 Digital",
        "description": "Dwukanałowy elektrostymulator z 64 programami. TENS przeciwbólowy + EMS wzmacniający.",
        "price": Decimal("189.00"),
        "stock_quantity": 15,
        "sku": "BEU-EM49",
        "category_idx": 2,
    },
    {
        "name": "Compex SP 4.0 elektrostymulator bezprzewodowy",
        "description": "Profesjonalny elektrostymulator z modułami MI (inteligencja mięśniowa). 30 programów.",
        "price": Decimal("1890.00"),
        "stock_quantity": 5,
        "sku": "COMP-SP40",
        "category_idx": 2,
    },
    {
        "name": "Elektrody samoprzylepne TENS 5x5cm (4 szt.)",
        "description": "Elektrody żelowe wielokrotnego użytku, kompatybilne z większością stymulatorów.",
        "price": Decimal("19.90"),
        "stock_quantity": 200,
        "sku": "ELEC-5X5-4",
        "category_idx": 2,
    },
    # Ortezy i stabilizatory (category index 3)
    {
        "name": "Orteza stawu kolanowego z fiszbinami bocznymi",
        "description": "Stabilizacja boczna kolana. Regulowane paski, neopren oddychający. Rozmiar uniwersalny.",
        "price": Decimal("119.00"),
        "stock_quantity": 30,
        "sku": "ORT-KNEE-FB",
        "category_idx": 3,
    },
    {
        "name": "Stabilizator nadgarstka z szyną aluminiową",
        "description": "Orteza nadgarstkowa z wyjmowaną szyną. Zapięcie rzepowe. Prawa/lewa ręka.",
        "price": Decimal("69.90"),
        "stock_quantity": 45,
        "sku": "STAB-WRIST",
        "category_idx": 3,
    },
    {
        "name": "Opaska uciskowa na łokieć tenisisty",
        "description": "Opaska z pelotą silikonową na epicondylitis. Regulowana, oddychająca.",
        "price": Decimal("49.90"),
        "stock_quantity": 55,
        "sku": "BAND-TENNIS",
        "category_idx": 3,
    },
    # Poduszki i kliny (category index 4)
    {
        "name": "Klin rehabilitacyjny 30° z pokrowcem",
        "description": "Klin pozycjonujący do ćwiczeń i układania kończyn. Pianka poliuretanowa, pokrowiec do prania.",
        "price": Decimal("149.00"),
        "stock_quantity": 25,
        "sku": "KLIN-30DEG",
        "category_idx": 4,
    },
    {
        "name": "Poduszka ortopedyczna do siedzenia Ergo-Sit",
        "description": "Poduszka zmniejszająca nacisk na kość ogonową. Memory foam, pokrowiec antypoślizgowy.",
        "price": Decimal("129.00"),
        "stock_quantity": 35,
        "sku": "ERGO-SIT",
        "category_idx": 4,
    },
    {
        "name": "Wałek półokrągły stabilizacyjny 90cm",
        "description": "Wałek do ćwiczeń równoważnych i stabilizacyjnych. Pianka HD, pokrowiec PVC.",
        "price": Decimal("89.00"),
        "stock_quantity": 40,
        "sku": "HALF-RLR-90",
        "category_idx": 4,
    },
    # Akcesoria do terapii manualnej (category index 5)
    {
        "name": "Kinesiology Tape 5cm x 5m (bawełniany)",
        "description": "Elastyczny plaster kinezjologiczny. Akrylowy klej hipoalergiczny, wodoodporny.",
        "price": Decimal("22.90"),
        "stock_quantity": 150,
        "sku": "KTAPE-5X5",
        "category_idx": 5,
    },
    {
        "name": "Bańki próżniowe silikonowe zestaw 4 szt.",
        "description": "Bańki do cupping therapy w 4 rozmiarach. Silikon medyczny, łatwe w użyciu.",
        "price": Decimal("54.90"),
        "stock_quantity": 65,
        "sku": "CUP-SIL-4",
        "category_idx": 5,
    },
    {
        "name": "Narzędzie IASTM do terapii tkanek miękkich",
        "description": "Narzędzie ze stali nierdzewnej do instrumentalnej mobilizacji tkanek miękkich. Ergonomiczny kształt.",
        "price": Decimal("159.00"),
        "stock_quantity": 20,
        "sku": "IASTM-STEEL",
        "category_idx": 5,
    },
    {
        "name": "Olejek do masażu arnikowy 250ml",
        "description": "Olejek z arniką górską do masażu sportowego i rehabilitacyjnego. Rozgrzewający.",
        "price": Decimal("34.90"),
        "stock_quantity": 90,
        "sku": "OIL-ARN-250",
        "category_idx": 5,
    },
]

USERS = [
    {
        "email": "admin@physioshop.pl",
        "password": "admin123",
        "full_name": "Admin PhysioShop",
        "role": "admin",
    },
    {
        "email": "manager@physioshop.pl",
        "password": "manager123",
        "full_name": "Zarządca Sklepu",
        "role": "manager",
    },
    {
        "email": "jan.kowalski@example.com",
        "password": "customer123",
        "full_name": "Jan Kowalski",
        "role": "customer",
    },
    {
        "email": "anna.nowak@example.com",
        "password": "customer123",
        "full_name": "Anna Nowak",
        "role": "customer",
    },
]


async def seed():
    """Populate the database with initial data."""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        # Create users
        print("👤 Tworzenie użytkowników...")
        db_users = []
        for user_data in USERS:
            user = User(
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                full_name=user_data["full_name"],
                role=user_data["role"],
            )
            session.add(user)
            db_users.append(user)

        await session.flush()
        print(f"   ✅ Utworzono {len(db_users)} użytkowników")

        # Create categories
        print("📁 Tworzenie kategorii...")
        db_categories = []
        for cat_data in CATEGORIES:
            category = Category(**cat_data)
            session.add(category)
            db_categories.append(category)

        await session.flush()
        print(f"   ✅ Utworzono {len(db_categories)} kategorii")

        # Create products
        print("📦 Tworzenie produktów...")
        db_products = []
        for prod_data in PRODUCTS:
            category = db_categories[prod_data["category_idx"]]
            product = Product(
                name=prod_data["name"],
                description=prod_data["description"],
                price=prod_data["price"],
                stock_quantity=prod_data["stock_quantity"],
                sku=prod_data["sku"],
                category_id=category.id,
                is_active=True,
            )
            session.add(product)
            db_products.append(product)

        await session.flush()
        print(f"   ✅ Utworzono {len(db_products)} produktów")

        # Create sample orders
        print("🛒 Tworzenie przykładowych zamówień...")
        customer = db_users[1]  # Jan Kowalski

        order = Order(
            user_id=customer.id,
            status="confirmed",
            total_amount=Decimal("174.89"),
            shipping_address="ul. Fizjoterapeutyczna 12/3, 00-001 Warszawa",
        )
        session.add(order)
        await session.flush()

        order_items = [
            OrderItem(order_id=order.id, product_id=db_products[0].id, quantity=1, unit_price=db_products[0].price),
            OrderItem(order_id=order.id, product_id=db_products[4].id, quantity=2, unit_price=db_products[4].price),
            OrderItem(order_id=order.id, product_id=db_products[16].id, quantity=1, unit_price=db_products[16].price),
        ]
        for item in order_items:
            session.add(item)

        await session.commit()
        print("   ✅ Utworzono 1 przykładowe zamówienie")

    print()
    print("=" * 50)
    print("🎉 Seed zakończony pomyślnie!")
    print("=" * 50)
    print()
    print("Dane logowania:")
    print(f"  Admin:       admin@physioshop.pl / admin123")
    print(f"  Zarządca:    manager@physioshop.pl / manager123")
    print(f"  Klient 1:    jan.kowalski@example.com / customer123")
    print(f"  Klient 2:    anna.nowak@example.com / customer123")
    print()


if __name__ == "__main__":
    asyncio.run(seed())
