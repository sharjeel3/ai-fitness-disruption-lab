# Dynamic Workout Writer (DW²)

AI-powered adaptive workout generator that creates personalized workouts based on your daily condition.

## Features

- 🎯 **Adaptive AI**: Uses Gemini LLM to generate workouts tailored to your current state
- 📊 **Daily Condition Analysis**: Considers fatigue, stress, and sleep quality
- 🏋️ **Multiple Fitness Levels**: Supports beginner, intermediate, and advanced
- ⏱️ **Flexible Duration**: Workouts from 5 to 120 minutes
- 🛠️ **Equipment Flexibility**: Works with bodyweight, dumbbells, barbells, and more
- 📱 **Mobile-First UI**: Beautiful iOS-inspired interface

## Quick Start

### Prerequisites

1. Python 3.10 or higher
2. Google AI Studio API key ([Get it here](https://aistudio.google.com/apikey))

### Installation

```bash
# 1. Navigate to the project root
cd /Users/sharjeel/dev/ai-fitness-disruption-lab

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Navigate to the experiment
cd experiments/dynamic-workout-writer

# 6. Run the server
uvicorn main:app --reload --port 8001
```

### Access the Application

- **Web Interface**: http://localhost:8001
- **Demo Workout**: http://localhost:8001/demo
- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

## API Endpoints

### `GET /`
Home page with workout generation form

### `GET /demo`
Pre-filled demo workout example

### `POST /generate`
Generate adaptive workout (returns HTML)

**Request Body:**
```json
{
  "fitness_level": "intermediate",
  "goals": ["strength", "cardio"],
  "time_available": 30,
  "equipment": ["dumbbells", "bodyweight"],
  "fatigue": 3,
  "stress": 2,
  "sleep_hours": 7
}
```

### `POST /generate-json`
Generate adaptive workout (returns JSON)

Same request body as `/generate`, but returns structured JSON instead of HTML.

## How It Works

1. **User Input**: Collects current fitness level, goals, available time, equipment, and daily condition (fatigue, stress, sleep)
2. **AI Processing**: Gemini LLM analyzes the inputs and generates an optimized workout plan
3. **Adaptation**: The AI adjusts intensity and volume based on recovery indicators
4. **Presentation**: Delivers a mobile-friendly workout card with exercise details

## Example Usage

### Using the Web Interface

1. Open http://localhost:8001
2. Fill in your details
3. Click "Generate Workout"
4. View your personalized workout card

### Using cURL

```bash
curl -X POST http://localhost:8001/generate-json \
  -H "Content-Type: application/json" \
  -d '{
    "fitness_level": "intermediate",
    "goals": ["strength"],
    "time_available": 30,
    "equipment": ["dumbbells"],
    "fatigue": 3,
    "stress": 2,
    "sleep_hours": 7
  }'
```

## Test Scenarios

Test data is available in `test_data.json`:

- **Beginner Low Energy**: Low-intensity recovery workout
- **Intermediate Fresh Morning**: Moderate to high intensity
- **Advanced High Stress**: Stress-relief elements included
- **Quick Mobility Session**: Focused stretching routine
- **Full Equipment Available**: Utilizes variety of equipment

## Visual Output

The workout is displayed as a mobile-first UI with:

- Status bar showing duration, exercise count, and level
- Intensity badge
- Rationale explaining why this workout suits your condition
- Exercise cards with sets, reps, rest periods, and form cues

## Safety Features

- Automatically reduces volume when fatigue is high (>7)
- Focuses on mobility/light activity when sleep is poor (<5 hours)
- Includes calming elements when stress is high (>8)
- Never prescribes maximal loads for beginners
- Respects time constraints (5-120 minutes)

## Troubleshooting

### "GEMINI_API_KEY not found" error
Make sure you've created a `.env` file in the project root with your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

### Import errors
Ensure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port already in use
Change the port in the uvicorn command:
```bash
uvicorn main:app --reload --port 8002
```

## Next Steps

- Add exercise database integration from `datasets/exercises.json`
- Implement workout history tracking
- Add progression tracking between sessions
- Create printable workout PDFs
- Add exercise video demonstrations

## License

Part of the AI Fitness Disruption Lab project.
