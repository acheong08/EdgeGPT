from enum import Enum

try:
    from typing import Literal, Union
except ImportError:
    from typing_extensions import Literal
from typing import Optional


class ConversationStyle(Enum):
    creative = [
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "h3imaginative",
        "cachewriteext",
        "e2ecachewrite",
        "nodlcpcwrite",
        "nointernalsugg",
        "saharasugg",
        "enablenewsfc",
        "dv3sugg",
        "clgalileo",
        "gencontentv3",
        "nojbfedge",
    ]
    balanced = [
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "harmonyv3",
        "cachewriteext",
        "e2ecachewrite",
        "nodlcpcwrite",
        "nointernalsugg",
        "saharasugg",
        "enablenewsfc",
        "dv3sugg",
        "nojbfedge",
    ]
    precise = [
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "h3precise",
        "cachewriteext",
        "e2ecachewrite",
        "nodlcpcwrite",
        "nointernalsugg",
        "saharasugg",
        "enablenewsfc",
        "dv3sugg",
        "clgalileo",
        "gencontentv3",
        "nojbfedge",
    ]


CONVERSATION_STYLE_TYPE = Optional[
    Union[ConversationStyle, Literal["creative", "balanced", "precise"]]
]
