class SubPageInfo:

    def __init__(self,
        academy_list:list,
        index_list:list,
        title_list:list,
        has_attachment_list:list,
        date_list:list,
        cache_file_path:str,
        mode:str
        ) -> None: # academy, index, title, hasAttachment, date
        self.academy_list = academy_list
        self.index_list = index_list
        self.title_list = title_list
        self.has_attachment_list = has_attachment_list
        self.date_list = date_list
        self.HTML_file_list = []
        self.attachment_file_list = []
        self.cache_file_path = cache_file_path
        self.mode = mode
        return None

    def __str__(self) -> str:
        return(str(self.academy_list),str(self.index_list),str(self.title_list),str(self.has_attachment_list),str(self.date_list))

    def remove_duplicate_page(self) -> None:
        pop_value_list = []
        for i in self.index_list:
            if i[-1] == 'r':
                pop_value_list.append(i)
                # self.academy_list.pop[i]
                # self.index_list.pop[i]
                # self.title_list.pop[i]
                # self.has_attachment_list.pop[i]
                # self.date_list.pop[i]
        for i in pop_value_list:
            self.academy_list.pop(self.index_list.index(i))
            self.title_list.pop(self.index_list.index(i))
            self.has_attachment_list.pop(self.index_list.index(i))
            self.date_list.pop(self.index_list.index(i))
            self.index_list.pop(self.index_list.index(i))
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

    def remove_deplicate_mark(self) -> None:
        for i in range(len(self.index_list)):
            self.index_list[i] = self.index_list[i].replace('r','')

    def creat_email_content(self,start_time:str) -> None:
        if self.mode == 'GWT':
            self.content = 'There is(are) '+str(len(self.academy_list))+' new announcement(s) now!\n'
            self.content += 'The message was generated at '+start_time+'\n'
            self.content += '\n'
            for i in range(len(self.academy_list)):
                self.content += '\n'
                self.content += 'From: '+self.academy_list[i]+'\n'
                self.content += 'Date: '+self.date_list[i]+'\n'
                self.content += 'Tittle: '+self.title_list[i]+'\n'
                self.content += 'Link: '+'http://nbw.sztu.edu.cn/info/'+self.index_list[i]+'.htm\n'
                if self.has_attachment_list[i].find('1') == -1:
                    self.content += 'Attachment: Flase\n'
                else:
                    self.content += 'Attachment: True\n'
            self.content += '\n'
            self.content += '\n'
            self.content += 'The message was sent at '+'datetime.datetime.now().strftime("%y-%m-%d_%H:%M:%S")'+'\n'
            self.content += '\n'
            self.content += '本程序所提供的信息，仅供参考之用。所有数据来自深圳技术大学内部网，版权归深圳技术大学及相关发布人所有。\n'
            self.content += '完整的免责声明见程序发布页或向邮件发送者索取'
        elif self.mode == 'XYGS':
            self.content = 'There is(are) '+str(len(self.academy_list))+' new publicity(ies) now!\n'
            self.content += 'The message was generated at '+start_time+'\n'
            self.content += '\n'
            for i in range(len(self.academy_list)):
                self.content += '\n'
                self.content += 'From: '+self.academy_list[i]+'\n'
                self.content += 'Date: '+self.date_list[i]+'\n'
                self.content += 'Tittle: '+self.title_list[i]+'\n'
                self.content += 'Link: '+'http://nbw.sztu.edu.cn/info/'+self.index_list[i]+'.htm\n'
                if self.has_attachment_list[i].find('1') == -1:
                    self.content += 'Attachment: Flase\n'
                else:
                    self.content += 'Attachment: True\n'
            self.content += '\n'
            self.content += '\n'
            self.content += 'The message was sent at '+'datetime.datetime.now().strftime("%y-%m-%d_%H:%M:%S")'+'\n'
            self.content += '\n'
            self.content += '本程序所提供的信息，仅供参考之用。所有数据来自深圳技术大学内部网，版权归深圳技术大学及相关发布人所有。\n'
            self.content += '完整的免责声明见程序发布页或向邮件发送者索取'
        # return self.content