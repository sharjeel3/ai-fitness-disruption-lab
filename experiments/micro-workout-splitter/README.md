# 🎯 Micro-Workout Splitter

**Break long workouts into micro-blocks that fit into fragmented schedules.**

## Problem Statement

Traditional fitness apps assume you have 45-60 minutes of uninterrupted time. But real life looks like:
- Busy parents with 10-minute windows
- Office workers between meetings
- Shift workers with irregular schedules

This prototype uses **Gemini AI** to intelligently split a full workout into smaller, achievable time blocks while:
- ✅ Maintaining workout logic (warm-up → strength → cool-down)
- ✅ Prioritizing high-value exercises
- ✅ Grouping by movement patterns
- ✅ Suggesting optimal timing for each segment

---

## Features

### 🧠 AI-Powered Splitting
- Analyzes workout structure and available time blocks
- Intelligently groups exercises by category and intensity
- Maintains proper progression and recovery

### 📊 Visual Timeline
- Color-coded segments by workout type
- Duration badges for each block
- Suggested timing (morning, lunch, evening)

### 🎯 Smart Prioritization
- High-priority exercises included first
- Essential mobility and warm-up preserved
- Flexible with lower-priority exercises

### 💡 Contextual Insights
- Explains splitting strategy
- Shows coverage percentage
- Provides rationale for each segment

---

## Technology Stack

- **Backend:** FastAPI (Python 3.10+)
- **AI Engine:** Gemini 2.0 Flash Exp
- **Templates:** Jinja2
- **Styling:** Pure CSS (iOS-inspired mobile UI)
- **Port:** 8007

---

## Installation

### 1. Navigate to experiment directory

```bash
cd experiments/micro-workout-splitter
```

### 2. Activate virtual environment

```bash
# From project root
source ../../venv/bin/activate  # macOS/Linux
# or
..\..\venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Make sure your `.env` file in the project root contains:

```bash
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

### Start the server

```bash
uvicorn main:app --reload --port 8007
```

### Access the UI

**Home Page (Input Form):**
```
http://localhost:8007
```

**Quick Demo:**
```
http://localhost:8007/demo
```

**API Docs:**
```
http://localhost:8007/docs
```

---

## API Endpoints

### `GET /`
Home page with input form for workout splitting.

### `POST /split`
Main endpoint to split a workout.

**Request Body:**
```json
{
  "workout": {
    "name": "Full Body Strength",
    "total_duration": 45,
    "exercises": [
      {
        "name": "Goblet Squats",
        "duration": 7,
        "category": "strength",
        "priority": "high",
        "sets": 3,
        "reps": "12",
        "rest": 60
      }
    ]
  },
  "available_blocks": [10, 8, 12, 6],
  "scenario": "Busy parent with 3 kids"
}
```

**Response:**
Returns HTML page with split workout visualization.

### `GET /demo`
Pre-loaded demo with sample workout and time blocks.

### `GET /health`
Health check endpoint.

---

## Test Data

The `test_data.json` file includes:

### Sample Workout
- **Full Body Strength** (45 minutes)
- 7 exercises covering mobility, strength, and core
- Includes sets, reps, rest periods

### Sample Scenarios
1. **Busy parent with 3 kids:** [10, 8, 12, 6] minutes
2. **Office worker with meetings:** [15, 10, 8] minutes
3. **Shift worker with irregular schedule:** [20, 5, 8, 7] minutes

---

## How It Works

### 1. User Input
- Selects a workout template
- Enters available time blocks
- Optionally provides schedule context

### 2. AI Processing
Gemini analyzes:
- Exercise priorities
- Movement patterns
- Category distribution
- Time constraints

### 3. Intelligent Splitting
AI creates segments that:
- Fit within time blocks
- Group related exercises
- Maintain workout logic
- Maximize coverage

### 4. Visual Output
Mobile-friendly UI displays:
- Timeline with color-coded segments
- Exercise details for each block
- Suggested timing
- AI rationale

---

## Visual Output Examples

### Input
- Workout: Full Body Strength (45 min)
- Available: [10, 8, 12, 6] minutes
- Context: Busy parent

### Output
```
┌──────────────────────────┐
│ Segment 1 (10 min)       │
│ Morning - 7am            │
│ Focus: Warm-up + Mobility│
│ • Dynamic Stretches (5m) │
│ • Goblet Squats (7m)     │
└──────────────────────────┘

┌──────────────────────────┐
│ Segment 2 (8 min)        │
│ Lunch break              │
│ Focus: Upper Body        │
│ • Push-ups (6m)          │
│ • Plank Hold (4m)        │
└──────────────────────────┘
```

---

## Color Coding

| Category | Color | Hex |
|----------|-------|-----|
| Mobility | Teal | `#a8edea` |
| Strength | Purple | `#667eea` |
| Cardio | Pink | `#fa709a` |
| Core | Green | `#43e97b` |

---

## Customization

### Adding New Workouts

Edit `test_data.json` and add to `sample_workouts`:

```json
{
  "name": "HIIT Circuit",
  "total_duration": 30,
  "exercises": [
    {
      "name": "Burpees",
      "duration": 5,
      "category": "cardio",
      "priority": "high",
      "sets": 3,
      "reps": "10"
    }
  ]
}
```

### Modifying AI Behavior

Edit the `build_split_prompt()` function in `main.py` to adjust:
- Splitting rules
- Priority logic
- Timing suggestions

### Styling

Modify `templates/home.html` and `templates/workout_splitter.html` for:
- Color schemes
- Layout changes
- Additional UI elements

---

## Safety & Limitations

### ✅ Safe Features
- Conservative time recommendations
- Maintains warm-up/cool-down priorities
- Respects exercise priorities

### ⚠️ Limitations
- Not medical advice
- Assumes user knows exercise form
- Cannot replace professional coaching
- AI suggestions should be validated

### 🛡️ Built-in Safety
- Never suggests skipping warm-ups
- Preserves high-priority exercises
- Conservative time allocations

---

## Troubleshooting

### API Key Issues
```bash
# Verify API key is set
echo $GEMINI_API_KEY

# Or check .env file
cat ../../.env
```

### Port Already in Use
```bash
# Use different port
uvicorn main:app --reload --port 8008
```

### Module Import Errors
```bash
# Ensure virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Output Storage

Generated splits are saved in `outputs/` directory:
```
outputs/
  split_20241222_143045.json
  split_20241222_150230.json
```

Each file contains:
- Original workout details
- Generated segments
- AI insights
- Timestamp

---

## Screenshots

To capture the output:

1. Run the demo: `http://localhost:8007/demo`
2. Use browser dev tools: Device emulation → iPhone 14
3. Take screenshot (CMD+Shift+4 on macOS)

---

## Future Enhancements

- [ ] Calendar integration
- [ ] Progress tracking across segments
- [ ] Adaptive rescheduling
- [ ] Wearable sync for completion tracking
- [ ] Social sharing of split strategies
- [ ] Video demos for each segment

---

## Contributing

This is a prototype experiment. To extend:

1. Fork the repository
2. Add features in separate branches
3. Test with various workout types
4. Submit PRs with clear documentation

---

## License

Part of AI Fitness Disruption Lab project.
See main repository LICENSE file.

---

## Contact & Support

For issues or questions:
- Open an issue in the main repository
- Check other experiments for similar patterns
- Review shared utilities in `/shared`

---

**Built with ❤️ using Gemini AI**
