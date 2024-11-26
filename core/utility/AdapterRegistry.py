from core.io.JSON import JSONAdapter
from core.io.XML import XMLAdapter

import sys, os

class Registry:
    """Centralized registry for managing components (e.g., adapters, schemas)."""
    
    _registry = {}

    @classmethod
    def register(cls, name, component, category="general"):
        """
        Register a component in the registry.

        Args:
            name (str): Name of the component.
            component (Any): The component instance.
            category (str): Category of the component (e.g., 'adapters', 'schemas').
        """
        if category not in cls._registry:
            cls._registry[category] = {}
        cls._registry[category][name] = component

    @classmethod
    def get(cls, name, category="general"):
        """
        Retrieve a component by name and category.

        Args:
            name (str): Name of the component.
            category (str): Category of the component.

        Returns:
            Any: The requested component.

        Raises:
            ValueError: If the component is not registered.
        """
        if category not in cls._registry or name not in cls._registry[category]:
            raise ValueError(f"Component '{name}' in category '{category}' is not registered.")
        return cls._registry[category][name]

    @classmethod
    def list_components(cls, category="general"):
        """List all registered components in a category."""
        return list(cls._registry.get(category, {}).keys())



def register():
    """Register all available adapters in the Registry."""
    Registry.register("JSON", JSONAdapter, category="adapters")
    Registry.register("XML", XMLAdapter, category="adapters")
    #Registry.register("Arrow", ArrowAdapter, category="adapters")
    #Registry.register("Numpy", NumpyAdapter, category="adapters")
    #Registry.register("Pandas", PandasAdapter, category="adapters")
    #Registry.register("SQL", SQLAdapter, category="adapters")
