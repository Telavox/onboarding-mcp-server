"""Tests for adapter system."""

from lib_logger import LoggerCore, configure_logging, reset_logging
from lib_logger.adapters import ConsoleAdapter, GCPAdapter, JSONAdapter


class TestAdapters:
    """Test suite for logging adapters."""

    def setup_method(self) -> None:
        """Reset logging before each test."""
        reset_logging()

    def test_console_adapter_configuration(self) -> None:
        """ConsoleAdapter should configure successfully."""
        adapter = ConsoleAdapter(level="INFO")
        configure_logging(adapters=[adapter])

        assert LoggerCore.is_configured()
        assert len(LoggerCore.get_adapters()) == 1

    def test_json_adapter_configuration(self) -> None:
        """JSONAdapter should configure successfully."""
        adapter = JSONAdapter(level="DEBUG")
        configure_logging(adapters=[adapter])

        assert LoggerCore.is_configured()
        assert len(LoggerCore.get_adapters()) == 1

    def test_gcp_adapter_configuration(self) -> None:
        """GCPAdapter should configure successfully."""
        adapter = GCPAdapter(level="WARNING")
        configure_logging(adapters=[adapter])

        assert LoggerCore.is_configured()
        assert len(LoggerCore.get_adapters()) == 1

    def test_multiple_adapters(self) -> None:
        """Multiple adapters should work simultaneously."""
        adapters = [
            ConsoleAdapter(level="INFO"),
            JSONAdapter(level="DEBUG"),
        ]
        configure_logging(adapters=adapters)

        assert LoggerCore.is_configured()
        assert len(LoggerCore.get_adapters()) == 2

    def test_default_console_adapter(self) -> None:
        """Should use ConsoleAdapter by default if no adapters provided."""
        configure_logging()

        assert LoggerCore.is_configured()
        adapters = LoggerCore.get_adapters()
        assert len(adapters) == 1
        assert isinstance(adapters[0], ConsoleAdapter)

    def test_adapter_level_filtering(self) -> None:
        """Adapters with different levels should filter appropriately."""
        adapters = [
            ConsoleAdapter(level="WARNING"),
            JSONAdapter(level="DEBUG"),
        ]
        configure_logging(adapters=adapters)

        # Just verify configuration works - actual filtering tested in integration
        assert len(LoggerCore.get_adapters()) == 2

    def test_reset_logging(self) -> None:
        """reset_logging should clear configuration."""
        configure_logging(adapters=[ConsoleAdapter()])
        assert LoggerCore.is_configured()

        reset_logging()
        assert not LoggerCore.is_configured()
        assert len(LoggerCore.get_adapters()) == 0

    def test_console_adapter_format(self) -> None:
        """ConsoleAdapter should have correct format string."""
        adapter = ConsoleAdapter()
        sink_config = adapter.get_sink_config()

        assert "format" in sink_config
        assert "{time" in sink_config["format"]
        assert "{level" in sink_config["format"]
        assert "{extra[trace_id]}" in sink_config["format"]
        assert "{extra[name]}" in sink_config["format"]

    def test_json_adapter_serialize(self) -> None:
        """JSONAdapter should enable serialization."""
        adapter = JSONAdapter()
        sink_config = adapter.get_sink_config()

        assert sink_config.get("serialize") is True

    def test_gcp_adapter_custom_formatter(self) -> None:
        """GCPAdapter should use custom formatter."""
        adapter = GCPAdapter()
        sink_config = adapter.get_sink_config()

        assert "format" in sink_config
        # GCPAdapter uses a callable formatter
        assert callable(sink_config["format"])


class TestAdapterSinkConfigs:
    """Test adapter sink configurations."""

    def test_console_adapter_sink_config(self) -> None:
        """ConsoleAdapter should return valid sink config."""
        adapter = ConsoleAdapter(level="INFO")
        config = adapter.get_sink_config()

        assert config["level"] == "INFO"
        assert config["colorize"] is True
        assert "format" in config

    def test_json_adapter_sink_config(self) -> None:
        """JSONAdapter should return valid sink config."""
        adapter = JSONAdapter(level="DEBUG")
        config = adapter.get_sink_config()

        assert config["level"] == "DEBUG"
        assert config["serialize"] is True

    def test_gcp_adapter_sink_config(self) -> None:
        """GCPAdapter should return valid sink config."""
        adapter = GCPAdapter(level="WARNING")
        config = adapter.get_sink_config()

        assert config["level"] == "WARNING"
        assert callable(config["format"])

    def test_adapter_level_validation(self) -> None:
        """Adapters should accept valid log levels."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in valid_levels:
            adapter = ConsoleAdapter(level=level)
            config = adapter.get_sink_config()
            assert config["level"] == level
