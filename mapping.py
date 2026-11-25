"""Reusable folium helpers for the catastrophe modelling project."""

import folium


def simplified(gdf, tol=0.01):
    """Return a lighter copy of a GeoDataFrame for display only.

    tol is in degrees (0.01 is roughly 1 km).
    """
    return gdf.assign(geometry=gdf.geometry.simplify(tol))


def add_layer(m, gdf, name, style, show=True, tooltip=None):
    """Add a GeoDataFrame to map m as a toggleable layer.

    style can be a fixed dict or a function that takes a feature.
    """
    style_fn = style if callable(style) else (lambda _f: style)
    folium.GeoJson(gdf, name=name, show=show, style_function=style_fn, tooltip=tooltip).add_to(m)


def add_legend(m, title, entries, corner="left", symbol="&#9679;"):
    """Add a fixed-position legend box. entries maps label -> colour."""
    rows = "".join(
        f'<span style="color:{c};font-size:16px;">{symbol}</span> {k}<br>'
        for k, c in entries.items()
    )
    html = (
        f'<div style="position: fixed; bottom: 30px; {corner}: 30px; z-index: 9999; '
        'background: white; padding: 10px 12px; border: 1px solid grey; '
        f'border-radius: 6px; font-size: 13px;"><b>{title}</b><br>{rows}</div>'
    )
    m.get_root().html.add_child(folium.Element(html))