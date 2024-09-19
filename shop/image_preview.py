from django.utils.html import format_html


def image_preview(bouquet):
    height = 300
    return format_html(
        "<img src={} height={} />",
        bouquet.picture.url,
        height,
    )
