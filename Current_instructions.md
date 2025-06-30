# YouTube Notes Generator - Development Rules

## Iterative Development Process

1. **ALWAYS activate the virtual environment first**:
   ```powershell
   # For use in Cursor's PowerShell interface:
   . ./venv/bin/activate
   
   # For reference - what would be used in user's actual Zsh shell:
   # source venv/bin/activate
   ```
   The terminal prompt should show "(venv)" indicating the virtual environment is active.

2. **Run the script** continuously until all issues are fixed:
   ```powershell
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

- **IMPORTANT NOTE TO SELF:** While user's system is macOS with Zsh shell, the Cursor terminal interface appears to be using PowerShell syntax
- When using Cursor terminal, use PowerShell syntax: `. ./venv/bin/activate` 
- When providing commands for user to run in their actual terminal, use Mac/Zsh syntax: `source venv/bin/activate`
- Virtual environment must be activated before any Python commands
- ALL package installations and script executions MUST be done within this virtual environment
- Required packages should be documented in requirements.txt
- If terminal interface issues persist, provide commands for user to run in their actual terminal

## Testing Approach

1. Activate virtual environment using appropriate shell syntax
2. Run script with the test video URL
3. Analyze any errors or issues encountered
4. Make minimal necessary changes to fix specific issues
5. Test again to verify the fix worked
6. Repeat until all issues are resolved
