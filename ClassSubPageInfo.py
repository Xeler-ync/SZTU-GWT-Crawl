class SubPageInfo:

    def __init__(self,academy_list,index_list,title_list,has_attachment_list,date_list) -> None: # academy, index, title, hasAttachment, date
        self.academy_list = academy_list
        self.index_list = index_list
        self.title_list = title_list
        self.has_attachment_list = has_attachment_list
        self.date_list = date_list
        self.HTML_file_list = []
        self.attachment_file_list = []
        return None

    def __str__(self) -> str:
        return(str(self.academy_list),str(self.index_list),str(self.title_list),str(self.has_attachment_list),str(self.date_list))

    def remove_duplicate_page(self) -> None:
        for i in range(len(self.index_list)):
            if self.index_list[i][-1] == 'r':
                self.academy_list.pop[i]
                self.index_list.pop[i]
                self.title_list.pop[i]
                self.has_attachment_list.pop[i]
                self.date_list.pop[i]
        return None

    def add_HTML_file(self,HTML_file) -> None:
        self.HTML_file_list.append(HTML_file)
        return None

    def add_attachment_file(self,attachment_file) -> None:
        self.attachment_file_list.append(attachment_file)
        return None

    def sort_file_name(self) -> None:
        self.HTML_file_list.sort()
        self.attachment_file_list.sort()