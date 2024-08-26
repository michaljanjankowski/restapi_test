from dataclasses import dataclass, field
from typing import Optional, Union, Dict

@dataclass
class User:
    _id: str
    name: Optional[str] = None
    handle: Optional[str] = None


@dataclass
class Status:
    __v: Optional[int] = None
    sentCount: Optional[int] = None
    verified: Optional[bool] = None
    feedback: Optional[str] = None


@dataclass
class Fact:
    _id: str
    text: str
    type: str = "cat"
    #__v: Optional[int] = field(default=None, metadata={"name": "__v"})
    _v: Optional[int] = None
    status: Optional[Status] = None
    user: Optional[Union[str, User]] = None  # Can be a string ID or a User object
    upvotes: Optional[int] = None
    userUpvoted: Optional[bool] = None
    source: Optional[str] = None
    updatedAt: Optional[str] = None
    createdAt: Optional[str] = None
    deleted: Optional[bool] = None
    used: Optional[bool] = None


    @classmethod
    def from_dict(cls, data: Dict) -> "Fact":
        """Helper method to convert a dictionary to a Fact dataclass instance."""
        # Handle nested 'user' object if it exists and is a dictionary
        if isinstance(data.get('user'), dict):
            data['user'] = User(**data['user'])

        if isinstance(data.get('status'), dict):
            data['status'] = Status(**data['status'])

        if '__v' in data:
            data['_v'] = data.pop('__v')

        return cls(**data)
