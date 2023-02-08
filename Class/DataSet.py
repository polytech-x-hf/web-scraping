import json

class DataSetItem:

    def __init__(self, file_name: str, char_name: str, caption: str):
        self.file_name = file_name
        self.char_name = char_name
        self.caption = caption

    def to_string(self):
        return "{ test : " + self.char_name + ", image_name : " + self.image_name + ", caption : " + self.caption + " }"


class DataSet:

    def __init__(self):
        self.items = []

    def add_item(self, item: DataSetItem):
        self.items.append(item)

    def to_string(self):
        res = ""
        for i in range(0, len(self.items)):
            res += self.items[i].to_string() + ",\n"
        return res

    def to_JSON(self):
        return json.dumps(self.items, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def from_JSON(json_string: str):
        return json.loads(json_string)
