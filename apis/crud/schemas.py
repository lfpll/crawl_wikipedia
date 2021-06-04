from pydantic import BaseModel
from pydantic.typing import Optional

# Pydantic Models
class UrlBase(BaseModel):
    id: Optional[int]
    url : str

    class Config:
        orm_mode = True


class Url(UrlBase):
    appearances: Optional[int]
    domain_length:  Optional[int]
    is_file:  Optional[bool]
    is_arabic:  Optional[bool]
    last_path_length:  Optional[int]
    percent_of_letters_path:  Optional[float]
    percent_of_numbers_path:  Optional[float]
    path_length:  Optional[int]
    full_lengh:  Optional[int]
    number_of_subpaths:  Optional[int]
    related_original_url: Optional[bool]


