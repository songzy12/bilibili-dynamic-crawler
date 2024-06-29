## Bilibili Crawler

初始化：

```
git clone --single-branch --branch main git@github.com:songzy12/bilibili-crawler.git

cd bilibili-crawler
git clone --single-branch --branch output git@github.com:songzy12/bilibili-crawler.git output
```

### 功能1：给定用户 MID，爬取其动态下的所有图片，并发布日期保存至相应的文件夹内。

示例：https://space.bilibili.com/34579852/dynamic

运行：

在 `dynamic` 文件夹下创建 `config.py`（可参考 `config_sample.py` 的内容），并填入

1. MID: 通过查看用户主页 url 获取：34579852
2. COOKIE: 通过 F12 查看网络请求头文件获取。

```
python -m dynamic
```

输出可见：`dynamic/output/34579852/`
