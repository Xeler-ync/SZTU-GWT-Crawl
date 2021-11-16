import datetime


class SubPageInfo:
    source_list = []
    index_list = []
    title_list = []
    has_attachment_list = []
    date_list = []

    def __init__(self,source_list,index_list,title_list,has_attachment_list,date_list) -> None: # source, index, title, hasAttachment, date
        self.source_list = source_list
        self.index_list = index_list
        self.title_list = title_list
        self.has_attachment_list = has_attachment_list
        self.date_list = date_list
        return None