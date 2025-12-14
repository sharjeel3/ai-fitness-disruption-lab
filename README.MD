# 🧪 AI Fitness Disruption Lab

### *Prototype Experiments to Challenge Centr, Sweat, and KIC Using Gemini LLM*

This repository contains a set of **isolated AI prototypes** that explore disruptive ideas in the fitness-app industry.
Each prototype demonstrates a capability that exposes weaknesses in current apps and showcases a future where adaptive, personalised, and emotionally intelligent fitness systems dominate.

Every experiment is designed to be:

* **Independent** (self-contained FastAPI service)
* **Visible** (produces a screenshot-ready visual output)
* **Safe** (follows fitness + AI boundaries)
* **Buildable** (Gemini-powered, minimal infrastructure)

---

# 📁 Repository Structure

```
/ai-fitness-disruption-lab
│
├── README.md
├── safety-guidelines.md
├── .env.example                # Template for API keys
├── .gitignore
├── requirements.txt            # Global dependencies
├── docker-compose.yml          # Optional: run all prototypes
│
├── datasets/                   # Shared seed/training data
│   ├── exercises.json
│   ├── nutrition.json
│   ├── personas.json
│   ├── cognitive-biases.json
│   └── narrative-templates.json
│
├── shared/                     # Common utilities
│   ├── __init__.py
│   ├── gemini_client.py
│   ├── image_generator.py
│   ├── validators.py
│   └── config.py
│
├── experiments/
│   ├── dynamic-workout-writer/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   ├── test_data.json
│   │   └── outputs/
│   ├── auto-progression-engine/
│   ├── emotion-aligned-training/
│   ├── cognitive-bias-antidote/
│   ├── calendar-adaptive-scheduler/
│   ├── fitness-persona-generator/
│   ├── micro-workout-splitter/
│   ├── nutrition-via-receipts/
│   ├── technique-feedback/
│   ├── rpg-narrative-training/
│   └── social-micro-battles/
│
└── api/
    ├── fastapi-server.py
    └── schemas/
```

---

# ⚙️ Technology Stack

* **LLM:** gemini-2.5-flash-lite via Google AI Studio
* **Backend:** Python 3.10+ with FastAPI
* **Data Storage:** Local JSON/SQLite only (prototypes)
* **Image Generation:** Gemini Image API or Python (matplotlib, Pillow)
* **Visual Output:** HTML templates with Jinja2 (mobile-first, app-like frames)
* **UI Framework:** Simple HTML/CSS (iOS-inspired cards, no JavaScript required)
* **Preview:** Browser-based (screenshot-ready)

---

# 🚀 Getting Started

## Prerequisites

