import json
from nonebot import get_app
from . import _error
import traceback
from fastapi.responses import HTMLResponse
from pyecharts import options as opts
import time
from pyecharts.render import make_snapshot
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.matcher import Matcher
from nonebot import on_startswith, on_command
from nonebot import get_bots

ctrl_group = json.load(open("data/ctrl.json", encoding="utf-8"))["control"]
on_six = on_startswith("6")
app = get_app()


@on_command("six-r").handle()
async def _(matcher: Matcher, event: MessageEvent):
    try:
        data = json.load(open("data/sixcount.data.json", encoding="utf-8"))
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        s = ""
        for i in range(5):
            user_id = sorted_data[i][0]
            count = data[user_id]
            s += f"{i + 1}. {user_id}: {count}\n"
        s += "------------------------------\n"
        user_id = event.get_user_id()
        count = data[user_id]
        s += f"{sorted_data.index(user_id) + 1}. {user_id}: {count}\n"
        await matcher.send(s)
    except Exception:
        await _error.report(traceback.format_exc())


@on_six.handle()
async def on_six_handle(event: MessageEvent) -> None:
    """「6」计数器"""
    try:
        data = json.load(open("data/sixcount.data.json", encoding="utf-8"))
        userID = event.get_user_id()
        if userID == "1226383994":
            userID = "2558938020"
        try:
            data[userID] += 1
        except KeyError:
            data[userID] = 1
        json.dump(data, open("data/sixcount.data.json", "w", encoding="utf-8"))

    except Exception:
        await _error.report(traceback.format_exc())


@app.get("/six/data.json")
async def get_data() -> dict | None:
    """从Web获取数据"""
    try:
        return json.load(open("data/sixcount.data.json", encoding="utf-8"))
    except Exception:
        await _error.report(traceback.format_exc())


@app.get("/six/startime.json")
async def get_start_time() -> dict | None:
    """从Web获取开始时间"""
    try:
        return json.load(open("data/sixcount.starttime.json", encoding="utf-8"))
    except Exception:
        await _error.report(traceback.format_exc())


@app.get("/six", response_class=HTMLResponse)
async def pie():
    """生成并反回饼图"""
    try:
        data = json.load(open("data/sixcount.data.json", encoding="utf-8"))
        start_time = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(
                json.load(
                    open("data/sixcount.starttime.json", encoding="utf-8"))["time"]),
        )

        user_data = []
        bots = get_bots()
        bot = bots[list(bots.keys())[0]]
        user_list = list(data.keys())

        for i in range(len(user_list)):
            user_data.append(
                (
                    (await bot.get_stranger_info(user_id=user_list[i]))["nickname"],
                    data[user_list[i]],
                )
            )

        file_path = (
            Pie(init_opts=opts.InitOpts(bg_color="rgba(255,255,255,1)"))
            .add("", user_data)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="6", subtitle=start_time + " 至今"),
                legend_opts=opts.LegendOpts(is_show=False))

            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).render(path="data/sixcount.render.ro.html")

        with open(file_path, encoding="utf-8") as f:
            html = f.read()

        return html
    except Exception:
        await _error.report(traceback.format_exc())