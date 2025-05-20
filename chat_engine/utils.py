import re

def extract_metadata(document):
    page_id = None
    link = None

    # -----------------------
    # 1) Extract Page ID
    # -----------------------
    marker_id = "Original DocHub Page ID:"
    index_id_marker = document.find(marker_id)
    if index_id_marker != -1:
        # Start searching for backticks after the marker
        search_start = index_id_marker + len(marker_id)
        first_tick = document.find("`", search_start)
        if first_tick != -1:
            second_tick = document.find("`", first_tick + 1)
            if second_tick != -1:
                page_id = document[first_tick+1 : second_tick].strip()

    # -----------------------
    # 2) Extract DocHub link
    # -----------------------
    marker_link = "[DocHub Link]("
    index_link_marker = document.find(marker_link)
    if index_link_marker != -1:
        # Start searching for ")" after the link marker
        search_start = index_link_marker + len(marker_link)
        end_paren = document.find(")", search_start)
        if end_paren != -1:
            link = document[search_start : end_paren].strip()

    return page_id, link