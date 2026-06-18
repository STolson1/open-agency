"""Configuration.

Defaults live in code. A `config.yaml` overrides them. Environment variables
(prefixed ``OPEN_AGENCY_``) override the YAML. Nothing to run — no Vault, no
Consul, no config service. Edit the YAML or set an env var and restart.

Precedence (highest first): init args -> env vars -> .env -> config.yaml -> code defaults.

The Anthropic API key is NOT a setting here — the ``anthropic`` SDK reads
``ANTHROPIC_API_KEY`` (or an ``ant auth login`` profile) from the environment
directly. See ``.env.example``.
"""

from __future__ import annotations

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

DEFAULT_PERSONA = (
    "You are a Human Resources representative. You are polite, procedural, and "
    "risk-averse. You speak in measured, professional language and never promise "
    "what policy does not allow. You treat the written policy as the only source "
    "of your authority: if the policy does not clearly permit something, you do "
    "not have the standing to approve it."
)


class Settings(BaseSettings):
    """Runtime configuration for the HR agent.

    Override any field via ``config.yaml`` or an ``OPEN_AGENCY_<FIELD>`` env var,
    without touching code. Example: ``OPEN_AGENCY_MODEL=claude-opus-4-8``.
    """

    model_config = SettingsConfigDict(
        env_prefix="OPEN_AGENCY_",
        env_file=".env",
        env_file_encoding="utf-8",
        yaml_file="config.yaml",
        extra="ignore",
    )

    # --- model: fully overridable, both the model and the effort ---
    model: str = "claude-sonnet-4-6"
    effort: str = "medium"  # low | medium | high | xhigh | max — auto-degraded per model
    max_tokens: int = 4096

    # --- the HR persona (the "typical HR person") ---
    persona: str = DEFAULT_PERSONA
    company_name: str = "Example Corp"

    # --- the policy (the searchable rulebook; each deployer supplies their own) ---
    policy_path: str = "open_agency/policies/example_company.md"
    max_policy_chunks: int = 5

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # env beats yaml beats code-default; yaml is the primary override surface.
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


def get_settings() -> Settings:
    return Settings()
