# Git Cleanup TODO - Remove blackboxai from commit history

## Steps:
- [ ] 1. Clean working directory (stash or commit changes)
- [ ] 2. Checkout businesslogik-aleksej
- [ ] 3. git rebase -i HEAD~3 to edit commits 863f4bd, 4b10619, drop revert if needed
  - Edit messages: remove all "blackboxai"/"BlackboxAI", e.g. "feat: demo_businesslogik.py updates"
- [ ] 4. Verify: git log --graph --oneline --all | grep -i blackbox (empty)
- [ ] 5. git push origin businesslogik-aleksej --force-with-lease
- [ ] 6. git stash pop or commit changes
- [ ] 7. Final verification and pytest tests/unit/

Progress will be updated after each step.

