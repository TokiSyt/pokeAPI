from __future__ import annotations

from typing import Protocol


class ImportFn(Protocol):
    def __call__(self, name_or_id: str, user=None): ...


_registry: dict[type, ImportFn] = {}


def register(model):
    def decorator(fn: ImportFn):
        _registry[model] = fn
        return fn

    return decorator


def import_for_model(model, name_or_id: str, user=None):
    return _registry[model](name_or_id, user)
