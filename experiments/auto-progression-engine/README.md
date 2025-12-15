# Auto-Progression Engine (APE)

AI-powered workout progression tracker that analyzes your training history and provides intelligent recommendations for your next session.

## Features

- 📊 **Smart Progression Analysis**: Uses Gemini LLM to analyze workout patterns and trends
- 🎯 **Goal-Specific Recommendations**: Tailored advice for strength, hypertrophy, or endurance goals
- 📈 **Visual Progress Tracking**: Clean dashboard showing weight progression and performance metrics
- ⚠️ **Deload Detection**: Automatically identifies when you need recovery
- 💡 **Coaching Tips**: Personalized guidance based on your training history
- 📱 **Mobile-First UI**: Beautiful iOS-inspired interface

## Quick Start

### Prerequisites

1. Python 3.10 or higher
2. Google AI Studio API key ([Get it here](https://aistudio.google.com/apikey))
3. Completed setup from main repository

### Installation

```bash
# 1. Ensure you're in the project root and virtual environment is activated
cd /Users/sharjeel/dev/ai-fitness-disruption-lab
source venv/bin/activate  # macOS/Linux

# 2. Verify environment variables are set
# Make sure .env file contains your GEMINI_API_KEY

# 3. Navigate to the experiment
cd experiments/auto-progression-engine

# 4. Run the server
uvicorn main:app --reload --port 8002
```

### Access the Application

- **Web Interface**: http://localhost:8002
- **Demo Analysis**: http://localhost:8002/demo
- **API Documentation**: http://localhost:8002/docs
- **Health Check**: http://localhost:8002/health

## How It Works

### 1. Input Your Workout History

Log at least 2 workout sessions for a specific exercise:
- Exercise name
- Weight used
- Sets and reps
- RPE (Rate of Perceived Exertion, 1-10 scale)
- Date
- Optional notes

### 2. AI Analysis

The Gemini LLM analyzes your data to:
- Identify progression patterns
- Evaluate fatigue management (RPE trends)
- Assess readiness for increased load
- Detect potential overtraining
- Consider your specific training goal

### 3. Get Recommendations

Receive personalized guidance including:
- Recommended weight for next session
- Target sets, reps, and RPE
- Progression rate (conservative/moderate/aggressive)
- Rationale explaining the recommendation
- Deload alerts if needed
- Specific coaching tips

## API Endpoints

### `GET /`
Home page with workout logging form

### `GET /demo`
Pre-filled demo with 5 workout sessions showing steady progression

### `POST /analyze`
Analyze workout progression (returns HTML)

**Request Body:**
```json
{
  "exercise": "Barbell Squat",
  "goal": "strength",
  "history": [
    {
      "exercise": "Barbell Squat",
      "weight": 60,
      "sets": 3,
      "reps": 5,
      "rpe": 7,
      "date": "2024-12-01",
      "notes": "Felt strong"
    },
    {
      "exercise": "Barbell Squat",
      "weight": 62.5,
      "sets": 3,
      "reps": 5,
      "rpe": 7,
      "date": "2024-12-04",
      "notes": "Good form"
    }
  ]
}
```

### `POST /analyze-json`
Analyze workout progression (returns JSON)

Same request body as `/analyze`, but returns structured JSON instead of HTML.

## Training Goals Explained

### Strength
- **Rep Range**: 3-6 reps
- **Focus**: Progressive overload with heavier weights
- **Progression**: Add weight when RPE < 8 for all sets
- **Rest**: 3-5 minutes between sets

### Hypertrophy (Muscle Growth)
- **Rep Range**: 8-12 reps
- **Focus**: Volume (total weight × reps × sets)
- **Progression**: Increase volume by 5-10% weekly
- **Rest**: 60-90 seconds between sets

### Endurance
- **Rep Range**: 15+ reps
- **Focus**: Work capacity and stamina
- **Progression**: Add reps first, then increase weight
- **Rest**: 30-60 seconds between sets

## Understanding RPE (Rate of Perceived Exertion)

RPE is a 1-10 scale measuring how hard an exercise feels:

- **1-3**: Very easy, could do many more reps
- **4-6**: Moderate effort, still comfortable
- **7**: Challenging, could do 3-4 more reps
- **8**: Hard, could do 2-3 more reps
- **9**: Very hard, could do 1-2 more reps
- **10**: Maximum effort, couldn't do another rep

**Ideal training RPE**: 7-8 for most sessions

## Progression Safety Rules

The AI follows these safety principles:

1. **Conservative Increments**: Never recommends more than 5% weight increase per session
2. **Fatigue Monitoring**: If last RPE was 9-10, recommends maintaining or reducing load
3. **Performance Tracking**: If performance declined, recommends maintaining or reducing load
4. **Sustainable Progress**: Prioritizes long-term gains over aggressive short-term increases

## Deload Detection

A deload (recovery week) is suggested when:
- RPE consistently 9-10 across multiple sessions
- Performance declining despite adequate recovery
- Failed to complete target reps for 2+ sessions
- Average RPE trending upward over 3+ weeks

**Typical deload**: Reduce weight by 10-20% while maintaining technique

## Test Scenarios

The `test_data.json` file includes 6 test scenarios:

1. **Steady Progression**: Normal strength gains
2. **High Fatigue**: Overtraining indicators, deload needed
3. **Hypertrophy Focus**: Volume-based progression
4. **Endurance Goal**: High-rep training
5. **Stalled Progress**: Plateau requiring strategy change
6. **Beginner Gains**: Rapid early progression

## Example Usage

### Using the Web Interface

1. Open http://localhost:8002
2. Enter exercise name and select your goal
3. Add at least 2 workout sessions with details
4. Click "Analyze Progression"
5. View your personalized dashboard

### Using cURL

```bash
curl -X POST http://localhost:8002/analyze-json \
  -H "Content-Type: application/json" \
  -d '{
    "exercise": "Barbell Squat",
    "goal": "strength",
    "history": [
      {
        "exercise": "Barbell Squat",
        "weight": 60,
        "sets": 3,
        "reps": 5,
        "rpe": 7,
        "date": "2024-12-01"
      },
      {
        "exercise": "Barbell Squat",
        "weight": 62.5,
        "sets": 3,
        "reps": 5,
        "rpe": 7,
        "date": "2024-12-04"
      }
    ]
  }'
```

### Using Python

```python
import requests

data = {
    "exercise": "Bench Press",
    "goal": "hypertrophy",
    "history": [
        {"exercise": "Bench Press", "weight": 70, "sets": 3, "reps": 10, "rpe": 7, "date": "2024-12-01"},
        {"exercise": "Bench Press", "weight": 72.5, "sets": 3, "reps": 10, "rpe": 7, "date": "2024-12-05"},
        {"exercise": "Bench Press", "weight": 75, "sets": 3, "reps": 9, "rpe": 8, "date": "2024-12-09"}
    ]
}

response = requests.post("http://localhost:8002/analyze-json", json=data)
print(response.json())
```

## Visual Output

The progression dashboard displays:

### Performance Metrics
- Current weight, volume, sets × reps
- Last session RPE
- Overall progression trend

### Interactive Chart
- Weight progression over time
- Visual trend indicators (📈 up, 📉 down, ➡️ maintaining)

### Next Session Card
- Recommended weight, sets, reps
- Target RPE
- Progression rate badge

### Rationale Box
- Explanation of why this progression is appropriate
- Considers current performance, fatigue, and goal

### Coaching Tips
- 2-3 specific actionable tips
- Based on your unique progression pattern

### Recent History
- Last 5 workout sessions
- Dates, weights, RPE, and notes

## Troubleshooting

### "GEMINI_API_KEY not found" error
Ensure `.env` file exists in project root with your API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

### Import errors
Make sure you're in the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port already in use
Change the port in the uvicorn command:
```bash
uvicorn main:app --reload --port 8003
```

### No progression recommendation showing
- Ensure you have at least 2 workout entries
- Check that all required fields are filled
- Verify dates are in YYYY-MM-DD format
- Check browser console for errors

## Advanced Features (Future)

Potential enhancements:
- Integration with `datasets/exercises.json` for exercise library
- Multi-exercise tracking (full workout analysis)
- Long-term progression visualization (12+ weeks)
- Export workout logs to CSV/PDF
- Integration with Calendar-Adaptive Scheduler
- Social sharing of progression achievements
- One-rep max (1RM) estimation

## Technical Details

### Data Flow

1. User submits workout history via web form
2. FastAPI validates input using Pydantic models
3. Data sent to Gemini LLM with structured prompt
4. AI analyzes patterns and generates recommendations
5. Response parsed and validated
6. HTML dashboard rendered with Jinja2 templates
7. User views mobile-optimized progression analysis

### AI Prompt Engineering

The system uses a carefully crafted prompt that:
- Provides clear context (exercise, goal, history)
- Calculates basic stats (weight increase, average RPE)
- Gives specific instructions based on training goal
- Enforces safety rules
- Requests structured JSON output
- Includes fallback logic for parsing errors

## License

Part of the AI Fitness Disruption Lab project.

## Contributing

See main repository README for contribution guidelines.

## Support

For issues or questions:
1. Check this README
2. Review test scenarios in `test_data.json`
3. Check API docs at http://localhost:8002/docs
4. Review main project README
