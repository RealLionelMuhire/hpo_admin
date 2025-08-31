# Player Registration API Documentation

This document describes the REST API endpoints for player self-registration and authentication in the HPO Django backend.

## Base URL
```
http://localhost:8000/api/players/
```

## Authentication
The API uses UUID-based token authentication. After successful registration or login, you'll receive a UUID token that should be included in subsequent requests.

### Header Format
```
Authorization: Token YOUR_UUID_TOKEN_HERE
```

## Endpoints

### 1. Player Registration
**Endpoint:** `POST /api/players/register/`
**Authentication:** Not required
**Description:** Register a new player account

#### Request Body
```json
{
  "player_name": "John Doe",           // Required
  "username": "johndoe123",            // Required, must be unique
  "email": "john@example.com",         // Optional
  "phone": "+250788123456",            // Required
  "password": "mypassword123",         // Required, min 6 characters
  "password_confirm": "mypassword123", // Required, must match password
  "age_group": "20-24",               // Optional: "10-14", "15-19", "20-24", "25+"
  "gender": "male",                   // Optional: "male", "female", "other", "prefer_not_to_say"
  "province": "Kigali City",          // Optional
  "district": "Gasabo"                // Optional, must be valid for the province
}
```

#### Success Response (201 Created)
```json
{
  "message": "Player registered successfully",
  "player": {
    "id": 24,
    "player_name": "Test User",
    "username": "testuser999",
    "email": "test999@example.com",
    "phone": "+1234567890",
    "age_group": null,
    "gender": null,
    "province": null,
    "district": null,
    "points": 0,
    "games_played": 0,
    "games_won": 0,
    "win_rate": 0.0,
    "last_login": null,
    "created_at": "2025-08-31T18:45:34.318560Z"
  },
  "token": "51a39b79-eb27-408b-a864-be41a5a73075"
}
```

#### Error Response (400 Bad Request)
```json
{
  "error": "Registration failed",
  "details": {
    "username": ["Username already exists."],
    "password_confirm": ["Passwords do not match."]
  }
}
```

### 2. Player Login
**Endpoint:** `POST /api/players/login/`
**Authentication:** Not required
**Description:** Login with existing credentials and update last_login timestamp

#### Request Body
```json
{
  "username": "testuser999",
  "password": "securepass123"
}
```

#### Success Response (200 OK)
```json
{
  "message": "Login successful",
  "player": {
    "id": 24,
    "player_name": "Test User",
    "username": "testuser999",
    "email": "test999@example.com",
    "phone": "+1234567890",
    "age_group": null,
    "gender": null,
    "province": null,
    "district": null,
    "points": 0,
    "games_played": 0,
    "games_won": 0,
    "win_rate": 0.0,
    "last_login": "2025-08-31T19:14:14.840030Z",
    "created_at": "2025-08-31T18:45:34.318560Z"
  },
  "token": "51a39b79-eb27-408b-a864-be41a5a73075"
}
```

#### Error Response (401 Unauthorized)
```json
{
  "error": "Invalid credentials",
  "details": "Username or password is incorrect"
}
```

### 3. Player Profile
**Endpoint:** `GET /api/players/profile/`
**Authentication:** Required
**Description:** Get current player's profile information

#### Success Response (200 OK)
```json
{
  "id": 24,
  "player_name": "Test User",
  "username": "testuser999",
  "email": "test999@example.com",
  "phone": "+1234567890",
  "age_group": null,
  "gender": null,
  "province": null,
  "district": null,
  "points": 0,
  "games_played": 0,
  "games_won": 0,
  "win_rate": 0.0,
  "last_login": "2025-08-31T19:14:14.840030Z",
  "created_at": "2025-08-31T18:45:34.318560Z"
}
```

### 4. Player Logout
**Endpoint:** `POST /api/players/logout/`
**Authentication:** Required
**Description:** Logout and validate the current token (client-side token management)

#### Success Response (200 OK)
```json
{
  "message": "Logout successful",
  "player_name": "Test User"
}
```

**Note:** Since we use UUID-based tokens that don't expire server-side, logout is primarily a client-side operation. The server validates the token and confirms the logout request.

## Helper Endpoints for Form Data

### 5. Get Age Groups
**Endpoint:** `GET /api/players/form-data/age-groups/`
**Authentication:** Not required
**Description:** Get available age group options

#### Success Response (200 OK)
```json
{
  "age_groups": [
    {"value": "10-14", "label": "10-14"},
    {"value": "15-19", "label": "15-19"},
    {"value": "20-24", "label": "20-24"},
    {"value": "25+", "label": "25+"}
  ]
}
```

### 6. Get Provinces and Districts
**Endpoint:** `GET /api/players/form-data/provinces-districts/`
**Authentication:** Not required
**Description:** Get available provinces and their districts

