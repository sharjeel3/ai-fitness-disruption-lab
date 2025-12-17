# Emotion-Aligned Training Model

**Experiment 3: Maps emotional state to ideal workout intensity & coaching tone**

## 🎯 Purpose

This prototype demonstrates how AI can create truly personalized fitness experiences by aligning workout recommendations with users' emotional states. Unlike traditional fitness apps that only consider physical metrics, this system factors in mood, energy, and stress levels to recommend workouts that meet users where they are emotionally and physically.

## 💡 The Insight

Current fitness apps like Centr, Sweat, and KIC treat users as purely physical beings. They ask "What muscles do you want to work?" but never "How are you feeling today?" 

This prototype shows that:
- A person feeling anxious needs grounding movement, not intensity
- Someone feeling frustrated benefits from cathartic, high-energy workouts
- Tired users need energizing (not depleting) movement

By mapping emotional states to appropriate workout types and coaching tones, we create a system that's adaptive, empathetic, and sustainable.

## 🚀 Features

- **Emotion-Based Matching**: 12 distinct emotional states mapped to optimal workout parameters
- **Dynamic Coaching Tones**: Adapts language style (grounding, motivating, compassionate, etc.)
- **AI Personalization**: Uses Gemini to generate personalized session introductions
- **Mobile-First UI**: iOS-inspired design with calming gradients
- **Real-Time Recommendations**: Instant workout suggestions based on current state

## 📊 How It Works

### Input
User provides three key metrics:
```json
{
  "mood": "anxious",      // One of 12 emotional states
  "energy": 3,            // Scale 1-10
  "stress": 7             // Scale 1-10
}
```

### Processing
1. System matches mood to emotion mapping database
2. Validates energy/stress levels against expected ranges
3. Selects appropriate workout types and intensity
4. Determines optimal coaching tone
5. Uses Gemini AI to generate personalized message

### Output
```json
{
  "recommended_session": "18-min calming yoga flow",
  "coaching_style": "grounding",
  "reason": "High stress + low energy = gentle movement to calm nervous system",
  "workout_types": ["yoga", "stretching", "walking", "breathwork"],
  "duration_range": [10, 20],
  "intensity": "low",
  "ai_message": "I can feel you're carrying a lot right now..."
}
```

## 🎨 Emotional States Supported

1. **Anxious** - Grounding, low-intensity movement
2. **Energetic** - High-intensity challenges
3. **Tired** - Gentle energizing movement
4. **Motivated** - Progressive strength training
5. **Frustrated** - Cathartic, empowering workouts
6. **Sad** - Mood-boosting light cardio
7. **Overwhelmed** - Calming breathwork & restoration
8. **Confident** - PR attempts & bold challenges
9. **Restless** - Channeling dynamic movement
10. **Content** - Balanced maintenance training
11. **Excited** - Fun, enthusiastic sessions
12. **Neutral** - Standard routine consistency

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- Google AI Studio API key ([Get it here](https://aistudio.google.com/apikey))

### Installation

1. **Navigate to the experiment directory:**
```bash
cd experiments/emotion-aligned-training
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root (or export variables):
```bash
export GEMINI_API_KEY="your-api-key-here"
export GEMINI_MODEL="gemini-2.0-flash-exp"  # Optional, defaults to this
```

### Running the Application

Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --port 8003
```

The application will be available at:
- **Home Page**: http://localhost:8003
- **Demo (Anxious Example)**: http://localhost:8003/demo
- **API Docs**: http://localhost:8003/docs

## 📱 Usage Examples

### Web Interface
1. Visit http://localhost:8003
2. Select your current mood from dropdown
3. Adjust energy and stress sliders
4. Click "Get My Workout"
5. View personalized recommendation

### API Usage

**Get Recommendation (Query Parameters):**
```bash
curl "http://localhost:8003/api/recommendation?mood=anxious&energy=3&stress=7"
```

**Response:**
```json
{
  "mood": "anxious",
  "energy": 3,
  "stress": 7,
  "recommended_session": "18-min calming yoga flow",
  "coaching_style": "grounding",
  "reason": "High stress + low energy = gentle movement to calm nervous system",
  "workout_types": ["yoga", "stretching", "walking", "breathwork"],
  "duration_range": [10, 20],
  "intensity": "low",
  "ai_message": "Given how you're feeling anxious today..."
}
```

## 🧪 Testing

The `test_data.json` file contains 12 test cases covering all emotional states. Use these to validate the system:

```bash
# Test with curl
curl -X POST "http://localhost:8003/generate" \
  -H "Content-Type: application/json" \
  -d '{"mood": "energetic", "energy": 9, "stress": 2}'
```

## 📂 Project Structure

```
emotion-aligned-training/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── test_data.json         # Test cases
├── README.md              # This file
├── templates/
│   ├── home.html          # Input form UI
│   └── emotion_card.html  # Recommendation display
└── outputs/               # Screenshots/demos (generated)
```

## 🎯 Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with emotion input form |
| `/demo` | GET | Pre-filled demo (anxious example) |
| `/generate` | POST | Generate recommendation (JSON input) |
| `/api/recommendation` | GET | API endpoint (query params) |

## 🌟 Competitive Advantages

**vs. Centr/Sweat/KIC:**
- ✅ Emotional intelligence (they have none)
- ✅ Adaptive to mental state, not just physical
- ✅ Prevents burnout through stress-aware programming
- ✅ Improves adherence by meeting users where they are
- ✅ Creates genuine connection through empathetic coaching

## 🔮 Future Enhancements

- [ ] Track emotional patterns over time
- [ ] Learn user's emotional-workout preferences
- [ ] Integrate with wearables for stress detection
- [ ] Add voice-based mood input
- [ ] Generate complete workout sequences (not just recommendations)
- [ ] Multi-language coaching tones
- [ ] Integration with calendar for stress prediction

## 📸 Screenshot Examples

**Input Screen:**
- Clean mobile UI with mood selector
- Visual sliders for energy/stress
- Real-time emoji updates

**Output Screen:**
- Personalized AI message
- Coaching tone with example phrases
- Session details with intensity badge
- "Why this works" explanation

## 🔐 Safety & Privacy

- No user data is stored (stateless prototype)
- API key required for Gemini integration
- All emotion mappings are evidence-based
- Coaching tones designed by fitness psychology principles

## 📄 License

Part of the AI Fitness Disruption Lab - See main repository LICENSE

## 🤝 Contributing

This is a prototype experiment. Feedback and improvements welcome!

---

**Built with:** FastAPI, Jinja2, Google Gemini AI
**Port:** 8003
**Status:** Prototype (MVP Complete)
