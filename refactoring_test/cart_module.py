"""
Модуль расчета и оформления корзины интернет-магазина.
Результат рефакторинга: внешний API (calc_ord) и результат расчетов не изменились.
"""

MIN_AGE = 18
VAT_RATE = 0.20
DISCOUNT_SALE10 = 0.10
DISCOUNT_SPRING5 = 0.05
DISCOUNT_VIP = 0.07
LOYALTY_MIN_DAYS = 365
LOYALTY_BONUS = 100.0

PROMO_CODE_SALE10 = "SALE10"
PROMO_CODE_SPRING5 = "SPRING5"
PROMO_CATEGORY = "promo"

PROMO_CODE_RATES = {
    PROMO_CODE_SALE10: DISCOUNT_SALE10,
    PROMO_CODE_SPRING5: DISCOUNT_SPRING5,
}


def is_user_eligible(user):
    """Может ли пользователь оформлять заказ (не заблокирован и совершеннолетний)."""
    if user is None:
        return False
    if user.get('is_blocked', False):
        return False
    if user.get('age', 0) < MIN_AGE:
        return False
    return True


def is_item_valid(item):
    """Цена и количество позиции должны быть положительными."""
    return item['price'] > 0 and item['qty'] > 0



def calculate_subtotal(cart_items):
    """Сумма корзины без скидок.

    Возвращает кортеж (сумма, есть_ли_акционный_товар)
    или None, если в корзине есть невалидная позиция.
    """
    subtotal = 0
    has_promo_item = False
    for item in cart_items:
        if not is_item_valid(item):
            return None
        subtotal += item['price'] * item['qty']
        if item.get('cat') == PROMO_CATEGORY:
            has_promo_item = True
    return subtotal, has_promo_item


def calculate_discount(user, subtotal, promo_code, is_vip, has_promo_item):
    """Общая скидка: промокод + VIP + бонус лояльности (не больше суммы корзины)."""
    discount = 0

    # промокод не действует, если в корзине есть акционный товар
    if not has_promo_item:
        discount += subtotal * PROMO_CODE_RATES.get(promo_code, 0)

    if is_vip:
        discount += subtotal * DISCOUNT_VIP

    if user.get('reg_days', 0) > LOYALTY_MIN_DAYS:
        discount += LOYALTY_BONUS

    return min(discount, subtotal)


def calc_ord(u, c, d_code, vip=False):
    """Главная функция расчета заказа.

    u      -- пользователь {'age': int, 'reg_days': int, 'is_blocked': bool}
    c      -- список товаров [{'id', 'name', 'price', 'qty', 'cat'}]
    d_code -- промокод ('SALE10', 'SPRING5', ...)
    vip    -- VIP-статус
    Возвращает словарь с итогами или None, если заказ оформить нельзя.
    """
    user, cart_items, promo_code = u, c, d_code

    if not is_user_eligible(user) or len(cart_items) == 0:
        return None

    result = calculate_subtotal(cart_items)
    if result is None:
        return None
    subtotal, has_promo_item = result

    discount = calculate_discount(user, subtotal, promo_code, vip, has_promo_item)
    amount_after_discount = subtotal - discount
    tax = amount_after_discount * VAT_RATE
    total = amount_after_discount + tax

    return {
        'subtotal': round(subtotal, 2),
        'discount': round(discount, 2),
        'tax': round(tax, 2),
        'total': round(total, 2),
    }
