from . import _error
from . import _lang
from nonebot import on_command, on_regex, on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from ._utils import Json
import time
import re

@on_regex(r"\[CQ:at,qq=([0-9]+|all)\]").handle()
async def at_handle(bot: Bot, event: GroupMessageEvent):
    try:
        at_user_id = re.search(r"\[CQ:at,qq=([0-9]+|all)\]", str(event.get_message()))\
            .group(0)\
                .replace("[CQ:at,qq=", "")\
                    .replace("]", "")
        event_data = {
            "time": time.time(),
            "group_id": event.group_id,
            "user_id": event.user_id
        }
        
        # 获取历史消息
        messages = []
        _messages = (await bot.call_api(
            "get_group_msg_history",
            # message_seq=event.message_id,
            group_id=event.group_id
        ))["messages"]
        for message in _messages:
            messages.append(message["message_id"])
        event_data["messages"] = messages

        data = Json("who_at_me.data.json")
        data.get(at_user_id, []).append(event_data)
        
    except: 
        await _error.report()

@on_command("who-at-me").handle()
async def whoatme_handler(bot: Bot, event: GroupMessageEvent):
    try:
        user_data = Json("who_at_me.data.json")[str(event.user_id)]
        # TODO Notice信息
        node_messages = []
        for item in user_data:
            sub_node = [
                {
                    "type": "node",
                    "data": {
                        "uin": (await bot.get_login_info())["user_id"],
                        "name": (await bot.get_login_info())["nickname"],
                        "content": _lang.text("who_at_me.info", [
                            (await bot.get_group_info(group_id=item["group_id"]))["group_name"],
                            item["group_id"],
                            time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(item["time"]))
                        ], event.get_user_id())
                    }
                }
            ]
            for messages in item["messages"]:
                sub_node.append({
                    "type": "node",
                    "data": {
                        "id": messages
                    }
                })
            node_messages.append(sub_node)
        await bot.call_api(
            "send_group_forward_msg",
            group_id=event.group_id,
            messages=node_messages
        )
    except:
        await _error.report()