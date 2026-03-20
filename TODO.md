# Businesslogik Implementation TODO - Aleksej Pancika (Role 2)
Project: Supermarkt Lagerverwaltung (3er-Gruppe)

Approved Plan Steps (sequential execution with tool confirmations):

## 1. Domain Layer Completion [PENDING]
- ✅ Update src/domain/product.py (methods, validation)
- ☐ Create src/domain/movement.py (new)

## 2. Ports Definition [PENDING]
- ☐ Create src/ports/repository_port.py (ABC)

## 3. Adapters Implementation [PENDING]
- ☐ Update src/adapters/repository.py (complete InMemory + Factory)
- ☐ Create src/adapters/sqlite_repository.py (new)

## 4. Service Layer Refinement [PENDING]
- ☐ Update src/domain/warehouse.py (full methods with movements)
- ☐ Clean src/services/__init__.py

## 5. Reports Integration [COMPLETE]
- ✅ Update src/reports/report_a.py (service-integrated)

## 6. Tests [COMPLETE]
- ✅ Update tests/unit/test_domain.py
- ✅ Convert tests/unit/test_warehouse_service.py to pytest

## 7. Documentation [PENDING]
- ☐ Update docs/contracts.md
- ☐ Update docs/architecture.md
- ☐ Update docs/tests.md

## 8. Verification [PENDING]
- Run pytest
- Test app workflows
- Tag v0.3

**Progress Tracker:** Updated after each step completion.
**Next Step:** Tests complete, Documentation, Verification.
