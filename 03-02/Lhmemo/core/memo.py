class Memo:
    '备忘录类'
    def __init__(self, date: str, thing: str):
        '初始化方法，保存id,date,name,thing'
        self._id = 0
        self.date = date
        self.thing = thing

    
    @property
    def id(self):
        '把私有属性供外部查看'
        return self._id

    @id.setter
    def id(self, val):
        '把私有属性供外部修改'
        self._id = val
