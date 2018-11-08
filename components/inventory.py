import libtcodpy as libtcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        print('INFO : Item recuperé {}', item.name, type(item))

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full.', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up {} {}!'.format(str(item.item.stack), item.name), libtcod.blue)
            })

            # v15 stack item.
            if item.item.use_function:
                for i in self.items:
                    # v15 : meme fonction, ignore les stats differentes et autres criteres uniques (plus tard).
                    if i.item.use_function == item.item.use_function:
                        i.item.stack += 1
                        break
                else:
                    self.items.append(item)
            else:
                self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        print('INVENTORY : item entity is ', item_entity)
        #item_component = item_entity.item

        if item_entity.item.use_function:
            if not item_entity.item.targeting and not item_entity.item.to_cast:
                results.append({'message': Message('{} doesn t have a targeting system. Canceled.'.format(
                    item_entity.name), libtcod.yellow)})

            elif kwargs.get('to_cast'):
                kwargs = {**item_entity.item.function_kwargs, **kwargs}
                spell_cast_results = item_entity.item.use_function(self.owner, item_entity, **kwargs)

                results.extend(spell_cast_results)

            # refacto v16c
            elif item_entity.item.targeting:
                results.append({'spell_targeting': {'spell': item_entity, 'target_mode': item_entity.item.targeting}})

            else:
                results.append({'message': Message('Error : {} has no target mode.'.format(item_entity.name),
                                                   libtcod.yellow)})

        else:
            equippable_component = item_entity.equippable
            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {} cannot be used.'.format(item_entity.name), libtcod.yellow)})

        return results

    def remove_item(self, item, nb_to_remove=1):
        # v15 : stack
        if item.item.use_function:
            if nb_to_remove > item.item.stack:
                nb_to_remove = item.item.stack

            if item.item.stack > nb_to_remove:
                item.item.stack -= nb_to_remove
            else:
                self.items.remove(item)
        else:
            self.items.remove(item)

    def drop_item(self, item):
        results = []

        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        # v15 : stack. Dirty. If dropped with 2 stacks, the item will be on the floor AND in inventory.
        # Dropping the second stack will teleport the one already dropped.
        # for now, all the stack are dropped.

        item.x = self.owner.x
        item.y = self.owner.y

        # v15 stack system
        if item.item.use_function:
            if item.item.stack > 1:
                results.append({'item_dropped': item, 'message': Message('You dropped {} {}'.format(str(item.item.stack), item.name), libtcod.yellow)})
            else:
                results.append({'item_dropped': item, 'message': Message('You dropped the {}'.format(item.name), libtcod.yellow)})
        else:
            results.append({'item_dropped': item, 'message': Message('You dropped the {}'.format(item.name), libtcod.yellow)})

        # v15 : all to drop the full stack.
        self.remove_item(item, nb_to_remove=999)

        return results
