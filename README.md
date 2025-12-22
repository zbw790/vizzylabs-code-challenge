# Vizzy Labs Coding Challenges

Welcome to Vizzy Labs' technical interview coding challenges! This repository contains two distinct challenges designed to evaluate candidates for different engineering positions.

---

## 📁 Repository Structure

```
vizzylabs-code-challenge/
├── ai-automation-challenge/          # AI Automation Engineer Challenge
│   ├── README.md                     # Candidate instructions
│   ├── SOLUTION_REFERENCE.md         # Evaluator solutions (private)
│   ├── models.py                     # Has validation bugs
│   ├── moderation_service.py         # Incomplete + bugs
│   ├── main.py                       # Incomplete
│   ├── mock_clients.py               # Working mock API clients
│   └── requirements.txt
│
├── mobile-backend-challenge/         # Mobile Backend Engineer Challenge
│   ├── README.md                     # Candidate instructions
│   ├── SOLUTION_REFERENCE.md         # Evaluator solutions (private)
│   ├── main.py                       # Complete FastAPI app
│   ├── database.py                   # Complete DB setup
│   ├── models.py                     # Complete SQLAlchemy models
│   ├── schemas.py                    # Incomplete Pydantic schemas
│   ├── seed_data.py                  # Database seeding script
│   ├── routes/
│   │   ├── creators.py              # Has bugs
│   │   └── analytics.py             # Incomplete stub
│   ├── services/
│   │   ├── creator_service.py       # Has N+1 bug
│   │   └── analytics_service.py     # Stub only
│   └── requirements.txt
│
├── INTERVIEWER_SCORING_SHEET.md      # Evaluation rubric for interviewers
└── README.md                          # This file
```

---

## 🎯 Challenge Overview

### 1. AI Automation Engineer Challenge

**Time:** 10-15 minutes
**Difficulty:** Intermediate
**Focus Areas:** AI coding, prompting, debugging, multi-tasking

**Scenario:** Build a content moderation service with OpenAI primary and Anthropic Claude fallback.

**Tasks:**
- Fix Pydantic validation bugs
- Fix OpenAI integration issues
- Implement Anthropic fallback with prompt engineering
- Implement timeout and error handling
- Fix FastAPI initialization

**Key Skills Tested:**
- Using AI assistants effectively
- Crafting prompts for structured LLM output
- Debugging validation and integration issues
- Async Python and error handling
- Service layer architecture

[📖 View Challenge Details](./ai-automation-challenge/README.md)

---

### 2. Mobile Backend Engineer Challenge

**Time:** 10-15 minutes
**Difficulty:** Intermediate
**Focus Areas:** Backend optimization, database queries, mobile-first thinking

**Scenario:** Debug performance crisis (3-5s response time) and implement analytics endpoint.

**Tasks:**
- Fix N+1 query bug causing slowness
- Implement proper pagination
- Fix duplicate creators bug
- Implement video analytics endpoint with engagement calculations
- Create mobile-optimized response schemas

**Key Skills Tested:**
- Database query optimization
- SQLAlchemy ORM proficiency
- Understanding mobile constraints
- API design for mobile clients
- Performance debugging

[📖 View Challenge Details](./mobile-backend-challenge/README.md)

---

## 🚀 Quick Start for Candidates

### Choose Your Challenge

**For AI Automation Engineer position:**
```bash
cd ai-automation-challenge
pip install -r requirements.txt
uvicorn main:app --reload
# Open README.md for instructions
```

**For Mobile Backend Engineer position:**
```bash
cd mobile-backend-challenge
pip install -r requirements.txt
uvicorn main:app --reload
# Open README.md for instructions
```

---

## 👨‍💼 For Interviewers

### Before the Interview

1. **Ensure candidate has:**
   - Cloned this repository
   - Python 3.9+ installed
   - VS Code or similar editor
   - AI coding assistant (Cursor, Copilot, etc.)
   - Screen sharing ready

