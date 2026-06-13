import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ToolExecutionSandbox:
    """
    Safe Tool Sandbox Boundary.
    Executes physical OS operations within safe directories and try-except wrappers.
    """
    def __init__(self, storage_dir: str = "./agent_storage"):
        self.storage_dir = os.path.abspath(storage_dir)
        # Ensure the isolated workspace folder exists safely on the disk
        os.makedirs(self.storage_dir, exist_ok=True)

    def write_local_file(self, filename: str, content: str) -> Dict[str, Any]:
        """Safely writes strings to disk, preventing path traversal attacks."""
        try:
            # Enforce path isolation: strip out any sneaky directory traversal attempts
            clean_filename = os.path.basename(filename)
            target_path = os.path.join(self.storage_dir, clean_filename)

            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"[SANDBOX TOOL] Successfully wrote isolated asset: {clean_filename}")
            return {
                "success": True,
                "msg": f"File written successfully to isolated storage workspace.",
                "absolute_path": target_path
            }
        except Exception as e:
            logger.error(f"[SANDBOX TOOL FAULT] File write operation failed: {str(e)}")
            return {"success": False, "msg": f"Sandbox execution crash: {str(e)}"}