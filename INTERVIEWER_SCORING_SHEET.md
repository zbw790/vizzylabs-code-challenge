# Vizzy Labs Coding Challenge - Interviewer Scoring Sheet

**Candidate Name:** ___________________________
**Position:** ☐ AI Automation Engineer  ☐ Mobile Backend Engineer
**Interview Date:** ___________________________
**Interviewer:** ___________________________

---

## Pre-Interview Setup

- [ ] Repository cloned and ready
- [ ] Dependencies installed
- [ ] Screen share working
- [ ] Timer ready (15 minutes)
- [ ] This scoring sheet printed/ready

---

## AI AUTOMATION ENGINEER CHALLENGE

### Part 1: AI Coding Ability (25 points)

**Effective Use of AI Assistant (10 pts)**
- [ ] 9-10: Excellent prompts, quick iteration, understands AI output
- [ ] 6-8: Good use, some inefficiency
- [ ] 3-5: Basic use, struggles with AI output
- [ ] 0-2: Doesn't use AI effectively

**Production-Quality Code (10 pts)**
- [ ] 9-10: Proper async, type hints, error handling, clean code
- [ ] 6-8: Mostly good, minor issues
- [ ] 3-5: Works but messy or missing patterns
- [ ] 0-2: Poor quality, major issues

**Completion Rate (5 pts)**
- [ ] 5: All features implemented and working
- [ ] 3-4: Most features done, 1-2 incomplete
- [ ] 1-2: Half complete
- [ ] 0: Minimal completion

**Subtotal: _____ / 25**

---

### Part 2: Prompting Ability (25 points)

**Claude Prompt Structure (15 pts)**
- [ ] 13-15: Returns valid JSON, clear schema, proper format
- [ ] 9-12: Works but could be clearer
- [ ] 5-8: Basic structure, issues with output
- [ ] 0-4: Poor structure or doesn't work

**Prompt Quality (10 pts)**
- [ ] 9-10: Examples, constraints, handles edge cases
- [ ] 6-8: Clear instructions, basic coverage
- [ ] 3-5: Vague or incomplete
- [ ] 0-2: Very poor quality

**Subtotal: _____ / 25**

---

### Part 3: Debugging Ability (20 points)

**Fixed Pydantic Validators (8 pts)**
- [ ] 8: All three validators correct (whitespace, creator_id, safety)
- [ ] 5-7: Two validators correct
- [ ] 2-4: One validator correct
- [ ] 0-1: No validators or all wrong

**Fixed OpenAI Integration (7 pts)**
- [ ] 7: Extracts violation type AND confidence correctly
- [ ] 4-6: One of the two correct
- [ ] 1-3: Attempted but incorrect
- [ ] 0: No fix attempted

**Fixed Initialization (5 pts)**
- [ ] 5: Service initialized, dependency injection, keys loaded
- [ ] 3-4: Initialized but missing some parts
- [ ] 1-2: Partial fix
- [ ] 0: No fix

**Subtotal: _____ / 20**

---

### Part 4: Multi-tasking (15 points)

**Error Handling (5 pts)**
- [ ] 5: Comprehensive try-except across all layers
- [ ] 3-4: Basic error handling
- [ ] 1-2: Minimal handling
- [ ] 0: No error handling

**Timeout Implementation (5 pts)**
- [ ] 5: Proper asyncio.wait_for with timeout
- [ ] 3-4: Timeout exists but issues
- [ ] 1-2: Attempted but incorrect
- [ ] 0: No timeout

**Fallback Chain (5 pts)**
- [ ] 5: OpenAI → Anthropic fallback working correctly
- [ ] 3-4: Fallback exists but issues
- [ ] 1-2: Attempted but doesn't work
- [ ] 0: No fallback

**Subtotal: _____ / 15**

---

### Part 5: System Thinking (15 points)

**Smart Trade-offs (5 pts)**
- [ ] 5: Excellent prioritization and decisions
- [ ] 3-4: Good decisions
- [ ] 1-2: Some questionable choices
- [ ] 0: Poor decisions

**Service Layer Pattern (5 pts)**
- [ ] 5: Proper separation of concerns
- [ ] 3-4: Mostly follows pattern
- [ ] 1-2: Mixed logic
- [ ] 0: No separation

**Code Maintainability (5 pts)**
- [ ] 5: Clean, documented, extensible
- [ ] 3-4: Readable but could improve
- [ ] 1-2: Hard to maintain
- [ ] 0: Very messy

**Subtotal: _____ / 15**

---

## MOBILE BACKEND ENGINEER CHALLENGE

### Part 1: Performance (40 points)

**Fixed N+1 Query (15 pts)**
- [ ] 13-15: Correct JOIN with GROUP BY or equivalent
- [ ] 9-12: Works but not optimal
- [ ] 5-8: Attempted but still has issues
- [ ] 0-4: No fix or still N+1

**Proper Pagination (10 pts)**
- [ ] 10: Correct offset/limit calculation
- [ ] 6-9: Works with minor issues
- [ ] 3-5: Attempted but incorrect
- [ ] 0-2: No pagination

**Feed Response Time (10 pts)**
- [ ] 10: <500ms consistently
- [ ] 7-9: 500-1000ms
- [ ] 4-6: 1-2 seconds
- [ ] 0-3: >2 seconds

