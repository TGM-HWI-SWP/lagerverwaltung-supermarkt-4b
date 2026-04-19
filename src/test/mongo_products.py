from datetime import datetime
from src.domain.product import Product
from src.adapters.mongodb_product_repository import MongoDBProductRepository

# MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:Gabi12345.@cluster0.jge9ku6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_URI = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"

repo = MongoDBProductRepository(MONGO_URI)


def make_product(id_, name, description, price, category, quantity, min_stock, sku, notes):
    p = Product(id_, name, description, price, category, quantity, min_stock)

    # fehlende Attribute ergänzen, damit dein Repo.save_product() funktioniert
    p.id = id_
    p.sku = sku
    p.notes = notes
    p.created_at = datetime.now()
    p.updated_at = datetime.now()

    return p


products = [
    make_product("P002", "Apfel", "Roter Apfel", 1.5, "Obst", 120, 10, "SKU-002", "Frisch geliefert"),
    make_product("P003", "Banane", "Gelbe Banane", 1.2, "Obst", 150, 10, "SKU-003", "Reif"),
    make_product("P004", "Orange", "Saftige Orange", 1.8, "Obst", 100, 10, "SKU-004", "Süß"),
    make_product("P005", "Trauben", "Süße Weintrauben", 2.4, "Obst", 80, 8, "SKU-005", "Kernlos"),
    make_product("P006", "Zitrone", "Frische Zitrone", 0.9, "Obst", 90, 10, "SKU-006", "Sauer"),

    make_product("P007", "Tomate", "Frische Tomate", 2.1, "Gemüse", 110, 10, "SKU-007", "Regional"),
    make_product("P008", "Gurke", "Grüne Gurke", 1.1, "Gemüse", 95, 10, "SKU-008", "Knackig"),
    make_product("P009", "Karotte", "Bio Karotte", 1.3, "Gemüse", 130, 12, "SKU-09", "Bio"),
    make_product("P010", "Paprika", "Rote Paprika", 1.9, "Gemüse", 85, 10, "SKU-010", "Mild"),
    make_product("P011", "Zwiebel", "Gelbe Zwiebel", 0.8, "Gemüse", 140, 15, "SKU-011", "Lagerware"),

    make_product("P012", "Milch", "Vollmilch 1L", 1.2, "Milchprodukte", 200, 20, "SKU-012", "Kühlware"),
    make_product("P013", "Joghurt", "Naturjoghurt", 0.95, "Milchprodukte", 160, 15, "SKU-013", "Ohne Zucker"),
    make_product("P014", "Butter", "Butter 250g", 2.3, "Milchprodukte", 90, 10, "SKU-014", "Marke Hausgut"),
    make_product("P015", "Käse", "Gouda Käse", 3.8, "Milchprodukte", 70, 8, "SKU-015", "Mild gereift"),
    make_product("P016", "Sahne", "Schlagsahne 250ml", 1.4, "Milchprodukte", 75, 10, "SKU-016", "Zum Kochen"),

    make_product("P017", "Brot", "Weißbrot", 1.9, "Backwaren", 100, 10, "SKU-017", "Tagesfrisch"),
    make_product("P018", "Semmel", "Frische Semmel", 0.5, "Backwaren", 220, 20, "SKU-018", "Knusprig"),
    make_product("P019", "Croissant", "Buttercroissant", 1.1, "Backwaren", 85, 10, "SKU-019", "Französische Art"),
    make_product("P020", "Wasser", "Mineralwasser 1.5L", 0.7, "Getränke", 300, 30, "SKU-020", "Still"),
    make_product("P021", "Cola", "Cola 1L", 1.6, "Getränke", 180, 20, "SKU-021", "Zuckerhaltig"),

    make_product("P022", "Erdbeeren", "Frische Erdbeeren", 3.2, "Obst", 70, 8, "SKU-022", "Saisonal"),
    make_product("P023", "Ananas", "Süße Ananas", 2.9, "Obst", 60, 6, "SKU-023", "Exotisch"),
    make_product("P024", "Mango", "Reife Mango", 2.5, "Obst", 65, 7, "SKU-024", "Import"),
    make_product("P025", "Brokkoli", "Frischer Brokkoli", 1.7, "Gemüse", 90, 10, "SKU-025", "Grün"),
    make_product("P026", "Spinat", "Blattspinat", 1.4, "Gemüse", 85, 10, "SKU-026", "Bio"),

    make_product("P027", "Kartoffel", "Speisekartoffel", 0.6, "Gemüse", 300, 25, "SKU-027", "Regional"),
    make_product("P028", "Champignons", "Frische Champignons", 2.2, "Gemüse", 75, 8, "SKU-028", "Zuchtware"),
    make_product("P029", "Eier", "10er Pack Eier", 2.8, "Milchprodukte", 120, 15, "SKU-029", "Freilandhaltung"),
    make_product("P030", "Mozzarella", "Mozzarella 125g", 1.3, "Milchprodukte", 95, 10, "SKU-030", "Italienisch"),
    make_product("P031", "Quark", "Magerquark 500g", 1.1, "Milchprodukte", 110, 12, "SKU-031", "Proteinreich"),

    make_product("P032", "Toastbrot", "Toastbrot 500g", 1.5, "Backwaren", 130, 15, "SKU-032", "Weich"),
    make_product("P033", "Baguette", "Frisches Baguette", 1.2, "Backwaren", 100, 10, "SKU-033", "Knusprig"),
    make_product("P034", "Donut", "Zucker Donut", 0.9, "Backwaren", 140, 15, "SKU-034", "Süß"),
    make_product("P035", "Apfelsaft", "Apfelsaft 1L", 1.8, "Getränke", 160, 20, "SKU-035", "Naturtrüb"),
    make_product("P036", "Orangensaft", "Orangensaft 1L", 2.0, "Getränke", 150, 20, "SKU-036", "Fruchtig"),

    make_product("P037", "Eistee", "Pfirsich Eistee 1.5L", 1.6, "Getränke", 170, 20, "SKU-037", "Erfrischend"),
    make_product("P038", "Kaffee", "Gemahlener Kaffee 500g", 4.5, "Getränke", 80, 10, "SKU-038", "Stark"),
    make_product("P039", "Tee", "Schwarzer Tee 20 Beutel", 2.2, "Getränke", 90, 10, "SKU-39", "Aromatisch"),
    make_product("P040", "Schokolade", "Vollmilchschokolade", 1.3, "Süßwaren", 200, 20, "SKU-040", "Klassisch"),
    make_product("P041", "Kekse", "Butterkekse 200g", 1.7, "Süßwaren", 180, 20, "SKU-041", "Knusprig"),

    make_product("P042", "Kiwi", "Grüne Kiwi", 0.8, "Obst", 95, 10, "SKU-042", "Vitaminreich"),
    make_product("P043", "Pfirsich", "Saftiger Pfirsich", 1.9, "Obst", 85, 8, "SKU-043", "Sommerobst"),
    make_product("P044", "Kirschen", "Süße Kirschen", 3.6, "Obst", 55, 6, "SKU-044", "Saisonal"),
    make_product("P045", "Avocado", "Reife Avocado", 2.4, "Obst", 70, 8, "SKU-045", "Cremig"),
    make_product("P046", "Birne", "Grüne Birne", 1.6, "Obst", 100, 10, "SKU-046", "Saftig"),

    make_product("P047", "Salat", "Kopfsalat", 1.3, "Gemüse", 75, 8, "SKU-047", "Frisch"),
    make_product("P048", "Sellerie", "Knollensellerie", 1.5, "Gemüse", 60, 6, "SKU-048", "Würzig"),
    make_product("P049", "Lauch", "Frischer Lauch", 1.4, "Gemüse", 80, 8, "SKU-049", "Regional"),
    make_product("P050", "Aubergine", "Dunkle Aubergine", 1.8, "Gemüse", 65, 7, "SKU-050", "Mediterran"),
    make_product("P051", "Zucchini", "Grüne Zucchini", 1.6, "Gemüse", 90, 10, "SKU-051", "Mild"),

    make_product("P052", "Frischkäse", "Natur Frischkäse 200g", 1.7, "Milchprodukte", 100, 10, "SKU-052", "Cremig"),
    make_product("P053", "Buttermilch", "Buttermilch 1L", 1.2, "Milchprodukte", 85, 10, "SKU-053", "Leicht"),
    make_product("P054", "Emmentaler", "Emmentaler Käse", 4.1, "Milchprodukte", 60, 8, "SKU-054", "Würzig"),
    make_product("P055", "Pudding", "Vanillepudding", 0.9, "Milchprodukte", 130, 12, "SKU-055", "Dessert"),
    make_product("P056", "Kefir", "Kefir 500ml", 1.5, "Milchprodukte", 70, 8, "SKU-056", "Fermentiert"),

    make_product("P057", "Muffin", "Schokomuffin", 1.4, "Backwaren", 95, 10, "SKU-057", "Süß"),
    make_product("P058", "Brezel", "Frische Brezel", 0.8, "Backwaren", 150, 15, "SKU-058", "Salzig"),
    make_product("P059", "Vollkornbrot", "Vollkornbrot 500g", 2.2, "Backwaren", 90, 10, "SKU-059", "Ballaststoffreich"),
    make_product("P060", "Limonade", "Zitronenlimonade 1.5L", 1.5, "Getränke", 140, 15, "SKU-060", "Spritzig"),
    make_product("P061", "Energydrink", "Energydrink 250ml", 1.9, "Getränke", 110, 12, "SKU-061", "Koffeinhaltig"),

    make_product("P062", "Granatapfel", "Frischer Granatapfel", 2.7, "Obst", 60, 6, "SKU-062", "Exotisch"),
    make_product("P063", "Blaubeeren", "Frische Blaubeeren", 3.4, "Obst", 70, 8, "SKU-063", "Antioxidantien"),
    make_product("P064", "Himbeeren", "Saftige Himbeeren", 3.6, "Obst", 65, 7, "SKU-064", "Empfindlich"),
    make_product("P065", "Melone", "Wassermelone", 4.2, "Obst", 40, 5, "SKU-065", "Sommerfrucht"),
    make_product("P066", "Kokosnuss", "Frische Kokosnuss", 3.0, "Obst", 50, 6, "SKU-066", "Hartschale"),

    make_product("P067", "Rucola", "Frischer Rucola", 1.6, "Gemüse", 80, 8, "SKU-067", "Würzig"),
    make_product("P068", "Radieschen", "Rote Radieschen", 1.2, "Gemüse", 90, 10, "SKU-068", "Scharf"),
    make_product("P069", "Mais", "Zuckermais", 1.9, "Gemüse", 70, 8, "SKU-069", "Süßlich"),
    make_product("P070", "Erbsen", "Grüne Erbsen", 1.5, "Gemüse", 85, 9, "SKU-070", "Frisch"),
    make_product("P071", "Grünkohl", "Frischer Grünkohl", 2.1, "Gemüse", 60, 7, "SKU-071", "Wintergemüse"),

    make_product("P072", "Ricotta", "Ricotta Käse 250g", 2.2, "Milchprodukte", 75, 8, "SKU-072", "Italienisch"),
    make_product("P073", "Mascarpone", "Mascarpone 250g", 2.8, "Milchprodukte", 65, 7, "SKU-073", "Dessert"),
    make_product("P074", "Schafskäse", "Feta Käse", 3.5, "Milchprodukte", 70, 8, "SKU-074", "Salzig"),
    make_product("P075", "Trinkjoghurt", "Erdbeer Trinkjoghurt", 1.3, "Milchprodukte", 90, 10, "SKU-075", "Flüssig"),
    make_product("P076", "Kondensmilch", "Kondensmilch Dose", 1.9, "Milchprodukte", 80, 9, "SKU-076", "Konzentriert"),

    make_product("P077", "Strudel", "Apfelstrudel", 2.5, "Backwaren", 70, 8, "SKU-077", "Süß"),
    make_product("P078", "Krapfen", "Marillenkrapfen", 1.6, "Backwaren", 100, 12, "SKU-078", "Gefüllt"),
    make_product("P079", "Ciabatta", "Ciabatta Brot", 2.1, "Backwaren", 85, 10, "SKU-079", "Italienisch"),
    make_product("P080", "Mineralwasser Sprudel", "Mineralwasser 1.5L Sprudel", 0.8, "Getränke", 200, 20, "SKU-080", "Spritzig"),
    make_product("P081", "Proteinshake", "Schoko Proteinshake 500ml", 2.9, "Getränke", 95, 10, "SKU-081", "Fitness"),
]


for product in products:
    repo.save_product(product)

print("Weitere Produkte gespeichert.")