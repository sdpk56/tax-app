# Tax Calculator API Documentation

## Overview
This API provides comprehensive tax calculation services with support for multiple tax regimes, deductions, rebates, and historical tracking.

## Base URL
```
http://tax-backend:5000
```

## Authentication
All endpoints (except `/signup` and `/login`) require JWT authentication via the `Authorization` header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### 1. User Registration
**POST** `/signup`

Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
- **Success (201)**
```json
{
  "message": "User registered successfully!"
}
```
- **Error (409)** - Username already exists
- **Error (400)** - Missing username or password
- **Error (500)** - Server error

---

### 2. User Login
**POST** `/login`

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
- **Success (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
- **Error (401)** - Invalid username or password
- **Error (400)** - Missing credentials

---

## Tax Calculation Endpoints

### 3. Calculate Tax
**POST** `/calculate-tax`

Calculate income tax with detailed breakdown.

**Request Body:**
```json
{
  "income": 1000000,
  "regime": "new",
  "deductions": 150000,
  "rebates": {},
  "save_history": true
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| income | float | Yes | Annual gross income |
| regime | string | Yes | Tax regime: "old" or "new" |
| deductions | float | No | Standard deductions/80C claims (default: 0) |
| rebates | object | No | Tax rebates applicable (default: {}) |
| save_history | boolean | No | Save to calculation history (default: true) |

**Response:**
- **Success (200)**
```json
{
  "gross_income": 1000000,
  "deductions": 150000,
  "taxable_income": 850000,
  "base_tax": 85000,
  "surcharge": 0,
  "health_education_cess": 3400,
  "total_tax": 88400,
  "effective_tax_rate": 8.84,
  "tax_per_month": 7366.67,
  "take_home_annual": 911600,
  "take_home_monthly": 75966.67
}
```
- **Error (400)** - Invalid input
- **Error (401)** - Unauthorized
- **Error (500)** - Server error

---

### 4. Compare Tax Regimes
**POST** `/compare-regimes`

Compare tax liability between old and new tax regimes.

**Request Body:**
```json
{
  "income": 1000000,
  "deductions": 150000
}
```

**Response:**
- **Success (200)**
```json
{
  "old_regime": {
    "gross_income": 1000000,
    "deductions": 150000,
    "taxable_income": 850000,
    "base_tax": 85000,
    "surcharge": 0,
    "health_education_cess": 3400,
    "total_tax": 88400,
    "effective_tax_rate": 8.84,
    "take_home_annual": 911600,
    "take_home_monthly": 75966.67
  },
  "new_regime": {
    "gross_income": 1000000,
    "deductions": 0,
    "taxable_income": 1000000,
    "base_tax": 120000,
    "surcharge": 0,
    "health_education_cess": 4800,
    "total_tax": 124800,
    "effective_tax_rate": 12.48,
    "take_home_annual": 875200,
    "take_home_monthly": 72933.33
  },
  "savings": 36400,
  "recommended_regime": "old"
}
```

---

### 5. Get Tax Slab Breakdown
**GET** `/tax-slabs/{regime}`

Get detailed breakdown of income across tax slabs.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| income | float | Yes | Annual income |

**Example:**
```
GET /tax-slabs/new?income=1000000
```

**Response:**
- **Success (200)**
```json
{
  "regime": "new",
  "income": 1000000,
  "slabs": [
    {
      "range": "0 - 2.5L",
      "income_in_slab": 250000,
      "rate": "0%",
      "tax": 0
    },
    {
      "range": "2.5L - 5L",
      "income_in_slab": 250000,
      "rate": "5%",
      "tax": 12500
    },
    {
      "range": "5L - 7.5L",
      "income_in_slab": 250000,
      "rate": "10%",
      "tax": 25000
    },
    {
      "range": "7.5L - 10L",
      "income_in_slab": 250000,
      "rate": "15%",
      "tax": 37500
    }
  ]
}
```

---

## Tax History Endpoints

### 6. Get Tax Calculation History
**GET** `/tax-history`

Retrieve all previous tax calculations for the current user.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| per_page | integer | No | Results per page (default: 10) |

**Response:**
- **Success (200)**
```json
{
  "total": 5,
  "pages": 1,
  "current_page": 1,
  "calculations": [
    {
      "id": 1,
      "gross_income": 1000000,
      "deductions": 150000,
      "taxable_income": 850000,
      "base_tax": 85000,
      "surcharge": 0,
      "health_education_cess": 3400,
      "total_tax": 88400,
      "effective_tax_rate": 8.84,
      "regime": "new",
      "take_home_annual": 911600,
      "take_home_monthly": 75966.67,
      "created_at": "2024-12-04T10:30:00"
    }
  ]
}
```

---

### 7. Delete Tax Calculation
**DELETE** `/tax-history/{calc_id}`

Delete a specific tax calculation from history.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| calc_id | integer | ID of the calculation to delete |

**Response:**
- **Success (200)**
```json
{
  "message": "Calculation deleted successfully."
}
```
- **Error (404)** - Calculation not found
- **Error (401)** - Unauthorized

---

## User Information Endpoints

### 8. Get User Info
**GET** `/user-info`

Get information about the currently authenticated user.

**Response:**
- **Success (200)**
```json
{
  "username": "john_doe",
  "created_at": "2024-12-01T08:15:00"
}
```
- **Error (404)** - User not found
- **Error (401)** - Unauthorized

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input parameters |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Token verification failed |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Username already exists |
| 500 | Internal Server Error |
| 503 | Service Unavailable - Backend connection error |

---

## Tax Slab Information

### Old Regime (FY 2024-25)
- 0 - ₹2.5L: 0%
- ₹2.5L - ₹5L: 5%
- ₹5L - ₹10L: 20%
- ₹10L+: 30%

### New Regime (FY 2024-25)
- 0 - ₹2.5L: 0%
- ₹2.5L - ₹5L: 5%
- ₹5L - ₹7.5L: 10%
- ₹7.5L - ₹10L: 15%
- ₹10L - ₹12.5L: 20%
- ₹12.5L - ₹15L: 25%
- ₹15L+: 30%

### Additional Components
- **Surcharge:** Applied based on income level
- **Health & Education Cess:** 4% on (base tax + surcharge)

---

## Example Usage

### Example 1: Calculate Tax in New Regime
```bash
curl -X POST http://localhost:5000/calculate-tax \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "income": 1000000,
    "regime": "new",
    "deductions": 0,
    "save_history": true
  }'
```

### Example 2: Compare Both Regimes
```bash
curl -X POST http://localhost:5000/compare-regimes \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "income": 1000000,
    "deductions": 150000
  }'
```

### Example 3: Get Tax History
```bash
curl -X GET "http://localhost:5000/tax-history?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Rate Limiting
Currently no rate limiting is implemented. This should be added for production deployments.

## Version
API Version: 1.0.0
Last Updated: December 4, 2024
