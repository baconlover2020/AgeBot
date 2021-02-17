import painel


class Mobi:
    def __init__(self, swf_path, icon_path, item_id, classname, name, description, furniture, catalog):
        if type(furniture) is str:
            furniture = Furniture(furniture)
        self.swf_path = swf_path
        self.icon_path = icon_path
        self.item_id = item_id
        self.classname = classname
        self.name = name
        self.description = description
        self.furniture = furniture
        self.catalog = catalog
        self.furnidata = painel.criar_furnidata(self.classname, self.name, self.description, self.item_id)
        self.furniture.id = self.item_id
        if self.furniture.sprite_id == '':
            self.furniture.sprite_id = self.item_id
        self.catalog.name = self.name
        self.catalog.id = self.item_id

    def add(self):
        print("Adicionando>>")
        painel.adicionar_swf(self.swf_path)
        painel.adicionar_icon(self.icon_path)
        painel.adicionar_furnidata(self.furnidata)
        self.furniture.add()
        self.catalog.add()
        print("Mobi adicionado com sucesso!\n")

    def get_parameters(self):
        separator = '\n'
        parameters = [self.swf_path, self.icon_path, self.item_id, self.classname, self.name, self.description]
        print(separator.join(parameters))


class Furniture:
    def __init__(self, id='', public_name='steinlindo', item_name='steinlindo', type='s', width='1', length='1',
                 stack_height='1', can_stack='1', can_sit='0', is_walkable='0', sprite_id='', interaction_type='default',
                 interaction_modes='10', vending_ids='0', effect_id='0', variable_heights='0', song_id='0'):
        if sprite_id == '':
            sprite_id = id
        self.id = id
        self.public_name = public_name
        self.item_name = item_name
        self.type = type
        self.width = width
        self.length = length
        self.stack_height = stack_height
        self.can_stack = can_stack
        self.can_sit = can_sit
        self.is_walkable = is_walkable
        self.sprite_id = sprite_id
        self.interaction_type = interaction_type
        self.interaction_modes = interaction_modes
        self.vending_ids = vending_ids
        self.effect_id = effect_id
        self.variable_heights = variable_heights
        self.song_id = song_id

    def add(self):
        painel.adicionar_furniture(self.id, self.public_name, self.item_name, self.type, self.width, self.length,
                                   self.stack_height, self.can_stack, self.can_sit, self.is_walkable, self.sprite_id,
                                   self.interaction_type, self.interaction_modes, self.vending_ids, self.effect_id,
                                   self.variable_heights, self.song_id)

    @staticmethod
    def parse_sql(path):
        furnitures = []
        with open(path, 'r') as sql:
            for line in sql:
                if 'furniture' in line and 'INSERT INTO' in line:
                    line = line.split('(')[-1].replace("'", "").replace(');', '').replace(' ','')
                    values = line.split(',')
                    _id, public_name, item_name, _type, width, length, stack_height, can_stack, can_sit, \
                    is_walkable, sprite_id, interaction_type, interaction_modes, vending_ids, = \
                        values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], \
                        values[8], values[9], values[10], values[16], values[17], values[18]
                    furnitures.append(Furniture(_id, public_name, item_name, _type, width, length, stack_height,
                                                can_stack, can_sit, is_walkable, sprite_id, interaction_type,
                                                interaction_type, interaction_modes, vending_ids))
            return furnitures


class Catalog:
    def __init__(self, page_id, item_id='', catalog_name='', cost_credits='0', amount='1', song_id='0',
                 limited_sells='0', extradata='', badge_id='', cost_diamonds='0'):
        self.page_id = page_id
        self.id = item_id
        self.name = catalog_name
        self.cost_credits = cost_credits
        self.amount = amount
        self.song_id = song_id
        self.limited_sells = limited_sells
        self.extratada = extradata
        self.badge_id = badge_id
        self.cost_diamonds = cost_diamonds

    def add(self):
        painel.adicionar_catalogo(self.page_id, self.id, self.name, self.cost_credits, self.amount, self.song_id,
                                  self.limited_sells, self.extratada, self.badge_id, self.cost_diamonds)








