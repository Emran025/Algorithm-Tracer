import subprocess
import sys
import pytest

def test_streamlit_app_smoke_test():
    """Runs a smoke test on the Streamlit app to check for import/run errors."""
    # Use subprocess to run the Streamlit app in a non-interactive way
    # We expect it to start without immediate errors, then terminate.
    # This is a basic check that all imports resolve and the app can initialize.
    command = [
        sys.executable, "-m", "streamlit", "run",
        "app/ui/streamlit_app.py",
        "--server.headless", "true", # Run in headless mode
        "--server.port", "8502", # Use a different port to avoid conflicts
        "--browser.gatherUsageStats", "false", # Disable usage stats
    ]

    process = None
    try:
        # Start the Streamlit app as a subprocess
        # We capture stdout and stderr to check for errors
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Give it a few seconds to start up and potentially crash
        # If it runs for this duration without error, we assume it started successfully.
        # A real integration test might involve more complex interaction.
        stdout, stderr = process.communicate(timeout=10)

        # Check for common error indicators in stderr or stdout
        assert "Error" not in stderr and "Traceback" not in stderr, \
            f"Streamlit app encountered an error during startup: {stderr}"
        assert "Error" not in stdout and "Traceback" not in stdout, \
            f"Streamlit app printed an error during startup: {stdout}"

        # If the process is still running after communicate with timeout, it means it didn't exit cleanly
        # For a smoke test, we expect it to exit after initialization if no user interaction.
        # However, Streamlit apps typically run indefinitely until killed. So, we just check for errors.
        # If it reaches here, it means no immediate crash.
        print("Streamlit app smoke test passed: No immediate errors on startup.")

    except subprocess.TimeoutExpired:
        print("Streamlit app process timed out, which is expected for a running server. Checking output...")
        # If it timed out, it means it was running. We can still check stderr/stdout if needed.
        if process:
            process.kill()
            stdout, stderr = process.communicate()
            assert "Error" not in stderr and "Traceback" not in stderr, \
                f"Streamlit app encountered an error during timeout: {stderr}"
            assert "Error" not in stdout and "Traceback" not in stdout, \
                f"Streamlit app printed an error during timeout: {stdout}"
            print("Streamlit app smoke test passed after timeout: No errors detected.")

    except Exception as e:
        if process:
            process.kill()
            stdout, stderr = process.communicate()
            print(f"Streamlit app stdout: {stdout}")
            print(f"Streamlit app stderr: {stderr}")
        pytest.fail(f"An unexpected error occurred during Streamlit app smoke test: {e}")

    finally:
        if process and process.poll() is None: # If process is still running
            process.kill()
            process.wait() # Wait for it to terminate


# To run this test:
# 1. Ensure you have `streamlit` and `pytest` installed.
# 2. Navigate to the AlgoVisEdu project root.
# 3. Run `pytest tests/test_streamlit_app.py`

