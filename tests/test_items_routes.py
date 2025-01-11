import uuid

def test_get_items_with_no_items(test_app):
    response = test_app.get("/items")
    data = response.json

    assert response.status_code == 200
    assert len(data["items"]) == 0

def test_get_item_by_id_when_item_does_not_exist(test_app):
    store_id = uuid.uuid4().hex
    item_id = uuid.uuid4().hex

    response = test_app.get("/stores/" + store_id + "/items/" + item_id)

    data = response.json

    assert response.status_code == 404
    assert data["message"] == "Item not found"

def test_put_item_when_item_does_not_exist(test_app):
    store_id = uuid.uuid4().hex
    item_id = uuid.uuid4().hex

    response = test_app.put(
        "/stores/" + store_id + "/items/" + item_id,
        json={ "name": "Jacket" }
    )

    data = response.json

    assert response.status_code == 404
    assert data["message"] == "Item not found"

def test_delete_items_when_item_does_not_exist(test_app):
    store_id = uuid.uuid4().hex
    item_id = uuid.uuid4().hex

    response = test_app.delete("/stores/" + store_id + "/items/" + item_id)

    data = response.json

    assert response.status_code == 404
    assert data["message"] == "Item not found"