**Analytics Efficiency (5 pts)**
- [ ] 5: Single optimized query
- [ ] 3-4: Works but not efficient
- [ ] 1-2: Has N+1 or other issues
- [ ] 0: Not implemented

**Subtotal: _____ / 40**

---

### Part 2: Correctness (30 points)

**No Duplicates (10 pts)**
- [ ] 10: No duplicates in results
- [ ] 5-9: Mostly fixed
- [ ] 0-4: Still has duplicates

**Engagement Calculation (10 pts)**
- [ ] 10: Correct SQL calculation + handles div-by-zero
- [ ] 7-9: Correct but no div-by-zero handling
- [ ] 4-6: Calculates in Python (works but inefficient)
- [ ] 0-3: Incorrect formula

**Error Handling (10 pts)**
- [ ] 9-10: Comprehensive exception handling
- [ ] 6-8: Basic error handling
- [ ] 3-5: Minimal handling
- [ ] 0-2: No error handling

**Subtotal: _____ / 30**

---

### Part 3: Mobile Optimization (20 points)

**Response Schemas (10 pts)**
- [ ] 9-10: Both schemas implemented correctly
- [ ] 6-8: One schema correct
- [ ] 3-5: Attempted but incomplete
- [ ] 0-2: Not implemented

**Pagination for Mobile (5 pts)**
- [ ] 5: Proper page-based pagination
- [ ] 3-4: Works but not ideal
- [ ] 1-2: Issues present
- [ ] 0: No pagination

**Mobile Constraints Understanding (5 pts)**
- [ ] 5: Clear evidence in code choices
- [ ] 3-4: Some awareness
- [ ] 1-2: Minimal consideration
- [ ] 0: No consideration

**Subtotal: _____ / 20**

---

### Part 4: Code Quality (10 points)

**Follows Pattern (4 pts)**
- [ ] 4: Route → Service → Database
- [ ] 2-3: Mostly follows
- [ ] 1: Mixed logic
- [ ] 0: No pattern

**Pydantic Usage (3 pts)**
- [ ] 3: Proper schemas with Config
- [ ] 2: Basic schemas
- [ ] 1: Issues present
- [ ] 0: Dict responses

**SQLAlchemy Quality (3 pts)**
- [ ] 3: Clean, efficient queries
- [ ] 2: Works but messy
- [ ] 1: Poor practices
- [ ] 0: Major issues

**Subtotal: _____ / 10**

---

## Behavioral Observations

### Problem-Solving Approach
- [ ] Systematic and methodical
- [ ] Reads instructions carefully
- [ ] Tests incrementally
- [ ] Asks clarifying questions

**Notes:**
_______________________________________________
_______________________________________________

### Communication
- [ ] Explains thinking clearly
- [ ] Articulates trade-offs
- [ ] Asks good questions
- [ ] Responds well to hints

**Notes:**
_______________________________________________
_______________________________________________

### Time Management
- [ ] Prioritizes effectively
- [ ] Doesn't get stuck too long
- [ ] Completes high-value tasks first
- [ ] Uses time wisely

**Notes:**
_______________________________________________
_______________________________________________

### AI Tool Usage
- [ ] Writes effective prompts
- [ ] Reviews AI output critically
- [ ] Iterates quickly with AI
- [ ] Understands AI suggestions

**Notes:**
_______________________________________________
_______________________________________________

---

## Post-Coding Discussion (5 minutes)

### Question 1: "Walk me through your [fallback logic / query optimization]"
**Answer Quality:**
- [ ] Excellent - deep understanding
- [ ] Good - understands core concepts
- [ ] Fair - surface level
- [ ] Poor - doesn't understand

**Notes:**
_______________________________________________
_______________________________________________

### Question 2: "How would you improve this with more time?"
**Answer Quality:**
- [ ] Excellent - specific, practical improvements
- [ ] Good - general improvements
- [ ] Fair - vague ideas
- [ ] Poor - no ideas

**Notes:**
_______________________________________________
_______________________________________________

### Question 3: "What was the hardest bug to fix and why?"
**Answer Quality:**
- [ ] Excellent - insightful analysis
- [ ] Good - identifies difficulty
- [ ] Fair - acknowledges challenge
- [ ] Poor - doesn't recognize difficulty

**Notes:**
_______________________________________________
_______________________________________________

---

## Final Scoring

| Category | Score | Max |
|----------|-------|-----|
| Part 1   | _____ | 25/40 |
| Part 2   | _____ | 25/30 |
| Part 3   | _____ | 20 |
| Part 4   | _____ | 15/10 |
| Part 5 (AI only) | _____ | 15 |
| **TOTAL** | **_____** | **100** |

---

## Recommendation

**Overall Assessment:**
- [ ] **Strong Hire** (85-100) - Exceeded expectations, strong skills
- [ ] **Hire** (70-84) - Met expectations, solid candidate
- [ ] **Maybe** (60-69) - Some concerns, discuss with team
- [ ] **No Hire** (<60) - Did not meet minimum bar

**Key Strengths:**
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

**Areas for Improvement:**
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

**Additional Notes:**
_______________________________________________
_______________________________________________
_______________________________________________
_______________________________________________

---

**Interviewer Signature:** ___________________________
**Date:** ___________________________
