# PawPal+ Project Reflection

## 1. System Design

** core actions** :
1. Add a pet (e.g., register a dog named Max with its owner)
2. Schedule a task for a pet (e.g., schedule a walk at 8:00 AM)
3. View today's tasks (e.g., see all tasks due today across all pets)

**a. Initial design**

- I designed four classes: Task holds a single activity's details (description, time, frequency, completion status). Pet stores pet info and maintains a list of tasks. Owner manages multiple pets and can aggregate all tasks. Scheduler is the brain  it retrieves, sorts, filters, and detects conflicts across all tasks for an owner.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
