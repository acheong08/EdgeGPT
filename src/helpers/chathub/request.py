from ..conversation_style import CONVERSATION_STYLE_TYPE, ConversationStyle
from ..utilities import guess_locale, get_ran_hex, get_location_hint_from_locale


class ChatHubRequest:
    def __init__(
        self,
        conversation_signature: str,
        client_id: str,
        conversation_id: str,
        invocation_id: int = 0,
    ) -> None:
        self.struct: dict = {}

        self.client_id: str = client_id
        self.conversation_id: str = conversation_id
        self.conversation_signature: str = conversation_signature
        self.invocation_id: int = invocation_id

    def update(
        self,
        prompt: str,
        conversation_style: CONVERSATION_STYLE_TYPE,
        options: list | None = None,
        webpage_context: str | None = None,
        search_result: bool = True,
        locale: str = guess_locale(),
    ) -> None:
        if options is None:
            options = [
                "deepleo",
                "enable_debug_commands",
                "disable_emoji_spoken_text",
                "enablemm",
            ]
        if conversation_style:
            if not isinstance(conversation_style, ConversationStyle):
                conversation_style = getattr(ConversationStyle, conversation_style)
            options = conversation_style.value
        self.struct = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": options,
                    "allowedMessageTypes": [
                        "Chat",
                        "Disengaged",
                        "AdsQuery",
                        "SemanticSerp",
                        "GenerateContentQuery",
                        "SearchQuery",
                        "ActionRequest",
                        "Context",
                        "Progress",
                        "AdsQuery",
                        "SemanticSerp",
                    ],
                    "sliceIds": [
                        "winmuid3tf",
                        "osbsdusgreccf",
                        "ttstmout",
                        "crchatrev",
                        "winlongmsgtf",
                        "ctrlworkpay",
                        "norespwtf",
                        "tempcacheread",
                        "temptacache",
                        "505scss0",
                        "508jbcars0",
                        "515enbotdets0",
                        "5082tsports",
                        "515vaoprvs",
                        "424dagslnv1s0",
                        "kcimgattcf",
                        "427startpms0",
                    ],
                    "traceId": get_ran_hex(32),
                    "isStartOfSession": self.invocation_id == 0,
                    "message": {
                        "locale": locale,
                        "market": locale,
                        "region": locale[-2:],  # en-US -> US
                        "locationHints": get_location_hint_from_locale(locale),
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": prompt,
                        "messageType": "Chat",
                    },
                    "conversationSignature": self.conversation_signature,
                    "participant": {
                        "id": self.client_id,
                    },
                    "conversationId": self.conversation_id,
                },
            ],
            "invocationId": str(self.invocation_id),
            "target": "chat",
            "type": 4,
        }
        if search_result:
            have_search_result = [
                "InternalSearchQuery",
                "InternalSearchResult",
                "InternalLoaderMessage",
                "RenderCardRequest",
            ]
            self.struct["arguments"][0]["allowedMessageTypes"] += have_search_result
        if webpage_context:
            self.struct["arguments"][0]["previousMessages"] = [
                {
                    "author": "user",
                    "description": webpage_context,
                    "contextType": "WebPage",
                    "messageType": "Context",
                    "messageId": "discover-web--page-ping-mriduna-----",
                },
            ]
        self.invocation_id += 1
