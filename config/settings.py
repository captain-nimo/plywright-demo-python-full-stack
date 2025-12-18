import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Config:
    """Base configuration class"""

    # Browser settings
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", 0))

    # Timeout settings (in milliseconds)
    DEFAULT_TIMEOUT = int(os.getenv("TIMEOUT", 30000))
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", 30000))

    # URLs
    BASE_UI_URL = os.getenv("BASE_UI_URL", "https://example.com")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")

    # API settings
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))

    # Recording settings
    RECORD_VIDEO = os.getenv("RECORD_VIDEO", "false").lower() == "true"
    RECORD_TRACE = os.getenv("RECORD_TRACE", "false").lower() == "true"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Screenshot settings
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "test-results/screenshots")

    @classmethod
    def get_browser_launch_args(cls):
        """Get browser launch arguments"""
        args = {
            "headless": cls.HEADLESS,
            "slow_mo": cls.SLOW_MO,
        }
        # Add flags for headless environments (e.g., GitHub Actions)
        if cls.HEADLESS:
            args["args"] = ["--disable-gpu", "--no-sandbox"]
        return args

    @classmethod
    def get_context_options(cls):
        """Get browser context options"""
        options = {
            "viewport": {"width": 1280, "height": 720},
            "ignore_https_errors": True,
        }

        if cls.RECORD_VIDEO:
            options["record_video_dir"] = "test-results/videos"

        if cls.RECORD_TRACE:
            options["record_trace_dir"] = "test-results/traces"

        return options


class DevelopmentConfig(Config):
    """Development configuration"""

    HEADLESS = False
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""

    HEADLESS = True
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration"""

    HEADLESS = True
    BASE_UI_URL = os.getenv("BASE_UI_URL", "https://staging.example.com")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://staging-api.example.com")


# Select configuration based on environment
def get_config():
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()
