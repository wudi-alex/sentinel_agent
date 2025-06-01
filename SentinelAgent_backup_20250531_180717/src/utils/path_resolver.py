"""
Path resolver utility for handling container vs host path differences.
"""

import os
from pathlib import Path
from typing import Optional, Dict


class PathResolver:
    """Resolves paths for both containerized and host environments."""
    
    def __init__(self):
        self.is_container = self._detect_container_environment()
        self.projects_dir = self._get_projects_directory()
        
        # Map of relative paths to container paths
        self.path_mappings = {
            "../crewai_gmail": "crewai_gmail",
            "../autogen_magneticone": "autogen_magneticone",
        }
    
    def _detect_container_environment(self) -> bool:
        """Detect if running inside a Docker container."""
        # Check for common container indicators
        indicators = [
            os.path.exists('/.dockerenv'),
            os.environ.get('SENTINEL_PROJECTS_DIR') is not None,
            os.path.exists('/proc/1/cgroup') and 'docker' in open('/proc/1/cgroup', 'r').read()
        ]
        return any(indicators)
    
    def _get_projects_directory(self) -> Path:
        """Get the projects directory based on environment."""
        if self.is_container:
            # In container, use the mounted projects directory
            projects_dir = os.environ.get('SENTINEL_PROJECTS_DIR', '/app/projects')
            return Path(projects_dir)
        else:
            # On host, use relative paths from current working directory
            return Path.cwd().parent
    
    def resolve_path(self, relative_path: str) -> str:
        """
        Resolve a relative path to work in both container and host environments.
        
        Args:
            relative_path: Original relative path like '../crewai_gmail'
            
        Returns:
            Resolved absolute path as string
        """
        if self.is_container:
            # In container, map to projects directory
            if relative_path in self.path_mappings:
                mapped_path = self.path_mappings[relative_path]
                resolved = self.projects_dir / mapped_path
            else:
                # For other paths, try to map based on pattern
                if relative_path.startswith('../'):
                    project_name = relative_path.replace('../', '')
                    resolved = self.projects_dir / project_name
                else:
                    resolved = Path(relative_path)
        else:
            # On host, use original relative path
            resolved = Path(relative_path).resolve()
        
        return str(resolved)
    
    def resolve_example_path(self, example_path: str) -> str:
        """
        Resolve example paths for the web interface.
        
        Args:
            example_path: Example path from configuration
            
        Returns:
            Resolved path that works in current environment
        """
        return self.resolve_path(example_path)
    
    def get_examples_config(self) -> list:
        """
        Get examples configuration with resolved paths.
        
        Returns:
            List of example configurations with correct paths
        """
        examples = [
            {
                'name': 'CrewAI Gmail',
                'path': '../crewai_gmail',
                'description': 'CrewAI Email Processing System',
                'type': 'crewai'
            },
            {
                'name': 'Magentic-One',
                'path': '../autogen_magneticone', 
                'description': 'AutoGen Magentic-One System',
                'type': 'autogen'
            }
        ]
        
        # Resolve paths for current environment
        for example in examples:
            example['resolved_path'] = self.resolve_path(example['path'])
            
        return examples
    
    def path_exists(self, path: str) -> bool:
        """
        Check if a path exists, resolving it first.
        
        Args:
            path: Path to check
            
        Returns:
            True if path exists, False otherwise
        """
        resolved_path = self.resolve_path(path)
        return Path(resolved_path).exists()


# Global instance
path_resolver = PathResolver()


def resolve_path(relative_path: str) -> str:
    """Convenience function to resolve a path."""
    return path_resolver.resolve_path(relative_path)


def get_examples_config() -> list:
    """Convenience function to get examples configuration."""
    return path_resolver.get_examples_config()
