# Zaptek Internship Applications API

A REST API for managing internship applications, built with **FastAPI** as part of the Zaptek Backend Engineering with FastAPI (Team 2), Week 1 individual task.

The API uses **mock data** (a Python list in memory) instead of a real database, to focus on API architecture, routing, CRUD operations, validation and error handling.

**Live API:** https://zaptek-internship.onrender.com
**Interactive docs:** https://zaptek-internship.onrender.com/docs

**Author:** Joseph Boafo Afful

---

## Tech stack

- **FastAPI**: web framework for building the API
- **Pydantic**: data validation through schemas
- **Uvicorn**: ASGI server that runs the app
- **Render**: hosting

---

## Project structure

```
week_1_backend_task/
├── app/
│   ├── main.py              # Creates the app, registers routers and error handlers
│   ├── data.py              # Mock data (the in-memory "database")
│   ├── schemas.py           # Pydantic schemas and validation rules
│   └── routers/
│       └── applications.py  # All /applications endpoints
├── requirements.txt
└── README.md
```

---

## Endpoints

Base URL: `https://zaptek-internship.onrender.com`

| Method | Endpoint | Description | Success code |
|---|---|---|---|
| GET | `/` | Health message | 200 |
| GET | `/applications/` | Get all applications | 200 |
| GET | `/applications/?status=accepted` | Filter by status (`pending`, `accepted`, `rejected`) | 200 |
| GET | `/applications/{id}` | Get a single application by id | 200 |
| POST | `/applications/` | Create a new application | 201 |
| PUT | `/applications/{id}` | Replace an application (all fields required) | 200 |
| PATCH | `/applications/{id}` | Update only the fields sent | 200 |
| DELETE | `/applications/{id}` | Delete an application | 204 |

---

## Schema design

| Schema | Purpose |
|---|---|
| `ApplicationBase` | Shared fields and validation rules |
| `ApplicationCreate` | Request body for POST and PUT. The client cannot set `id`, `status` or `submittedAt` |
| `ApplicationUpdate` | Request body for PATCH. Every field is optional |
| `Application` | Response model. Base fields plus `id`, `status` and `submittedAt` |

The server sets `id`, `status` (always `pending` for new applications) and `submittedAt`.

---

## Validation rules

| Field | Rule |
|---|---|
| `fullName` | 3–100 characters |
| `email` | Valid email format, must be unique |
| `phone`, `whatsappNumber` | 10 digits, starting with 0 (e.g. `0245567812`) |
| `university`, `course` | At least 2 characters |
| `motivation` | 20–1000 characters |
| `portfolioLink`, `resumeLink` | Optional, must be valid URLs |
| `joinInnovationClub` | Boolean, defaults to `false` |
| `status` | One of `pending`, `accepted`, `rejected` |

---

## Error handling

Every error returns the same format:

```json
{
  "success": false,
  "error": {
    "status": 404,
    "message": "Application with id 1 not found"
  }
}
```

Validation errors also include which fields failed:

```json
{
  "success": false,
  "error": {
    "status": 422,
    "message": "Invalid data",
    "details": [
      { "field": "phone", "message": "must be 10 digits starting with 0, e.g. 0245567812" }
    ]
  }
}
```

| Code | Meaning |
|---|---|
| 400 | PATCH sent with no fields |
| 404 | Application or route not found |
| 409 | Email already used by another application |
| 422 | Request data failed validation |

---

## Example request

**POST** `/applications/`

```json
{
  "fullName": "Willy Doe",
  "email": "willy@gmail.com",
  "phone": "0244456667",
  "whatsappNumber": "0244456667",
  "university": "KNUST",
  "course": "Computer Science",
  "level": "2nd Year",
  "track": "Backend Engineering",
  "motivation": "I want to build real backend systems with FastAPI.",
  "joinInnovationClub": true
}
```

Returns **201 Created** with the new application, including its `id`, `status: "pending"` and `submittedAt`.

---

## Run locally

```bash
git clone https://github.com/astrolabscig/zaptek_internship.git
cd zaptek_internship/week_1_backend_task
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

---

## Deployment (Render)

| Setting | Value |
|---|---|
| Root Directory | `week_1_backend_task` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

---

## Notes

- Data is stored in memory, so it resets to the original 4 records whenever the server restarts.
- On Render's free plan, the service sleeps after about 15 minutes of inactivity. The first request after that may take 30–60 seconds.
