import re
from dataclasses import dataclass
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, PydanticCustomError, core_schema


@dataclass
class Regex:
    pattern: str

    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        regex = re.compile(self.pattern)

        def match(string: str) -> str:
            if not regex.match(string):
                raise PydanticCustomError(
                    "string_pattern_mismatch",
                    "String should match pattern '{pattern}'",
                    {"pattern": self.pattern},
                )
            return string

        return core_schema.no_info_after_validator_function(
            match,
            handler(source_type),
        )
