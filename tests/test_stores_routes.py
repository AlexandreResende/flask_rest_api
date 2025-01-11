def test_get_stores_with_no_stores(test_app):
    response = test_app.get("/stores")
    data = response.json

    assert response.status_code == 200
    assert len(data["stores"]) == 0