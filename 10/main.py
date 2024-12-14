#! /usr/bin/env python3
import json
import time
from random import randint

import cjson
import ujson
from faker import Faker


def test_loads():
    faker = Faker()
    json_test_data = {}
    for _ in range(1000):
        json_test_data[faker.first_name() * 5] = faker.last_name() * 5

    json_dump = json.dumps(json_test_data)

    ujson_doc = ujson.loads(json_dump)
    json_doc = json.loads(json_dump)
    cjson_doc = cjson.loads(json_dump)

    assert ujson_doc == json_doc == cjson_doc


def test_loads_with_digits():
    faker = Faker()
    json_test_data = {}
    for _ in range(1000):
        json_test_data[faker.first_name()] = randint(1, 10)

    json_dump = ujson.dumps(json_test_data)

    json_doc = json.loads(json_dump)
    ujson_doc = ujson.loads(json_dump)
    cjson_doc = cjson.loads(json_dump)

    assert json_doc == ujson_doc == cjson_doc


def test_dumps():
    faker = Faker()
    json_test_data = {}
    for _ in range(1000):
        json_test_data[faker.first_name()] = faker.last_name()

    json_dump = json.dumps(json_test_data)
    cjson_dump = cjson.dumps(json_test_data)

    assert json_dump == cjson_dump


def test_dumps_with_digits():
    faker = Faker()
    json_test_data = {}
    for _ in range(1000):
        json_test_data[faker.first_name()] = randint(1, 10)

    json_dump = json.dumps(json_test_data)
    cjson_dump = cjson.dumps(json_test_data)

    assert json_dump == cjson_dump


def test_speed():
    faker = Faker()
    json_test_data = {}
    for _ in range(100_000):
        json_test_data[faker.first_name()] = faker.last_name()

    json_dump = json.dumps(json_test_data)

    start_ts_json = time.time()
    json_doc = json.loads(json_dump)
    stop_ts_json = time.time()
    runtime_json = stop_ts_json - start_ts_json

    start_ts_ujson = time.time()
    ujson_doc = ujson.loads(json_dump)
    stop_ts_ujson = time.time()
    runtime_ujson = stop_ts_ujson - start_ts_ujson

    start_ts_cjson = time.time()
    cjson_doc = cjson.loads(json_dump)
    stop_ts_cjson = time.time()
    runtime_cjson = stop_ts_cjson - start_ts_cjson

    print(
        f"========== loads speed test ========== \njson:\t{runtime_json}\nujson: {runtime_ujson}\n \
        cjson: {runtime_cjson}\n"
    )

    start_ts_json = time.time()
    json_dump = json.dumps(json_test_data)
    stop_ts_json = time.time()
    runtime_json = stop_ts_json - start_ts_json

    start_ts_cjson = time.time()
    _ = cjson.dumps(json_test_data)
    stop_ts_cjson = time.time()
    runtime_cjson = stop_ts_cjson - start_ts_cjson

    print(
        f"========== dumps speed test ========== \njson:\t{runtime_json}\ncjson: {runtime_cjson}\n"
    )

    assert ujson_doc == json_doc == cjson_doc


if __name__ == "__main__":
    test_loads()
    print("Test 1 passed")

    test_loads_with_digits()
    print("Test 2 passed")

    test_dumps()
    print("Test 3 passed")

    test_dumps_with_digits()
    print("Test 4 passed")

    test_speed()
    print("Test 5 passed")

    print("All tests passed")
