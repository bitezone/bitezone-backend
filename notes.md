## Designing the user checkout for calorie tracking
# 🍽️ User Meal Logging: Backend Structure

## 🧠 Goal
Allow users (authenticated via Google OAuth) to **log meals** with:
- Date
- Time (e.g., breakfast, lunch)
- Dining Hall Location
- Menu items + quantity

## 🗃️ Data Model (Normalized)

### 1. `MealSession`
Represents a **single meal event** (e.g., "Lunch at Lakeside on April 20").

| Field     | Type             | Description                      |
|-----------|------------------|----------------------------------|
| id        | Primary Key      | Unique ID for the session        |
| user_id   | ForeignKey(User) | Logged-in user                   |
| date      | Date             | Date of the meal                 |
| time      | String           | Meal type (breakfast, lunch...) |
| location  | String           | Dining hall location             |
| created_at| Timestamp        | When the log was created         |

### 2. `MealItemEntry`
Represents **each item** eaten in a session.

| Field        | Type                   | Description                       |
|--------------|------------------------|-----------------------------------|
| id           | Primary Key            | Unique log ID                     |
| session_id   | ForeignKey(MealSession)| Linked meal session               |
| menu_item_id | ForeignKey(MenuItem)   | Menu item eaten                   |
| quantity     | Integer                | How many servings were eaten      |

## ✅ Why This Structure?
- Groups data per **meal** not per item — avoids duplication
- Easy to **query** all items for a session or filter by date
- Scalable for **analytics**, meal summaries, calorie tracking
- Backend-friendly and **frontend-display-ready**

## 🔍 Example
> A user eats 2x Pancakes and 1x Eggs for **Breakfast on April 20 at Lakeside**:

### MealSession
```json
{
  "user_id": 3,
  "date": "2024-04-20",
  "time": "breakfast",
  "location": "Lakeside"
}
```

### MealItemEntry
```json
[
  { "session_id": 1, "menu_item_id": 10, "quantity": 2 },
  { "session_id": 1, "menu_item_id": 14, "quantity": 1 }
]
```

---

Let me know if you want to support additional features like:
- Editing meals
- Notes or tags
- Weekly or monthly summaries