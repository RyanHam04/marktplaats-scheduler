# Requirements
## 1. Overview
### 1.1 Purpose
This system allows user to define marktplaats search jobs using the `marktplaats` python package.
These search jobs will periodically query Marktplaats to retrieve the newly posted advertisements since their last query.
The jobs will be executed at a configurable interval, executed in the background and results can be retrieved automatically.

### 1.2 Goals
- Allow users to create scheduled jobs at configurable intervals.
  - Why: It allows the system to balance data freshness needs with system load and potential rate limits.
- Allow users to retrieve new advertisements
- Allow users to copy and modify their jobs
  - Why: Enables reuse and adaptation of similar search queries without recreating jobs from scratch.
- Allow users to deploy their own instance of the system:
  - Why: Self-hosting improves flexibility, allowing higher poll rates, and overcomes potential IP reputation issues
- Simple login system
  - Why: Login enables multiple users to use the system
### 1.3 Non-Goals
- Production-grade authentication system
- Any security beyond a basic login implementation.

##