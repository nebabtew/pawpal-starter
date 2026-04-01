# PawPal+ Project Reflection

## 1. System Design

** core actions** :
1. Add a pet (e.g., register a dog named Max with its owner)
2. Schedule a task for a pet (e.g., schedule a walk at 8:00 AM)
3. View today's tasks (e.g., see all tasks due today across all pets)

**a. Initial design**

- I designed four classes: Task holds a single activity's details (description, time, frequency, completion status). Pet stores pet info and maintains a list of tasks. Owner manages multiple pets and can aggregate all tasks. Scheduler is the brain  it retrieves, sorts, filters, and detects conflicts across all tasks for an owner.

**b. Design changes**

1b. Design Changes

Changes made based on Copilot feedback and full implementation:

1. Task.mark_complete()
   - Changed: Added self.completed = True instead of pass
   - Why: The method needs to actually update the task's status, otherwise marking complete does nothing

2. Pet.add_task()
   - Changed: Added type checking and duplicate prevention
   - Why: Prevents invalid objects or repeated tasks from corrupting the pet's task list

3. Pet.get_tasks()
   - Changed: Returns list(self.tasks) instead of pass
   - Why: Returning a copy protects the internal list from being modified outside the class

4. Owner.add_pet()
   - Changed: Added type checking and duplicate prevention
   - Why: Same reason as Pet.add_task() — keeps the owner's pet list clean and valid

5. Owner.get_all_tasks()
   - Changed: Loops through all pets and uses extend() to combine their tasks
   - Why: The Scheduler needs one unified task list to sort, filter, and detect conflicts

6. Scheduler.get_todays_tasks()
   - Changed: Filters out completed tasks and handles all three frequency types
   - Why: Users should only see tasks that still need to be done today

7. Scheduler.sort_by_time()
   - Changed: Parses HH:MM strings into real time objects before sorting
   - Why: String sorting would give wrong order (e.g. "09:00" vs "10:00" works but "8:00" would not)

8. Scheduler.filter_tasks()
   - Changed: Accepts completed and frequency as filter parameters
   - Why: Makes filtering flexible and reusable instead of hardcoded

9. Scheduler.detect_conflicts()
   - Changed: Uses a dictionary to track seen times and collect duplicates
   - Why: Efficient way to find exact time collisions without nested loops

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers time and frequency as its main constraints. Tasks are sorted chronologically so the owner sees what's due first, and the frequency determines whether a task appears today (daily tasks always show, weekly tasks show on their scheduled date, one-time tasks show once). I decided time mattered most because a pet owner's day revolves around when things need to happen — a morning feeding can't wait until afternoon. Priority levels weren't included in the base design to keep things simple, but could be added as a secondary sort.

**b. Tradeoffs**

- My conflict detection only checks for exact time matches — if two tasks are at 08:00 and 08:15 but both take 30 minutes, it won't flag the overlap. I chose this simpler approach for clarity.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools throughout the project for different purposes. During Phase 1, I used Copilot to generate the Mermaid.js UML diagram from my brainstormed class list, which helped me visualize relationships before writing code. During implementation, I used Copilot's Agent Mode to flesh out class skeletons into working methods. For testing, I gave Copilot a specific prompt describing exactly what three tests to write and it generated them accurately. The most helpful prompts were ones that referenced specific files and gave numbered requirements — vague prompts like "make it better" gave generic results, while specific prompts like "add mark_task_complete to Scheduler that handles recurring tasks using timedelta" gave exactly what I needed.

**b. Judgment and verification**

- During Phase 1, Copilot's initial skeleton used __post_init__ to initialize the tasks list in Pet. I later changed this to field(default_factory=list) which is the more standard dataclass pattern and avoids the extra method. I also noticed that Copilot used st.experimental_rerun() in the Streamlit app, which is deprecated — I replaced it with st.rerun(). I verified AI suggestions by running the code every time, checking terminal output from main.py, and running pytest to confirm tests passed before committing.

---

## 4. Testing and Verification

**a. What you tested**
I tested five core behaviors: task completion (mark_complete changes status to True), task addition (adding a task increases the pet's task count), sorting correctness (tasks added out of order come back in chronological order), recurrence logic (completing a daily task auto-creates one for the next day), and conflict detection (two tasks at the same time are both flagged). These tests are important because they verify the Scheduler's core intelligence — if sorting or recurrence breaks, the whole app gives wrong information to the user.

**b. Confidence**

I'm at 4 out of 5 confidence. The core happy paths all work and are verified by automated tests. If I had more time, I'd test edge cases like: adding a task with an invalid time format, a pet with zero tasks going through the scheduler, two pets with the same name, and overlapping task durations rather than just exact time matches.

---

## 5. Reflection

**a. What went well**

-I'm most satisfied with how the Scheduler class turned out. It cleanly separates the "brain" logic from the data classes, so sorting, filtering, conflict detection, and recurring tasks all live in one place. The mark_task_complete method that handles recurrence felt like the most "real" feature — it actually saves the user from manually re-entering daily tasks.

**b. What you would improve**

-I'd add a duration field to Task so conflict detection could catch overlapping tasks, not just exact time matches. I'd also add priority levels and sort by priority first, then time. The UI could use delete and edit buttons for tasks, and data persistence with JSON so everything isn't lost when the app restarts.
**c. Key takeaway**

- The most important thing I learned is that being specific with AI prompts makes all the difference. When I gave vague instructions, I got generic code that needed heavy editing. When I gave numbered, file-referenced prompts with clear requirements, the output was almost ready to commit. The human's job isn't to write every line — it's to be the architect who knows what the system needs and can evaluate whether the AI's output actually fits that vision.
