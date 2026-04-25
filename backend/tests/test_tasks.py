def test_create_task(client, auth_headers):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Study for exam",
            "priority": "HIGH",
            "category": "ASSIGNMENT",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Study for exam"
    assert data["priority"] == "HIGH"


def test_list_tasks(client, auth_headers):
    client.post(
        "/api/v1/tasks",
        json={"title": "Task 1"},
        headers=auth_headers,
    )
    response = client.get("/api/v1/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_task(client, auth_headers):
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "My Task"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task(client, auth_headers):
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "Old Title"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "New Title", "status": "IN_PROGRESS"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["status"] == "IN_PROGRESS"


def test_delete_task(client, auth_headers):
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "To Delete"},
        headers=auth_headers,
    )
    task_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204


def test_unauthorized_access(client):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 401
