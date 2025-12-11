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
├── experiments/
│   ├── dynamic-workout-writer/
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

# ⚙️ Technology Assumptions

* **LLM:** gemini-2.5-flash-lite via Google AI Studio
* **Backend:** Python + FastAPI
* **Data Storage:** Local JSON/SQLite only (prototypes)
* **Image Generation:** Gemini Image API or Python
* **Visual Output:** PNG/SVG/HTML for screenshots
* **UI:** Optional (you do *not* need to build a frontend)

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

