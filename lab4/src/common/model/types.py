from typing import Annotated

from pydantic import Field

Address = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{40}$")]