#### Success Response (200 OK)
```json
{
  "provinces": [
    {
      "province": "Kigali City",
      "districts": [
        {"value": "Gasabo", "label": "Gasabo"},
        {"value": "Kicukiro", "label": "Kicukiro"},
        {"value": "Nyarugenge", "label": "Nyarugenge"}
      ]
    },
    {
      "province": "Northern Province",
      "districts": [
        {"value": "Burera", "label": "Burera"},
        {"value": "Gakenke", "label": "Gakenke"},
        // ... more districts
      ]
    }
    // ... more provinces
  ]
}
```

### 7. Get Gender Choices
**Endpoint:** `GET /api/players/form-data/genders/`
**Authentication:** Not required
**Description:** Get available gender options

#### Success Response (200 OK)
```json
{
  "genders": [
    {"value": "male", "label": "Male"},
    {"value": "female", "label": "Female"},
    {"value": "other", "label": "Other"},
    {"value": "prefer_not_to_say", "label": "Prefer not to say"}
  ]
}
```

## Field Requirements

### Required Fields for Registration
- `player_name`: Full name of the player
- `username`: Unique username (will be used for login)
- `phone`: Phone number (mandatory)
- `password`: Password (minimum 6 characters)
- `password_confirm`: Password confirmation (must match password)

### Optional Fields for Registration
- `email`: Email address (optional but recommended)
- `age_group`: Age group selection
- `gender`: Gender identity
- `province`: Province in Rwanda
- `district`: District in Rwanda (must be valid for the selected province)

## Province-District Validation

The API validates that the selected district belongs to the selected province. Valid combinations include:

- **Kigali City**: Gasabo, Kicukiro, Nyarugenge
- **Northern Province**: Burera, Gakenke, Gicumbi, Musanze, Rulindo
- **Southern Province**: Gisagara, Huye, Kamonyi, Muhanga, Nyamagabe, Nyanza, Nyaruguru, Ruhango
- **Eastern Province**: Bugesera, Gatsibo, Kayonza, Kirehe, Ngoma, Nyagatare, Rwamagana
- **Western Province**: Karongi, Ngororero, Nyabihu, Nyamasheke, Rubavu, Rusizi, Rutsiro

## Error Codes

- **200**: Success
- **201**: Created (successful registration)
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (invalid credentials or token)
- **500**: Internal Server Error

## Testing

✅ **API Status**: Fully tested and working!

**Recent Test Results (2025-08-31):**
- ✅ Registration: Successfully creates new players with all fields
- ✅ Login: Successfully authenticates existing players and updates last_login
- ✅ Last Login Tracking: Automatically updates timestamp on successful login
- ✅ Token Generation: UUID-based tokens working correctly
- ✅ Logout: Token validation working (client-side logout recommended)
- ✅ Profile: Returns complete player data including last_login
- ✅ Validation: Duplicate username/email detection working
- ✅ Error Handling: Proper error responses for validation failures
- ✅ CORS: Configured for React frontend integration

**Test Data Used:**
- Username: `testuser999`
- Password: `securepass123`
- Token: `51a39b79-eb27-408b-a864-be41a5a73075`
- Last Login: `2025-08-31T19:14:14.840030Z`

Use the provided test script to test all endpoints:

```bash
python3 test_player_registration_api.py
```

Make sure the Django development server is running:

```bash
python3 manage.py runserver
```

## React Frontend Integration

### Example React Registration Form

```javascript
const registerPlayer = async (formData) => {
  try {
    const response = await fetch('http://localhost:8000/api/players/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Store UUID token for future requests
      localStorage.setItem('authToken', data.token);
      console.log('Registration successful:', data);
      return { success: true, data };
    } else {
      return { success: false, errors: data.details };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

### Example Authenticated Request

```javascript
const getProfile = async () => {
  const token = localStorage.getItem('authToken');
  
  try {
    const response = await fetch('http://localhost:8000/api/players/profile/', {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    });
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

const loginPlayer = async (credentials) => {
  try {
    const response = await fetch('http://localhost:8000/api/players/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials)
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Store token and note the last_login timestamp
      localStorage.setItem('authToken', data.token);
      console.log('Login successful. Last login:', data.player.last_login);
      return { success: true, data };
    } else {
      return { success: false, error: data.error };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};

const logoutPlayer = async () => {
  const token = localStorage.getItem('authToken');
  
  try {
    const response = await fetch('http://localhost:8000/api/players/logout/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    });
    
    if (response.ok) {
      // Remove token from storage
      localStorage.removeItem('authToken');
      console.log('Logout successful');
      return { success: true };
    }
  } catch (error) {
    console.error('Logout error:', error);
  }
};
```