2. **Have ready:**
   - [Interviewer Scoring Sheet](./INTERVIEWER_SCORING_SHEET.md) (print or digital)
   - Timer (15 minutes coding + 5 minutes discussion)
   - Solution reference for the chosen challenge

### During the Interview

**Format:** Live screen share observation

**Time Allocation:**
- 0-1 min: Setup and orient candidate
- 1-16 min: Candidate codes (15 minutes)
- 16-21 min: Discussion and questions (5 minutes)

**Observe:**
- Problem-solving approach
- AI tool usage and prompting
- Debugging methodology
- Code quality and patterns
- Time management
- Communication

**After Coding:**
Ask 3 discussion questions from the scoring sheet about their approach, improvements, and challenges faced.

### Scoring

Use the [Interviewer Scoring Sheet](./INTERVIEWER_SCORING_SHEET.md) to evaluate:
- Technical skills (coding, debugging, optimization)
- AI/LLM usage (for AI challenge) or mobile optimization (for backend challenge)
- System thinking and architecture
- Communication and problem-solving

**Passing Score:** 70/100 minimum

---

## 📊 What We're Looking For

### AI Automation Engineer

✅ **Strong candidates:**
- Use AI effectively (good prompts, quick iteration)
- Write clean async code
- Understand LLM prompt engineering
- Debug systematically
- Think about production concerns (errors, timeouts, fallbacks)

❌ **Red flags:**
- Can't use AI tools effectively
- Messy, non-production code
- Poor understanding of async patterns
- Can't debug validation issues
- Ignores error handling

### Mobile Backend Engineer

✅ **Strong candidates:**
- Identify N+1 queries quickly
- Write efficient SQL/SQLAlchemy
- Understand mobile constraints (payload size, latency)
- Follow proper architecture patterns
- Think about performance

❌ **Red flags:**
- Can't identify performance issues
- Loads all data then filters in Python
- No understanding of database optimization
- Ignores mobile-specific concerns
- Poor query construction

---

## 🔒 Confidential Files

**Do NOT share with candidates:**
- `SOLUTION_REFERENCE.md` files (in each challenge directory)
- `INTERVIEWER_SCORING_SHEET.md`
- Any internal evaluation notes

---

## 📝 Modifications and Customization

### Adjusting Difficulty

**Make Easier:**
- Provide more hints in comments
- Fix some of the bugs
- Add helper functions
- Extend time to 20 minutes

**Make Harder:**
- Remove some hints
- Add more bugs
- Require additional features
- Reduce time to 10 minutes
- Require real API integration (not mocks)

### Adding Test Cases

Both challenges currently use manual testing. To add automated tests:

```python
# tests/test_moderation.py
@pytest.mark.asyncio
async def test_openai_fallback_to_anthropic():
    # Test that fallback works when OpenAI fails
    pass
```

---

## 🆘 Troubleshooting

### Common Issues

**"ModuleNotFoundError"**
→ Run `pip install -r requirements.txt`

**"Port already in use"**
→ Change port: `uvicorn main:app --port 8001`

**"Database is empty" (mobile challenge)**
→ Restart the app, seed_data.py runs automatically

**Mock clients not working (AI challenge)**
→ They should work by default, check import statements

---

## 🤝 Contributing

To improve these challenges:

1. Test with real candidates and gather feedback
2. Document common pitfalls
3. Adjust difficulty based on results
4. Keep solution references updated
5. Improve clarity in READMEs

---

## 📄 License

Internal use only - Vizzy Labs © 2024

---

## Contact

For questions or issues with these challenges, contact:
- **Technical Lead:** [Your Name]
- **Email:** [Your Email]
- **Slack:** [Your Slack Channel]

---

**Good luck to all candidates!** 🚀

We're excited to see how you approach these real-world problems and demonstrate your skills with AI-assisted coding!
