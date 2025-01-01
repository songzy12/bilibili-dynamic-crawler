<https://space.bilibili.com/34579852/dynamic>
<https://t.bilibili.com/1016739370268360729>

## API URL

<https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid=34579852>

## URL参数

| 参数名          | 类型 | 必要性 | 内容       | 备注                   |
| --------------- | ---- | ------ | ---------- | ---------------------- |
| offset          | num  | 非必要 | 分页偏移量 | 默认为空, 翻页时使用   |
| host_mid        | num  | 非必要 | UP主UID    | 仅新版, 如 `293793435` |
| timezone_offset | str  | 非必要 | `-480`     | 新版无                 |

## `data`

| 字段名          | 类型  | 内容                         | 备注                                               |
| --------------- | ----- | ---------------------------- | -------------------------------------------------- |
| has_more        | bool  | 是否有更多数据               |                                                    |
| items           | array | 数据数组                     |                                                    |
| offset          | str   | 偏移量                       | 等于`items`中最后一条记录的id<br/>获取下一页时使用 |
| update_baseline | str   | 更新基线                     | 等于`items`中第一条记录的id                        |
| update_num      | num   | 本次获取获取到了多少条新动态 | 在更新基线以上的动态条数                           |

## `data.items[n]`

| 字段名  | 类型 | 内容       | 备注                                           |
| ------- | ---- | ---------- | ---------------------------------------------- |
| basic   | obj  |            |                                                |
| id_str  | str  | 动态id     |                                                |
| modules | obj  | 动态信息   |                                                |
| type    | str  | 动态类型   | [动态类型](./dynamic_enum.md#动态类型)         |
| visible | bool | 是否显示   | `true`：正常显示<br/>`false`：折叠动态         |
| orig    | obj  | 原动态信息 | 仅动态类型为`DYNAMIC_TYPE_FORWARD`的情况下存在 | # 动态类型 |

### 动态类型

| 类型              | 说明     | 示例                                                            |
| ----------------- | -------- | --------------------------------------------------------------- |
| DYNAMIC_TYPE_DRAW | 带图动态 | [718384798557536290](https://t.bilibili.com/718384798557536290) |

## `data.items[n].modules.module_author`

| 字段名   | 类型 | 内容       | 备注                               |
| -------- | ---- | ---------- | ---------------------------------- |
| pub_time | str  | 更新时间   | `x分钟前`<br/>`x小时前`<br/>`昨天` |
| pub_ts   | num  | 更新时间戳 | UNIX 秒级时间戳                    |

## `data.items[n].modules.module_dynamic.desc`

| 字段 | 类型 | 内容           | 备注 |
| ---- | ---- | -------------- | ---- |
| text | str  | 动态的文字内容 |      |

## `data.items[n].modules.module_dynamic.major.draw.items[o]`

| 字段名 | 类型  | 内容     | 备注   |
| ------ | ----- | -------- | ------ |
| height | num   | 图片高度 |        |
| size   | num   | 图片大小 | 单位KB |
| src    | str   | 图片URL  |        |
| tags   | array |          |        |
| width  | num   | 图片宽度 |        |

## Reference

- <https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/dynamic/space.md>
- <https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/dynamic/all.md>
- <https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/dynamic/dynamic_enum.md>
