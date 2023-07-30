import enum


class Categories(enum.StrEnum):
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    LACTOSE_FREE = "lactose_free"
    VEGETARIAN = "vegetarian"
    FINGER_FOOD = "finger_food"
    CAFE = "cafe"
    HAMBURGER_SHOP = "hamburger_shop"
    PIZZA_SHOP = "pizzeria"
    RESTAURANT = "restaurant"
    BAR = "bar"
    FAST_FOOD = "fast_food"
    BAKERY = "bakery"

    def verbose_name(self) -> str:
        return {
            Categories.VEGAN: "Vegan",
            Categories.GLUTEN_FREE: "Gluten-free",
            Categories.LACTOSE_FREE: "Lactose-free",
            Categories.VEGETARIAN: "Vegetarian",
            Categories.FINGER_FOOD: "Finger food",
            Categories.CAFE: "Cafe",
            Categories.CAFE: "Cafe",
            Categories.HAMBURGER_SHOP: "Hamburger shop",
            Categories.PIZZA_SHOP: "Pizza shop",
            Categories.RESTAURANT: "Restaurant",
            Categories.BAR: "Bar",
            Categories.FAST_FOOD: "Fast food",
            Categories.BAKERY: "Bakery",
        }[self]