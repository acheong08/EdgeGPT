import uuid
from ..conversation_style import CONVERSATION_STYLE_TYPE, ConversationStyle
from ..utilities import guess_locale, get_ran_hex, get_location_hint_from_locale
from datetime import datetime


class ChatHubRequest:
    def __init__(
        self,
        conversation_signature: str,
        client_id: str,
        conversation_id: str,
        invocation_id: int = 3,
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
        message_id = str(uuid.uuid4())
        # Generate timestamp in format: 2023-06-05T20:49:30+08:00
        timestamp = datetime.now().isoformat(sep="T")
        self.struct = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": options,
                    "allowedMessageTypes": [
                        "ActionRequest",
                        "Chat",
                        "Context",
                        "InternalSearchQuery",
                        "InternalSearchResult",
                        "Disengaged",
                        "InternalLoaderMessage",
                        "Progress",
                        "RenderCardRequest",
                        "AdsQuery",
                        "SemanticSerp",
                        "GenerateContentQuery",
                        "SearchQuery",
                    ],
                    "sliceIds": [
                        "winmuid1tf",
                        "styleoff",
                        "ccadesk",
                        "smsrpsuppv4cf",
                        "ssrrcache",
                        "contansperf",
                        "crchatrev",
                        "winstmsg2tf",
                        "creatgoglt",
                        "creatorv2t",
                        "sydconfigoptt",
                        "adssqovroff",
                        "530pstho",
                        "517opinion",
                        "418dhlth",
                        "512sprtic1s0",
                        "emsgpr",
                        "525ptrcps0",
                        "529rweas0",
                        "515oscfing2s0",
                        "524vidansgs0",
                    ],
                    "verbosity": "verbose",
                    "traceId": get_ran_hex(32),
                    "isStartOfSession": self.invocation_id == 3,
                    "message": {
                        "locale": locale,
                        "market": locale,
                        "region": locale[-2:],  # en-US -> US
                        "locationHints": get_location_hint_from_locale(locale),
                        "timestamp": timestamp,
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": prompt,
                        "messageType": "Chat",
                        "messageId": message_id,
                        "requestId": message_id,
                    },
                    "tone": conversation_style.name.capitalize(),  # Make first letter uppercase
                    "requestId": message_id,
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

        # print(self.struct)
