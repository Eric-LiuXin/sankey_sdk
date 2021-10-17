import pandas as pd
from pyecharts.charts import Sankey
from pyecharts import options as opts


def _get_nodes(df, fields):
    nodes = []
    for field_name in fields:
        for value in df[field_name].unique():
            nodes.append({"name": value})
    return nodes


def _get_links(df, fields):
    table_list = []
    for i in range(len(fields) - 1):
        _table = _df.groupby([fields[i], fields[i + 1]])["value"].sum().reset_index()
        _table.columns = ["source", "target", "value"]
        table_list.append(_table)

    result = pd.concat(table_list)
    links = result.to_dict("records")

    return links


def _create_pic(series_name, title_name, nodes, links):
    pic = (
        Sankey()
        .add(
            series_name,
            nodes=nodes,
            links=links,
            linestyle_opt=opts.LineStyleOpts(opacity=0.3, curve=0.5, color="source"),
            label_opts=opts.LabelOpts(position="top"),
            node_gap=30,
            pos_top="15%",
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=title_name))
    )

    pic.render("../target/target.html")


if __name__ == "__main__":
    _df = pd.read_csv("../source/source.csv")
    title_list = [field for field in _df.columns.values][:-1]

    nodes = _get_nodes(_df, title_list)
    links = _get_links(_df, title_list)

    _create_pic("series_name", "title_name", nodes, links)
