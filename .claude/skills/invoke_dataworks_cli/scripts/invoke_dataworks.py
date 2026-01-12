#!/usr/bin/env python3
"""
DataWorks CLI Wrapper
Invokes Alibaba Cloud DataWorks CLI with proper authentication and error handling.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Optional, Tuple


class DataWorksError(Exception):
    """Base exception for DataWorks CLI operations"""
    pass


class CredentialError(DataWorksError):
    """Raised when credentials are missing or invalid"""
    pass


class CLINotFoundError(DataWorksError):
    """Raised when DataWorks CLI is not installed"""
    pass


class DataWorksCLI:
    """Wrapper for Alibaba Cloud DataWorks CLI operations"""

    MAX_NETWORK_RETRIES = 3
    MAX_RATE_LIMIT_RETRIES = 5
    NETWORK_BACKOFF_BASE = 1  # seconds
    RATE_LIMIT_BACKOFF = 60  # seconds

    def __init__(self, env_file: str = ".env"):
        """Initialize DataWorks CLI wrapper with credentials from .env file"""
        self.env_file = Path(env_file)
        self.access_key_id = None
        self.access_key_secret = None
        self.reference_docs = ""
        self._reference_docs_loaded = False
        self._load_credentials()
        self._validate_cli_installation()

    def _load_credentials(self):
        """Load credentials from .env file"""
        if not self.env_file.exists():
            raise CredentialError(
                f"Environment file not found: {self.env_file}\n"
                f"Please create .env file with ALIYUN_ACCESS_KEY_ID and ALIYUN_ACCESS_KEY_SECRET"
            )

        if not os.access(self.env_file, os.R_OK):
            raise CredentialError(
                f"Environment file not readable: {self.env_file}\n"
                f"Please check file permissions"
            )

        # Parse .env file manually to avoid external dependencies
        with open(self.env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    if key == 'ALIYUN_ACCESS_KEY_ID':
                        self.access_key_id = value
                    elif key == 'ALIYUN_ACCESS_KEY_SECRET':
                        self.access_key_secret = value

        if not self.access_key_id or not self.access_key_secret:
            raise CredentialError(
                "Missing credentials in .env file\n"
                "Required: ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET"
            )

    def _validate_cli_installation(self):
        """Check if DataWorks CLI is installed"""
        try:
            result = subprocess.run(
                ['aliyun', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                raise CLINotFoundError("Aliyun CLI installed but not working properly")
        except FileNotFoundError:
            raise CLINotFoundError(
                "Aliyun CLI not found\n"
                "Install: https://www.alibabacloud.com/help/en/alibaba-cloud-cli/latest/install"
            )
        except subprocess.TimeoutExpired:
            raise CLINotFoundError("Aliyun CLI check timeout")

    def _sanitize_output(self, output: str) -> str:
        """Remove potential credential leaks from output"""
        sanitized = output
        if self.access_key_id:
            sanitized = sanitized.replace(self.access_key_id, "***ACCESS_KEY***")
        if self.access_key_secret:
            sanitized = sanitized.replace(self.access_key_secret, "***SECRET***")
        return sanitized

    def _read_reference_docs(self) -> None:
        """Read product reference docs before executing CLI commands"""
        if self._reference_docs_loaded:
            return

        doc_path = Path(__file__).resolve().parent.parent / "references" / "dataworks_cli_commands.md"
        try:
            self.reference_docs = doc_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(
                f"Warning: reference docs not found at {doc_path}",
                file=sys.stderr
            )
        except Exception as exc:
            print(
                f"Warning: failed to read reference docs: {exc}",
                file=sys.stderr
            )
        finally:
            self._reference_docs_loaded = True

    def _execute_with_retry(
        self,
        command: list,
        timeout: int = 300
    ) -> Tuple[int, str, str]:
        """Execute command with retry logic for network failures"""
        network_attempt = 0
        rate_limit_attempt = 0

        while True:
            try:
                # Set environment variables for authentication
                env = os.environ.copy()
                env['ALIBABA_CLOUD_ACCESS_KEY_ID'] = self.access_key_id
                env['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = self.access_key_secret

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env
                )

                # Sanitize output
                stdout = self._sanitize_output(result.stdout)
                stderr = self._sanitize_output(result.stderr)

                # Check for rate limiting
                if 'Throttling' in stderr or 'Rate limit' in stderr:
                    rate_limit_attempt += 1
                    if rate_limit_attempt >= self.MAX_RATE_LIMIT_RETRIES:
                        return result.returncode, stdout, stderr

                    print(f"Rate limit detected, retry {rate_limit_attempt}/{self.MAX_RATE_LIMIT_RETRIES} after {self.RATE_LIMIT_BACKOFF}s", file=sys.stderr)
                    time.sleep(self.RATE_LIMIT_BACKOFF)
                    continue

                return result.returncode, stdout, stderr

            except subprocess.TimeoutExpired:
                network_attempt += 1
                if network_attempt >= self.MAX_NETWORK_RETRIES:
                    raise DataWorksError(f"Command timeout after {self.MAX_NETWORK_RETRIES} retries")

                backoff = self.NETWORK_BACKOFF_BASE * (2 ** (network_attempt - 1))
                print(f"Timeout, retry {network_attempt}/{self.MAX_NETWORK_RETRIES} after {backoff}s", file=sys.stderr)
                time.sleep(backoff)

            except Exception as e:
                raise DataWorksError(f"Command execution failed: {str(e)}")

    def execute(self, cli_args: list, timeout: int = 300) -> Tuple[int, str, str]:
        """
        Execute DataWorks CLI command

        Args:
            cli_args: List of CLI arguments (e.g., ['dataworks', 'list-projects'])
            timeout: Command timeout in seconds (default: 300)

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        # Validate command
        if not cli_args or not isinstance(cli_args, list):
            raise ValueError("cli_args must be a non-empty list")

        # Ensure reference docs are read before running commands
        self._read_reference_docs()

        # Build full command
        command = ['aliyun'] + cli_args

        # Execute with retry logic
        return self._execute_with_retry(command, timeout)


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 invoke_dataworks.py <dataworks-command> [args...]", file=sys.stderr)
        print("Example: python3 invoke_dataworks.py dataworks ListProjects", file=sys.stderr)
        sys.exit(1)

    try:
        cli = DataWorksCLI()
        cli_args = sys.argv[1:]

        returncode, stdout, stderr = cli.execute(cli_args)

        if stdout:
            print(stdout)
        if stderr:
            print(stderr, file=sys.stderr)

        sys.exit(returncode)

    except DataWorksError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)


if __name__ == '__main__':
    main()
