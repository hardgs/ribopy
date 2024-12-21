
class NightDB:
    headers=[]
    body=[]
    def read(self,content: str,sep=","):
        content = content.splitlines()
        self.headers = content[0].split(sep)
        items = content[1:]
        del(content)
        for item in items:
            item = item.split(sep)
            self.body.append({})
            i=0
            for header in self.headers:
                if item[i]=="True":
                    self.body[-1][header] = True
                elif item[i]=="False":
                    self.body[-1][header] = False
                else:    
                    self.body[-1][header] = item[i]
                i = i +1
    def get_colums(self,header: str):
        result = []
        for row in self.body:
            result.append(row.get(header))
        return result
    def get_row_by_colum(self,header: str,value: str):
        for row in self.body:
            if row[header]==value:
                return row
    def save(self,sep = ","):
        #handle = open(path,"w")
        handle = sep.join(self.headers)+'\n'
        for row in self.body:
            for header in self.headers:
                handle += str(row[header])
                if not self.headers[-1]==header:
                    handle+= sep
            if not self.body[-1]==row:
                handle+='\n'
        return handle
