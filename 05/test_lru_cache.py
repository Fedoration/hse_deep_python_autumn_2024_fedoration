from lru_cache import LRUCache


def test_create_empty_cache():
    """Проверяем, что кэш создается пустым и имеет правильный лимит."""
    cache = LRUCache(2)
    assert cache.size == 0
    assert cache.limit == 2
    assert cache.get("non_existing") is None


def test_add_and_get_values():
    """Проверяем, что кэш может добавлять и извлекать значения."""
    cache = LRUCache(2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2"


def test_cache_eviction():
    """Проверяем, что кэш удаляет наименее недавно использованный элемент при превышении лимита."""
    cache = LRUCache(2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")

    cache.set("key3", "value3")

    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_update_existing_key():
    """Проверяем, что кэш корректно обновляет значение существующего ключа."""
    cache = LRUCache(2)
    cache.set("key1", "value1")
    cache.set("key1", "new_value1")

    assert cache.get("key1") == "new_value1"


def test_zero_limit():
    """При нулевом лимите кэш должен быть пустым"""
    cache = LRUCache(0)
    cache.set("key1", "value1")
    assert cache.get("key1") is None


def test_negative_limit():
    """При отрицательном лимите кэш должен быть пустым"""
    cache = LRUCache(-1)
    cache.set("key1", "value1")
    assert cache.get("key1") is None


def test_single_item_cache():
    """Проверяем, что кэш корректно работает с одним элементом."""
    cache = LRUCache(1)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"

    cache.set("key2", "value2")
    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"


def test_lru_order():
    """Проверяем, что кэш корректно обновляет порядок использования элементов."""
    cache = LRUCache(3)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    assert cache.get("key1") == "value1"

    cache.set("key4", "value4")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"


def test_bracket_access():
    """Проверяем, что кэш можно использовать через []."""
    cache = LRUCache(2)
    cache["key1"] = "value1"
    cache["key2"] = "value2"

    assert cache["key1"] == "value1"
    assert cache["key2"] == "value2"

    cache["key3"] = "value3"
    assert cache.get("key1") is None
    assert cache["key3"] == "value3"


def test_key_not_in_cache():
    """Проверяем, что кэш возвращает None, если ключа нет в кэше."""
    cache = LRUCache(2)
    assert cache.get("non_existent") is None


def test_large_cache_limit():
    """Проверяем, что кэш может хранить согласно лимиту."""
    cache = LRUCache(1000)
    for i in range(1000):
        cache.set(f"key{i}", f"value{i}")

    assert cache.size == 1000
    assert cache.get("key0") == "value0"


def test_none_values():
    """Проверяем, что кэш может хранить и извлекать значения None."""
    cache = LRUCache(2)
    cache.set("key1", None)
    assert cache.get("key1") is None
    cache.set("key2", "value2")
    assert cache.get("key2") == "value2"
    assert cache.get("key1") is None


def test_different_key_types():
    """Проверяем, что кэш может работать с разными типами ключей."""
    cache = LRUCache(2)
    cache.set(1, "value1")
    cache.set(2.5, "value2")
    assert cache.get(1) == "value1"
    assert cache.get(2.5) == "value2"

    cache.set(True, "value3")
    assert cache.get(True) == "value3"


def test_large_data():
    """Проверяем, что кэш может хранить элементы с большим объемом данных."""
    cache = LRUCache(2)
    large_value = "x" * 10**6
    cache.set("large_key", large_value)
    assert cache.get("large_key") == large_value
