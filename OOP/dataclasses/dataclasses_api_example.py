from dataclasses import dataclass
from typing import List

@dataclass
class Post:
    id: int
    title: str
    content: str
    tags: List[str]

json_data = {
    "id": 1,
    "title": "Hello World",
    "content": "This is a blog post",
    "tags": ["python", "dataclass"]
}

post = Post(**json_data)
print(post.title)
