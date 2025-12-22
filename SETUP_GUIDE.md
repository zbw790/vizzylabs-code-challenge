# Setup Guide for Vizzy Labs Coding Challenges

Quick reference for setting up and running the coding challenges.

---

## 📦 Files Created

### AI Automation Challenge (8 files)
```
ai-automation-challenge/
├── README.md                  ✅ Candidate instructions
├── SOLUTION_REFERENCE.md      🔒 Evaluator only
├── requirements.txt           ✅ Dependencies
├── models.py                  🐛 Has validation bugs
├── moderation_service.py      🐛 Incomplete + bugs
├── main.py                    🐛 Incomplete
└── mock_clients.py            ✅ Working mock APIs
```

### Mobile Backend Challenge (13 files)
```
mobile-backend-challenge/
├── README.md                     ✅ Candidate instructions
├── SOLUTION_REFERENCE.md         🔒 Evaluator only
├── requirements.txt              ✅ Dependencies
├── main.py                       ✅ Complete
├── database.py                   ✅ Complete
├── models.py                     ✅ Complete
├── schemas.py                    🐛 Incomplete
├── seed_data.py                  ✅ Working
├── routes/
│   ├── creators.py              🐛 Has bugs
│   └── analytics.py             🐛 Stub only
└── services/
    ├── creator_service.py       🐛 N+1 bug
    └── analytics_service.py     🐛 Stub only
```

### Repository Root (3 files)
```
├── README.md                      ✅ Main repo README
├── INTERVIEWER_SCORING_SHEET.md   🔒 Evaluation rubric
└── SETUP_GUIDE.md                 ✅ This file
```

**Total:** 24 files created

---

## 🚀 Quick Test - AI Automation Challenge

```bash
cd ai-automation-challenge
pip install -r requirements.txt
uvicorn main:app --reload
```

**Expected:** Server starts but service is None (intentional bug)

**Test endpoint:**
```bash
curl -X POST "http://localhost:8000/moderate" \
  -H "Content-Type: application/json" \
  -d '{"content": "test", "creator_id": "123"}'
```

**Expected:** Error (service not initialized - candidate must fix)

---

## 🚀 Quick Test - Mobile Backend Challenge

```bash
cd mobile-backend-challenge
pip install -r requirements.txt
uvicorn main:app --reload
```

**Expected:**
- Server starts
- Database seeded automatically
- Message: "✅ Successfully seeded database with 100 creators and 1000 videos"

**Test endpoints:**
```bash
# Test slow endpoint (3-5 seconds - intentional bug)
time curl "http://localhost:8000/creators/feed?page=1&page_size=20"

# Test health check
curl "http://localhost:8000/health"
```

**Expected:** Feed endpoint is SLOW (candidate must fix)

---

## ✅ Pre-Interview Checklist

**For Candidates:**
- [ ] Python 3.9+ installed
- [ ] pip or poetry available
- [ ] Code editor (VS Code recommended)
- [ ] AI coding assistant (Cursor/Copilot)
- [ ] Screen share working
- [ ] Microphone working
- [ ] Repository cloned

**For Interviewers:**
- [ ] Scoring sheet ready (printed or digital)
- [ ] Timer ready (15 + 5 minutes)
- [ ] Solution reference accessible
- [ ] Note-taking tool ready
- [ ] Screen recording (optional but recommended)

---

## 🎯 Interview Flow

### Phase 1: Introduction (1 minute)
1. Welcome candidate
2. Confirm they can share screen
3. Brief overview of challenge format
4. Start timer when they begin coding

### Phase 2: Coding (15 minutes)
**Candidate codes while you observe:**
- Problem-solving approach
- AI tool usage
- Debugging methodology
- Communication
- Time management

**Do NOT:**
- Give away solutions
- Rush the candidate
- Interrupt excessively
- Judge prematurely

**DO:**
- Answer clarifying questions
- Provide hints if stuck >2 minutes
- Take notes on scoring sheet
- Observe how they use AI

### Phase 3: Discussion (5 minutes)
Ask 3 questions from scoring sheet:
1. "Walk me through your approach to [specific implementation]"
2. "How would you improve this with more time?"
3. "What was the hardest bug and why?"

### Phase 4: Wrap Up (1 minute)
- Thank candidate
- Explain next steps
- Complete scoring sheet

**Total time:** ~22 minutes

---

## 📊 Scoring Quick Reference

| Score Range | Interpretation |
|-------------|----------------|
| 85-100 | **Strong Hire** - Exceeded expectations |
| 70-84  | **Hire** - Met expectations |
| 60-69  | **Maybe** - Discuss with team |
| <60    | **No Hire** - Below minimum bar |

**Minimum passing:** 70/100

---

## 🛠️ Common Setup Issues

### Issue: "No module named 'fastapi'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
uvicorn main:app --port 8001
```

### Issue: "Mock clients not working"
**Solution:** They should work automatically. Check:
```python
from mock_clients import MockOpenAIClient
client = MockOpenAIClient()
```

### Issue: "Database not seeding"
**Solution:** Restart the app - seed_data runs on startup

---

## 🔄 Resetting Between Candidates

**For AI Challenge:**
```bash
cd ai-automation-challenge
git checkout . # Reset all files
# Or manually restore from git
```

**For Mobile Challenge:**
```bash
cd mobile-backend-challenge
git checkout . # Reset all files
# Database is in-memory, resets automatically on restart
```

---

## 📝 Post-Interview Tasks

1. **Complete scoring sheet** - Fill out all sections
2. **Write summary** - Key strengths and concerns
3. **Make recommendation** - Hire/No Hire with rationale
4. **Share with team** - Upload to hiring platform
5. **Provide feedback** (if requested) - Constructive notes for candidate

---

## 🎓 Training for New Interviewers

### Before Your First Interview

1. **Read both challenge READMEs** completely
2. **Review solution references** - understand expected solutions
3. **Practice with the scoring sheet** - know what to look for
4. **Run both challenges yourself** - understand the bugs
5. **Shadow an experienced interviewer** (recommended)

### During Your First Interview

- Have this guide open for reference
- Don't worry about perfect scoring - consistency improves
- Focus on observing and taking notes
- Ask for calibration after first few interviews

---

## 🔧 Customization Options

### Make Easier
- Add more hints in code comments
- Pre-fix some bugs
- Extend time to 20 minutes
- Provide skeleton code

### Make Harder
- Remove hints
- Add more bugs
- Reduce time to 10 minutes
- Require testing
- Require real API integration

---

## 📞 Support

**Issues with challenges?**
- Check SOLUTION_REFERENCE.md files
- Review this setup guide
- Ask team in Slack: #eng-hiring
- Email: [hiring@vizzylabs.com]

**Technical issues during interview?**
- Have backup plan (reschedule)
- Screen share alternatives ready
- Keep calm and professional

---

## ✨ Success Tips

**For getting good signal:**
1. ✅ Let candidates use AI freely - we want to see how they use it
2. ✅ Focus on process, not just results
3. ✅ Ask follow-up questions to understand thinking
4. ✅ Take detailed notes - memory fades quickly
5. ✅ Be consistent across candidates

**For candidate experience:**
1. ✅ Be friendly and welcoming
2. ✅ Explain the format clearly
3. ✅ Answer clarifying questions
4. ✅ Don't leave them stuck too long
5. ✅ Thank them for their time

---

Good luck with your interviews! 🎉
