# 🧠 Cognitive Bias Antidote Engine

**Prototype Experiment 4 - AI Fitness Disruption Lab**

## Overview

The Cognitive Bias Antidote Engine detects cognitive distortions in fitness-related self-talk and provides evidence-based psychological reframes using Gemini LLM. This prototype demonstrates how AI can act as a personal psychology coach, identifying harmful thinking patterns and offering CBT-based interventions.

## The Problem

Most fitness apps ignore the psychological barriers that sabotage progress:
- **All-or-nothing thinking**: "I missed one workout, this whole week is ruined"
- **Catastrophizing**: "I'll never get fit"
- **Comparison trap**: "Everyone else is stronger than me"
- **Future discounting**: "I'll start tomorrow"
- **Impostor syndrome**: "I don't belong at the gym"
- **Perfectionism paralysis**: "I need the perfect setup to begin"

These cognitive biases cause people to quit before they see results.

## The Solution

This engine:
1. **Detects** cognitive biases in user thoughts using pattern matching + Gemini AI
2. **Explains** why the thought is distorted
3. **Reframes** the thought with evidence-based psychology
4. **Recommends** specific interventions (scaled workouts, micro-sessions, progress reminders)
5. **Provides** actionable next steps and affirmations

## Features

- 🔍 **8 Cognitive Bias Types** tracked (all-or-nothing, catastrophizing, comparison trap, future discounting, impostor syndrome, perfectionism paralysis, fixed mindset, emotional reasoning)
- 🤖 **Gemini-powered analysis** for personalized, context-aware reframes
- 💚 **Evidence-based coaching** using CBT principles
- 📊 **Confidence scoring** for detected biases
- 🎯 **Actionable interventions** with specific next steps
- 📱 **Beautiful iOS-style UI** for screenshot-ready output

## Technical Architecture

```
User Input (Thought + Context)
    ↓
Pattern Matching (cognitive-biases.json)
    ↓
Gemini Analysis (deep CBT reframe)
    ↓
Structured Response (bias type, reframe, intervention, next step)
    ↓
Visual Card Output (HTML template)
```

## Quick Start

### Prerequisites

