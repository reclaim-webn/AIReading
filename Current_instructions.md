# YouTube Notes Generator - Development Rules

## Iterative Development Process

1. **Run the script** continuously until all issues are fixed:
   ```bash
   python youtube_notes_fixed.py "https://www.youtube.com/watch?v=qWm8yJ_mDAs"
   ```

2. **Verify issues** using appropriate methods (e.g., curl commands) when necessary to diagnose API/connection problems.

3. **Modify code** to fix identified issues.

4. **Track iterations** with a counter, starting at 1. Each code modification cycle is a new iteration.

5. **Provide commit messages** for each code change and wait for user to push to GitHub.

6. **Request approval** before installing any new packages or requiring special permissions.

7. **Document progress** with iteration numbers in commit messages.

## Critical Process Enforcement

1. **NO EXCEPTIONS** to the established process - follow every step in order
2. **Always run first** to observe actual errors before proposing changes
3. **Share error outputs** with the user before suggesting modifications
4. **Never implement changes** without explicit user approval
5. **Propose specific changes** based on observed errors only
6. **Wait for approval** after providing commit messages
7. **No assumptions** about what might be causing errors without evidence

## Development Environment

- Virtual environment has been created and activated with `source venv/bin/activate`
- All package installations should be done within this virtual environment
- Required packages should be documented in requirements.txt

## Testing Approach

1. Run script with the test video URL
2. Analyze any errors or issues encountered
3. Make minimal necessary changes to fix specific issues
4. Test again to verify the fix worked
5. Repeat until all issues are resolved
