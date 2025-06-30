# YouTube Notes Generator - Development Rules

## Iterative Development Process

1. **ALWAYS activate the virtual environment first**:
   ```bash
   source venv/bin/activate
   ```
   The terminal prompt should show "(venv)" indicating the virtual environment is active.

2. **Run the script** continuously until all issues are fixed:
   ```bash
   python youtube_notes_fixed.py "https://www.youtube.com/watch?v=qWm8yJ_mDAs"
   ```

3. **Verify issues** using appropriate methods (e.g., curl commands) when necessary to diagnose API/connection problems.

4. **Modify code** to fix identified issues.

5. **Track iterations** with a counter, starting at 1. Each code modification cycle is a new iteration.

6. **Provide commit messages** for each code change and wait for user to push to GitHub.

7. **Request approval** before installing any new packages or requiring special permissions.

8. **Document progress** with iteration numbers in commit messages.

## Critical Process Enforcement

1. **NO EXCEPTIONS** to the established process - follow every step in order
2. **Always run first** to observe actual errors before proposing changes
3. **Share error outputs** with the user before suggesting modifications
4. **Never implement changes** without explicit user approval
5. **Propose specific changes** based on observed errors only
6. **Wait for approval** after providing commit messages
7. **No assumptions** about what might be causing errors without evidence
8. **Always use the virtual environment** for all commands - never run Python commands outside of it

## Development Environment

- The shell environment is Zsh (NOT PowerShell) - all commands must use Zsh syntax
- Virtual environment has been created and must be activated with `source venv/bin/activate` before any commands
- ALL package installations and script executions MUST be done within this virtual environment
- Required packages should be documented in requirements.txt
- Verify the "(venv)" indicator appears in the terminal prompt before running any commands

## Testing Approach

1. Activate virtual environment
2. Run script with the test video URL
3. Analyze any errors or issues encountered
4. Make minimal necessary changes to fix specific issues
5. Test again to verify the fix worked
6. Repeat until all issues are resolved