- Python 3.10+
- Google AI Studio API key ([Get it here](https://aistudio.google.com/apikey))

### Installation

```bash
# Navigate to this experiment
cd experiments/cognitive-bias-antidote

# Install dependencies
pip install -r requirements.txt

# Set up your API key (from project root)
export GOOGLE_API_KEY="your-api-key-here"
```

### Run the Service

```bash
python main.py
```

The app will be available at: **http://localhost:8004**

## Usage

### Web Interface

1. Open http://localhost:8004 in your browser
2. Enter a negative fitness thought (e.g., "I missed my workout yesterday so this whole week is ruined")
3. Optionally add context (e.g., "Started a new program 2 weeks ago")
4. Click "Analyze My Thought"
5. Get a detailed bias analysis with reframes and action steps

### API Endpoints

#### `POST /analyze`

Analyze a thought and return JSON response.

**Request:**
```json
{
  "thought": "I missed one workout so this whole week is pointless",
  "context": "Started new program 2 weeks ago",
  "user_history": {
    "workouts_completed": 10,
    "current_streak": 0,
    "longest_streak": 7
  }
}
```

**Response:**
```json
{
  "original_thought": "I missed one workout so this whole week is pointless",
  "context": "Started new program 2 weeks ago",
  "primary_bias": {
    "bias_type": "all-or-nothing",
    "bias_description": "Viewing situations in extreme terms without recognizing middle ground",
    "confidence": 0.95,
    "detected_patterns": ["missed one workout", "whole week is pointless"],
    "reframe": "Missing one day doesn't erase your progress. One workout is better than none.",
    "intervention": "scaled_workout",
    "intervention_details": {
      "action": "Do a 10-minute workout today to rebuild momentum",
      "why": "Consistency matters more than perfection. Small actions break the all-or-nothing cycle."
    },
    "coaching_tone": "supportive_realistic",
    "actionable_next_step": "Put on your workout clothes right now and do just 5 minutes of movement",
    "affirmation": "Progress isn't perfect, and that's perfectly okay"
  },
  "secondary_biases": [],
  "overall_assessment": "This is classic all-or-nothing thinking. You've completed 10 workouts in 2 weeks - that's progress! One missed day doesn't erase that.",
  "recommended_action": "Do a shortened workout today to rebuild your momentum",
  "timestamp": "2025-12-18T10:30:45.123456"
}
```

#### `POST /analyze/visual`

Same as `/analyze` but returns an HTML card for visual display.

## Example Scenarios

### Scenario 1: All-or-Nothing Thinking
**Input:** "I ate dessert, my diet is ruined"  
**Output:**
- Bias: All-or-nothing thinking
- Reframe: "One meal doesn't define your nutrition. Get back on track with the next one."
- Intervention: Progress reminder
- Next step: "Plan your next healthy meal right now"

### Scenario 2: Comparison Trap
**Input:** "Everyone else can lift more than me"  
**Output:**
- Bias: Comparison trap
- Reframe: "Your only competition is who you were yesterday. Everyone has their own timeline."
- Intervention: Personal progress review
- Next step: "Look at your workout log from 1 month ago and compare to today"

### Scenario 3: Future Discounting
**Input:** "I'll start tomorrow"  
**Output:**
- Bias: Future discounting
- Reframe: "The best time was yesterday. The second best time is now. 10 minutes is enough."
- Intervention: Micro commitment
- Next step: "Set a 5-minute timer and do one exercise right now"

## Dataset Structure

Uses `datasets/cognitive-biases.json` which contains:
- 8 cognitive bias types
- Pattern examples for each
- Evidence-based reframes
- Intervention strategies
- Coaching tone guidelines

## Why This Matters

### Competitive Advantage Over Centr/Sweat/KIC

| Feature | Traditional Apps | This Prototype |
|---------|-----------------|----------------|
| Negative self-talk detection | ❌ | ✅ |
| CBT-based reframing | ❌ | ✅ |
| Context-aware psychology | ❌ | ✅ |
| Personalized interventions | ❌ | ✅ |
| Mental health integration | Basic tips | Deep AI coaching |

### Real-World Impact

- **Reduces quit rates** by addressing psychological barriers
- **Increases adherence** through cognitive reframing
- **Builds self-efficacy** with evidence-based affirmations
- **Prevents burnout** by catching perfectionism early
- **Promotes healthy mindset** around fitness

## Technology Stack

- **Backend:** FastAPI (Python 3.10+)
- **AI/LLM:** Gemini 2.0 Flash (via Google AI Studio)
- **Templates:** Jinja2
- **UI:** Pure HTML/CSS (iOS-inspired design)
- **Data:** JSON-based cognitive bias database

## Future Enhancements

- [ ] Track bias patterns over time
- [ ] Suggest therapist referral for severe patterns
- [ ] Integration with workout data for context
- [ ] Voice input for thoughts
- [ ] Daily check-in prompts
- [ ] Community success stories
- [ ] Bias trend analytics

## Safety Considerations

- **Not a replacement for therapy**: This is a coaching tool, not clinical treatment
- **Referral system**: Severe patterns should trigger professional help recommendations
- **Data privacy**: Thoughts are not stored (prototype mode)
- **Ethical AI**: Transparent about being AI-generated advice

## Screenshots

*Run the app and take screenshots of:*
- Home screen with thought input
- Bias analysis card showing primary bias
- Reframe and intervention display
- Secondary biases section

## License

MIT License - Part of AI Fitness Disruption Lab

## Author

Built with ❤️ as part of the AI Fitness Disruption Lab experiments.

---

**🎯 Goal:** Demonstrate that AI can provide psychological coaching that traditional fitness apps completely miss.
