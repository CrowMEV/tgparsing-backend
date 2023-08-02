from sqlalchemy import types
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


class UtcNow(expression.FunctionElement):  # pylint: disable=W0223,R0901
    type = types.DateTime()
    inherit_cache = True


@compiles(UtcNow, "postgresql")
def pg_utcnow(element, compiler, **kw):  # pylint: disable=W0613
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