* Python 3.10 or higher
* Google AI Studio API key ([Get it here](https://aistudio.google.com/apikey))
* Git
* (Optional) Docker & Docker Compose for containerized deployment

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sharjeel3/ai-fitness-disruption-lab.git
cd ai-fitness-disruption-lab
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
# Install global dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# GEMINI_API_KEY=your_api_key_here
```

### 5. Initialize Datasets

```bash
# Datasets are included in the repo
# Verify they exist in datasets/
ls datasets/
```

> **⚠️ Important:** Always activate the virtual environment before running any Python scripts or commands:
> ```bash
> source venv/bin/activate  # macOS/Linux
> venv\Scripts\activate     # Windows
> ```
> Your terminal prompt should show `(venv)` when activated.

## Running Individual Experiments

Each experiment is self-contained:

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Navigate to an experiment
cd experiments/dynamic-workout-writer

# Install experiment-specific dependencies (if any)
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload --port 8001

# Access at http://localhost:8001
# API docs at http://localhost:8001/docs
```

## Running Multiple Experiments (Docker)

```bash
# Build and start all services
docker-compose up --build

# Each experiment will run on a different port:
# Dynamic Workout Writer: http://localhost:8001
# Auto Progression Engine: http://localhost:8002
# etc.
```

## Project Configuration

### Port Allocation

| Experiment | Port |
|------------|------|
| Dynamic Workout Writer | 8001 |
| Auto Progression Engine | 8002 |
| Emotion-Aligned Training | 8003 |
| Cognitive Bias Antidote | 8004 |
| Calendar-Adaptive Scheduler | 8005 |
| Fitness Persona Generator | 8006 |
| Micro-Workout Splitter | 8007 |
| Nutrition via Receipts | 8008 |
| Technique Feedback | 8009 |
| RPG Narrative Training | 8010 |
| Social Micro Battles | 8011 |

### API Rate Limits

* Gemini API: Check current limits at [Google AI Studio](https://aistudio.google.com)
* Recommended: Implement basic rate limiting in production
* For prototypes: Sequential requests are fine

---

# 📱 Visual Output Strategy

## Philosophy: Browser-Based App Frames

Each prototype produces **user-facing HTML output** that renders as a mobile app mockup in the browser. No frontend framework needed—just clean HTML/CSS templates.

## Implementation Approach

### 1. FastAPI + Jinja2 Templates

Each experiment endpoint returns rendered HTML:

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/generate", response_class=HTMLResponse)
async def generate_workout(request: Request, data: WorkoutInput):
    # Process with Gemini LLM
    workout = await generate_adaptive_workout(data)
    
    # Render user-facing template
    return templates.TemplateResponse(
        "workout_card.html",
        {"request": request, "workout": workout}
    )
```

### 2. Mobile-First HTML Templates

Templates use iOS-inspired card design:

```html
<!-- templates/workout_card.html -->
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .phone-frame {
            width: 375px;
            background: white;
            border-radius: 40px;
            padding: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .card {
            background: #f8f9fa;
            border-radius: 16px;
            padding: 16px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="phone-frame">
        <h1>Today's Adaptive Workout</h1>
        {% for exercise in workout.exercises %}
        <div class="card">
            <h3>{{ exercise.name }}</h3>
            <p>{{ exercise.sets }} sets × {{ exercise.reps }} reps</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
```

### 3. Screenshot-Ready Output

**Access the rendered page:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux

# Start the experiment
uvicorn main:app --reload --port 8001

# POST your data to the endpoint
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"fitness_level": "intermediate", ...}'

# Open in browser: http://localhost:8001/generate
# Or visit a GET endpoint: http://localhost:8001/demo
```

**Take screenshots:**
- Browser dev tools: Device emulation (iPhone 14)
- CMD+Shift+4 (macOS) or Snipping Tool (Windows)
- Automated: Use Playwright/Puppeteer if needed

### 4. Shared Template Components

**Location:** `shared/templates/components/`

**Reusable elements:**
- `base.html` - Phone frame wrapper
- `exercise_card.html` - Exercise display component
- `chart_container.html` - For matplotlib charts
- `persona_card.html` - Persona display
- `chat_bubble.html` - Message displays

### 5. Visual Output Checklist

Every experiment must provide:

- ✅ Mobile phone frame (375px width)
- ✅ Clean, app-like styling
- ✅ User-readable content (not JSON dumps)
- ✅ Proper typography and spacing
- ✅ Screenshot-friendly colors
- ✅ Responsive to viewport

## Example: Emotion-Aligned Training Output

**User submits:** `{"mood": "anxious", "energy": 3, "stress": 7}`

**Browser displays:**
```
┌─────────────────────────┐
│  📱 iPhone Frame        │
│  ┌───────────────────┐  │
│  │ How You're Feeling│  │
│  │ 😰 Anxious        │  │
│  │ ⚡ Energy: 3/10   │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ Recommended       │  │
│  │ 18-min Calming    │  │
│  │ Yoga Flow         │  │
│  │                   │  │
│  │ 🧘 Grounding tone │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ Why This Works    │  │
│  │ High stress + low │  │
│  │ energy = gentle   │  │
│  │ movement focus    │  │
│  └───────────────────┘  │
└─────────────────────────┘
```

## Alternative: Static HTML Generation

For experiments without live interaction:

```python
# Run this script with venv activated: source venv/bin/activate

# Generate static HTML file
output_html = templates.get_template("workout_card.html").render(
    workout=workout_data
)

with open("outputs/workout_2024_12_15.html", "w") as f:
    f.write(output_html)

# Open directly in browser
import webbrowser
webbrowser.open("outputs/workout_2024_12_15.html")
```

## Color Schemes by Experiment

| Experiment | Primary Color | Use Case |
|------------|---------------|----------|
| Dynamic Workout Writer | `#667eea` (Purple) | Energy/Action |
| Auto Progression | `#4facfe` (Blue) | Analytics/Trust |
| Emotion-Aligned | `#43e97b` (Green) | Calm/Balance |
| Cognitive Bias | `#fa709a` (Pink) | Support/Care |
| Calendar Scheduler | `#ffd89b` (Orange) | Planning/Time |
| Persona Generator | `#ee0979` (Red-Pink) | Identity/Bold |
| Micro Splitter | `#a8edea` (Teal) | Flexibility |
| Nutrition | `#fbc2eb` (Purple-Pink) | Nourishment |
| Technique Feedback | `#fdcbf1` (Light Pink) | Guidance |
| RPG Narrative | `#0f2027` (Dark) | Adventure |
| Social Battles | `#f2994a` (Amber) | Competition |

---

# 📊 Dataset Requirements

Each dataset file provides seed data for AI-powered features. All files are in JSON format and stored in `datasets/`.

## 1. Exercise Library (`exercises.json`)

```json
{
  "exercises": [
    {
      "id": "squat_001",
      "name": "Goblet Squat",
      "category": "strength",
      "primary_muscles": ["quadriceps", "glutes"],
      "secondary_muscles": ["hamstrings", "core"],
      "equipment": ["dumbbell", "kettlebell"],
      "difficulty": "beginner",
      "progression_path": ["bodyweight_squat", "goblet_squat", "barbell_squat"],
      "default_sets": 3,
      "default_reps": "8-12",
      "common_issues": ["knees_caving", "forward_lean"]
    }
  ]
}
```

**Purpose:** Dynamic Workout Writer, Auto Progression Engine, Technique Feedback

## 2. Nutrition Database (`nutrition.json`)

```json
{
  "ingredients": [
    {
      "name": "chicken breast",
      "category": "protein",
      "per_100g": {
        "calories": 165,
        "protein": 31,
        "carbs": 0,
        "fat": 3.6
      },
      "recipes": ["protein_salad", "grilled_chicken"]
    }
  ],
  "recipes": [
    {
      "id": "protein_salad",
      "name": "Protein Chicken Salad",
      "ingredients": ["chicken breast", "spinach"],
      "prep_time": 12,
      "difficulty": "easy"
    }
  ]
}
```

**Purpose:** Nutrition via Receipts

## 3. Persona Templates (`personas.json`)

```json
{
  "archetypes": [
    {
      "name": "The Precision Phoenix",
      "traits": ["disciplined", "analytical"],
      "goals": ["lean", "strength"],
      "style": "controlled intensity",
      "tagline": "Rise. Refine. Repeat.",
      "color_palette": ["#FF6B35", "#FFD23F"],
      "music_preference": "instrumental"
    }
  ]
}
```

**Purpose:** Fitness Persona Generator

## 4. Cognitive Biases (`cognitive-biases.json`)

```json
{
  "biases": [
    {
      "type": "all-or-nothing",
      "patterns": [
        "I missed one workout so this whole week is pointless",
        "If I can't do the full workout, why bother"
      ],
      "reframes": [
        "Missing one day doesn't erase your progress. One workout is better than none.",
        "Consistency over perfection. Let's find what you CAN do today."
      ],
      "interventions": ["scaled_workout", "micro_session"]
    }
  ]
}
```

**Purpose:** Cognitive Bias Antidote Engine

## 5. Narrative Templates (`narrative-templates.json`)

```json
{
  "worlds": [
    {
      "theme": "cyberpunk",
      "chapters": [
        {
          "id": 1,
          "story": "You infiltrate the neon compound. Security drones patrol above.",
          "mission_type": "strength",
          "workout_duration": 15
        }
      ]
    }
  ]
}
```

**Purpose:** RPG Narrative Training Engine

## 6. Emotion-Workout Mapping (`emotion-mapping.json`)

```json
{
  "mappings": [
    {
      "mood": "anxious",
      "energy_range": [1, 4],
      "stress_range": [6, 10],
      "recommended_intensity": "low",
      "workout_types": ["yoga", "stretching", "walking"],
      "coaching_tone": "grounding",
      "duration": [10, 20]
    }
  ]
}
```

**Purpose:** Emotion-Aligned Training Model

---

# 🧯 Global Safety Guidelines

### 1. Not Medical Advice

Prototypes must avoid:

* diagnosing
* prescribing
* providing medical-grade instructions

Outputs must remain general and beginner-safe.

### 2. Healthy Behaviour Boundaries

If user requests extreme goals → respond with safer pacing guidance.

### 3. Conservative Technique Guidance

Never:

* advise maximal loading
* give advanced corrective cues
* attempt remote clinical assessment

### 4. Emotional Safety

AI must not:

* analyse trauma
* act as therapist
* diagnose mental health conditions

### 5. Data Minimisation

Store no user health or personal info unless explicitly required for testing.

---

# 🧪 Experiment Catalogue with Visual Output Specifications

Each prototype includes:

* Purpose
* Inputs
* Outputs
* **Visual Output** (core requirement for screenshots)
* Whether chat interface is required

---

# 1. **Dynamic Workout Writer (DW²)**

AI generates a unique workout based on daily conditions.

## Inputs

```json
{
  "fitness_level": "intermediate",
  "goals": ["strength"],
  "time_available": 30,
  "equipment": ["dumbbells"],
  "fatigue": 3,
  "stress": 2,
  "sleep_hours": 6
}
```

## Outputs

```json
{
  "workout": [
    { "exercise": "Goblet Squat", "sets": 3, "reps": "12" },
    { "exercise": "Push-up", "sets": 3, "reps": "8-12" }
  ],
  "rationale": "Moderate fatigue → moderate volume focus"
}
```

## **Visual Output** (Screenshot Target)

A mock mobile UI screen that shows:

* “Today’s Adaptive Workout”
* Exercise cards with icons
* Duration and intensity badges

### Generate via Gemini Image Prompt:

> “Create a clean iOS-style fitness app UI showing an adaptive workout with exercise cards (Goblet Squat, Push-ups). Minimalist design, white background, soft shadows.”

---

# 2. **Auto-Progression Engine**

Learns from performance data to recommend progression.

## Inputs

```json
{
 "history": [
   { "exercise": "squat", "weight": 40, "reps": 10, "rpe": 7 },
   { "exercise": "squat", "weight": 42.5, "reps": 10, "rpe": 8 }
 ]
}
```

## Outputs

```json
{
 "next_session_recommendations": {
   "squat_weight": 45,
   "target_rpe": 7
 }
}
```

## **Visual Output**

A simple dashboard containing:

* A line chart showing weight progression
* A summary card showing recommended next load
* A rationale box

### Generate via Python (matplotlib) or Gemini Image:

> “Generate a fitness analytics dashboard UI with a squat progression line chart and a recommendation card.”

---

# 3. **Emotion-Aligned Training Model**

Maps emotional state → ideal workout intensity & coaching tone.

## Inputs

```json
{
  "mood": "anxious",
  "energy": 3,
  "stress": 7
}
```

## Outputs

```json
{
  "recommended_session": "18-min calming yoga flow",
  "coaching_style": "grounding",
  "reason": "High stress + low energy"
}
```

## **Visual Output**

A UI card displaying:

* Mood
* Recommended session
* Tone description
* Simple calming colors

### Gemini Prompt:

> “Create a calming fitness app screen showing mood-based session recommendation with soft colors and clean layout.”

**Chat interface recommended**
(for input collection & emotional conversation).

---

# 4. **Cognitive Bias Antidote Engine**

Detects mindset traps and gives micro-interventions.

## Inputs

User journal:

> “I missed one workout so this whole week is pointless.”

## Outputs

```json
{
 "bias_detected": "all-or-nothing",
 "reframe": "Missing one day doesn’t break progress...",
 "scaled_workout": {...}
}
```

## **Visual Output**

A chat interface showing:

* User message
* AI reframe
* Updated scaled workout

### Gemini Prompt:

> “Create a minimalist chat UI layout showing a user message expressing frustration and an AI response offering a healthy reframe.”

**Chat interface required**

---

# 5. **Calendar-Adaptive Scheduler**

## Inputs

```json
{
  "events": [
    { "title": "Meeting", "start": "08:00", "end": "09:00" },
    { "title": "Dinner", "start": "18:30", "end": "20:00" }
  ]
}
```

## Outputs

```json
{
 "schedule": [
   { "day": "Tuesday", "workout": "12-minute HIIT at 7:15am" }
 ]
}
```

## **Visual Output**

A weekly calendar UI with:

* Time blocks
* Auto-inserted workout sessions

### Gemini Prompt:

> “Generate a modern weekly calendar UI with a workout scheduled in a free morning time slot.”

---

# 6. **Fitness Persona Generator**

Creates a sharable identity card.

## Inputs

```json
{
 "traits": ["disciplined", "creative"],
 "goals": ["lean"],
 "music_preference": "pop"
}
```

## Outputs

```json
{
 "persona_name": "The Precision Phoenix",
 "style": "controlled intensity",
 "tagline": "Rise. Refine. Repeat."
}
```

## **Visual Output**

A stylised persona poster containing:

* Persona name
* Icon/illustration
* Traits
* Tagline

### Gemini Prompt:

> “Design a stylized fitness persona card for ‘The Precision Phoenix’ using a red-gold palette and clean typography.”

---

# 7. **Micro-Workout Splitter**

Breaks long workouts into small achievable chunks.

## Inputs

```json
{
 "full_workout": [...],
 "available_blocks": [8, 10, 6]
}
```

## Outputs

```json
{
 "segments": [
   { "duration": 8, "focus": "mobility" },
   { "duration": 10, "focus": "strength" }
 ]
}
```

## **Visual Output**

A timeline bar graphic:

* Segment blocks (8m, 10m, 6m)
* Color-coded based on focus area

### Gemini Prompt:

> “Create a simple timeline bar UI showing three color-coded workout segments with durations.”

---

# 8. **Nutrition via Receipts**

## Inputs

```json
{
 "items": [
   { "name": "spinach", "quantity": "250g" },
   { "name": "chicken breast", "quantity": "500g" }
 ]
}
```

## Outputs

```json
{
 "recipes": [
   { "name": "Protein Chicken Salad", "prep_time": 12 }
 ]
}
```

## **Visual Output**

Recipe cards showing:

* Photo
* Ingredients used
* Prep time

### Gemini Prompt:

> “Create a recipe card UI showing meals created from spinach and chicken breast.”

---

# 9. **Technique Feedback**

## Inputs

```json
{
 "issue_description": "My knees hurt during squats."
}
```

## Outputs

```json
{
 "possible_cause": "Knees collapsing inward",
 "safe_suggestions": [...]
}
```

## **Visual Output**

A diagnostic card:

* Title: “Squat Issue Detected”
* Probable cause
* Conservative suggestions

### Gemini Prompt:

> “Generate a fitness help card showing common squat problems with safe corrective advice.”

---

# 10. **RPG Narrative Training Engine**

## Inputs

```json
{
 "world": "cyberpunk",
 "progress": 3
}
```

## Outputs

```json
{
 "chapter": "You infiltrate the neon compound...",
 "next_workout_mission": "Complete 15-min strength circuit"
}
```

## **Visual Output**

A mission screen:

* Short story paragraph
* Workout as mission objective

### Gemini Prompt:

> “Create a cyberpunk mission UI with neon accents and a workout objective.”

---

# 11. **Social Micro Battles**

## Inputs

```json
{
 "user_profile": {
   "steps_today": 3200,
   "strength_level": "intermediate"
 }
}
```

## Outputs

```json
{
 "challenge": "Hit 6000 steps by 3pm."
}
```

## **Visual Output**

A challenge card:

* Challenge description
* Countdown timer
* Placeholder leaderboard

### Gemini Prompt:

> “Generate a challenge card UI showing a daily micro-battle such as hitting a step target.”

---

# 🎯 Final Note on Prototype Presentation

Each experiment must produce:

### 1. Input field (JSON or chat)

2. Processed output (JSON)
3. Visual output (PNG/SVG/UI mock)

The *visual* is what sells the idea as disruptive — not the backend code.

